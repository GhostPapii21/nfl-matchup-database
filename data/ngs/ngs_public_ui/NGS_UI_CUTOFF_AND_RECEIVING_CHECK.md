# NFL Next Gen Stats public UI: week-filter and receiving-field check

Captured: 2026-11-07 08:16 EST
Purpose: validate the visible 2026 week selector/cutoff and inspect the public receiving leaderboard for actual routes/alignment fields. This is not a transcription of the full passing table; the parent noted that table is already captured at `v7raw/ngs_passing.md`.

## Findings

- Public NGS pages expose Season `2026` and a Week selector. Selecting `Week 8` in the visible UI changed the URL to `/2026/REG/8`; the screenshot shows `Week 8` selected and a week-specific passing leaderboard. The corresponding receiving URL also resolves to `/stats/receiving/2026/REG/8` and the visible rows are week-specific (e.g. individual weekly reception/target totals), not season-to-date totals.
- The selector is a single-week filter; no W1–8 multi-week range selector was observed. For a defensible W1–8 dataset, collect/aggregate Weeks 1 through 8 individually and exclude the `Regular Season`/`all` view. The `/all` view is not an explicit W1–8 cutoff. This check does not establish whether that live all-season view already contains Week 9 Thursday; do not label it W1–8.
- Passing qualifier: the Week 8 page footer says `Minimum 15 Pass Attempts`. The Regular Season `/all` page says `Minimum 68 Pass Attempts` and gives `(15 Attempts, Multiplied By Number of Weeks, Divided By 2)`. A player missing below a qualifier is not a zero. The 68-attempt all-season threshold is not a W1–8 threshold. This UI check does not reconcile the previously noted 14 attempt discrepancies.
- Receiving leaderboard columns visible: `CUSH`, `SEP`, `TAY`, `TAY%`, `REC`, `TAR`, `CTCH%`, `YDS`, `TD`, `YAC/R`, `xYAC/R`, `+/-`; the Week 8 page footer says `Minimum 5 Targets`. No route count or receiver alignment/formation column was present. CUSH/SEP are aggregate receiver metrics, not route classifications or attribution to a named defender.
- The linked official NGS glossary defines: CUSH as yards between a WR/TE and the defender they are lined up against at snap on all targets; SEP as yards to the nearest defender at catch/incompletion; TAY as average passing air yards per target; TAY% as receiver intended air yards divided by team intended air yards; YAC as yards gained after catch; xYAC as expected yards after catch; and `+/-` as YAC compared with xYAC.
- Passing glossary definitions relevant to the published table: TT averages snap-to-throw time on pass attempts (sacks excluded); CAY/IAY are average air yards on completions/all attempts; AYD is CAY minus IAY; LCAD is actual release-to-reception distance; AGG% is attempts into coverage with a defender within 1 yard at completion/incompletion divided by attempts; AYTS is air yards relative to the first-down marker; xCOMP is expected completion percentage; `+/-` is actual completion percentage compared with xCOMP.

## Exact source URLs inspected

- Passing live regular-season view: https://nextgenstats.nfl.com/stats/passing/2026/REG/all#yards
- Passing Week 8 selected in public UI: https://nextgenstats.nfl.com/stats/passing/2026/REG/8#yards
- Receiving regular-season view: https://nextgenstats.nfl.com/stats/receiving#yards
- Receiving Week 8 selected in public UI: https://nextgenstats.nfl.com/stats/receiving/2026/REG/8#yards
- Official glossary: https://nextgenstats.nfl.com/glossary

## Evidence screenshots

- `evidence/NGS_2026_Week8_passing_filter.png`
- `evidence/NGS_2026_Week8_receiving_filter.png`
- `evidence/NGS_2026_receiving_regular_season.png`

## Scope/limitations

Only the filter behavior, sample qualifiers, visible receiving headers, and glossary definitions were checked. No full passing-table transcription, W1–8 aggregation, receiving routes/alignment data, or per-defender charting was produced. Treat below-qualifier players as unlisted/insufficient sample, never as zero.
