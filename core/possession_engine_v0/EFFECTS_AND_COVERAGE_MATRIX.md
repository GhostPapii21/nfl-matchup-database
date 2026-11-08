# Effects / coverage / pressure matrix (updated 2026-11-05 ~16:11 ET)

Attribution: FTN public subset via nflverse (CC-BY-SA) — attribute **FTN Data via nflverse**. Paid FTN catalog fields (`qbp` true pressure, `rte` routes) **not** in free 29-col extract.

| Feature | Status | Source | n / dates | Alters sim? |
|---|---|---|---|---|
| Q1–Q4 / H1 / H2 / reg / OT scoreboards | **IMPLEMENTED** | event `add_score` → period bucket | sim | Yes |
| Explosive pass≥20 / rush≥12 | **IMPLEMENTED** | PBP | W1–8 | annotate + tables |
| FTN blitz `n_blitzers≥1` | **IMPLEMENTED** | local ftn_charting_2026 | join_rate≈0.97; date_pulled in file | Yes (strata) |
| Defense empirical blitz rate faced | **IMPLEMENTED** | FTN×PBP by defteam | see dossier | Yes (`EFFECT_DEF_BLITZ_*`) |
| Pressure PROXY (sack\|qb_hit\|scramble) | **IMPLEMENTED tables** | PBP | labeled PROXY | audit; not mislabeled as true pressure |
| True pressure (`qbp`) | **MISSING** | Paid FTN catalog only | — | No |
| Man/zone / MOFO / MOFC / routes | **MISSING** | Not in nflverse FTN 29-col dictionary | confirmed nflreadr dictionary | Sensitivity only |
| CB/S/DT replacements | **UNVERIFIED notes** | r6 coverage.json | assignment_status UNVERIFIED | No coefficients |
| Shaan numbers | **ATTRIBUTED_NOT_VERIFIED** | — | — | Not model inputs |
