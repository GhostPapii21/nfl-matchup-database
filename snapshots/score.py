"""Score a locked snapshot after the game is FINAL (NFL-49 calibration evidence; NFL-44 future-only games).

    python3 -m snapshots.score --snapshot snapshots/2026_10_WAS_NYG/<locked_utc>
    python3 -m snapshots.score --all                       # every unscored snapshot whose game is final
    [--final-json f.json]  offline: {"home_score": int, "away_score": int, "source": "...", "quarters": {...}}

Final score source: ESPN public scoreboard (game must report STATUS_FINAL). NOT yet cross-checked against
nflverse games (TODO; Ghost6's grading loop uses nflverse). Writes SCORE.json next to LOCK.json
(never edits locked files; refuses if LOCK hashes no longer match). Metrics: win log-loss / Brier (ex-tie),
margin and total CRPS, PIT of the actual margin/total, per-book spread/total/moneyline Brier for model vs
the book's own no-vig probability. Research only; no stakes; one game is not calibration evidence on its own.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ESPN = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?dates={date}"
ESPN_ALIAS = {"WSH": "WAS", "LAR": "LA"}


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def crps(samples: np.ndarray, y: float) -> float:
    x = np.sort(samples.astype(float))
    n = len(x)
    # E|X-y| - 0.5 E|X-X'| (sorted-sample identity)
    term1 = np.mean(np.abs(x - y))
    i = np.arange(1, n + 1)
    term2 = np.sum((2 * i - n - 1) * x) / (n * n)
    return float(term1 - term2)


def espn_final(game: dict, kickoff_utc: str) -> dict:
    ko = datetime.fromisoformat(kickoff_utc).astimezone(timezone.utc)
    from zoneinfo import ZoneInfo
    date = ko.astimezone(ZoneInfo("America/New_York")).strftime("%Y%m%d")
    url = ESPN.format(date=date)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    d = json.loads(urllib.request.urlopen(req, timeout=20).read())
    for e in d.get("events", []):
        comp = e["competitions"][0]
        teams = {ESPN_ALIAS.get(c["team"]["abbreviation"], c["team"]["abbreviation"]): c for c in comp["competitors"]}
        if game["home"] in teams and game["away"] in teams:
            st = comp["status"]["type"]["name"]
            if st != "STATUS_FINAL":
                raise SystemExit(f"score: game not final yet ({st}); nothing scored")
            h, a = teams[game["home"]], teams[game["away"]]
            q = {f"q{i+1}": [int(h["linescores"][i]["value"]), int(a["linescores"][i]["value"])]
                 for i in range(min(len(h.get("linescores", [])), len(a.get("linescores", []))))}
            return {"home_score": int(h["score"]), "away_score": int(a["score"]), "source": url, "espn_event": e["id"],
                    "status": st, "quarters": q, "retrieved_utc": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    raise SystemExit("score: game not found on ESPN scoreboard")


def score(snap: Path, final: dict, game: dict) -> dict:
    lk = json.loads((snap / "LOCK.json").read_text())
    for rel, h in lk["files"].items():
        if _sha(snap / rel) != h:
            raise SystemExit(f"score: REFUSED, locked file changed: {rel}")
    A = np.load(snap / "sim_arrays.npz")
    s = json.loads((snap / "summary.json").read_text())
    hs, as_ = final["home_score"], final["away_score"]
    m_act, t_act = hs - as_, hs + as_
    margin = A["fg_home"].astype(float) - A["fg_away"].astype(float)
    total = A["fg_home"].astype(float) + A["fg_away"].astype(float)
    p_home = s["p_home_win"] / max(1e-9, 1 - s["p_tie"])
    y_home = None if hs == as_ else float(hs > as_)
    eps = 1e-6
    out = {"schema": "snapshot-score/1", "game_id": lk["game_id"], "locked_utc": lk["locked_utc"],
           "scored_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "final": final,
           "model": {"p_home_win_ex_tie": p_home, "mean_margin": float(margin.mean()), "mean_total": float(total.mean())},
           "metrics": {
               "win_logloss": None if y_home is None else float(-(y_home * np.log(max(eps, p_home)) + (1 - y_home) * np.log(max(eps, 1 - p_home)))),
               "win_brier": None if y_home is None else float((p_home - y_home) ** 2),
               "margin_crps": crps(margin, m_act), "total_crps": crps(total, t_act),
               "margin_pit": float((margin < m_act).mean() + 0.5 * (margin == m_act).mean()),
               "total_pit": float((total < t_act).mean() + 0.5 * (total == t_act).mean()),
               "margin_abs_err": float(abs(margin.mean() - m_act)), "total_abs_err": float(abs(total.mean() - t_act))},
           "vs_market": []}
    home_name = game.get("home_name") or game["home"]
    for x in s.get("vs_market", []):
        mk, rec = x["market"], dict(x)
        if mk == "total":
            over = x["side"].lower().startswith("over")
            if t_act == x["line"]:
                rec["result"] = "PUSH"
            else:
                y = float((t_act > x["line"]) == over)
                rec.update(result=y, brier_model=(x["p_model"] - y) ** 2,
                           brier_book=None if x["p_book_novig"] is None else (x["p_book_novig"] - y) ** 2)
        elif mk == "spread":
            team_is_home = x["side"] == home_name
            adj = (m_act + x["line"]) if team_is_home else (-m_act + x["line"])
            if adj == 0:
                rec["result"] = "PUSH"
            else:
                y = float(adj > 0)
                rec.update(result=y, brier_model=(x["p_model_cover"] - y) ** 2,
                           brier_book=None if x["p_book_novig"] is None else (x["p_book_novig"] - y) ** 2)
        elif mk == "moneyline":
            if hs == as_:
                rec["result"] = "TIE"
            else:
                y = float((hs > as_) == (x["side"] == home_name))
                rec.update(result=y, brier_model=(x["p_model_win_ex_tie"] - y) ** 2,
                           brier_book=None if x["p_book_novig"] is None else (x["p_book_novig"] - y) ** 2)
        out["vs_market"].append(rec)
    b = [r for r in out["vs_market"] if isinstance(r.get("result"), float) and not r["reference_only"]]
    out["metrics"]["brier_model_mean_lines"] = float(np.mean([r["brier_model"] for r in b])) if b else None
    out["metrics"]["brier_book_mean_lines"] = float(np.mean([r["brier_book"] for r in b if r["brier_book"] is not None])) if b else None
    out["note"] = "One game. Aggregate across future games under the NFL-44 protocol before any calibration claim."
    (snap / "SCORE.json").write_text(json.dumps(out, indent=1, default=float) + "\n")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot", type=Path)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--final-json", type=Path)
    a = ap.parse_args(argv)
    snaps = [a.snapshot] if a.snapshot else sorted(p.parent for p in (ROOT / "snapshots").glob("*/*/LOCK.json") if not (p.parent / "SCORE.json").exists())
    rc = 0
    for snap in snaps:
        snap = snap if snap.is_absolute() else ROOT / snap
        lk = json.loads((snap / "LOCK.json").read_text())
        cfgs = list((snap / "inputs").glob("*.json"))
        game = None
        for c in cfgs:
            d = json.loads(c.read_text())
            if "config_id" in d:
                game = d["game"]
        try:
            final = json.loads(a.final_json.read_text()) if a.final_json else espn_final(game, lk["kickoff_utc"])
        except SystemExit as e:
            print(f"{snap.relative_to(ROOT)}: {e}"); rc = 3; continue
        r = score(snap, final, game)
        print(f"{snap.relative_to(ROOT)}: scored {final['away_score']}-{final['home_score']} (away-home) "
              f"win_brier={r['metrics']['win_brier']} margin_crps={r['metrics']['margin_crps']:.2f} total_crps={r['metrics']['total_crps']:.2f}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
