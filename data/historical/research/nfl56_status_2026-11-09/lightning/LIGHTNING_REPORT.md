# Lightning vs current model + opportunity breakdowns (research only)
Compiled 2026-11-09 ~15:30–16:00 ET from read-only GitHub reads (cursor-github; public raw for nfl-matchup-database). No writes anywhere. projection_ready=false unchanged.

## 1. What "Lightning" is
- **It is not in `nfl-matchup-database`.** That repo mentions Lightning only to *exclude* it. For example, the branch sim script says "NOT the production sportsbook-odds-bridge main model or actual trained Lightning network." No Linear issue mentions Lightning, and code search returned 0 results (GitHub search was incomplete, so I checked file contents directly).
- **Where it lives:**
  - Private repo `GhostPapii21/sportsbook-odds-bridge`, branch `experiment/nfl-lightning-opportunity-v1` @ cdec0a7.
  - Draft PR **#32**, open and unmerged, created 4:06 AM ET and updated 6:43 AM ET today: https://github.com/GhostPapii21/sportsbook-odds-bridge/pull/32
- **What it is:** PyTorch **Lightning 2.6.6**, a CPU-only *opportunity-count* model (`experiments/nfl_opportunity_lightning.py`).
  - Network: small feed-forward net, 5 inputs → 24 hidden (ReLU) → Softplus output.
  - Training: Poisson negative log-likelihood, Adam optimizer, seed 17, normalization fit on training rows only.
  - It predicts **receiver targets** (WR/TE/RB pooled) and **player rush attempts** (all rushers, including QBs). It does not predict yards, receptions or probabilities.
- **Inputs (5):**
  - The player's prior 3-game and 5-game opportunity averages.
  - The player's last game count.
  - The team's 3-game average pass or rush attempts.
  - The opponent's 3-game average opportunities allowed.
- **Data:**
  - Pinned nflverse 2024 and 2025 (W1–18) plus the frozen 2026 W1–8 package.
  - All 41 overtime games excluded, leaving 12,922 rows.
  - Features are rebuilt from earlier weeks. They are *not* timestamped vendor snapshots.
- **"Lightning bridge" to yards:** Lightning opportunities × the player's pre-Week 9 historical yards per opportunity (or catch rate). The efficiency term is not learned. The repo itself flags `not_a_real_lightning_yardage_model=true`.
- **Workflows on the branch:**
  - `nfl-lightning-research.yml` (research Actions runs 42594523084, 42599045065).
  - `nfl-week9-lightning-shadow.yml`.
  - `nfl-week9-matched-props.yml`.
- **No Lightning output exists for BUF@MIN.** The Week 9 shadow covers only the 13 Sunday games.

## 2. Accuracy comparison (lower MAE/RMSE/Brier = better)
"Main" in the Lightning files = the frozen Week 9 boards from our current research model: season_empirical for Madrid/1 PM, mean overlay for late/SNF. sim_v6 Monte Carlo/Bias/Game Randomness was never run, so there's no comparison against it.

| Comparison | Window / split | n | Lightning | Comparator | Notes |
|---|---|---:|---:|---:|---|
| Targets count MAE (pilot, 2026-only) | Train W4–6, val W7, test W8 | 189 | 1.832 | rolling-5 **1.462** | Lightning 25% worse |
| Rush-attempt MAE (pilot) | same | 127 | 3.589 | rolling-5 **2.406** | 49% worse |
| Targets MAE (2024–26 expanded) | Test W8 (not blind: W8 seen in pilot) | 189 | 1.477 (RMSE **1.925**) | rolling-5 **1.462** (RMSE 1.950) | MAE 1% worse, RMSE better |
| Rush-attempt MAE (expanded) | same | 127 | **2.381** (RMSE **3.986**) | 2.406 (4.164) | about 1% better |
| **W9 shadow targets MAE** | Train ≤ W7, val W8, **test W9 Sunday** | 164 | **1.599** (RMSE **2.222**) | rolling-5 1.670 (2.264); training mean 2.289 | Best evidence; still postgame-selected cohort |
| **W9 shadow rush-attempt MAE** | same | 79 | **2.616** (RMSE **3.961**) | rolling-5 2.756 (4.127); training mean 5.066 | |
| W9 matched props, side hit rate (all) | Sunday 13 games, DK+FD lines | 248 | 131/248 = **52.8%** | Main 134/248 = **54.0%** | Lightning slightly worse. They agreed on 185 rows (101 hits). On the 63 disagreements: Lightning 30, Main 33 |
| — receiving yds, 1 PM/Madrid | | 88 | 46.6%, MAE 21.19 | **51.1%**, MAE **20.40** | |
| — receptions, 1 PM/Madrid | | 84 | 53.6%, MAE 1.594 | 53.6%, MAE **1.579** | |
| — rushing yds, 1 PM/Madrid | | 36 | **50.0%**, MAE 16.92 | 47.2%, MAE **16.43** | |
| — receiving yds, late/SNF | | 25 | **68.0%**, 25.74 | 64.0%, **25.68** | small n |
| — receptions, late/SNF | | 6 | 83.3% | **100%** | n=6 |
| — rushing yds, late/SNF | | 9 | 55.6% | 55.6% | n=9 |
| Hybrid yards vs lines (separate file) | Sunday, DK lines | 144 | 73/144 = 50.7%, MAE 22.02 | Main 74/144 = **51.4%**, MAE **21.34**; rolling bridge 66/144 = 45.8%, MAE 22.43 | |
| Context: current model, prospective Sunday scorecard (main repo) | Madrid + 1 PM, DK | 212 | — | season_empirical 104/212 = 49.1%, **Brier 0.289** (worse than a 0.250 coin flip); rolling5 47.2% / 0.319; opp-shrunk 44.3% / 0.325 | `research/WEEK9_SUNDAY_CALIBRATION_REVIEW_20261108.md`. 60–80% confidence calls hit only about 40% |

