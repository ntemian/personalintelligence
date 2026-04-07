# LOSC CRM Module — Product Concept

**Origin:** Discord thought, 6 Apr 2026
**Status:** Concept / Design phase
**Decision:** LOSC module (not standalone) — 80% of infrastructure already exists

---

## Problem Statement

Ntemis has 5,320 contacts and 9,661 companies in Connector, plus unified messaging across 6 platforms (WhatsApp, Viber, SMS, Telegram, Gmail, Discord) and AI phone calls — but **no automatic relationship tracking**. Every interaction is a data point that disappears into channel silos. There's no "when did I last talk to X?", no decay alerts, no deal pipeline for PersonalIntelligence consultancy.

## What Already Exists in LOSC

| Capability | Tool | Status |
|---|---|---|
| Unified contact view | `losc_contact` | ✅ Working |
| Communication history | `losc_comms_log` | ⚠️ Schema exists, no auto-logging |
| Unified inbox | `losc_messages` | ✅ Working (6 platforms) |
| AI phone calls + transcripts | `losc_phone_call/history` | ✅ Working |
| Morning comms triage | `losc_comms_triage` | ✅ Working |
| Contact graph + tags | Connector (5,320 people) | ✅ Working |
| Company database | Connector (9,661 companies) | ✅ Working |
| Referral chains | Connector (399 chains) | ✅ Working |
| Relationship health agent | `losc_relationship_capital_*` | ❌ Stopped — needs rebuild |
| Google Contacts sync | `losc_contacts_sync` | ✅ Connected |

## What Needs Building (the 20%)

### Layer 1: Auto-Touchpoint Logger
**The backbone.** Every inbound/outbound message and call creates a `touchpoint` record:

```
touchpoint {
  contact_id: "person:john-smith"
  channel: "whatsapp" | "viber" | "sms" | "telegram" | "email" | "discord" | "phone" | "in-person"
  direction: "inbound" | "outbound"
  timestamp: ISO8601
  summary: "Discussed project timeline" (AI-generated, not raw content)
  sentiment: "positive" | "neutral" | "negative"
  follow_up_needed: bool
  follow_up_by: ISO8601 | null
  deal_id: string | null
}
```

**Implementation:** Hook into existing message/phone handlers. When `losc_messages` processes a message or `losc_phone_call` completes, auto-create a touchpoint. Privacy-first: store AI summary, not raw content.

### Layer 2: Relationship Health Score

Per-contact score (0-100) based on:
- **Recency** — days since last touchpoint (exponential decay)
- **Frequency** — touchpoints per month vs historical baseline
- **Reciprocity** — ratio of inbound vs outbound (one-sided = unhealthy)
- **Depth** — call > meeting > long message > short message > reaction
- **Sentiment trend** — improving or declining?

Formula: `health = w1*recency + w2*frequency + w3*reciprocity + w4*depth + w5*sentiment`

Decay rate varies by relationship tier:
- **Inner circle** (family, close friends): alert after 7 days silence
- **Active network** (colleagues, collaborators): alert after 30 days
- **Warm contacts** (occasional): alert after 90 days
- **Cold contacts**: no alerts, but track for Connector enrichment

### Layer 3: Deal Pipeline (for PersonalIntelligence)

Simple Kanban pipeline:
```
Lead → Qualified → Proposal → Negotiation → Won/Lost
```

