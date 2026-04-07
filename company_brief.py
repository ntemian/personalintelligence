#!/usr/bin/env python3
"""
PersonalIntelligence — Company Intelligence Brief Generator
============================================================
Input: AFM (tax ID) or company name
Output: AI-powered company intelligence brief (HTML)

Data sources:
  1. GEMI OpenData API (free, ODC-BY-1.0 license)
  2. Web scraping (Google Maps, social presence)
  3. AI analysis (Claude API)

License attribution: Πηγή δεδομένων: ΓΕΜΗ — Κεντρική Ένωση Επιμελητηρίων Ελλάδος (ODC-BY-1.0)
"""

import argparse
import asyncio
import json
import os
import sys
import webbrowser
from datetime import datetime
from pathlib import Path

import httpx

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

GEMI_API_BASE = "https://opendata-api.businessportal.gr/api/opendata/v1"
GEMI_API_KEY = os.environ.get("GEMI_API_KEY", "")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
OUTPUT_DIR = Path(__file__).parent / "briefs"


# ---------------------------------------------------------------------------
# GEMI API Client
# ---------------------------------------------------------------------------

class GemiClient:
    """Client for the GEMI OpenData API."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base = GEMI_API_BASE
        self.headers = {"api_key": api_key}

    async def search(self, afm: str = None, name: str = None, limit: int = 5) -> list:
        """Search companies by AFM or name."""
        params = {"resultsSize": limit}
        if afm:
            params["afm"] = afm
        if name:
            params["name"] = name

        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(
                f"{self.base}/companies",
                headers=self.headers,
                params=params,
            )
            resp.raise_for_status()
            return resp.json()

    async def get_company(self, ar_gemi: int) -> dict:
        """Get full company details by GEMI number."""
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(
                f"{self.base}/companies/{ar_gemi}",
                headers=self.headers,
            )
            resp.raise_for_status()
            return resp.json()

    async def get_documents(self, ar_gemi: int) -> list:
        """Get public documents for a company."""
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(
                f"{self.base}/companies/{ar_gemi}/documents",
                headers=self.headers,
            )
            resp.raise_for_status()
            return resp.json()


# ---------------------------------------------------------------------------
# Web Enrichment (scraping public data)
# ---------------------------------------------------------------------------

async def enrich_web(company_name: str, website: str = None) -> dict:
    """Scrape public web data to enrich company profile."""
    enrichment = {
        "google_maps": None,
        "social_media": [],
        "news_mentions": [],
        "job_postings": False,
    }

    async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
        # Check if website is live
        if website:
            try:
                resp = await client.get(website)
                enrichment["website_live"] = resp.status_code == 200
                enrichment["website_title"] = _extract_title(resp.text)
            except Exception:
                enrichment["website_live"] = False

    return enrichment


def _extract_title(html: str) -> str:
    """Extract <title> from HTML."""
    import re
    match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    return match.group(1).strip() if match else ""


# ---------------------------------------------------------------------------
# AI Analysis
# ---------------------------------------------------------------------------

async def analyze_with_ai(company_data: dict, web_data: dict) -> str:
    """Send company data to Claude for AI analysis."""
    if not ANTHROPIC_API_KEY:
        return _fallback_analysis(company_data)

    prompt = f"""You are a Greek business intelligence analyst. Analyze this company and produce a concise intelligence brief in English.

COMPANY DATA (from GEMI — Greek General Commercial Registry):
{json.dumps(company_data, ensure_ascii=False, indent=2, default=str)}

WEB ENRICHMENT:
{json.dumps(web_data, ensure_ascii=False, indent=2, default=str)}

Produce a brief with these sections:
1. **Company Identity** — Name, AFM, legal form, founded, status, location
2. **Business Activities** — What they do (translate KAD codes to plain language)
3. **Management & Ownership** — Key people, roles, ownership structure
4. **Capital Structure** — Share capital, stock info if available
5. **Risk & Opportunity Signals** — Based on: age, status, capital, activity breadth, management changes
6. **AI Assessment** — 2-3 sentences: what this company likely needs, how to approach them, what to watch out for

