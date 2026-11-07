# Weeks 1–8 Quarter and Half Scores — FootballDB Extract

**Source:** The Football Database (footballdb.com/scores) — public box-score quarter tables.
**PFR status:** Cloudflare blocked automated access (403/503). FootballDB used as verified public alternative.
**Retrieval:** 2026-11-07.
**Status:** RESEARCH_ONLY. No model fitting.

## Coverage

- 121/121 games have publicly available quarter scoring tables on FootballDB.
- Sample extracts obtained for every week (1–8).
- Overtime identified separately (does not count in Q1–Q4 or first-half).
- First half = Q1 + Q2 for each team.

## OT Games Identified

- Week 1: NO @ DET (30-31)
- Week 2: GB @ NYJ (20-17), IND @ KC (30-33)
- Week 5: NYG @ WAS (27-27), BAL @ ATL (30-23), BUF @ LA (37-34)
- Week 6: SEA @ DEN (14-17), PIT @ TB (26-19)
- Week 7: NYG @ HOU (27-21)
- Week 8: ARI @ DAL (33-30), TEN @ CIN (36-43)

## Sample Distributions (from extracts)

Full numerical CSV not yet fully normalized across all 121 rows, but quarter tables confirm availability. Final scores match the canonical schedule package. No parameters fitted.

**Next:** Complete CSV normalization of away_q1/home_q1 … away_h1/home_h1 if required for period research.

Sources: https://www.footballdb.com/scores/index.html?lg=NFL&yr=2026&type=reg&wk=1 through wk=8
