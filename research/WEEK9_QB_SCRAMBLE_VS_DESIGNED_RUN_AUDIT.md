# WEEK9 QB Scramble vs Designed Run Audit (Weeks 1–8)

**As of:** 2026-11-07 ~11:53 ET
**Status:** Research evidence only. No model coefficients fit. Model NOT READY.
**Retrieval date:** 2026-11-07.

## Source
- **Primary:** nflverse / nflfastR play-by-play 2026 (public, CC-BY-4.0).
- **Release:** https://github.com/nflverse/nflverse-data/releases/expanded_assets/pbp (play_by_play_2026.csv.gz updated 2026-11-07).
- **Key fields present:** `qb_dropback`, `qb_scramble`, `qb_kneel`, `qb_spike`, `play_type`, `desc`, `game_id`, `play_id`, `down`, `ydstogo`, `score_differential`, `posteam`, `passer_player_name`, `rusher_player_name`.
- **Definitions (from nflfastR field descriptions):**
  - `qb_dropback`: binary for whether the QB dropped back (pass attempt, sack, or scramble).
  - `qb_scramble`: binary for whether the QB scrambled.
  - `qb_kneel`: binary for QB kneel.
  - Designed runs are QB rushes that are not flagged as scrambles or kneels (play_type = run and rusher is QB, not scramble/kneel).
- **Prior branch note:** All 32 attempt discrepancies previously explained by spikes being counted differently; designed-rush distinction remains partial.

## Priority QBs (Weeks 1–8 available observations)
| QB | Team | Notes from public sources | Sample-size warning |
|----|------|---------------------------|---------------------|
| Josh Allen | BUF | Multiple sources note high scramble volume; Week 5 example cited 8 scrambles + 1 designed run. | Full play-level separation requires nflverse pbp filter. |
| Lamar Jackson | BAL | On IR as of 2026-11-07; limited games (5 with stats noted). | Small sample; IR status. |
| Brock Purdy | SF | Public sources note low designed-run volume. | Standard sample. |
| Drake Maye | NE | Public play logs note scrambles and kneels. | Standard sample. |

Other QBs with sufficient dropback observations can be stratified the same way once the full pbp is filtered.

## Requested metrics (available vs missing)
- **Available in free nflverse pbp:** dropbacks (`qb_dropback`), scrambles (`qb_scramble`), scramble yards (yards_gained on scramble plays), kneels (`qb_kneel`), designed runs (QB rushes not flagged scramble/kneel), sacks (sack == 1), game_id / play_id, down/ydstogo, score differential for game-state stratification.
- **Missing or incomplete in free public pbp:** charted pressures (no consistent free `qb_hit` or pressure flag that equates to charted pressure), blitz indicators with reliable coverage (some blitz fields exist but are incomplete), and confirmed clean-pocket indicators. “No QB hit recorded” is **not** treated as a confirmed clean pocket.
- **Rates that can be computed from free data:** P(scramble | dropback), P(scramble | no charted pressure) cannot be reliably computed because charted pressure is not fully available. Association only; no causation claimed.

## Stratification
- Down/distance and score differential can be applied where sample sizes permit (recommended minimum ~20 dropbacks per bin).
- Lamar Jackson sample is small due to IR and limited games; flag as low-confidence.

## Uncertainty / sample-size warnings
- Scramble vs designed-run distinction in nflverse relies on play description parsing and manual adjustments; false positives have been noted in historical seasons.
- Charted pressure data is restricted (PFF/FTN) or incomplete in free pbp; do not treat absence of a hit as clean.
- No model coefficients fit. No production writes.

## What remains unavailable
- Full charted pressure and blitz flags with denominators for all priority QBs.
- Confirmed clean-pocket indicators.
- Per-play source timestamps beyond the nflverse release date (2026-11-07).

**Rules followed:** Designed runs kept separate from scrambles. No inference of clean pocket from missing hit. No causation claimed. No model changes.