Be specific and actionable. No generic filler. Write for a business development professional who wants to sell AI services to this company."""

    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 2000,
                "messages": [{"role": "user", "content": prompt}],
            },
        )
        resp.raise_for_status()
        return resp.json()["content"][0]["text"]


def _fallback_analysis(company_data: dict) -> str:
    """Generate a basic analysis without AI when no API key is available."""
    name = company_data.get("coNameEl", "Unknown")
    afm = company_data.get("afm", "N/A")
    status = company_data.get("status", {})
    status_desc = status.get("description", "Unknown") if isinstance(status, dict) else str(status)
    inc_date = company_data.get("incorporationDate", "Unknown")
    activities = company_data.get("activities", [])
    persons = company_data.get("persons", [])
    capital = company_data.get("capital", [])

    activity_list = ""
    for a in activities[:5]:
        act = a.get("activity", {})
        desc = act.get("description", "N/A") if isinstance(act, dict) else str(act)
        atype = a.get("type", "")
        activity_list += f"- {desc} ({atype})\n"

    person_list = ""
    for p in persons[:10]:
        pname = p.get("personName", p.get("businessName", "N/A"))
        role = p.get("role", "N/A")
        pct = p.get("percentage", "")
        pct_str = f" ({pct}%)" if pct else ""
        person_list += f"- {pname}: {role}{pct_str}\n"

    capital_info = ""
    for c in capital[:3]:
        amount = c.get("amount", "N/A")
        capital_info += f"- {amount}\n"

    # Calculate company age
    age_str = "Unknown"
    if inc_date and inc_date != "Unknown":
        try:
            inc = datetime.fromisoformat(inc_date.replace("Z", "+00:00"))
            age = (datetime.now() - inc.replace(tzinfo=None)).days // 365
            age_str = f"{age} years"
        except Exception:
            age_str = inc_date

    return f"""## Company Identity
**{name}** | AFM: {afm} | Status: {status_desc} | Founded: {inc_date} ({age_str})

## Business Activities
{activity_list if activity_list else "No activities registered"}

## Management & Ownership
{person_list if person_list else "No persons registered"}

## Capital
{capital_info if capital_info else "No capital data available"}

## Signals
- Company age: {age_str}
- Status: {status_desc}
- Activities registered: {len(activities)}
- People registered: {len(persons)}