**What doesn't exist:**
- **Brier, log loss and ROI for Lightning:** none. It produces no probabilities. The files state "not a calibrated over/under probability, betting edge or money-return measure."
- **Confidence intervals and rolling-origin folds:** none. Every comparison is a single split.

**Leakage / validity risks:**
1. **Week 8 test isn't blind.** It was reviewed during the pilot before the expanded model was configured.
2. **The Week 9 "matched props" comparison was built after the games** (`RESEARCH_ONLY_RETROSPECTIVE_NOT_BLIND`). The bridge design (3-game minimum, efficiency definition, exclusions) could have been chosen after seeing outcomes. Main's calls were frozen pregame. Lightning's were not timestamped pregame.
3. **Survivorship.** The cohort is limited to players who appear in postgame stat records ("not a full pregame active-player population"). That excluded 18 identity mismatches, 47 players with insufficient priors and 8 non-gamebook rows (shadow), plus 20 with no Lightning opportunity, 2 inactive and 3 pushes (props).
4. **Pooled labels.** Targets mix WR/TE/RB, and rush attempts mix QBs, scrambles and kneels.
5. **Feature timestamps are reconstructed**, not archived vendor snapshots.
6. **Main vs Lightning use different methods by window** (season empirical vs mean overlay), and the lines come from frozen DK/FD boards.

**Bottom line:**
- Lightning is roughly even with a rolling 5-game average on opportunity counts. It's slightly better on Week 9 Sunday (targets MAE 1.60 vs 1.67; rushes 2.62 vs 2.76).
- Converted to yardage/receptions props, it was **slightly worse than our current main model** on hit rate (52.8% vs 54.0%) and MAE.
- None of these differences is statistically meaningful at these sample sizes.
- The repo's own decision is "keep shadow-only; do not promote."

## 3. Opportunity breakdowns found
| Where | Players / scope | Formula actually used | Measured inputs | Assumed inputs | Backtested? |
|---|---|---|---|---|---|
| Branch `research/wentz-2025-third-down-drive-audit` → `research/third_down/mnf_week9_route_opportunity_scenarios_20261109.json` (+ `MNF_HOCKENSON_ROUTE_INJURY_OPPORTUNITY_BOARD_20261109.md`) | **MNF:** Hockenson (full route chain), Jefferson, Addison, Wentz attempts | dropbacks × route participation × targets/route × catch rate × yds/rec | Hockenson routes 102, team dropbacks 151, routes/dropback 0.6755, TPRR 0.2255 (RotoWire/PlayerProfiler vendor charting, W1–3 and W7–8; W4 and W5 excluded). Wentz–Hockenson: 37 targets / 208 attempts (0.178/att), catch rate 78.4%, 8.72 yds/rec | Dropbacks per scenario (28/36/46). Hockenson participation 0.55–0.70. Jefferson share 27–31% ("SUBJECTIVE"). Jefferson/Addison 12.5 yds/catch (stress assumption). Sacks are a pressure proxy. No defender assignment | **No** |
| Same branch → `BUF_MIN_W9_THREE_SCENARIO_PROP_RESEARCH_20261109.json` → 900k MC (`mnf_20261109_joint_monte_carlo.py`, seed 20261109, 100k × 3 scripts × 3 methods) | **MNF:** Wentz, Jefferson, Hockenson, Addison, A. Jones, Mason; Allen, Cook, Shakir, Moore, Coleman, Kincaid | Scenario team volume (Wentz 24/30/38 attempts; Allen 27/31/25; Cook 23/20/25 carries) × shares × efficiency | Wentz-era target history (2 appearances); gamebook team totals | **BUF receiver shares "set as scenarios, not fitted."** Scenario weights are null. The injury method uses non-fitted haircuts | **No**. Status `COMPLETED_RESEARCH_ONLY_NO_VALIDATED_PROBABILITIES` |
| `main` → `research/WEEK9_MNF_*_OFFENSE_VS_*_DEFENSE_20261109.md` | MNF team and target hierarchy (Jefferson 40 targets in 6 games, Hockenson 37 in 7, Addison 33 in 6; Cook 138 carries for 707; Shakir 38 targets; Kincaid 35 targets) | Descriptive. No product chain | Gamebook-verified box scores; MIN dropback proxy 51.8% | Pressure/blitz from TruMedia via the Bills site; zone/MOF from Sharp snapshot | No |
| `sportsbook-odds-bridge` Lightning W9 shadow + matched props | **Sunday**, 13 games: 164 target rows, 79 rush rows, 248 prop rows | Lightning opportunities × historical yds/opportunity | W1–8 nflverse counts | Efficiency = historical average | **Yes, retrospectively** (see section 2) |
| `main` → `research/WEEK9_PLAYER_USAGE.csv`, `WEEK9_TE_USAGE_TARGET_ROUTE.csv`, `PLAYER_USAGE_OPPORTUNITY_TABLE.md`, `WEEK1_8_PLAYER_USAGE_FULL.csv` | Sunday: about 10 TEs/WRs (McBride, Likely, …), Burden/Golden/Swift | Snap %, routes, TPRR, target share | Public aggregators / SumerSports / RotoWire (dated Nov 7) | — | No. The file says "INSUFFICIENT for full opportunity models" |
| `main` current model, Sunday frozen boards | Sunday Madrid/1 PM props | targets/g × Jeffreys catch rate × yds/rec; carries/g × YPC (no route or play-count layer) | W1–8 locked inputs | — | **Yes, prospectively**: 49.1% DK, Brier 0.289 |

