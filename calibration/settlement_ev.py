"""NFL-75: one settlement and EV module (outside-AI review memo items B1, B5, B6; refs NFL-75).

Every probability here is split three ways: P(under), P(push), P(over), summing to 1. A leg's side turns that into
P(win), P(push), P(loss), and the only EV is the push-refund form at the ACTUAL decimal price:

    EV = P(win) * (dec - 1) - P(loss)          with P(loss) = 1 - P(win) - P(push)

so the real break-even win probability at that price is (1 - P(push)) / dec (1/dec on a half line). The no-vig price
is a market diagnostic only and is never the bar a label has to clear.

Lines:
  * half line (x.5): P(push) = 0.
  * integer line, two-way Over/Under: equality is a push (stake refunded).
  * "X+" milestone (an alt Over written as an integer, e.g. 40+): equality WINS; there is no push.
Engines that return only P(x >= k) cannot price an integer two-way line (the push mass is unknown); `split_from_ge`
refuses rather than putting the push in the Over.

Pure functions on numpy arrays / scalars; no model weights, no gates of their own. Research only; projection_ready
stays false."""
from __future__ import annotations

import numpy as np

LINE_TOL = 1e-9
SIDES = ("Under", "Over")


def american_to_decimal(a):
    a = np.asarray(a, float)
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(a > 0, 1 + a / 100, 1 + 100 / -a)


def is_integer_line(line):
    line = np.asarray(line, float)
    return np.isfinite(line) & (np.abs(line - np.round(line)) < LINE_TOL)


def split_from_samples(x, line, milestone: bool = False) -> tuple:
    """(p_under, p_push, p_over) from simulated values. milestone=True: an "X+" rung, so x == line counts as over."""
    x = np.asarray(x, float)
    line = float(line)
    if x.size == 0:
        raise ValueError("no samples")
    eq = np.abs(x - line) < LINE_TOL
    over = (x > line) & ~eq
    under = (x < line) & ~eq
    if milestone:
        return float(under.mean()), 0.0, float((over | eq).mean())
    return float(under.mean()), float(eq.mean()), float(over.mean())


def split_from_ge(p_ge, line, p_eq=None, milestone: bool = False):
    """(p_under, p_push, p_over) from an engine's P(x >= line).
    half line: P(push)=0, P(over)=P(x>=line). milestone: P(over)=P(x>=line), no push.
    integer two-way line: needs P(x == line) (p_eq); without it every output is NaN (never push-in-the-Over)."""
    p_ge = np.asarray(p_ge, float)
    line = np.asarray(line, float)
    integer = is_integer_line(line) & (not milestone)
    eq = np.zeros_like(p_ge) if p_eq is None else np.asarray(p_eq, float)
    if p_eq is None:
        eq = np.where(integer, np.nan, 0.0)
    eq = np.where(integer, eq, 0.0)
    p_over = p_ge - eq
    p_under = 1.0 - p_ge
    return p_under, eq, p_over


def side_probs(side, p_under, p_push, p_over):
    """(p_win, p_push, p_loss) for side 'Under' / 'Over'."""
    side = np.asarray(side, dtype=object)
    under = side == "Under"
    p_under, p_push, p_over = (np.asarray(v, float) for v in (p_under, p_push, p_over))
    p_win = np.where(under, p_under, p_over)
    p_loss = np.where(under, p_over, p_under)
    ok = np.isin(side, SIDES)
    nan = np.full(np.broadcast(p_win, ok).shape, np.nan)
    return np.where(ok, p_win, nan), np.where(ok, p_push, nan), np.where(ok, p_loss, nan)


def win_from_decisive(p_decisive, p_push):
    """Unconditional P(win) from a push-excluded P(win | no push)."""
    return np.asarray(p_decisive, float) * (1.0 - np.asarray(p_push, float))


def ev_at_price(p_win, p_push, dec):
    """EV per unit stake at decimal price dec: P(win)(dec-1) - P(loss), pushes refunded. NaN if dec <= 1."""
    p_win, p_push, dec = (np.asarray(v, float) for v in (p_win, p_push, dec))
    ev = p_win * (dec - 1.0) - (1.0 - p_win - p_push)
    return np.where(dec > 1, ev, np.nan)


