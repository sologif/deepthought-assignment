# Part B – Sourcing Strategy & 1,000-Company Scale-Up Proposal

## Question 1: How Would You Source Target Companies?

### 1.1 Primary Sourcing Channels

| Channel | What It Gives Us | Effort | Quality |
|---------|------------------|--------|---------|
| **MCA / Registrar of Companies** | Official company list filtered by NIC code, city, incorporation date | Low (API/bulk download) | High |
| **Industry Directories** (BioSpectrum, Pharma Bio World, ICMA) | Curated manufacturer lists with product details | Medium (manual + scraping) | High |
| **PLI / Make-in-India Participant Lists** | Government-verified manufacturers in priority sectors | Low (PDF/CSV from DPIIT) | Very High |
| **LinkedIn Sales Navigator** | Decision-maker profiles, company size, hiring activity | Medium (manual + API) | High |
| **Naukri / Indeed Job Postings** | Hiring signals = growth proxy; reveals plant locations | Low (automated scrape) | Medium |
| **Google News Alerts** | Expansion announcements, new certifications, funding | Low (RSS/API) | Medium |
| **Trade Shows & Conferences** (BioAsia, CPHI India) | Exhibitor lists = active manufacturers seeking visibility | Medium (annual, PDF) | High |
| **Patent Databases** (Indian Patent Office, Google Patents) | Differentiates innovators from generic manufacturers | Medium (search + export) | High |
| **Startup Databases** (Tracxn, Crunchbase) | Funding, team, revenue estimates for emerging companies | Low (API/export) | Medium |

### 1.2 Sourcing Workflow

```
┌─────────────────┐
│ 1. Bulk Extract  │  MCA, industry directories, PLI lists
│    (Universe)    │  → ~5,000 raw entries
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 2. Filter        │  City, NIC code, revenue band, active status
│    (Longlist)    │  → ~1,500 qualified
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 3. Enrich        │  LinkedIn, website, news, patents, jobs
│    (Data Layer)  │  → structured JSON per company
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 4. Score         │  6-criterion Federer scoring engine
│    (Shortlist)   │  → ranked list with scores
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 5. Validate      │  Manual review of top candidates
│    (Final List)  │  → 25 / 100 / 1,000 verified targets
└─────────────────┘
```

### 1.3 Quality Assurance

- **Cross-reference** every company against at least 2 independent sources
- **Disqualify** traders, distributors, and shell companies (no manufacturing evidence)
- **Flag** companies with <2 years of operations or litigation/insolvency proceedings
- **Verify** decision-maker profiles on LinkedIn (not just company website)

---

## Question 2: Proposal for Sourcing 1,000 Companies

### 2.1 Scaling Strategy

To go from 25 → 1,000 companies, we expand across three dimensions:

| Dimension | From (25) | To (1,000) |
|-----------|-----------|------------|
| **Geography** | Hyderabad only | 8 cities: Hyderabad, Pune, Ahmedabad, Chennai, Coimbatore, Vadodara, Bengaluru, Indore |
| **Segments** | Specialty Biotech | + Performance Chemicals, Precision Engineering, Advanced Materials, Agri-tech |
| **Revenue Band** | Rs.50Cr–500Cr+ | Rs.10Cr–1,000Cr (wider funnel) |

### 2.2 Phase Plan

#### Phase 1: Foundation (Week 1–2)
- Deploy MCA bulk extractor for all 8 cities × 5 segments
- Set up automated enrichment pipeline (LinkedIn API, Google News, patent search)
- Expected output: **3,000–5,000** raw entries

#### Phase 2: Scoring & Filtering (Week 3)
- Run `scoring.py` on the full universe
- Apply Federer Score threshold (≥70 for longlist, ≥80 for shortlist)
- Expected output: **1,200–1,500** scored companies

#### Phase 3: Validation & Curation (Week 4)
- Manual review of top 1,000 by score
- Cross-reference with industry experts and trade body member lists
- Final output: **1,000 verified Federer companies**

### 2.3 Automation & Tools

| Tool | Purpose | Cost |
|------|---------|------|
| Python + Pandas | Data extraction, cleaning, scoring | Free |
| Selenium / Playwright | Web scraping for company websites | Free |
| LinkedIn Sales Navigator | Decision-maker identification | ~$80/mo |
| Google Custom Search API | News and website indexing | ~$5/1K queries |
| Airtable / Google Sheets | Collaborative review and validation | Free tier |
| GitHub Actions | Scheduled data refresh (weekly) | Free tier |

### 2.4 Team & Timeline

| Role | Hours/Week | Duration |
|------|-----------|----------|
| Lead Analyst (me) | 20 hrs | 4 weeks |
| Data Engineer (automation) | 10 hrs | 2 weeks |
| Domain Expert (validation) | 5 hrs | 1 week |
| **Total effort** | **~100 person-hours** | **4 weeks** |

### 2.5 Quality Metrics

| Metric | Target |
|--------|--------|
| Data completeness (all columns filled) | ≥95% |
| Cross-reference rate (2+ sources) | ≥90% |
| Federer Score ≥80 | ≥60% of final list |
| Decision-maker identified | ≥85% |
| Website verified & active | 100% |

### 2.6 Ongoing Maintenance

- **Weekly refresh**: GitHub Actions cron job re-runs enrichment on new MCA filings
- **Quarterly review**: Re-score all 1,000 companies with updated data
- **Expansion**: Add 200–300 new companies per quarter as sectors grow

---

## Funnel Diagram Description

The hand-drawn funnel diagram (see `assets/hand_drawn_funnel.jpg`) illustrates:

```
        ╔══════════════════════════════════════╗
        ║     UNIVERSE: ~5,000 raw entries     ║  ← MCA, directories, PLI lists
        ╠══════════════════════════════════════╣
        ║                                      ║
        ║  FILTER: City + Segment + Revenue    ║  → ~1,500
        ║                                      ║
        ╠══════════════════════════════════════╣
        ║                                      ║
        ║  ENRICH: LinkedIn + News + Patents   ║  → ~1,200
        ║                                      ║
        ╠══════════════════════════════════════╣
        ║                                      ║
        ║  SCORE: Federer 6-criteria engine    ║  → ~1,000
        ║                                      ║
        ╠══════════════════════════════════════╣
        ║                                      ║
        ║  VALIDATE: Manual expert review      ║  → 1,000 final
        ║                                      ║
        ╚══════════════════════════════════════╝
```

*Note: Upload the actual hand-drawn diagram as `assets/hand_drawn_funnel.jpg`.*
