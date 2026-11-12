"""Phase 15: official game-day inactives, timestamped (NFL-49 / NFL-56 hook `official_inactives`).

    python -m phase15.official_inactives --game 2026_10_WAS_NYG [--kickoff-utc 2026-11-13T01:15:00Z]

Source of record: each club's official site (NFL Clubs platform), the "Inactives" article the club
publishes ~90 minutes before kickoff (e.g. giants.com/news/inactives-..., commanders.com/news/inactives-...).
Fallback: NONE automatic. A wire/aggregator list is not official; if a club article is missing the team stays
MISSING and Phase 15 stays blocked (fail closed).

Writes phase15/inactives/<game_id>/inactives_<UTC>.json with the article URL, its published timestamp,
retrieved_utc, the sha256 of the fetched HTML and the parsed names. The pipeline hook
`phase15.official_inactives:hook` only READS the newest file (no network inside the gate).
A file is OK only when BOTH teams parsed >=1 name from an article published after T-90-minutes-minus-30
(clubs sometimes post a few minutes early) and before kickoff. No API keys, no credits.
"""
from __future__ import annotations

import argparse
import hashlib
import html as _html
import json
import re
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phase15" / "inactives"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
EARLIEST_BEFORE_KICKOFF = timedelta(minutes=120)  # T-90 posting, allow 30 min early

# nflverse code -> (club news index URL, club site root, nickname used in headings)
CLUB_SITES = {
    "ARI": ("https://www.azcardinals.com/news/", "https://www.azcardinals.com", "CARDINALS"),
    "ATL": ("https://www.atlantafalcons.com/news/", "https://www.atlantafalcons.com", "FALCONS"),
    "BAL": ("https://www.baltimoreravens.com/news/", "https://www.baltimoreravens.com", "RAVENS"),
    "BUF": ("https://www.buffalobills.com/news/", "https://www.buffalobills.com", "BILLS"),
    "CAR": ("https://www.panthers.com/news/", "https://www.panthers.com", "PANTHERS"),
    "CHI": ("https://www.chicagobears.com/news/", "https://www.chicagobears.com", "BEARS"),
    "CIN": ("https://www.bengals.com/news/", "https://www.bengals.com", "BENGALS"),
    "CLE": ("https://www.clevelandbrowns.com/news/", "https://www.clevelandbrowns.com", "BROWNS"),
    "DAL": ("https://www.dallascowboys.com/news/", "https://www.dallascowboys.com", "COWBOYS"),
    "DEN": ("https://www.denverbroncos.com/news/", "https://www.denverbroncos.com", "BRONCOS"),
    "DET": ("https://www.detroitlions.com/news/", "https://www.detroitlions.com", "LIONS"),
    "GB": ("https://www.packers.com/news/", "https://www.packers.com", "PACKERS"),
    "HOU": ("https://www.houstontexans.com/news/", "https://www.houstontexans.com", "TEXANS"),
    "IND": ("https://www.colts.com/news/", "https://www.colts.com", "COLTS"),
    "JAX": ("https://www.jaguars.com/news/", "https://www.jaguars.com", "JAGUARS"),
    "KC": ("https://www.chiefs.com/news/", "https://www.chiefs.com", "CHIEFS"),
    "LA": ("https://www.therams.com/news/", "https://www.therams.com", "RAMS"),
    "LAC": ("https://www.chargers.com/news/", "https://www.chargers.com", "CHARGERS"),
    "LV": ("https://www.raiders.com/news/", "https://www.raiders.com", "RAIDERS"),
    "MIA": ("https://www.miamidolphins.com/news/", "https://www.miamidolphins.com", "DOLPHINS"),
    "MIN": ("https://www.vikings.com/news/", "https://www.vikings.com", "VIKINGS"),
    "NE": ("https://www.patriots.com/news/", "https://www.patriots.com", "PATRIOTS"),
    "NO": ("https://www.neworleanssaints.com/news/", "https://www.neworleanssaints.com", "SAINTS"),
    "NYG": ("https://www.giants.com/news/", "https://www.giants.com", "GIANTS"),
    "NYJ": ("https://www.newyorkjets.com/news/", "https://www.newyorkjets.com", "JETS"),
    "PHI": ("https://www.philadelphiaeagles.com/news/", "https://www.philadelphiaeagles.com", "EAGLES"),
    "PIT": ("https://www.steelers.com/news/", "https://www.steelers.com", "STEELERS"),
    "SEA": ("https://www.seahawks.com/news/", "https://www.seahawks.com", "SEAHAWKS"),
    "SF": ("https://www.49ers.com/news/", "https://www.49ers.com", "49ERS"),
    "TB": ("https://www.buccaneers.com/news/", "https://www.buccaneers.com", "BUCCANEERS"),
    "TEN": ("https://www.tennesseetitans.com/news/", "https://www.tennesseetitans.com", "TITANS"),
    "WAS": ("https://www.commanders.com/news/football/football-news-archive", "https://www.commanders.com", "COMMANDERS"),
}
POS = r"(?:QB|RB|FB|WR|TE|OT|OL|OG|G|C|T|DL|DT|DE|NT|EDGE|OLB|ILB|LB|CB|S|SS|FS|DB|K|P|LS|KR|PR)"
ITEM = re.compile(rf"^(?:No\.\s*\d+\s+)?(?P<pos>{POS}(?:/{POS})?)\s+(?P<name>[A-Z][A-Za-z.'\- ]+?(?:\s(?:Jr\.|Sr\.|II|III|IV))?)\s*(?:\((?P<note>[^)]*)\))?$")


