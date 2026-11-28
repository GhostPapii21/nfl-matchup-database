"""The three branches are a disjoint, exhaustive partition, and C is not A seen from the other sideline.

Classification uses only end-of-Q3 and regulation margins, which the engine already records. No new simulation.
"""
from __future__ import annotations

import glob
from pathlib import Path

import numpy as np
import pytest

from game_script_contract.allocation import classify_trial, classify_trials, errors, validate_payload
from game_script_contract.partition import favorite_margins, partition_score_arrays
from game_script_contract.schema import BRANCH_IDS, DEFAULT_BRANCH_DEFINITION
from game_script_contract.tests._synthetic import payload

ROOT = Path(__file__).resolve().parents[2]
SNAPS = sorted(glob.glob(str(ROOT / "snapshots/*/*/sim_arrays.npz")))
DEF = DEFAULT_BRANCH_DEFINITION


@pytest.mark.parametrize("m_q3,m_reg,expected", [
    (12, 12, "favorite_controls"),
    (9, 9, "favorite_controls"),          # hold boundary: still more than one score
    (9, 8, "underdog_chases"),             # cut to within one score
    (9, 0, "underdog_chases"),             # tied in regulation
    (9, -3, "underdog_chases"),            # underdog takes the lead in Q4
    (14, 8, "underdog_chases"),
    (8, 20, "competitive"),                # never led by 9+ at the Q3 gun
    (0, 0, "competitive"),
    (-9, -14, "competitive"),              # underdog ahead and pulling away: B, not C
    (-12, 0, "competitive"),               # underdog ahead at Q3, favorite comes back: still B
    (-20, -20, "competitive"),
])
def test_classify_trial_truth_table(m_q3, m_reg, expected):
    assert classify_trial(m_q3, m_reg, DEF) == expected


def test_classify_trials_is_disjoint_and_exhaustive():
    m_q3 = np.array([12, 9, 9, 8, -9, 0, 20, 9])
    m_reg = np.array([12, 9, 8, 20, -14, 0, 4, -1])
    labels = classify_trials(m_q3, m_reg, DEF)
    assert list(labels) == [
        "favorite_controls", "favorite_controls", "underdog_chases", "competitive",
        "competitive", "competitive", "underdog_chases", "underdog_chases",
    ]
    assert len(labels) == len(m_q3)
    assert set(labels) <= set(BRANCH_IDS)


def test_underdog_ahead_is_competitive_not_a_chase():
    """The rejected reading ('C = underdog leads') would label these C. The adopted reading labels them B."""
    assert classify_trial(-12, -18, DEF) == "competitive"
    assert classify_trial(-9, -9, DEF) == "competitive"


def test_synthetic_labels_are_disjoint_exhaustive_and_match_the_definition():
    p, t, labels = payload()
    assert len(labels) == len(t["m_q3"]) == p["provenance"]["n_trials_total"]
    assert set(np.unique(labels)) == set(BRANCH_IDS)
    assert (classify_trials(t["m_q3"], t["m_reg"], DEF) == labels).all()
    n = {b: int((labels == b).sum()) for b in BRANCH_IDS}
    assert sum(n.values()) == len(labels)
    assert n["favorite_controls"] == p["branches"]["favorite_controls"]["n_trials"]
    # Every A trial held the lead; every C trial cut it; no B trial had a 9+ Q3 lead.
    assert (t["m_q3"][labels == "favorite_controls"] >= 9).all()
    assert (t["m_reg"][labels == "favorite_controls"] >= 9).all()
    assert (t["m_q3"][labels == "underdog_chases"] >= 9).all()
    assert (t["m_reg"][labels == "underdog_chases"] <= 8).all()
    assert (t["m_q3"][labels == "competitive"] < 9).all()
    ahead = p["competitive_composition"]["underdog_ahead_end_q3_by_control_margin"]
    assert ahead["n_trials"] == int(((labels == "competitive") & (t["m_q3"] <= -9)).sum())
    assert validate_payload(p) == []


