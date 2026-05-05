# Methodology for DeepThought Internship Assignment

## Overview
This document outlines the end-to-end workflow used to identify, evaluate, and curate **25 target "Federer" companies** for DeepThought's Business Analytics Internship.

1. **Data-source selection** — primary registries, industry directories, government portals, and professional networks.
2. **Automated extraction & enrichment** — Python scripts that pull raw company lists, scrape websites, and query LinkedIn, MCA, and news APIs for evidence.
3. **Scoring engine** — a deterministic function that maps the six criteria to *Weak / Moderate / Strong* based on keyword patterns and quantitative signals.
4. **Manual validation** — a human reviewer checks the top-N candidates, adds evidence links, and finalises the CSV.
5. **Deliverables** — CSV, methodology, and scoring code.

The methodology is intentionally reproducible so the same pipeline can be scaled to **1,000 companies** (see `partB_sourcing_and_1000_proposal.md`).

---

## 1. Data Sources

| Category | Source | Why It Fits the ICP | Access Method |
|----------|--------|---------------------|---------------|
| Corporate Registry | Ministry of Corporate Affairs (MCA) | Official registration, city, incorporation date, paid-up capital | REST API (JSON) |
| Financials & Revenue | Tofler / MCA annual returns | Revenue band, growth trends | Web-scrape / CSV export |
| Industry Directories | Indian Chemical Manufacturers Association, Biotech India, SISI | Curated lists of specialty manufacturers | PDF/HTML download |
| Government Programs | PLI scheme participant list, EPCG list, Make-in-India | Confirms sector tailwinds and Indian-based operations | Open data portals (CSV) |
| Professional Networks | LinkedIn (Company pages, Sales Navigator), Naukri job postings | Hiring signals, team size, technical leadership | LinkedIn API / manual search |
| News & Announcements | Google News API, Press-release feeds | Facility expansions, certifications, new contracts | API / RSS |
| Patents & Regulatory | Indian Patent Office, USFDA/EU-GMP databases | Demonstrates differentiated IP | Patent search CSV |

## 2. Enrichment Pipeline

The `src/` folder contains the scoring script:
- `scoring.py` — implements the deterministic scoring (see below).

For each company, the following data points were collected:
- Company website content (About, Manufacturing, Careers pages)
- LinkedIn company profile (employee count, recent posts)
- News articles (Google News, Economic Times, BioSpectrum)
- Patent filings (Indian Patent Office, Google Patents)
- Regulatory approvals (USFDA facility list, EU-GMP certificates)
- Job postings (Naukri, LinkedIn Jobs)

## 3. Scoring Logic (Criteria Mapping)

| Criterion | Evidence Signals | Weight | Weak / Moderate / Strong Mapping |
|-----------|-----------------|--------|----------------------------------|
| C1 Manufacturer | Keywords: "factory", "plant", "in-house production"; manufacturing address | 10% | Strong if explicit plant listed; Moderate if only assembly; else Weak |
| C2 India-based | Registered address in India AND manufacturing location in India | 5% | Strong if both; Moderate if only address; else Weak |
| C3 Differentiated | Patents, USFDA/EU-GMP approval, "first/only" claim, proprietary tech | 25% | Strong if any of these appear; Moderate if R&D centre but no IP; else Weak |
| C4 Technical DM | Founder/MD bio: PhD, IIT/NIT/IISC, ex-ISRO/DRDO, publications | 20% | Strong if PhD or ex-ISRO; Moderate if engineering degree; else Weak |
| C5 Growing Sector | Sector listed in PLI or Make-in-India priority list | 20% | Strong if PLI-eligible; Moderate if stable sector; else Weak |
| C6 Growth Signals (≥2) | Hiring >5 new roles, plant news, new cert, revenue growth, new export market | 20% | Strong if ≥2 signals; Moderate if 1; else Weak |

The script returns a **Federer Score** (0–100) and the per-criterion ratings used in the CSV.

## 4. Manual Validation

1. Sort the enriched list by **Federer Score** (descending).
2. Review the top entries; verify each evidence link (company website, LinkedIn, news article).
3. Record any disqualifications with a short rationale (e.g., "Trader only, no plant").
4. Choose the top 25 that satisfy score ≥ 80 (or best-available if fewer).
5. Populate the final CSV with the required columns.

## 5. City Selection: Why Hyderabad?

- **Genome Valley** — India's largest life-sciences cluster (200+ biotech companies)
- **PLI Scheme** — Hyderabad pharma/biotech companies are PLI beneficiaries
- **Talent density** — University of Hyderabad, IICT, CCMB provide pipeline
- **Government support** — Telangana state actively promotes biotech manufacturing
- **DeepThought fit** — Many mid-size manufacturers (Rs.50Cr–500Cr) with technical founders

## 6. Limitations & Assumptions

- Revenue figures are approximate (sourced from Tofler, Tracxn, company websites)
- Some smaller companies have limited public data; scoring relied on available evidence
- LinkedIn data is point-in-time and may not reflect current headcount
- The scoring model weights are based on the assignment brief's emphasis on differentiation and growth

---

*The same pipeline, with minor parameter tweaks (e.g., expanding the industry-segment filter), will be used to generate the 1,000-company list in Phase 2 of the scale-up proposal.*
