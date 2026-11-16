"""Matchup adjustments for the opportunity check: coverage fit, pressure fit, opponent tier.

RESULT (dashboard/backtest_coverage.py, results in dashboard/results/coverage_backtest.md): fitted on 5,561
player-games from 2023-2024 and tested on 2,757 player-games from 2025 that the fit never saw, NONE of the three
adjustments improved the projection beyond what dashboard/opportunity.py already does. So every function here returns
a multiplier of 1.0 (no change) with the reason in `why`. Each function still computes the adjustment exactly as it
was derived and tested and returns it under `raw_*` keys, so the board can show the matchup context ("this defense
plays 41% man; his split points to +1.8%; not applied because it did not prove its value"). Research only.

Current model on the 2025 holdout: average Brier 0.11163 over receiving yards 40+/60+/70+/80+ and receptions 4+/6+
(0.1615, 0.1084, 0.0850, 0.0676, 0.1595, 0.0878); mean absolute yardage error 20.01.

    adjustment (2025 holdout)                         avg Brier change (90% range)        yardage error change
    coverage, man/zone, as derived (m=40)             +0.00002 (-0.00011 to +0.00016)     +0.010
    coverage, man/zone, as fitted                     -0.00003 (-0.00017 to +0.00011)     +0.009
    coverage, middle open/closed, as derived (m=40)   -0.00000 (-0.00011 to +0.00011)     +0.006
    coverage, middle open/closed, as fitted           -0.00002 (-0.00016 to +0.00012)     -0.000
    pressure, as derived (m=100)                      -0.00011 (-0.00024 to +0.00003)     +0.000
    pressure, as fitted                               -0.00003 (-0.00009 to +0.00002)     +0.000
    tier split, raw, replacing the defense factor     +0.00309 (+0.00207 to +0.00409)     +0.842   (clearly worse)
    his own tier split on top of the current model    +0.00001 (-0.00002 to +0.00004)     -0.003
    defense factor weight 0.125 instead of 0.5        -0.00031 (-0.00063 to +0.00000)     -0.026

Decision rule (fixed before looking at 2025): use an adjustment only if its fitted strength is positive with t >= 2 on
2023-2024 AND the 2025 average Brier improves with a 90% range below zero AND the yardage error is not worse. Nothing
met it. The largest "improvement" is 0.3% of the Brier score and inside the range of luck.

To switch one on later (only after a new backtest supports it), set the matching USE_* flag to True; the function then
returns raw multiplier ** strength.
"""
from __future__ import annotations

import math

# ----------------------------------------------------------------------------------------------- verdicts and fitted constants
USE_COVERAGE = False      # holdout: -0.00003 / -0.00002 average Brier, ranges include zero
USE_PRESSURE = False      # fit-season strength negative (wrong direction); holdout range includes zero
USE_TIER = False          # raw tier split is clearly worse; shrunk version adds nothing

# Fitted on 2023-2024 (strength beta in: actual - expected = beta * expected * log(multiplier)). Kept for the record.
COVERAGE_PRIOR_TARGETS = 40          # m: league-average targets blended into each side of his split (as tested)
MU_PRIOR_TARGETS = 40                # league-average targets blended into his overall yards per target (the prior's level)
COVERAGE_SHARE_PRIOR_FACTOR = 8      # the target-share split uses m x 8 team targets
COVERAGE_FIT = {
    "man_zone": {"yards_per_target": {"m": 0, "beta": 0.637, "t": 1.42, "beta_2025": 0.126, "t_2025": 0.20},
                 "targets": {"m": 80, "beta": 1.17, "t": 2.14, "beta_2025": 0.744, "t_2025": 0.92}},
    "mof": {"yards_per_target": {"m": None, "beta": 0.0, "note": "strength negative at every prior weight"},
            "targets": {"m": 20, "beta": 1.71, "t": 2.51, "beta_2025": 0.539, "t_2025": 0.53}},
}
PRESSURE_PRIOR_DROPBACKS = 100       # m: league-average dropbacks blended into his pressured and his clean results
PRESSURE_RATE_PRIOR_DROPBACKS = 100  # league-average dropbacks blended into his own pressure rate
PRESSURE_FIT = {"yards_per_attempt": {"m": 40, "beta": -1.633, "t": -0.88, "beta_2025": 1.309, "t_2025": 0.51},
                "completion": {"m": 40, "beta": -1.348, "t": -1.26, "beta_2025": 3.533, "t_2025": 2.14},
                "attempts": {"m": 0, "beta": 0.125, "t": 0.10, "beta_2025": 3.229, "t_2025": 1.93}}