No file contains the full chain (plays × pass rate × route participation × targets/route × catch rate × YPR) for **every** BUF/MIN skill player. Only Hockenson has a measured route layer. No rushing chain (plays × run rate × carry share × YPC) with measured shares exists for Cook, Jones or Mason; it's scenario carries only.

## 4. BUF@MIN key opportunity numbers vs lines (research, unvetted)
- Lines are the branch's BetSharp-relayed snapshot (10:01 ET). The FD line is shown unless noted.
- "Sim over %" = range across the 9 cells of the 900k run.
- These are conditional on unweighted scripts. **They are not probabilities.**
- Passing yards stay off slips (Rico rule).

| Player | Market | Line | Scenario means (A / B / C or low / base / trail) | 900k sim over % range |
|---|---|---:|---|---|
| T.J. Hockenson | receptions | 4.5 | 3.27 / 4.39 / 5.69 (targets 4.2 / 5.6 / 7.3; routes 18 / 25 / 32) | 16.6–61.6 |
| T.J. Hockenson | rec yds | 38.5 (DK 41.5 at 04:08) | 28.5 / 38.3 / 49.6 | 19.8–59.3 |
| Justin Jefferson | receptions | 6.5 | 4.5 / 6.1 / 8.2 (targets 6.5 / 8.7 / 11.8) | 18.3–66.5 |
| Justin Jefferson | rec yds | 77.5 | 56.7 / 76.1 / 103.1 | 23.9–64.2 |
| Jordan Addison | receptions | 3.5 | 2.9 / 3.7 / 4.6 | 31.9–63.0 |
| Jordan Addison | rec yds | 39.5 | 36.7 / 45.9 / 58.1 | 36.1–61.1 |
| Carson Wentz | pass attempts (DK) | 30.5 | 24 / 30 / 38 | 9.1–89.4 |
| James Cook | rush attempts (DK) | 18.5 | 23 / 20 / 25 carries (assumed) | 65.8–96.6 |
| James Cook | rush yds | 86.5 | — | 37.4–84.1 |
| Khalil Shakir | receptions | 3.5 | — | 44.3–57.8 |
| Josh Allen | rush yds | 30.5 | — | 34.4–53.1 |
| Aaron Jones | rush yds | 31.5 | — | 5.8–41.2 |
| Jordan Mason | rush yds | 47.5 | — | 13.5–56.4 |

Full table: `mnf_900k_player_prop_ranges.csv`.

## 5. Conflicts with README (`main` @101d4cc)
1. **100k workflows.** The README says "100k trials and the 15-phase ledger: Deferred … not implemented here." But main holds 471 × 100,000-draw Sunday simulations (`research/week9_1pm_live/WEEK9_1PM_100K_SIMULATIONS.csv`, `research/week9_930/simulation_100k_20261108_0908ET.csv`, validated by `research/validate_week9_readiness.py`). The research branch ran 900k MNF draws via Actions. These are ungated research simulations, not the NFL-56 fail-closed entrypoint, and the README doesn't describe them.
2. **"Nothing in this repository runs on a loop."** `.github/workflows/cin-atl-live-tracker.yml` is a cron workflow with contents:write that used `ODDS_API_KEY`. The research branch has four push-triggered workflows that commit outputs.
3. **The README doesn't mention Lightning or the odds-bridge comparison at all**, even though that is where the model-vs-model accuracy evidence lives.
4. **The repo's 15-phase taxonomy** (ledger: slate → final-inactives freeze) differs from the skill's 15 phases. The README should name which is canonical.
