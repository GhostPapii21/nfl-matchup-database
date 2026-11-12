# Week 8 breakdown — sources (built 2026-10-29, data Wks 1-7)
REAL (computed by build.py, no LLM):
- nflverse play_by_play_2026 (fresh pull, thru Wk7): RB carries, run_location/run_gap direction splits, YPC by direction offense & defense, RB rush TD/yds allowed, RB/WR/TE targets & yds allowed, RZ (inside 20/10) usage, drive RZ TD%, 3rd/4th down rates & conversions, points allowed, seesaw game-by-game yards/target share.
- nflverse ftn_charting_2026 (thru Wk7): blitz (n_blitzers>0), 3rd-down blitz %, box count, 5+ rushers; QB blitzed vs not (comp%, YPA, sacks, INT, EPA); target tree when blitzed by air-yard band.
- nflverse PFR advstats_week_def_2026: per-defender targets/rec/yds/TD allowed (CB/S), pressures & sacks for top rushers.
- fixes.sqlite fix_participation: TE snap % (receiving vs blocking TE by targets per snap). player_types.json (fixes-based) for receiver types/target shares.
- Sharp Football Oct 20 (via defense_profiles.json): man/zone, YPT allowed by position/alignment, blitz, light/heavy box, pass-rush win rate.
- ESPN injuries (week8/injuries.json, pulled 05:07 ET Oct 29).
GAPS:
- CB alignment / shadow assignments (which CB lines up on which WR): not public; "likely matchup" = most-targeted DBs, INFERRED.
- Per-defender run-defense (weak DT/edge YPC): not public; team direction/gap split used as the proxy.
- Pressure splits (QB under pressure, not blitz): FTN has no pressure flag; only blitz splits + sack/PFR pressure counts.
- Personnel 11/12/13 rates: 2026 participation not published (404).
- HC/OC/DC notes: not re-pulled; see team_baselines.
- Prop lines: none pulled. 10G script labels pending.
- QB changes (e.g., PHI Hurts out -> McKee): QB splits shown are the season's main passer.
Grok API: not used for this build (all numeric, script-computed); cost $0.