TIER_PRIOR_GAMES = 8                 # m used for the displayed raw multiplier; the fit found no m with value
TIER_FIT = {"replacing_defense_factor": {"m": "inf", "beta": 0.081, "t": 0.71},
            "own_split_on_top": {"m": 0, "beta": 0.018, "t": 0.35}}
# The weight on opportunity.def_factor that minimised squared yardage error on 2023-2024 (current value is 0.5).
# 2025: -0.00031 average Brier (range -0.00063 to +0.00000); 2026 weeks 5-10: -0.00018 (range -0.00068 to +0.00034).
# Not distinguishable from luck, so opportunity.DEF_WEIGHT is left alone. Reported for the owner's judgement.
DEF_WEIGHT_FITTED = 0.125
STRENGTH = {"coverage_ypt": 0.0, "coverage_targets": 0.0, "pressure": 0.0, "tier": 0.0}   # exponents applied when USE_* is True

# League reference numbers (2024 season plus 2025 weeks, NGS participation; pass a fresher dict when one is available).
# ypt = league yards per target in that look / league yards per target overall, for the position.
# share = the position's share of targets in that look / its share overall. ypt_all = league yards per target, overall.
LEAGUE_SPLIT = {
    "WR": {"ypt_all": 7.93, "man": {"ypt": 0.931, "share": 1.103}, "zone": {"ypt": 1.060, "share": 0.925},
           "mofo": {"ypt": 0.982, "share": 0.923}, "mofc": {"ypt": 1.011, "share": 1.054}},
    "TE": {"ypt_all": 7.29, "man": {"ypt": 0.921, "share": 0.935}, "zone": {"ypt": 1.051, "share": 1.047},
           "mofo": {"ypt": 1.007, "share": 1.036}, "mofc": {"ypt": 0.994, "share": 0.975}},
    "RB": {"ypt_all": 5.90, "man": {"ypt": 1.065, "share": 0.731}, "zone": {"ypt": 0.971, "share": 1.196},
           "mofo": {"ypt": 0.963, "share": 1.216}, "mofc": {"ypt": 1.037, "share": 0.849}},
}
# The NGS labels are not consistent from season to season (league man rate 41% in 2023, 48% in 2024, 32% in 2025), so an
# opponent's rate must always be compared with the league rate from the SAME season. These are the 2025 values.
LEAGUE_MAN_RATE = 0.324
LEAGUE_MOFO_RATE = 0.445
LEAGUE_PRESSURE_RATE = 0.294
LEAGUE_PRESSURED = {"sack_rate": 0.230, "comp_pct": 0.481, "ypa": 5.78}
LEAGUE_CLEAN = {"sack_rate": 0.0, "comp_pct": 0.707, "ypa": 7.515}     # NGS counts every sack as a pressure


def _num(x, default=0.0):
    try:
        x = float(x)
    except (TypeError, ValueError):
        return default
    return default if (math.isnan(x) or math.isinf(x)) else x


def _clip(x, lo, hi):
    return max(lo, min(hi, x))


def _mix(p, a, b):
    return p * a + (1 - p) * b


def _side(d):
    d = d or {}
    return _num(d.get("targets")), _num(d.get("yards")), _num(d.get("team_targets"))


