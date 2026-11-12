"""Pregame guard for The Odds API pulls (SOURCE_AUDIT 2026-11-01, BUG odds-inplay).
The Odds API event-odds endpoint keeps returning markets after kickoff (in-play). pull_odds.py had no
commence_time check, so the 18:51 ET pull (odds_i1850.csv) mixed live lines for LAC@LAR and KC@DEN with pregame lines."""
import datetime as dt
def _t(s): return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
def pregame_events(events, now_utc=None):
    now_utc = now_utc or dt.datetime.now(dt.timezone.utc)
    return [e for e in events if _t(e["commence_time"]) > now_utc]
def flag_inplay(rows, commence_by_game):
    """True = quote updated at/after kickoff (live), False = pregame, None = kickoff unknown (never assume pregame)."""
    out = []
    for r in rows:
        c = commence_by_game.get(r["game"])
        out.append(None if not c or not r.get("last_update_utc") else _t(r["last_update_utc"]) >= _t(c))
    return out
