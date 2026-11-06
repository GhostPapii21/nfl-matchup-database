"""Demo report: raw model p vs screenshot market quotes. PINNACLE_MISSING (no credits pull). Research only."""
from __future__ import annotations
import json
from pathlib import Path
import pandas as pd
from reconstruct import load_pbp, period_table_from_pbp, as_of_mask
from monte_carlo import raw_probs_mc_and_gr, simulate_game
from market import build_mirror, novig_two_way, novig_three_way

ROOT = Path(__file__).resolve().parent
ART = ROOT / "artifacts"

def main():
    p26 = period_table_from_pbp(load_pbp(ROOT/"data/play_by_play_2026.parquet"))
    p25 = period_table_from_pbp(load_pbp(ROOT/"data/play_by_play_2025.parquet"))
    hist = pd.concat([p25, p26], ignore_index=True)
    # TNF is week 9 on ESPN but folder labeled week10; kickoff Thu Nov 5 2026 — as-of: all through week 8
    asof = hist[as_of_mask(hist, 2026, 9)]  # strictly before week 9
    home, away = "BAL", "JAX"  # BAL home
    # Note: simulate uses home/away labels as teams; markets from JAX perspective often

    sim = simulate_game(asof, home, away, n=50000, seed=20261105, apply_gr=False)
    report = {
        "game": "JAX@BAL",
        "asof": "2026 weeks < 9 (+ 2025 REG)",
        "asof_games": int(len(asof)),
        "home": home, "away": away,
        "sim_status": sim.get("status"),
        "summaries": sim.get("summaries"),
        "outcome_meta": sim.get("outcome_meta"),
        "source_composition": (sim.get("status") or {}).get("source_composition"),
        "markets": [],
        "disclaimer": "Research only. PINNACLE_MISSING (no odds history pull). Screenshot quotes are FanDuel UI evidence, not Pin. NO edge/PASS claim. Bias UNIMPLEMENTED.",
    }

    # Screenshot quotes from audit correction + new TT quotes
    # JAX 1Q -2.5 -124 / BAL +2.5 +102 — spread from JAX side: away -2.5
    markets = [
        dict(name="JAX Q1 -2.5", period="q1", market="spread_2way", line=-2.5, side="away",
             fd_two=(-124, 102), note="screenshot 12:51; side=JAX"),
        dict(name="JAX H1 -6.5", period="h1", market="spread_2way", line=-6.5, side="away",
             fd_two=(-105, -115), note="screenshot main 1H"),
        dict(name="JAX H1 -2.5", period="h1", market="spread_2way", line=-2.5, side="away",
             fd_two=(-235, 180), note="screenshot alt; API had NO_QUOTE"),
        dict(name="JAX H1 3-way", period="h1", market="winner_3way", line=None, side="away",
             fd_three=(-280, 310, 950), note="JAX/BAL/Tie order for novig indices"),
        dict(name="BAL TT U13.5", period="fg", market="team_total_2way", line=13.5, side="home_under",
             fd_two=(-108, -118), note="U/O screenshot"),
        dict(name="BAL TT U14.5", period="fg", market="team_total_2way", line=14.5, side="home_under",
             fd_two=(-132, 104), note="U-132 / O+104 screenshot"),
        dict(name="JAX TT O24.5", period="fg", market="team_total_2way", line=24.5, side="away_over",
             fd_two=(-115, -111), note="O-115 / U-111"),
    ]

    for m in markets:
        raw = raw_probs_mc_and_gr(
            asof, home, away, n=30000, seed=20261105,
            period=m["period"], market=m["market"],
            line=m["line"] if m["line"] is not None else 0.0,
            side=m["side"],
        )
        if "fd_three" in m:
            # order JAX, BAL, Tie -> indices 0,1,2; side away=JAX index 0
            j, b, t = m["fd_three"]
            # novig_three_way(a,b,tie) — we pass JAX, BAL, Tie
            # but build_mirror pinnacle_three_way uses side_index; here FD not Pin
            raw_block = {
                "monte_carlo": raw["monte_carlo"],
                "monte_carlo_decisive": raw.get("p_win_decisive"),
                "p_win": raw.get("p_win"), "p_push": raw.get("p_push"), "p_lose": raw.get("p_lose"),
                "p_win_decisive": raw.get("p_win_decisive"),
                "bias": raw["bias"], "game_randomness": raw["game_randomness"],
            }
            mirror = build_mirror(
                raw_block,
                pinnacle_three_way=None,
                consensus_two_ways=None,
                proposed_blend_weight=0.25,
                comparison_basis="decisive_two_way",
            )
            ja, ba, ta = novig_three_way(j, b, t)
            fd_novig = {"JAX": ja, "BAL": ba, "Tie": ta, "source": "fanduel_screenshot_not_pinnacle"}
            mirror.flags.append("PINNACLE_MISSING")
            mirror.flags.append("SCREENSHOT_FD_ONLY")
            keep3 = ("monte_carlo","bias","game_randomness","mc_error","gr_error","p_side","p_opp","p_tie","tie_mc","tie_gr")
            entry = {"market": m["name"], "raw": {k: raw[k] for k in keep3 if k in raw}, "mirror": mirror.to_dict(), "fd_novig_3way": fd_novig, "note": m["note"]}
        else:
            # two-way: first price is primary side
            a, b = m["fd_two"]
            raw_block = {
                "monte_carlo": raw["monte_carlo"],
                "monte_carlo_decisive": raw.get("p_win_decisive"),
                "p_win": raw.get("p_win"), "p_push": raw.get("p_push"), "p_lose": raw.get("p_lose"),
                "p_win_decisive": raw.get("p_win_decisive"),
                "bias": raw["bias"], "game_randomness": raw["game_randomness"],
            }
            mirror = build_mirror(
                raw_block,
                pinnacle_two_way=None,
                consensus_two_ways=[("fanduel_screenshot", a, b)],
                consensus_side_index=0,
                consensus_pulled_et="2026-11-05 12:50 screenshot",
                proposed_blend_weight=0.25,
                comparison_basis="decisive_two_way",
            )
            pa, pb = novig_two_way(a, b)
            keep = ("monte_carlo","bias","game_randomness","mc_error","gr_error",
                    "p_win","p_push","p_lose","p_win_decisive","p_win_decisive_gr",
                    "comparison_basis_recommended","settlement_note","gr_detail")
            entry = {
                "market": m["name"],
                "raw": {k: raw[k] for k in keep if k in raw},
                "mirror": mirror.to_dict(),
                "fd_novig_primary": pa, "fd_novig_other": pb,
                "comparison_note": "two-way: use p_win_decisive vs FD/Pin no-vig; monte_carlo is unconditional",
                "note": m["note"] + "; consensus uses FD screenshot only — NOT Pinnacle",
            }
        report["markets"].append(entry)

    (ART/"demo_jaxbal_period_report.json").write_text(json.dumps(report, indent=2, default=str)+"\n")
    print("wrote", ART/"demo_jaxbal_period_report.json")
    for e in report["markets"]:
        print(e["market"], "raw_mc", e["raw"].get("monte_carlo"), "decisive", e["raw"].get("p_win_decisive"), "push", e["raw"].get("p_push"), "basis", e["mirror"].get("comparison_basis"), "flags", e["mirror"]["flags"][:3])

if __name__ == "__main__":
    main()