def _pair(player_split, league_split, a, b, opp_rate, league_rate, m):
    """One two-way split (a = man or mofo, b = zone or mofc). Returns (ypt multiplier, target multiplier, targets a, targets b)."""
    tg_a, yd_a, tt_a = _side(player_split.get(a))
    tg_b, yd_b, tt_b = _side(player_split.get(b))
    la, lb = league_split.get(a) or {}, league_split.get(b) or {}
    r_a, r_b = _num(la.get("ypt"), 1.0), _num(lb.get("ypt"), 1.0)
    s_a, s_b = _num(la.get("share"), 1.0), _num(lb.get("share"), 1.0)
    if opp_rate is None or league_rate is None:
        return 1.0, 1.0, tg_a, tg_b
    po, pl = _clip(_num(opp_rate), 0.0, 1.0), _clip(_num(league_rate), 0.0, 1.0)
    # his own level: only the ratio between the two looks matters, so the level cancels when he has no data
    lg_ypt = _num(league_split.get("ypt_all"), 0.0)
    if lg_ypt > 0:        # as in the backtest: 40 league-average targets blended into his overall rate
        mu = (yd_a + yd_b + MU_PRIOR_TARGETS * lg_ypt) / (tg_a + tg_b + MU_PRIOR_TARGETS)
    else:
        mu = (yd_a + yd_b) / (tg_a + tg_b) if (tg_a + tg_b) > 0 else 1.0
    mu = mu if mu > 0 else 1.0
    e_a = (yd_a + m * mu * r_a) / (tg_a + m)
    e_b = (yd_b + m * mu * r_b) / (tg_b + m)
    den = _mix(pl, e_a, e_b)
    ypt = _mix(po, e_a, e_b) / den if den > 0 else 1.0
    sh = (tg_a + tg_b) / (tt_a + tt_b) if (tt_a + tt_b) > 0 else 1.0
    ms = m * COVERAGE_SHARE_PRIOR_FACTOR
    h_a = (tg_a + ms * sh * s_a) / (tt_a + ms)
    h_b = (tg_b + ms * sh * s_b) / (tt_b + ms)
    den = _mix(pl, h_a, h_b)
    tgm = _mix(po, h_a, h_b) / den if den > 0 else 1.0
    return _clip(ypt, 0.5, 2.0), _clip(tgm, 0.5, 2.0), tg_a, tg_b


