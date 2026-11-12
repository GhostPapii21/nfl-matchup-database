# Nov 1 vetting notes (Blitz, 07:33–07:45 ET)

## A. Primary-star unders cut (Ghost6 rule) — primary = team target leader (WR/TE), carries leader (RB), starting QB, from nflverse pbp 2026 wk1-8
Penix pass U229.5 (ATL QB), London rec yds U79.5 (ATL tgt leader 57), Irving rush U70.5 (TB RB1 120 car), Henry rush U78.5 (BAL RB1 148), Watson pass U210.5 (CLE QB), Concepcion rec yds U46.5 (CLE tgt leader 45 vs Boston 43), G. Wilson rec yds U63.5 + rec U5.5 (NYJ tgt leader 52), Ollie Gordon rush U64.5 (MIA carries leader 72).
NOTE: Ghost6 VETTED Concepcion and O. Gordon, but by the pbp leaders they are primary stars, so they stay CUT pending Ghost6's ruling. Addison (MIN #3 by targets), J. Williams (DET #3), Dotson, Boston (CLE #2), O. Cooper are not primary.
Passes 19 -> 10 after A; -> 6 after Ghost6 rejections/bias re-score.

## Bias findings (199 legs; model median vs FD line)
| market | n | MC | Bias | GR | MC below line | MC minus Pinnacle pt |
|---|---|---|---|---|---|---|
| passyds | 23 | -4.3 (-2.4%) | -39.1 (-17.7%) | -5.4 (-2.8%) | 52% | -5.8 |
| rec | 64 | -0.20 (-5.3%) | -0.66 (-16.9%) | -0.39 (-10.7%) | 61% | -0.21 |
| recyds | 64 | -1.4 (-3.5%) | -8.7 (-20.5%) | -3.5 (-9.3%) | 56% | -1.0 |
| rushrec | 22 | -2.5 (-0.8%) | -13.4 (-14.6%) | -3.8 (-2.2%) | 50% | n/a |
| rushyds | 26 | +1.5 (+10.1%) | -6.1 (-4.9%) | +0.6 (+9.2%) | 42% | +1.9 |
All: MC -1.9%, Bias -16.3%, GR -5.8%. Avg-p edge: unders +13.3, overs +6.4; MC-only +9.8 vs +10.9.
Conclusion: the systematic low bias is the bias model's flat haircut (BUGLOG BUG-2026-11-01-BIAS). Secondary: GR is mildly low on receptions/rec yds (-10%/-9%); MC receptions skew under (61% below line, integer medians). Rush yds models run high (+10%).

## C. TE/RB receiving legs — all stay CUT
The PFR advanced-defense cache gives each defender's season totals (targets, completions, yards, rating allowed as nearest defender). It does not say which receiver each defender covered. So it can't name "the LB or S who covers that player most". Picking the opponent's most-targeted LB/S would be a team-level stand-in, which Ghost6's rule (3) forbids. No alignment/matchup source (FTN per-route matchups, PFF premium) is available. Cuts stay: Pitts, Otton, LaPorta, Kincaid, Gesicki, Hockenson, McBride, Goedert, Dulcich, Raridon, Andrews, Ferguson, Okonkwo, plus every RB rush+rec leg.