Each deal links to:
- Contact(s) + Company
- Touchpoint history
- Estimated value
- Next action + deadline
- Referral source (from Connector's referral chains)

### Layer 4: Follow-Up Engine

Proactive nudges integrated into `/brief`:
- "You haven't spoken to **Apollon** in 8 days" (inner circle alert)
- "**John Smith** sent you a WhatsApp 3 days ago — no reply" (reciprocity gap)
- "Deal **PI-003** next action overdue by 2 days" (pipeline alert)
- "**Maria K.** birthday in 3 days — last touchpoint 45 days ago" (opportunity)

### Layer 5: `/crm` Command

```
/crm                    — Dashboard: health alerts + pipeline + today's follow-ups
/crm {name}             — Contact CRM card: touchpoints, health score, deals, notes
/crm pipeline           — Deal pipeline Kanban view
/crm neglected          — Contacts with declining health scores
/crm touchpoints {name} — Full interaction timeline for a person
/crm log {name} {note}  — Manual touchpoint (meetings, in-person)
/crm deal new           — Create a new deal
/crm stats              — Relationship analytics (most active, most neglected, response times)
```

## Architecture

```
┌─────────────────────────────────────────────┐
│                  /crm command                │
├─────────────────────────────────────────────┤
│          CRM Router (api/routers/crm.py)     │
├──────────┬──────────┬───────────┬───────────┤
│Touchpoint│ Health   │ Pipeline  │ Follow-up │
│ Logger   │ Scorer   │ Manager   │ Engine    │
├──────────┴──────────┴───────────┴───────────┤
│              LOSC Core Database              │
├──────────┬──────────┬───────────┬───────────┤
│losc_msgs │losc_phone│ Connector │losc_comms │
│(6 chans) │ (calls)  │ (graph)   │ (log)     │
└──────────┴──────────┴───────────┴───────────┘
```

**New tables:**
- `crm_touchpoints` — interaction log
- `crm_health_scores` — cached per-contact scores (recomputed daily)
- `crm_deals` — pipeline entries
- `crm_follow_ups` — scheduled nudges

**New LOSC MCP tools:**
- `losc_crm_dashboard` — main view
- `losc_crm_contact` — enriched contact card
- `losc_crm_touchpoint` — log interaction
- `losc_crm_deal` — manage deals
- `losc_crm_health` — relationship health query
- `losc_crm_neglected` — at-risk relationships

## Why LOSC Module (Not Standalone)

1. **Data gravity** — contacts, messages, phone, email already live in LOSC
2. **No re-integration** — standalone CRM would need APIs to every messaging platform LOSC already handles
3. **Briefing integration** — `/brief` already aggregates daily priorities; CRM nudges slot right in
4. **Connector synergy** — referral chains + company graph + tag groups = instant CRM enrichment
5. **PersonalIntelligence** — when PI launches, the CRM module becomes its sales engine, no migration needed

## Build Sequence

| Phase | What | Effort | Dependencies |
|-------|------|--------|-------------|
| 1 | Touchpoint logger + DB tables | 1 session | Message/phone hook points |
| 2 | Health score computation | 1 session | Phase 1 |
| 3 | `/crm` command (basic) | 1 session | Phase 1-2 |
| 4 | Follow-up engine + `/brief` integration | 1 session | Phase 2-3 |
| 5 | Deal pipeline (for PI) | 1 session | Phase 3 |
| 6 | Rebuild Relationship Capital Agent on CRM data | 1 session | Phase 1-4 |

## Relationship to Existing Systems

- **Connector** — READ-ONLY source. CRM adds temporal data on top of Connector's static graph.
- **Relationship Capital Agent** — REPLACED by CRM health scores. Agent was stopped because it was noisy without real touchpoint data. CRM fixes the data problem first.
- **`losc_comms_log`** — SUPERSEDED by `crm_touchpoints`. Richer schema, auto-populated.
- **`/brief`** — CONSUMER. CRM follow-ups appear in morning briefing.

## Open Questions

1. **Privacy granularity** — Should touchpoint summaries be opt-in per contact? (e.g., don't summarize lawyer messages)
2. **Retroactive backfill** — Can we mine existing `losc_messages` history to seed touchpoints?
3. **In-person logging** — Voice capture (`losc_voice_capture`) after meetings → auto-touchpoint?
4. **Multi-user** — If PersonalIntelligence grows, does this need team CRM features?