def coverage_multiplier(player_split, league_split, opp_man_rate, opp_mofo_rate, n_targets=None, *,
                        league_man_rate=LEAGUE_MAN_RATE, league_mofo_rate=LEAGUE_MOFO_RATE, prior_targets=COVERAGE_PRIOR_TARGETS):
    """Coverage fit: his own man/zone and middle-open/closed production against how often this opponent plays each.

    Arguments
      player_split   {"man": {"targets", "yards", "team_targets"}, "zone": {...}, "mofo": {...}, "mofc": {...}} from the
                     previous season plus earlier weeks. team_targets = his team's targets in that look in the games he
                     played (only needed for the target multiplier). mofo = Cover 2, 4, 6, 2-Man; mofc = Cover 0, 1, 3.
      league_split   "WR" / "TE" / "RB" to use LEAGUE_SPLIT, or a dict {"ypt_all": x, "man": {"ypt", "share"}, ...} of
                     league ratios for his position (rate in that look / rate overall; ypt_all optional).
      opp_man_rate, opp_mofo_rate   share of the opponent's pass plays in man / with the middle open, this season.
                     Pass None to skip one split.
      n_targets      his total prior targets (reported only; the shrinkage uses the per-look counts).
      league_man_rate, league_mofo_rate   league rates from the SAME season as the opponent rates.

    Equation (for looks a, b; m = prior_targets = 40; mu = his overall yards per target with 40 league targets blended in):
      ypt_a      = (yards_a + m * mu * league_ypt_a) / (targets_a + m)                  same for b
      share_a    = (targets_a + 8m * his_share * league_share_a) / (team_targets_a + 8m)  same for b
      raw_ypt    = [opp*ypt_a + (1-opp)*ypt_b] / [league*ypt_a + (1-league)*ypt_b]
      raw_target = [opp*share_a + (1-opp)*share_b] / [league*share_a + (1-league)*share_b]
    The man/zone and open/closed results are multiplied together.

    Fit (2023-2024, 5,561 player-games): yards per target, man/zone: best prior weight m=0 with strength 0.64 (t 1.4),
    and the strength turns negative from m=80 up; middle open/closed: strength negative at every m. Targets: strength
    1.17 (t 2.1, m=80) for man/zone and 1.71 (t 2.5, m=20) for open/closed, driven by running backs, who draw more
    targets against zone.
    Holdout (2025, 2,757 player-games): average Brier -0.00003 (man/zone) and -0.00002 (open/closed) on 0.11163, ranges
    -0.00017..+0.00011 and -0.00016..+0.00012; yardage error +0.009 and -0.000 on 20.01. Not distinguishable from zero.

    Returns {"ypt_mult": 1.0, "target_mult": 1.0, "raw_ypt_mult", "raw_target_mult", "applied": False, "why"}.
    """
    lg = LEAGUE_SPLIT.get(str(league_split).upper(), LEAGUE_SPLIT["WR"]) if not isinstance(league_split, dict) else league_split
    ps = player_split or {}
    m = max(float(prior_targets), 1e-6)
    y1, t1, n_man, n_zone = _pair(ps, lg, "man", "zone", opp_man_rate, league_man_rate, m)
    y2, t2, n_open, n_closed = _pair(ps, lg, "mofo", "mofc", opp_mofo_rate, league_mofo_rate, m)
    raw_y, raw_t = _clip(y1 * y2, 0.5, 2.0), _clip(t1 * t2, 0.5, 2.0)
    out = {"ypt_mult": 1.0, "target_mult": 1.0, "raw_ypt_mult": round(raw_y, 4), "raw_target_mult": round(raw_t, 4),
           "raw_parts": {"man_zone": {"ypt": round(y1, 4), "targets": round(t1, 4)}, "mof": {"ypt": round(y2, 4), "targets": round(t2, 4)}},
           "sample": {"n_targets": n_targets, "vs_man": n_man, "vs_zone": n_zone, "mof_open": n_open, "mof_closed": n_closed},
           "applied": USE_COVERAGE}
    if USE_COVERAGE:
        out["ypt_mult"] = round(raw_y ** STRENGTH["coverage_ypt"], 4)
        out["target_mult"] = round(raw_t ** STRENGTH["coverage_targets"], 4)
        out["why"] = "Coverage fit applied at the fitted strength."
    else:
        out["why"] = ("Not applied. On the 2025 holdout the coverage fit changed the average Brier score by -0.00003 (man/zone) and "
                      "-0.00002 (middle open/closed) on a base of 0.11163, both inside the range of luck, and did not lower the yardage "
                      f"error. Shown for context only: his split against this defense points to {100 * (raw_y - 1):+.1f}% yards per target "
                      f"and {100 * (raw_t - 1):+.1f}% targets.")
    return out


def _qb(d, league):
    d = d or {}
    n = _num(d.get("dropbacks"))
    sacks = _num(d.get("sacks"))
    att = _num(d.get("attempts"), n - sacks)
    return n, sacks, att, _num(d.get("completions")), _num(d.get("yards")), league


