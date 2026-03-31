# Personal Intelligence — Social Media Strategy

**Goal**: Drive form submissions on personalintelligence.ai
**Market**: Greek professionals and SMBs (lawyers, doctors, accountants, hotels, real estate)
**Voice**: Confident, technical but accessible, zero fluff. Show don't tell.
**Language**: Greek primary, English secondary (for international reach)

---

## Channels

| Channel | Role | Frequency | Content Type |
|---------|------|-----------|-------------|
| **LinkedIn** | Primary B2B | 3x/week | Case studies, demos, thought leadership |
| **Instagram** | Visual proof | 4x/week | Before/after, reels, infographics |
| **Facebook** | Greek market reach | 2x/week | Cross-post from LinkedIn + local events |
| **Twitter/X** | Tech credibility | Daily | AI insights, hot takes, threads |
| **YouTube** | Deep demos | 1x/week | Screen recordings, tutorials |

## Content Pillars

### 1. "Watch This" Demos (40%)
Short screen recordings showing AI doing real work:
- "We built this in 48 hours for a law firm"
- "This accountant's invoices now process themselves"
- "From 3 hours of data entry to 3 seconds"

**Format**: 30-60s reels/videos, screen capture with voiceover
**CTA**: "Describe what you need → personalintelligence.ai"

### 2. "Before/After" Transformations (25%)
Split-screen or side-by-side showing the old way vs the PI way:
- Manual email triage → automated inbox
- Paper filing → instant search
- Copy-paste reports → auto-generated documents

**Format**: Carousel posts (Instagram), image posts (LinkedIn/Facebook)
**CTA**: "Your workflow could look like this → link"

### 3. "AI Explained" Education (20%)
Demystify AI for Greek professionals — position PI as the trusted guide:
- "Τι μπορεί (και τι ΔΕΝ μπορεί) η AI για δικηγόρους"
- "5 πράγματα που αυτοματοποιεί η AI σε ένα λογιστικό γραφείο"
- "Γιατί τα δεδομένα σας πρέπει να μείνουν στον δικό σας server"

**Format**: Threads (Twitter), carousels (Instagram/LinkedIn)
**CTA**: "Ρωτήστε μας χωρίς δέσμευση"

### 4. Social Proof & Testimonials (15%)
Client quotes, feedback scores, pipeline stats:
- "5/5 from Dr. [Name] — document analysis system"
- Anonymised metrics: "73% time saved on report generation"
- Screenshot of feedback form submissions (with consent)

**Format**: Quote cards, short video testimonials
**CTA**: "Join them → personalintelligence.ai"

## Content Calendar Template

| Day | LinkedIn | Instagram | Twitter | YouTube |
|-----|----------|-----------|---------|---------|
| Mon | Demo post | Reel | AI insight | — |
| Tue | — | Before/After | Thread | — |
| Wed | Education | Story poll | Hot take | Upload |
| Thu | — | Reel | AI news + take | — |
| Fri | Case study | Carousel | Thread | — |
| Sat | — | Story | — | — |
| Sun | — | — | — | — |

## Automation via LOSC

The social pipeline is already built into LOSC:

```
Content idea → losc_thought(subcategory: "social")
              → losc_imagine(preset: "infographic") for visuals
              → losc_social_broadcast() for multi-platform posting
              → losc_twitter_post() / losc_instagram_post() / losc_facebook_post()
```

### Automated flows:
1. **New client feedback** (score 4+) → auto-draft testimonial post → review → broadcast
2. **Pipeline milestone** (lead → paid) → internal celebration thought, anonymised stat for social
3. **Weekly stats** → auto-generate "This week at PI" infographic

## Launch Sequence (Week 1-4)

### Week 1: Foundation
- [ ] Set up LinkedIn company page
- [ ] Set up Instagram business profile (@personalintelligence.ai)
- [ ] Create 5 demo videos from Antonopoulou system (anonymised)
- [ ] Design brand templates (Canva or losc_imagine)

### Week 2: Seed Content
- [ ] Post 3 "Watch This" demos
- [ ] Post 2 educational carousels in Greek
- [ ] Start daily Twitter presence (AI news + commentary)

### Week 3: Engagement
- [ ] Run first LinkedIn poll ("What takes the most time in your practice?")
- [ ] DM 10 target professionals with personalised demo links
- [ ] First YouTube deep-dive video

### Week 4: Optimise
- [ ] Review analytics — which content drove form submissions?
- [ ] Double down on winning format
- [ ] Ask first clients for video testimonials

## Metrics to Track

| Metric | Target (Month 1) | Target (Month 3) |
|--------|-------------------|-------------------|
| Form submissions | 5 | 20 |
| LinkedIn followers | 100 | 500 |
| Instagram followers | 200 | 1,000 |
| Demo video views | 500 | 5,000 |
| Conversion rate (view → form) | 1% | 2% |

## Key Rules

1. **Every post has a CTA** — either "personalintelligence.ai" or "reply/DM for a free assessment"
2. **Greek first** — the market is Greek professionals. English versions for reach.
3. **Show real systems** — screenshots, screen recordings, actual output. Never stock photos.
4. **Privacy sacred** — never reveal client data. Always anonymise or get explicit consent.
5. **Reply to everything** — every comment, every DM. The business IS personal attention.
6. **No AI-generated filler** — every post should have substance. Quality over quantity.
7. **Track attribution** — use `?source=linkedin` / `?source=instagram` params on the PI URL

## Hashtag Strategy

**Greek**: #τεχνητηνοημοσυνη #αυτοματοποιηση #ψηφιακοςμετασχηματισμος #AIγιαεπιχειρησεις
**English**: #AIforBusiness #CustomAI #PersonalIntelligence #Automation
**Industry**: #legaltech #healthtech #proptech #fintech

---

*This strategy feeds directly into the PI pipeline: social → form → LOSC → WhatsApp → Stripe → delivery → feedback → testimonial → social (flywheel)*
