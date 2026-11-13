"""NFL-75 volume fixes for the simv56 engines (outside-AI review memo B2, B3, B8, B9; refs NFL-75). OPT-IN ONLY.

The engines call these only when the leg carries volume_fix=True (calibration.simv56_pmodel.run_all(volume_fix=True)).
Without that key the engines run byte-for-byte the Phase 4 code path, so the 88-leg W8-9 reproduction, the countable
`run` CLI and every #46 provenance digest are unchanged.

  B2 active_games  keep games the player PLAYED with 0 carries and 0 targets (a QB who dropped back but never ran).
                   Played = any carry, target, or dropback (pass attempt or sack as the passer) in that game. Team games
                   with no trace of the player (inactive, injured) stay out, as before.
  B3 script_tv     the "gr" team-volume draw normalised to a FIXED neutral-script reference: the player's history mean
                   is matched at his own games' average margin (mbar), and the expected margin -spread then moves the
                   mean by exp(b * (-spread - mbar)). Before, the spread term was divided back out by TV.mean(), so the
                   spread never changed expected carries or targets.
  B8 scale_count   carry boosts above 2x are no longer capped at 2x (C*(1+floor(m-1)) + Binomial(C, frac(m-1))).
  B9 ypc_ratio     the regress-to-league YPC ratio (w*pm + (1-w)*lg) / pm is skipped when the player's mean YPC pm is
                   <= 0 (it was undefined at 0 and flipped sign below 0); the opponent factor still applies.
No weights, no fitted constants. Research only; projection_ready stays false."""
import numpy as np


def active_games(d, pbp, gsis):
    """Rows of the per-game table d (one row per team game) where the player recorded a carry, a target or a dropback."""
    db = pbp[(pbp.passer_player_id == gsis) & ((pbp.pass_attempt == 1) | (pbp.sack == 1))]
    dropback_games = set(db.game_id)
    keep = ((d.tgt + d.car) > 0) | d.game_id.isin(dropback_games)
    return d[keep]


def mean_margin(tg, team, game_ids):
    """Average final margin of the team in the player's own history games (the script his volume was observed in)."""
    m = tg[(tg.posteam == team) & tg.game_id.isin(set(game_ids))].margin
    return float(m.mean()) if len(m) else 0.0


def script_tv(tm_mean, pace, b, Mg, spread, mean, m_s, mbar):
    """Team volume draws: neutral-script normalisation, then the expected-margin shift exp(b * (-spread - mbar))."""
    tv = tm_mean * pace * np.exp(b * (Mg - (-spread)))          # script noise around the expected margin only
    tv = tv * (mean / (m_s * tv.mean()))                         # history mean matched at the history script ...
    return tv * np.exp(b * ((-spread) - mbar))                   # ... then moved to this game's expected margin


def scale_count(rng, C, m):
    """Thin (m < 1) or boost (m >= 1) a count array to mean C * m with no 2x cap."""
    if m < 1:
        return rng.binomial(C, m)
    k = int(np.floor(m - 1.0))
    return C * (1 + k) + rng.binomial(C, (m - 1.0) - k)


def ypc_ratio_ok(pm):
    """True when the player's mean YPC supports the multiplicative regress-to-league ratio."""
    return bool(np.isfinite(pm) and pm > 0)
