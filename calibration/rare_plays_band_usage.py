"""NFL-75 diagnostic: how often rare-play outcome rows come from the exact line of scrimmage vs a wider band.
    python3 -m calibration.rare_plays_band_usage
Research only (research_unaccepted=("rare_plays",), n=2,000 per game); nothing fitted."""
import json
from calibration.common import PBP, engine_path, make_cfg

GAMES = (("NYG", "WAS", 10), ("KC", "BUF", 9), ("DEN", "LV", 7))


def main() -> int:
    engine_path()
    import simulate
    tot, note = {}, None
    for home, away, wk in GAMES:
        cfg = make_cfg(home, away, wk, h2h="off")
        cfg["semantics"]["rare_plays"] = "asof_league_v1"
        o = simulate.simulate_games(cfg, pbp_path=str(PBP), n=2000, seed=777, research_unaccepted=("rare_plays",))
        for k, v in o["rare_band_usage"].items():
            tot[k] = tot.get(k, 0) + v
        note = o["rare_band_note"]
    print(json.dumps({"counts": dict(sorted(tot.items())), "note": note}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