def _get(url: str, timeout: int = 20) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def _text(fragment: str) -> str:
    return _html.unescape(re.sub(r"<[^>]+>", "", fragment)).replace("\xa0", " ").strip()


def find_article_links(index_html: str) -> list[str]:
    links = re.findall(r'href="(/news/[^"#?]*inactive[^"#?]*)"', index_html, flags=re.I)
    seen, out = set(), []
    for l in links:
        if l not in seen:
            seen.add(l); out.append(l)
    return out


def published_utc(article_html: str) -> datetime | None:
    for pat in (r'"datePublished"\s*:\s*"([^"]+)"', r'article:published_time"\s+content="([^"]+)"'):
        m = re.search(pat, article_html)
        if m:
            s = m.group(1).replace("Z", "+00:00")
            s = re.sub(r"\.(\d+)\+", lambda x: "." + x.group(1)[:6].ljust(6, "0") + "+", s)
            try:
                return datetime.fromisoformat(s).astimezone(timezone.utc)
            except ValueError:
                continue
    return None


def parse_inactives(article_html: str, nickname: str) -> list[dict]:
    """Players from <li> items. When the article has per-team headings ('GIANTS INACTIVES'), only the section
    under this club's heading is used; otherwise every matching item (club articles list only their own team)."""
    heads = [h for h in re.finditer(r"<(h\d|p|strong)[^>]*>([^<]*INACTIVES[^<]*)</\1>", article_html, flags=re.I)
             if re.fullmatch(r"\s*[\w.' ]+\s+INACTIVES\s*", _text(h.group(2)), flags=re.I)]
    if len(heads) >= 2:
        for i, h in enumerate(heads):
            if nickname.lower() in h.group(2).lower():
                end = heads[i + 1].start() if i + 1 < len(heads) else len(article_html)
                return _items(article_html[h.end():end])
        return []
    return _items(article_html)


def _items(body: str) -> list[dict]:
    out = []
    for frag in re.findall(r"<li[^>]*>(.*?)</li>", body, flags=re.S):
        t = re.sub(r"\s+", " ", _text(frag))
        m = ITEM.match(t)
        if m:
            out.append({"pos": m.group("pos"), "name": m.group("name").strip(), "note": m.group("note")})
    return out


