# Personal Intelligence — Operating Plan

**Version**: 1.0
**Date**: 1 April 2026
**Status**: Pre-revenue — building the model
**URL**: personalintelligence.ai

---

## 1. What We Do

We design, build, and operate bespoke AI systems for Greek businesses and professionals. Every system is custom-built for the client's specific workflows, data, and needs. We deliver a working prototype in 48 hours and a production system within 1-2 weeks.

We are not a platform. We are not a training academy. We build systems.

---

## 2. Service Packages

### 2.1 Knowledge Base
**One-liner**: All your company knowledge, searchable in seconds.
**What the client gets**: A unified, searchable system that ingests all company documents, emails, notes, and records. Queryable in Greek natural language.
**Target**: Any business with scattered information — law firms, medical practices, consulting firms, hotels.
**Setup**: €1,400–2,100 | **Monthly**: €140–280
**Delivery effort**: ~15 hours

### 2.2 Document Intelligence
**One-liner**: Upload, analyze, compare — auto-generated reports.
**What the client gets**: Automated document analysis — extract key points, detect contradictions, compare versions, generate structured reports. Works with legal docs, medical reports, financial statements, contracts.
**Target**: Lawyers, psychologists, accountants, consultants dealing with high document volume.
**Setup**: €2,100–3,500 | **Monthly**: €210–350
**Delivery effort**: ~25 hours

### 2.3 Client Finder
**One-liner**: AI-powered lead discovery and qualification.
**What the client gets**: A system that identifies, qualifies, and scores potential clients from public data, business directories, and industry signals. Automated outreach drafting. CRM intelligence layer.
**Target**: B2B service firms, real estate agencies, hotels seeking corporate clients.
**Setup**: €3,500–5,600 | **Monthly**: €350–560
**Delivery effort**: ~30 hours
**ICAP synergy**: Natural fit for co-branded offering — ICAP provides the business data layer, PI provides the intelligence.

### 2.4 Competitive Intelligence
**One-liner**: Know what your competitors do before they do it.
**What the client gets**: Continuous monitoring of competitors — web presence, pricing changes, new products, regulatory filings, market moves. Weekly or daily bespoke reports delivered automatically.
**Target**: Any business in a competitive market — hotels, real estate, professional services, retail.
**Setup**: €3,500–5,600 | **Monthly**: €350–700
**Delivery effort**: ~30 hours setup, then automated
**Revenue note**: Highest recurring revenue potential. Monitoring is inherently ongoing — clients can't turn it off without going blind.

### 2.5 Custom Build
**One-liner**: Describe what you need. We build it.
**What the client gets**: Fully bespoke system for any use case not covered above. Scoped after discovery call.
**Target**: Anyone with a specific need.
**Setup**: €5,600+ | **Monthly**: Negotiated
**Delivery effort**: 40+ hours

---

## 3. Pricing Philosophy

- **30% below Western European rates** — priced for the Greek market reality.
- **Setup fee covers the build** — prototype in 48h, production in 1-2 weeks.
- **Monthly fee covers operations** — monitoring, maintenance, improvements, SLA.
- **Two tiers per package**:
  - **Full Ownership**: Setup fee + handoff. Client runs it independently. No monthly.
  - **Managed Service**: Setup fee + monthly. We operate, monitor, and improve. Automated via Claude Code with defined SLAs.
- **Upsell path**: Knowledge Base → Document Intelligence → Client Finder / Competitive Intelligence. Each builds on the previous. Grow revenue per client naturally.

---

## 4. Delivery

### 4.1 Process
1. **Discovery** (Day 0): Client describes their pain via form, call, or in-person. We identify which package fits.
2. **Prototype** (Day 1-2): Working prototype delivered within 48 hours. Client sees their own data in the system.
3. **Refinement** (Day 3-10): Feedback loop. Adjust, extend, polish based on real usage.
4. **Handoff or Go-Live** (Day 10-14): Either hand over the system (Full Ownership) or activate managed service.
5. **Ongoing** (Managed only): Automated monitoring, monthly reports, continuous improvement.

### 4.2 Tech Stack
- **Engine**: LOSC (Life Operating System Core) — our proprietary AI infrastructure.
- **Deployment**: Each client gets a configured LOSC instance with only relevant modules active. Personal/family modules removed manually.
- **AI backbone**: Model-agnostic. Claude, OpenAI, DeepSeek, Gemini, Grok, Kimi, MiniMax, and more — plus open-source models running locally on our own servers (Ollama). Best model selected per task. No vendor lock-in for clients.
- **Managed service automation**: Claude Code agents running scheduled health checks, report generation, and SLA monitoring.
- **Data sovereignty**: Client data stays on their infrastructure. We do not store or access sensitive data unless explicitly authorised.

### 4.3 Fork Strategy
- **Current**: Deploy from LOSC monolith, strip personal modules per client manually.
- **Trigger for fork**: When manual stripping takes longer than the build, or when we exceed 5 active managed clients.
- **Future architecture**: Shared LOSC core (search, ingestion, API, agents, MCP) + pluggable module system. Personal LOSC = core + personal modules. Client systems = core + their package modules.

---

## 5. Team

### 5.1 Current
| Role | Person | Capacity |
|------|--------|----------|
| Founder / Lead architect | Ntemis | Full technical capability. Sets direction, handles complex builds, client relationships. |
| Delivery lawyers (x3) | Law firm staff | 70% delivery capability. Handle standard builds, client config, support. Need playbook. |