def pressure_multiplier(qb_pressured, qb_clean, opp_pressure_rate, league_pressure_rate=LEAGUE_PRESSURE_RATE, *,
                        league_pressured=None, league_clean=None, prior_dropbacks=PRESSURE_PRIOR_DROPBACKS):
    """Pressure fit: the opponent's pressure rate against the quarterback's own pressured vs clean results.

    Arguments
      qb_pressured, qb_clean   {"dropbacks", "sacks", "attempts", "completions", "yards"} for the starting quarterback,
                               previous season plus earlier weeks (attempts exclude sacks; yards are passing yards).
      opp_pressure_rate        share of the opponent's pass plays with pressure, this season.
      league_pressure_rate     league rate, same season.
      league_pressured, league_clean   {"sack_rate", "comp_pct", "ypa"}; defaults LEAGUE_PRESSURED / LEAGUE_CLEAN.

    Equation (m = prior_dropbacks = 100):
      P0 = (his pressured dropbacks + 100 * league rate) / (his dropbacks + 100)        his usual pressure rate
      P  = P0 * opp_pressure_rate / league_pressure_rate                                expected this game (5%..70%)
      each of his pressured and clean sack rate, completion rate and yards per attempt = (own + m * league) / (n + m)
      a(p) = p(1 - sack_p) / [p(1 - sack_p) + (1 - p)(1 - sack_c)]                       share of throws under pressure
      raw_ypt    = ypa(a(P)) / ypa(a(P0))        raw_catch = comp(a(P)) / comp(a(P0))
      raw_target = [1 - sack(P)] / [1 - sack(P0)]                                       attempts lost to sacks

    Fit (2023-2024): strength NEGATIVE for yards per attempt (-1.6, t -0.9) and completions (-1.3, t -1.3), near zero
    for attempts (0.1, t 0.1). In 2025 the same regressions came out positive (completions 3.5, t 2.1): the sign is not
    stable from year to year. At team level the pre-game expected pressure rate does predict the pressure rate
    (correlation +0.27 / +0.20) and the sack rate (+0.20 / +0.18) in the game, but barely yards per attempt
    (-0.03 / -0.08) in 2023-2024 / 2025.
    Holdout (2025): as derived -0.00011 average Brier (range -0.00024..+0.00003), yardage error +0.000; as fitted
    -0.00003 (range -0.00009..+0.00002). Not distinguishable from zero.

    Returns {"ypt_mult": 1.0, "catch_mult": 1.0, "target_mult": 1.0, "raw_ypt_mult", "raw_catch_mult",
             "raw_target_mult", "expected_pressure_rate", "usual_pressure_rate", "applied": False, "why"}.
    """
    Lp, Lc = league_pressured or LEAGUE_PRESSURED, league_clean or LEAGUE_CLEAN
    n_p, sk_p, att_p, cmp_p, yd_p, _ = _qb(qb_pressured, Lp)
    n_c, sk_c, att_c, cmp_c, yd_c, _ = _qb(qb_clean, Lc)
    lg = _clip(_num(league_pressure_rate, LEAGUE_PRESSURE_RATE), 0.01, 0.99)
    opp = lg if opp_pressure_rate is None else _clip(_num(opp_pressure_rate, lg), 0.0, 1.0)
    k = PRESSURE_RATE_PRIOR_DROPBACKS
    P0 = (n_p + k * lg) / (n_p + n_c + k)
    P = _clip(P0 * opp / lg, 0.05, 0.70)
    m = max(float(prior_dropbacks), 1e-6)
    s_p, s_c = (sk_p + m * Lp["sack_rate"]) / (n_p + m), (sk_c + m * Lc["sack_rate"]) / (n_c + m)
    c_p, c_c = (cmp_p + m * Lp["comp_pct"]) / (att_p + m), (cmp_c + m * Lc["comp_pct"]) / (att_c + m)
    y_p, y_c = (yd_p + m * Lp["ypa"]) / (att_p + m), (yd_c + m * Lc["ypa"]) / (att_c + m)

    def at(p):
        a = p * (1 - s_p) / (p * (1 - s_p) + (1 - p) * (1 - s_c))
        return _mix(a, y_p, y_c), _mix(a, c_p, c_c), 1 - _mix(p, s_p, s_c)
    (y1, c1, a1), (y0, c0, a0) = at(P), at(P0)
    raw_y, raw_c, raw_t = _clip(y1 / y0, 0.7, 1.3), _clip(c1 / c0, 0.7, 1.3), _clip(a1 / a0, 0.8, 1.2)
    out = {"ypt_mult": 1.0, "catch_mult": 1.0, "target_mult": 1.0, "raw_ypt_mult": round(raw_y, 4), "raw_catch_mult": round(raw_c, 4),
           "raw_target_mult": round(raw_t, 4), "expected_pressure_rate": round(P, 4), "usual_pressure_rate": round(P0, 4),
           "applied": USE_PRESSURE}
    if USE_PRESSURE:
        e = STRENGTH["pressure"]
        out.update({"ypt_mult": round(raw_y ** e, 4), "catch_mult": round(raw_c ** e, 4), "target_mult": round(raw_t ** e, 4),
                    "why": "Pressure fit applied at the fitted strength."})
    else:
        out["why"] = ("Not applied. On 2023-2024 the pressure fit pointed the wrong way for yards and completions; on the 2025 holdout it "
                      "changed the average Brier score by -0.00011 as derived (range -0.00024 to +0.00003) on a base of 0.11163. A "
                      "high-pressure defense does bring more pressure and sacks, but that did not carry through to receiver yards. "
                      f"Shown for context only: expected pressure rate {100 * P:.1f}% against his usual {100 * P0:.1f}%, which points to "
                      f"{100 * (raw_y - 1):+.1f}% yards per target.")
    return out