def fetch_team(team: str, kickoff_utc: datetime, now: datetime, getter=_get) -> dict:
    index_url, site, nick = CLUB_SITES[team]
    res = {"team": team, "status": "MISSING", "source": "club official site", "index_url": index_url}
    try:
        idx = getter(index_url)
    except Exception as e:
        res["reason"] = f"index fetch failed: {e!r}"
        return res
    for rel in find_article_links(idx)[:6]:
        url = site + rel
        try:
            art = getter(url)
        except Exception as e:
            res.setdefault("errors", []).append(f"{url}: {e!r}")
            continue
        pub = published_utc(art)
        if pub is None or not (kickoff_utc - EARLIEST_BEFORE_KICKOFF <= pub <= kickoff_utc):
            res.setdefault("skipped", []).append({"url": url, "published_utc": pub.isoformat() if pub else None,
                                                  "why": "not published in [T-120m, kickoff]"})
            continue
        players = parse_inactives(art, nick)
        if not players:
            res.setdefault("skipped", []).append({"url": url, "why": "no inactive list parsed"})
            continue
        res.update(status="OK", url=url, published_utc=pub.isoformat(), players=players,
                   sha256=hashlib.sha256(art.encode()).hexdigest())
        res.pop("reason", None)
        return res
    res.setdefault("reason", "no club inactives article for this game yet")
    return res


def pull(game_id: str, kickoff_utc: datetime, now: datetime | None = None, getter=_get, out_dir: Path = OUT) -> Path:
    now = now or datetime.now(timezone.utc)
    _, _, away, home = game_id.split("_")
    teams = {t: fetch_team(t, kickoff_utc, now, getter) for t in (away, home)}
    ok = all(v["status"] == "OK" for v in teams.values())
    rec = {"schema": "official-inactives/1", "game_id": game_id, "kickoff_utc": kickoff_utc.isoformat(),
           "retrieved_utc": now.isoformat(timespec="seconds"), "status": "OK" if ok else "INCOMPLETE",
           "teams": teams, "inactives": {t: [p["name"] for p in v.get("players", [])] for t, v in teams.items()}}
    d = Path(out_dir) / game_id
    d.mkdir(parents=True, exist_ok=True)
    f = d / f"inactives_{now:%Y%m%dT%H%M%SZ}.json"
    f.write_text(json.dumps(rec, indent=1) + "\n")
    return f


def newest(game_id: str, out_dir: Path = OUT) -> Path | None:
    files = sorted((Path(out_dir) / game_id).glob("inactives_*.json"))
    return files[-1] if files else None


def hook(pk: dict, out_dir: Path = OUT) -> dict:
    """pipeline.hooks REGISTRY['official_inactives'] contract. Read-only, no network."""
    gid = (pk.get("game") or {}).get("game_id")
    f = newest(gid, out_dir) if gid else None
    if f is None:
        return {"status": "MISSING", "reason": f"No phase15/inactives/{gid}/inactives_*.json; run "
                f"`python -m phase15.official_inactives --game {gid}` after T-90."}
    rec = json.loads(f.read_text())
    if rec.get("status") != "OK":
        bad = {t: v.get("reason") for t, v in rec.get("teams", {}).items() if v.get("status") != "OK"}
        return {"status": "INCOMPLETE", "reason": f"{f.name}: not OK for {bad}", "file": str(f)}
    return {"status": "OK", "retrieved_utc": rec["retrieved_utc"], "inactives": rec["inactives"],
            "file": str(f.relative_to(ROOT)) if f.is_relative_to(ROOT) else str(f),
            "sources": {t: v.get("url") for t, v in rec["teams"].items()}}


def _kickoff_from_packet(game_id: str) -> datetime | None:
    p = ROOT / "pregame" / "packets" / game_id / "packet.json"
    if not p.exists():
        return None
    w = json.loads(p.read_text()).get("weather") or {}
    ko = w.get("kickoff_utc")
    return datetime.fromisoformat(ko.replace("Z", "+00:00")) if ko else None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--game", required=True)
    ap.add_argument("--kickoff-utc")
    a = ap.parse_args(argv)
    ko = datetime.fromisoformat(a.kickoff_utc.replace("Z", "+00:00")) if a.kickoff_utc else _kickoff_from_packet(a.game)
    if ko is None:
        print("kickoff unknown: pass --kickoff-utc", file=sys.stderr)
        return 2
    f = pull(a.game, ko)
    rec = json.loads(f.read_text())
    print(f"{f.relative_to(ROOT)}: {rec['status']}")
    for t, v in rec["teams"].items():
        print(f"  {t}: {v['status']} {v.get('url') or v.get('reason')} {[p['name'] for p in v.get('players', [])]}")
    return 0 if rec["status"] == "OK" else 3


if __name__ == "__main__":
    sys.exit(main())