def test_branch_c_is_not_branch_a_relabeled_from_the_other_sideline_synthetic():
    """If C were 'underdog leads' (A from the other sideline), flipping favorite/underdog would send A to C."""
    _, t, labels = payload()
    flipped = classify_trials(-t["m_q3"], -t["m_reg"], DEF)
    a, c = labels == "favorite_controls", labels == "underdog_chases"
    assert a.sum() and c.sum()
    assert not np.any(a & (flipped == "underdog_chases"))
    assert np.all(flipped[a] == "competitive")
    assert not np.any(c & (flipped == "underdog_chases"))
    assert np.all(flipped[c] == "competitive")
    # The rejected single-margin rule (final m >= 9 vs m <= -9) DOES map A onto C after a flip.
    rejected_a = t["m_reg"] >= 9
    rejected_flip_c = (-t["m_reg"]) <= -9
    assert np.any(rejected_a & rejected_flip_c), "guard: the rejected rule would have identified A with C"


def test_committed_snapshots_are_disjoint_and_exhaustive():
    assert SNAPS, "no committed sim_arrays.npz"
    for path in SNAPS:
        z = {k: np.asarray(v) for k, v in np.load(path).items()}
        n = len(z["fg_home"])
        fav_home = (z["fg_home"].astype(float) - z["fg_away"]).mean() > 0
        m_q3, m_reg = favorite_margins(z, favorite_is_home=fav_home)
        labels = classify_trials(m_q3, m_reg, DEF)
        assert len(labels) == n
        assert set(np.unique(labels)) <= set(BRANCH_IDS)
        counts = {b: int((labels == b).sum()) for b in BRANCH_IDS}
        assert sum(counts.values()) == n
        assert (m_q3[labels == "favorite_controls"] >= 9).all()
        assert (m_reg[labels == "favorite_controls"] >= 9).all()
        assert (m_q3[labels == "underdog_chases"] >= 9).all()
        assert (m_reg[labels == "underdog_chases"] <= 8).all()
        assert (m_q3[labels == "competitive"] < 9).all()
        # Complement: every 9+ Q3 lead is A or C, never B.
        ac = m_q3 >= 9
        assert set(np.unique(labels[ac])) <= {"favorite_controls", "underdog_chases"}


def test_branch_c_is_not_branch_a_relabeled_from_the_other_sideline_committed():
    assert SNAPS
    for path in SNAPS:
        z = {k: np.asarray(v) for k, v in np.load(path).items()}
        fav_home = (z["fg_home"].astype(float) - z["fg_away"]).mean() > 0
        m_q3, m_reg = favorite_margins(z, favorite_is_home=fav_home)
        labels = classify_trials(m_q3, m_reg, DEF)
        flipped = classify_trials(-m_q3, -m_reg, DEF)
        a, c = labels == "favorite_controls", labels == "underdog_chases"
        if a.any():
            assert not np.any(a & (flipped == "underdog_chases")), path
            assert np.all(flipped[a] == "competitive"), path
        if c.any():
            assert not np.any(c & (flipped == "underdog_chases")), path
            assert np.all(flipped[c] == "competitive"), path


def test_partition_payload_from_a_committed_run_is_valid_and_exhaustive():
    path = sorted(glob.glob(str(ROOT / "snapshots/2026_11_CIN_WAS/*/sim_arrays.npz")))[-1]
    z = dict(np.load(path))
    home_fav = (z["fg_home"].astype(float) - z["fg_away"]).mean() > 0
    p = partition_score_arrays(z, game_id="2026_11_CIN_WAS", home="WAS", away="CIN",
                               favorite="WAS" if home_fav else "CIN", favorite_source="engine_mean_margin",
                               source_engine="core/possession_engine_v0 (committed snapshot)",
                               source_ref=str(Path(path).relative_to(ROOT)))
    assert errors(validate_payload(p)) == []
    n = p["provenance"]["n_trials_total"]
    assert n == 100_000
    assert sum(p["branches"][b]["n_trials"] for b in BRANCH_IDS) == n
    assert p["competitive_composition"]["underdog_ahead_end_q3_by_control_margin"]["n_trials"] + \
        p["competitive_composition"]["other_competitive"]["n_trials"] == p["branches"]["competitive"]["n_trials"]
    # A 9-point Q3 lead that is held is the majority of 9+ Q3 leads in this engine (Q4 barely responds).
    a = p["branches"]["favorite_controls"]["n_trials"]
    c = p["branches"]["underdog_chases"]["n_trials"]
    assert a > c and c > 0