def tier_split(avg_vs_tier, games_vs_tier, avg_overall, league_tier_ratio=1.0, *, prior_games=TIER_PRIOR_GAMES):
    """Opponent tier: his yards per game against defenses in this opponent's tier vs his overall yards per game.

    Tier = top 10 / middle / bottom 10 by yards per game allowed to his position (previous-season games use that
    season's final ranks, this season's games use ranks to date).

    Arguments
      avg_vs_tier        his receiving yards per game against the opponent's tier (previous season + earlier weeks)
      games_vs_tier      number of those games
      avg_overall        his receiving yards per game over the same window
      league_tier_ratio  league yards per game against that tier / overall for his position (2025: top 10 about 0.89 WR / 0.81 TE / 0.80 RB,
                         middle about 1.00, bottom 10 about 1.09 WR / 1.22 TE / 1.18 RB); 1.0 if unknown

    Equation (m = prior_games):
      raw_yards = [(avg_vs_tier * games + m * avg_overall * league_tier_ratio) / (games + m)] / avg_overall

    Fit (2023-2024): the raw split (m=0) in place of the defense factor has strength 0.02 (t 0.5): 98% of it is noise
    (typical player: 6 prior games against the tier). Its best form is m=infinity, the league effect alone, at
    strength 0.08 (t 0.7). His own split on top of the current model: strength 0.02 (t 0.35).
    Holdout (2025): raw tier split replacing the defense factor +0.00309 average Brier (range +0.00207..+0.00409) and
    +0.84 yards of error: clearly worse. His own split on top: +0.00001 (range -0.00002..+0.00004). The same on 2026
    weeks 5-10 (+0.00404 for the raw split).
    Against the current half-weighted defense factor: the tier average is far less predictive. The fitted weight for
    the defense factor itself is DEF_WEIGHT_FITTED = 0.125, not 0.5, but the gain over 0.5 (-0.00031 average Brier,
    range -0.00063..+0.00000) is within luck, so the current weight is left alone.

    Returns {"yards_mult": 1.0, "raw_yards_mult", "games_vs_tier", "applied": False, "why"}.
    """
    g, avg_t, avg = max(_num(games_vs_tier), 0.0), _num(avg_vs_tier), _num(avg_overall)
    L = _num(league_tier_ratio, 1.0) or 1.0
    m = max(float(prior_games), 1e-6)
    raw = ((avg_t * g + m * avg * L) / (g + m)) / avg if avg > 0 else L
    raw = _clip(raw, 0.5, 2.0)
    out = {"yards_mult": 1.0, "raw_yards_mult": round(raw, 4), "games_vs_tier": g, "applied": USE_TIER}
    if USE_TIER:
        out.update({"yards_mult": round(raw ** STRENGTH["tier"], 4), "why": "Tier split applied at the fitted strength."})
    else:
        out["why"] = ("Not applied. A player's average against top-10 or bottom-10 defenses rests on a handful of games and did not predict "
                      "his next game: used in place of the defense factor it made the 2025 holdout clearly worse (+0.00309 average Brier, "
                      "+0.84 yards of error), and on top of the current model it changed nothing (+0.00001). "
                      f"Shown for context only: {avg_t:.1f} yards a game in {g:.0f} games against this tier vs {avg:.1f} overall.")
    return out
