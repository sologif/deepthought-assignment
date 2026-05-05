# DeepThought Business Analytics Internship – Assignment

## About DeepThought
DeepThought is a B2B company that helps Indian manufacturing MSMEs become better-run organizations through execution consulting and PDGMS, an AI-powered SaaS operating system.

## Assignment Overview

### Part A – Target Company Research
Identify and profile **25 "Federer" companies** — Indian specialty manufacturers in Hyderabad that match DeepThought's Ideal Customer Profile (ICP).

**Deliverables:**
- `output/target_companies_25.csv` — 25 companies with 6-criterion Federer scoring
- `docs/methodology.md` — Research methodology and data sources
- `src/scoring.py` — Reusable scoring engine

### Part B – Sourcing Strategy & Scale-Up Proposal
- `docs/partB_sourcing_and_1000_proposal.md` — Sourcing methods + 1,000-company outreach plan
- `assets/hand_drawn_funnel.jpg` — Hand-drawn funnel diagram *(to be added)*

## Folder Structure
```
deepthought-assignment/
│
├── output/
│   └── target_companies_25.csv
│
├── src/
│   └── scoring.py
│
├── docs/
│   ├── methodology.md
│   └── partB_sourcing_and_1000_proposal.md
│
├── assets/
│   └── hand_drawn_funnel.jpg   ← upload your hand-drawn diagram
│
└── README.md
```

## Scoring Criteria (Federer Score)
| # | Criterion | Weight | What We Look For |
|---|-----------|--------|------------------|
| C1 | Manufacturer | 10% | In-house production, factory/plant |
| C2 | India-based | 5% | Registered + manufacturing in India |
| C3 | Differentiated | 25% | Patents, USFDA/EU-GMP, proprietary tech |
| C4 | Technical Decision-Maker | 20% | PhD / IIT / ex-ISRO founder or MD |
| C5 | Growing Sector | 20% | PLI-eligible, Make-in-India priority |
| C6 | Growth Signals (≥2) | 20% | Hiring, plant expansion, new certs |

## Target Segment
**Specialty Biotech** — Hyderabad (Genome Valley hub)

## How to Run the Scoring Engine
```bash
pip install pandas
python src/scoring.py
```

## Author
**Anushka** — MSIT, Delhi  
[GitHub](https://github.com/sologif) · [LinkedIn](https://linkedin.com/in/anushka)
