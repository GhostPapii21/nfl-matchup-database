# Receiver volatility research (Nov 14, 2026)

Questions: can explosive receiving games be predicted pregame; do teammate pairs seesaw; do quarterback changes reshuffle
targets; does a defense that allows a lot to a position send more targets there; how predictable is each team's target tree;
and why the Rams are big favorites at Arizona. Research only.

Run in order (data comes from the nflverse files in `pregame/.cache/`):

    python3 research/receiver_volatility_2026-11-14/build_table.py   # rows.parquet: 13,526 receiver-games 2022-2026, pre-game info only
    python3 research/receiver_volatility_2026-11-14/explosive.py     # explosive_results.json
    python3 research/receiver_volatility_2026-11-14/studies.py       # studies_results.json
    python3 research/receiver_volatility_2026-11-14/deepdives.py     # deepdives.json
    python3 research/receiver_volatility_2026-11-14/extra.py         # extra.json (needs dashboard/data for this week's simulation)
    python3 research/receiver_volatility_2026-11-14/report.py        # report.html

Headline results: volume, efficiency and the implied team total predict 100-yard games (top tenth: 22.6% predicted, 21.6%
happened); a recent run of big plays does not; top-two receivers move slightly together (+0.06), not opposite; full-season
shares beat new-QB-only shares; defense targets allowed to a position do not move the offense's targets to it (receivers, tight
ends), only slightly for backs; first-meeting results do not carry into rematches (+0.035). See report.html.
