# PFF Week 9 Recap fetch — JAX 33, BAL 10 (POSTGAME ONLY)

**Classification:** POSTGAME_EVIDENCE_ONLY — not a pregame forecast input; do not feed CORE projection_ready / as-of freeze.
**Event:** NFL Week **9** · 2026-11-05 · Jacksonville @ Baltimore · Final JAX 33–BAL 10  
**ESPN event id (local audit):** `401873037`  
**Canonical folders:** `/workspace/nfl-database/live/2026-11-05_JAX_BAL/` (not week10 planning labels)

## Source
- URL: https://www.pff.com/news/nfl-week-9-recap-jacksonville-jaguars-33-baltimore-ravens-10
- Byline: Mark Chichester · Posted Nov 5, 2026 11:42 pm EST (JSON-LD `datePublished` 2026-11-06T04:42:33Z)
- JSON-LD: `NewsArticle`, `isAccessibleForFree: true`, **no `articleBody` field** (empty prose body in schema)

## Fetch attempts (authorized public only; no login/paywall bypass)
| Method | Result | Artifact |
|---|---|---|
| Firecrawl scrape JSON | SUCCESS (Scrape ID `01a1b129-064a-754d-946d-e6a0d329fb69`) | `firecrawl_pff_jaxbal_wk9.json` |
| Firecrawl scrape markdown | SUCCESS (`01a1b129-0d32-7078-8930-a48d83918679`) | `firecrawl_pff_jaxbal_wk9.md` (~56KB rendered widget text) |
| curl HTML | SUCCESS HTTP body ~81KB | `raw_curl.html` |
| Author public mirror | SUCCESS | `https://markchichester.github.io/PFF_Chichester/week-9_jacksonville-jaguars-33_at_baltimore-ravens-10_v4.html` → `mirror_chichester_v4.md` |
| Parent WebFetch | Metadata/title only (no body) — expected given schema |

**Content shape:** Public page is an interactive **game-recap dashboard** (overview / rush / pass / QB / snaps / initial grades / coverage widgets), not a traditional narrative article. Premium upsells present (`Go Premium`, `PFF Pro` trial) but core dashboard widgets were returned without authentication.

## Pulled stamp
America/New_York local pull ~2026-11-06 morning (executor); files mtime on box.