def break_even(dec, p_push=0.0):
    """Smallest P(win) with EV >= 0 at decimal price dec: (1 - P(push)) / dec."""
    dec, p_push = np.asarray(dec, float), np.asarray(p_push, float)
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(dec > 1, (1.0 - p_push) / dec, np.nan)


def settle_outcome(actual, line, side, milestone=False):
    """(win, push) per leg: win 1.0/0.0, NaN on push or unknown actual; push 0/1.
    Two-way integer line: actual == line pushes. milestone ("X+" Over): actual >= line wins, no push."""
    a = np.asarray(actual, float)
    ln = np.asarray(line, float)
    side = np.asarray(side, dtype=object)
    ms = np.broadcast_to(np.asarray(milestone, bool), a.shape)
    eq = np.abs(a - ln) < LINE_TOL
    over_win = np.where(ms, (a > ln) | eq, (a > ln) & ~eq)
    under_win = (a < ln) & ~eq
    win = np.where(side == "Under", under_win, over_win).astype(float)
    push = eq & ~ms & np.isfinite(a)
    win = np.where(push | ~np.isfinite(a), np.nan, win)
    return win, push.astype(int)


# ---------------------------------------------------------------- label gate (B1)
EV_REASON = "ev_not_positive_at_price"
PUSH_MISSING_REASON = "push_prob_missing_integer_line"
EV_EPS = 1e-12   # EV within float noise of 0 (exactly at break-even) is not positive


def leg_ev(df):
    """Per-leg (p_win, p_push, be_true, ev) from columns p_model (P(side)), dec, line and optional p_push /
    p_model_basis ('decisive' = P(side | no push)). A half line has p_push 0; an integer line without p_push is NaN."""
    import pandas as pd
    n = len(df)
    col = lambda c, v: (df[c].astype(float).to_numpy() if c in df else np.full(n, v, float))
    p_model, dec, line = col("p_model", np.nan), col("dec", np.nan), col("line", np.nan)
    pp = col("p_push", np.nan)
    p_push = np.where(np.isfinite(pp), pp, np.where(is_integer_line(line), np.nan, 0.0))
    basis = df["p_model_basis"].astype(str).to_numpy() if "p_model_basis" in df else np.full(n, "", object)
    p_win = np.where(basis == "decisive", win_from_decisive(p_model, p_push), p_model)
    return pd.DataFrame(dict(p_win=p_win, p_push_used=p_push, be_true=break_even(dec, p_push),
                             ev=ev_at_price(p_win, p_push, dec)), index=df.index)


def apply_ev_gate(df, candidate_labels, no_edge_label):
    """No leg keeps a candidate label unless its EV at the actual price is > 0 (strict, > EV_EPS). Demoted legs get
    label=no_edge_label and reason EV_REASON (or PUSH_MISSING_REASON when an integer line has no push probability);
    the classifier's own label/reason are kept in label_pre_ev / reason_pre_ev. Adds ev, be_true, edge_vs_be
    (p_win - be_true) and p_push_used. Non-candidate labels are untouched."""
    out = df.copy()
    e = leg_ev(out)
    for c in e:
        out[c] = e[c]
    out["edge_vs_be"] = out.p_win - out.be_true
    out["label_pre_ev"], out["reason_pre_ev"] = out["label"], out["reason"]
    cand = out.label.isin(candidate_labels)
    push_missing = cand & ~np.isfinite(out.p_push_used.to_numpy(float))
    bad = cand & ~(out.ev.to_numpy(float) > EV_EPS)
    out.loc[bad, "label"] = no_edge_label
    out.loc[bad, "reason"] = EV_REASON
    out.loc[push_missing, "reason"] = PUSH_MISSING_REASON
    out["ev_gate"] = np.where(~cand, "", np.where(bad, "demoted", "pass"))
    return out