*AI analysis requires ANTHROPIC_API_KEY — set it for full intelligence brief.*"""


# ---------------------------------------------------------------------------
# HTML Report Generator
# ---------------------------------------------------------------------------

def generate_html(company_data: dict, analysis: str, web_data: dict) -> str:
    """Generate a beautiful HTML intelligence brief."""
    name = company_data.get("coNameEl", "Unknown Company")
    afm = company_data.get("afm", "N/A")
    ar_gemi = company_data.get("arGemi", "N/A")
    status = company_data.get("status", {})
    status_desc = status.get("description", "Unknown") if isinstance(status, dict) else str(status)
    inc_date = company_data.get("incorporationDate", "Unknown")
    legal_type = company_data.get("legalType", {})
    legal_desc = legal_type.get("description", "N/A") if isinstance(legal_type, dict) else str(legal_type)
    city = company_data.get("city", "")
    street = company_data.get("street", "")
    street_num = company_data.get("streetNumber", "")
    zipcode = company_data.get("zipCode", "")
    email = company_data.get("email", "")
    website = company_data.get("url", "")
    objective = company_data.get("objective", "")

    address = f"{street} {street_num}, {city} {zipcode}".strip(", ")

    # Status color
    status_lower = status_desc.lower() if status_desc else ""
    if "ενεργ" in status_lower or "active" in status_lower:
        status_color = "#22c55e"
        status_icon = "&#9679;"
    elif "διαγρ" in status_lower or "delet" in status_lower:
        status_color = "#ef4444"
        status_icon = "&#9679;"
    else:
        status_color = "#f59e0b"
        status_icon = "&#9679;"

    # Convert markdown analysis to HTML (basic)
    analysis_html = analysis
    import re
    analysis_html = re.sub(r"## (.+)", r"<h3>\1</h3>", analysis_html)
    analysis_html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", analysis_html)
    analysis_html = re.sub(r"^- (.+)$", r"<li>\1</li>", analysis_html, flags=re.MULTILINE)
    analysis_html = re.sub(r"(<li>.*</li>\n?)+", r"<ul>\g<0></ul>", analysis_html)
    analysis_html = analysis_html.replace("\n\n", "</p><p>").replace("\n", "<br>")
    analysis_html = f"<p>{analysis_html}</p>"

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    return f"""<!DOCTYPE html>
<html lang="el">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Intelligence Brief — {name}</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
    background: #0a0a0a;
    color: #e5e5e5;
    line-height: 1.6;
  }}
  .container {{
    max-width: 900px;
    margin: 0 auto;
    padding: 40px 24px;
  }}
  .header {{
    border-bottom: 1px solid #262626;
    padding-bottom: 24px;
    margin-bottom: 32px;
  }}
  .brand {{
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 3px;
    color: #737373;
    margin-bottom: 16px;
  }}
  .brand span {{ color: #3b82f6; }}
  .company-name {{
    font-size: 32px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 8px;
  }}
  .meta-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 12px;
    margin-top: 16px;
  }}
  .meta-item {{
    background: #171717;
    border: 1px solid #262626;
    border-radius: 8px;
    padding: 12px 16px;
  }}
  .meta-label {{
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #737373;
    margin-bottom: 4px;
  }}
  .meta-value {{
    font-size: 15px;
    color: #d4d4d4;
    font-weight: 500;
  }}
  .status-badge {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    color: {status_color};
  }}
  .section {{
    margin-bottom: 32px;
  }}
  .section h2 {{
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #525252;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 1px solid #1a1a1a;
  }}
  .analysis {{
    background: #171717;
    border: 1px solid #262626;
    border-radius: 12px;
    padding: 24px;
  }}
  .analysis h3 {{
    font-size: 16px;
    color: #3b82f6;
    margin: 20px 0 8px 0;
  }}
  .analysis h3:first-child {{ margin-top: 0; }}
  .analysis ul {{
    margin: 8px 0;
    padding-left: 20px;
  }}
  .analysis li {{
    margin: 4px 0;
    color: #a3a3a3;
  }}
  .analysis strong {{ color: #e5e5e5; }}
  .analysis p {{ margin: 8px 0; color: #a3a3a3; }}
  .objective {{
    background: #171717;
    border-left: 3px solid #3b82f6;
    padding: 16px;
    border-radius: 0 8px 8px 0;
    color: #a3a3a3;
    font-size: 14px;
    margin-top: 12px;
  }}
  .footer {{
    margin-top: 48px;
    padding-top: 24px;
    border-top: 1px solid #262626;
    font-size: 12px;
    color: #525252;
    text-align: center;
  }}
  .footer a {{ color: #3b82f6; text-decoration: none; }}
  .signals {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 12px;
  }}
  .signal {{
    background: #171717;
    border: 1px solid #262626;
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 14px;
  }}
  .signal-green {{ border-left: 3px solid #22c55e; }}
  .signal-yellow {{ border-left: 3px solid #f59e0b; }}
  .signal-red {{ border-left: 3px solid #ef4444; }}
  @media print {{
    body {{ background: white; color: #1a1a1a; }}
    .container {{ max-width: 100%; }}
    .meta-item, .analysis, .signal {{ border-color: #e5e5e5; background: #f9f9f9; }}
  }}
</style>
</head>
<body>
<div class="container">

  <div class="header">
    <div class="brand"><span>Personal</span>Intelligence — Company Brief</div>
    <div class="company-name">{name}</div>
    <div class="meta-grid">
      <div class="meta-item">
        <div class="meta-label">AFM</div>
        <div class="meta-value">{afm}</div>
      </div>
      <div class="meta-item">
        <div class="meta-label">GEMI</div>
        <div class="meta-value">{ar_gemi}</div>
      </div>
      <div class="meta-item">
        <div class="meta-label">Status</div>
        <div class="meta-value"><span class="status-badge">{status_icon} {status_desc}</span></div>
      </div>
      <div class="meta-item">
        <div class="meta-label">Legal Form</div>
        <div class="meta-value">{legal_desc}</div>
      </div>
      <div class="meta-item">
        <div class="meta-label">Founded</div>
        <div class="meta-value">{inc_date}</div>
      </div>
      <div class="meta-item">
        <div class="meta-label">Address</div>
        <div class="meta-value">{address}</div>
      </div>
      {"" if not email else f'<div class="meta-item"><div class="meta-label">Email</div><div class="meta-value">{email}</div></div>'}
      {"" if not website else f'<div class="meta-item"><div class="meta-label">Website</div><div class="meta-value"><a href="{website}" style="color:#3b82f6">{website}</a></div></div>'}
    </div>
    {"" if not objective else f'<div class="objective"><strong>Objective:</strong> {objective[:500]}{"..." if len(objective) > 500 else ""}</div>'}
  </div>

  <div class="section">
    <h2>Intelligence Analysis</h2>
    <div class="analysis">
      {analysis_html}
    </div>
  </div>

  <div class="footer">
    <p>Generated {now} by <a href="https://personalintelligence.ai">PersonalIntelligence</a></p>
    <p style="margin-top:8px">Πηγή δεδομένων: ΓΕΜΗ — Κεντρική Ένωση Επιμελητηρίων Ελλάδος (ODC-BY-1.0)</p>
  </div>

</div>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

async def generate_brief(afm: str = None, name: str = None, open_browser: bool = True) -> Path:
    """Generate a company intelligence brief."""
    gemi = GemiClient(GEMI_API_KEY)

    # Step 1: Search GEMI
    print(f"[1/4] Searching GEMI for {'AFM ' + afm if afm else 'name: ' + name}...")
    if not GEMI_API_KEY:
        print("  WARNING: No GEMI_API_KEY set. Using demo mode with sample data.")
        print("  Register at: https://opendata.businessportal.gr/register/")
        print("  Then: export GEMI_API_KEY=your_key")
        # Demo mode — generate with placeholder
        company_data = _demo_company(afm or "000000000", name or "Demo Company")
    else:
        results = await gemi.search(afm=afm, name=name)
        if not results:
            print("  No companies found.")
            sys.exit(1)

        if isinstance(results, list):
            company_list = results
        else:
            company_list = results.get("results", results.get("companies", [results]))

        if len(company_list) > 1:
            print(f"  Found {len(company_list)} companies:")
            for i, c in enumerate(company_list[:10]):
                cname = c.get("coNameEl", "?")
                cafm = c.get("afm", "?")
                print(f"    [{i}] {cname} (AFM: {cafm})")
            # Use first result
            print(f"  Using first result.")

        first = company_list[0]
        ar_gemi = first.get("arGemi")

        # Step 2: Get full details
        print(f"[2/4] Fetching full details for GEMI #{ar_gemi}...")
        company_data = await gemi.get_company(ar_gemi)

    # Step 3: Web enrichment
    print("[3/4] Enriching with web data...")
    web_data = await enrich_web(
        company_data.get("coNameEl", ""),
        company_data.get("url"),
    )

    # Step 4: AI analysis
    print("[4/4] Running AI analysis...")
    analysis = await analyze_with_ai(company_data, web_data)

    # Generate HTML
    html = generate_html(company_data, analysis, web_data)

    # Save
    OUTPUT_DIR.mkdir(exist_ok=True)
    safe_name = (company_data.get("coNameEl", "company") or "company").replace(" ", "-")[:50]
    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
    filename = f"brief-{safe_name}-{timestamp}.html"
    filepath = OUTPUT_DIR / filename
    filepath.write_text(html, encoding="utf-8")

    print(f"\nBrief saved: {filepath}")

    if open_browser:
        webbrowser.open(f"file://{filepath.absolute()}")

    return filepath


def _demo_company(afm: str, name: str) -> dict:
    """Generate demo company data for testing without API key."""
    return {
        "arGemi": 123456789,
        "afm": afm,
        "coNameEl": name or "ΔΟΚΙΜΑΣΤΙΚΗ ΕΤΑΙΡΕΙΑ Α.Ε.",
        "coNamesEn": ["TEST COMPANY S.A."],
        "coTitlesEl": ["ΔΟΚΙΜΑΣΤΙΚΗ"],
        "city": "ΑΘΗΝΑ",
        "street": "ΣΤΑΔΙΟΥ",
        "streetNumber": "1",
        "zipCode": "10562",
        "url": "https://example.com",
        "email": "info@example.com",
        "objective": "Παροχή υπηρεσιών πληροφορικής και τεχνολογίας. Ανάπτυξη λογισμικού και εφαρμογών τεχνητής νοημοσύνης.",
        "legalType": {"description": "Ανώνυμη Εταιρεία"},
        "incorporationDate": "2015-03-15",
        "status": {"description": "Ενεργή"},
        "activities": [
            {"activity": {"code": "62.01", "description": "Δραστηριότητες προγραμματισμού ηλεκτρονικών υπολογιστών"}, "type": "Κύρια"},
            {"activity": {"code": "62.02", "description": "Δραστηριότητες παροχής συμβουλών σχετικά με τους ηλεκτρονικούς υπολογιστές"}, "type": "Δευτερεύουσα"},
        ],
        "persons": [
            {"personName": "ΠΑΠΑΔΟΠΟΥΛΟΣ ΓΕΩΡΓΙΟΣ", "role": "Πρόεδρος & Διευθύνων Σύμβουλος", "percentage": "60"},
            {"personName": "ΑΝΤΩΝΙΟΥ ΜΑΡΙΑ", "role": "Μέλος ΔΣ", "percentage": "40"},
        ],
        "capital": [{"amount": "50000", "currency": "EUR"}],
    }


def main():
    parser = argparse.ArgumentParser(
        description="PersonalIntelligence — Company Intelligence Brief Generator",
        epilog="Example: python company_brief.py --afm 094004914",
    )
    parser.add_argument("--afm", help="Company AFM (tax ID)")
    parser.add_argument("--name", help="Company name (partial match)")
    parser.add_argument("--no-open", action="store_true", help="Don't open in browser")

    args = parser.parse_args()

    if not args.afm and not args.name:
        parser.error("Provide either --afm or --name")

    asyncio.run(generate_brief(
        afm=args.afm,
        name=args.name,
        open_browser=not args.no_open,
    ))


if __name__ == "__main__":
    main()