### 5.2 Scaling Plan
- **Month 1-3**: Ntemis + 3 lawyers. Max 2-3 concurrent builds. Focus on first 5 paying clients.
- **Month 4-6**: Develop delivery playbook from first 5 projects. Document repeatable patterns.
- **Month 6+**: Recruit Claude Code specialists via CollegeLink.gr. Target: university students with technical aptitude, trained on the PI delivery playbook.
- **Capacity model**: Each trained person handles ~2 managed clients or 1 active build. 4-person team = 6-8 managed clients + 2-3 concurrent builds.

### 5.3 Lawyer Delivery Playbook (to be developed)
After the first 3 client deliveries, document:
- Step-by-step onboarding procedure
- LOSC configuration checklist per package
- Testing and QA protocol
- Client communication templates
- Escalation triggers (when to pull in Ntemis)

---

## 6. Distribution

### 6.1 ICAP CRIF Partnership
- **Relationship**: Existing client and partner. Proven co-marketing track record.
- **Model**: Co-branded offering — "ICAP Intelligence powered by Personal Intelligence."
- **ICAP provides**: Business database, market credibility, client reach across all Greek businesses.
- **PI provides**: AI layer — analysis, monitoring, intelligence, custom systems.
- **Target products**: Client Finder and Competitive Intelligence are natural co-branded packages.
- **Action**: Propose co-marketing agreement. Start with 1 pilot package.

### 6.2 Direct Network
- Strong professional network in Greece — lawyers, doctors, business owners.
- Word-of-mouth from early clients.
- personalintelligence.ai form → LOSC pipeline → WhatsApp follow-up.

### 6.3 Social Media
- Strategy documented in `SOCIAL-STRATEGY.md`.
- LinkedIn (primary B2B) + Instagram (visual proof) + Facebook (Greek reach) + Twitter (tech credibility).
- Content pillars: demos (40%), before/after (25%), AI education in Greek (20%), testimonials (15%).
- Not yet active — launch after first 2 paying clients provide case study material.

---

## 7. Revenue Model

### 7.1 Revenue Streams
1. **Setup fees**: One-time per project. €1,400–5,600+ depending on package.
2. **Managed service subscriptions**: €140–700/month per client. Automated delivery, high margin after setup.
3. **ICAP co-branded revenue**: Revenue share or joint pricing on co-branded packages. TBD.

### 7.2 Projections (Conservative)

**Month 1-3 target**: 3 paying clients.
| Metric | Target |
|--------|--------|
| Clients | 3 |
| Setup revenue | €6,000–12,000 |
| Monthly recurring | €600–1,500/mo |
| Total Q1 | ~€8,000–16,500 |

**Month 4-6 target**: 5 additional clients (8 total).
| Metric | Target |
|--------|--------|
| Clients | 8 |
| Setup revenue (new) | €10,000–20,000 |
| Monthly recurring | €1,600–4,000/mo |
| Total Q2 | ~€15,000–32,000 |

**Month 7-12**: Scale via ICAP partnership + CollegeLink hires.
| Metric | Target |
|--------|--------|
| Clients | 15-20 |
| Monthly recurring | €4,000–10,000/mo |
| Annualised recurring | €48,000–120,000 |

### 7.3 Unit Economics
- **Gross margin on setup**: ~80% (time is the main cost, no infrastructure costs per client).
- **Gross margin on managed**: ~90% after automation (Claude Code handles monitoring, reports, health checks).
- **Break-even**: Client #2 covers operational costs. Client #5 covers Ntemis's time allocation.

---

## 8. The LOSC Flywheel

Every PI client delivery feeds back into LOSC:

```
Client need → Build/configure system → Learn what works
    ↓
Fold improvements into LOSC core
    ↓
Next client gets faster, better delivery
    ↓
Lower delivery cost → higher margin → more capacity
    ↓
More clients → more learning → better LOSC
```

This is the core competitive advantage. Competitors build one-off projects. PI builds on a living, improving platform that gets better with every deployment. After 10 clients, delivery that took 20 hours takes 8. After 20 clients, it takes 4.

---

## 9. Competitive Position

### Why PI wins in Greece
1. **We use what we sell.** LOSC is not a demo — it manages a real person's entire life. No competitor has that credibility.
2. **Greek-first.** Systems work in Greek. Support is in Greek. We understand Greek business culture, regulation, and pain points.
3. **48-hour prototype.** Competitors quote weeks for a proposal. We show a working system in 2 days.
4. **Data stays with the client.** In a market where trust matters, we never hold client data hostage.
5. **ICAP distribution.** Co-branded access to every serious Greek business. Ungated.

### Risks
- **Founder dependency**: Ntemis is the bottleneck until the playbook is written and team is trained.
- **LOSC complexity**: Deploying from a monolith means each client setup requires careful module management until the fork happens.
- **Greek market pricing**: SMBs may resist monthly fees. Prove ROI fast or offer quarterly billing.
- **AI model dependency**: Heavy reliance on Claude API. Mitigate with multi-model capability (already in LOSC via council).

---

## 10. Immediate Actions

### This Week
- [ ] Send Antonopoulou pitch email (first client)
- [ ] Identify 2 more warm leads from network for pilot clients
- [ ] Set up Stripe or billing integration through law firm

### This Month
- [ ] Close first paying client
- [ ] Deliver first prototype (48h challenge — prove the promise)
- [ ] Begin documenting delivery steps for the playbook
- [ ] Initiate ICAP co-marketing conversation

### This Quarter
- [ ] 3 paying clients across at least 2 package types
- [ ] Delivery playbook v1 complete
- [ ] 3 lawyers trained on standard deployments
- [ ] Social media launched with real case studies
- [ ] ICAP pilot co-branded package agreed

---

*This document is the operating plan for Personal Intelligence. Update it as decisions are made and the model evolves.*
*LOSC entity: to be created after first client closes.*
