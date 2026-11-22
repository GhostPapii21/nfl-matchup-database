"""Turn OCR tokens from Circa betting sheets into market rows (NFL-40 / NFL-33).

Layouts handled:
  game   NFL weekly page 1: rotation, team, full game / 1st half / 1st quarter spread, total, moneyline
  pairs  stacked rotation pairs (odd = over, even = under): NFL team totals page and the player-props sheet

Rules (no invented numbers):
  * A price Circa did not print is left empty (price=None, price_printed=False). We do not assume -110.
  * Circa prints the spread only on the favourite's row. The other side's line is its negation and is flagged
    line_derived=True. Nothing else is derived.
  * Totals: Circa prints one number between the two team rows with an optional stacked price pair. The upper
    price is the over and the lower price the under, matching the sheet's own rotation convention (odd = OVER,
    as printed in the Grand Salami block). Rows record side_basis so this is auditable.
  * Any cell whose OCR is not clean ('?' in the text) is dropped and counted in the report, never guessed.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, asdict, field

NUM = re.compile(r"^[+-]?\d*½?$")
MONTHS = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")


def num(text: str):
    """'-3½' -> -3.5, 'EVEN' -> 100.0, '-½' -> -0.5, else None."""
    t = (text or "").strip()
    if t.upper() in ("EVEN", "EV"):
        return 100.0
    if not t or not NUM.match(t) or t in ("+", "-", "½") and t != "½":
        return None
    half = t.endswith("½")
    core = t[:-1] if half else t
    sign = -1 if core.startswith("-") else 1
    core = core.lstrip("+-")
    if core == "" and not half:
        return None
    v = (int(core) if core else 0) + (0.5 if half else 0)
    return sign * v


def price(text: str):
    v = num(text)
    if v is None or "½" in text:
        return None
    if abs(v) < 100:
        return None
    return int(v)


@dataclass
class Row:
    layout: str
    page: int
    section: str
    game_date: str
    away_rot: int | None
    home_rot: int | None
    away: str
    home: str
    period: str
    market: str
    prop: str
    player: str
    team: str
    side: str
    side_rot: int | None
    line: float | None
    price: int | None
    price_printed: bool
    line_derived: bool
    side_basis: str
    kickoff_raw: str = ""
    y: float = 0.0

    def as_dict(self):
        return asdict(self)


def _g(t, k):
    return t[k] if isinstance(t, dict) else getattr(t, k)


class T:
    """thin view over token dicts."""
    def __init__(self, d):
        self.d = d if isinstance(d, dict) else d.as_dict()
        for k, v in self.d.items():
            setattr(self, k, v)
        self.yc = (self.y0 + self.y1) / 2
        self.xc = (self.x0 + self.x1) / 2
        self.h = self.y1 - self.y0


def _clean(t):
    return "?" not in t.text


def _is_int(t, digits):
    return re.fullmatch(r"\d{%d}" % digits, t.text) is not None if isinstance(digits, int) else re.fullmatch(digits, t.text) is not None


# ---------------------------------------------------------------- game layout
# Column x-ranges in PDF points relative to the full-game rotation column. Measured on the 2026 NFL weekly sheet
# template (612x1008 pt). Each range is [lo, hi) on the token's centre.
GAME_COLS = {
    "FG": {"rot": (85, 102), "spread": (165, 191), "sprice": (191, 212), "total": (210, 240), "tprice": (240, 255), "ml": (252, 286)},
    "1H": {"rot": (286, 308), "spread": (308, 334), "sprice": (334, 354), "total": (354, 376), "tprice": (376, 395), "ml": (395, 428)},
    "1Q": {"rot": (428, 450), "spread": (450, 476), "sprice": (476, 497), "total": (497, 517), "tprice": (517, 537), "ml": (537, 575)},
}


def _in(t, rng):
    return rng[0] <= t.xc < rng[1]


def _date_headers(toks):
    out = []
    groups = []
    for t in sorted(toks, key=lambda t: t.yc):
        if groups and abs(t.yc - groups[-1][-1].yc) < 0.35 * max(t.h, groups[-1][-1].h, 1):
            groups[-1].append(t)
        else:
            groups.append([t])
    for ts in groups:
        txt = " ".join(x.text for x in sorted(ts, key=lambda x: x.x0))
        m = re.search(r"\b(SUN|MON|TUE|WED|THU|FRI|SAT)\w*\s+(%s)\w*\s+(\d{1,2})\b" % "|".join(MONTHS), txt.upper())
        if m and max(x.h for x in ts) > 8:
            out.append((min(x.yc for x in ts), f"{m.group(1).title()} {m.group(2).title()} {m.group(3)}"))
    return sorted(out)


def parse_game_page(tokens, page=1):
    toks = [T(t) for t in tokens if _g(t, "page") == page]
    headers = _date_headers(toks)
    rots = sorted([t for t in toks if _in(t, GAME_COLS["FG"]["rot"]) and re.fullmatch(r"\d{3}", t.text)], key=lambda t: t.yc)
    rows, dropped = [], []
    i = 0
    while i + 1 < len(rots):
        a, b = rots[i], rots[i + 1]
        if int(b.text) != int(a.text) + 1 or int(a.text) % 2 == 0 or not (6 < b.yc - a.yc < 22):
            i += 1
            continue
        i += 2
        if not [t for t in toks if _in(t, GAME_COLS["1H"]["rot"]) and abs(t.yc - a.yc) < 3.2 and re.fullmatch(r"\d{4}", t.text)]:
            continue   # not a game row (e.g. Grand Salami block, rotation 291-294)
        ya, yb, mid = a.yc, b.yc, (a.yc + b.yc) / 2
        date = ""
        for (hy, hd) in headers:
            if hy < ya:
                date = hd
        def row_toks(y, tol=3.2):
            return [t for t in toks if abs(t.yc - y) < tol]
        team = {}
        for side, y in (("away", ya), ("home", yb)):
            names = [t for t in row_toks(y) if 102 <= t.x0 < 170 and re.search(r"[A-Z]", t.text)]
            team[side] = " ".join(t.text for t in sorted(names, key=lambda t: t.x0)).strip()
        kick = " ".join(t.ocr_full for t in sorted(row_toks(ya), key=lambda t: t.x0) if t.x1 < 86 and t.ocr_full).strip()
        base = dict(layout="game", page=page, section="game lines", game_date=date, away_rot=int(a.text), home_rot=int(b.text),
                    away=team["away"], home=team["home"], prop="", player="", team="", kickoff_raw=kick)
        for per, cols in GAME_COLS.items():
            # rotation numbers for this period (1H: 1xxx, 1Q: 3xxx); a period is present only if its rot exists
            prot = {}
            for side, y in (("away", ya), ("home", yb)):
                c = [t for t in row_toks(y) if _in(t, cols["rot"]) and re.fullmatch(r"\d{3,4}", t.text)]
                prot[side] = int(c[0].text) if c else None
            if prot["away"] is None and prot["home"] is None:
                continue
            if per != "FG" and any(v is not None and v < 1000 for v in prot.values()):
                continue
            # spreads
            cell = {}
            for side, y in (("away", ya), ("home", yb)):
                rt = row_toks(y)
                sp = [t for t in rt if _in(t, cols["spread"]) and t.h > 5]
                pr = [t for t in rt if _in(t, cols["sprice"]) and t.h > 3]
                ml = [t for t in rt if _in(t, cols["ml"]) and t.h > 5]
                cell[side] = (sp, pr, ml)
            fav = [s for s in ("away", "home") if cell[s][0]]
            bad = [t for s in cell for grp in cell[s] for t in grp if not _clean(t)]
            if bad:
                dropped.append((per, base["away"], base["home"], [t.text for t in bad]))
            if len(fav) == 1 and all(_clean(t) for t in cell[fav[0]][0]):
                f = fav[0]; d = "home" if f == "away" else "away"
                fl = num(cell[f][0][0].text)
                if fl is not None:
                    for s, line, derived in ((f, fl, False), (d, -fl if fl != 0 else 0.0, True)):
                        ps = [t for t in cell[s][1] if _clean(t) and price(t.text) is not None]
                        rows.append(Row(**base, period=per, market="spread", side=team[s], side_rot=prot[s], line=line,
                                        price=price(ps[0].text) if ps else None, price_printed=bool(ps), line_derived=derived,
                                        side_basis="favourite row prints the line; other side negated" if derived else "printed",
                                        y=round(ya if s == "away" else yb, 1)))
            for s in ("away", "home"):
                ms = [t for t in cell[s][2] if _clean(t) and price(t.text) is not None]
                if ms:
                    rows.append(Row(**base, period=per, market="moneyline", side=team[s], side_rot=prot[s], line=None,
                                    price=price(ms[0].text), price_printed=True, line_derived=False, side_basis="printed",
                                    y=round(ya if s == "away" else yb, 1)))
            # total: number centred between the rows, optional stacked prices
            tot = [t for t in toks if _in(t, cols["total"]) and abs(t.yc - mid) < 3.5 and t.h > 5 and _clean(t) and num(t.text) is not None and price(t.text) is None]
            if tot:
                line = num(tot[0].text)
                tp = [t for t in toks if _in(t, cols["tprice"]) and ya - 1 < t.yc < yb + 1 and t.h < 6.5]
                up = [t for t in tp if t.yc < mid and _clean(t) and price(t.text) is not None]
                lo = [t for t in tp if t.yc > mid and _clean(t) and price(t.text) is not None]
                for side, p in (("over", up), ("under", lo)):
                    rows.append(Row(**base, period=per, market="total", side=side, side_rot=prot["away" if side == "over" else "home"],
                                    line=line, price=price(p[0].text) if p else None, price_printed=bool(p), line_derived=False,
                                    side_basis="upper stacked price = over, lower = under (sheet convention odd rot = OVER)",
                                    y=round(mid, 1)))
    return rows, dropped


# ---------------------------------------------------------------- stacked-pair layout (team totals, props)
SECTION_WORDS = ("PROPS", "YARDS", "PASSES", "TOTALS", "RECEPTIONS", "ATTEMPTS", "COMPLETIONS", "TOUCHDOWN", "POINTS", "INTERCEPTIONS")


def _sections(toks):
    cand = sorted([t for t in toks if t.h > 6 and re.search(r"[A-Za-z]", t.text)], key=lambda t: t.yc)
    groups = []
    for t in cand:
        if groups and abs(t.yc - groups[-1][-1].yc) < 0.35 * max(t.h, groups[-1][-1].h):
            groups[-1].append(t)
        else:
            groups.append([t])
    out = []
    for ts in groups:
        ts = sorted(ts, key=lambda x: x.x0)
        txt = " ".join(x.text for x in ts)
        if any(w in txt.upper() for w in SECTION_WORDS) and not re.search(r"\(\w+\)", txt) and len(ts) <= 5:
            out.append((min(x.yc for x in ts), txt.strip(), ts[0].x0, ts[-1].x1))
    return sorted(out)


def parse_pair_page(tokens, page, kind):
    """kind = 'team_total' or 'player_prop'."""
    toks = [T(t) for t in tokens if _g(t, "page") == page]
    secs = _sections(toks)
    rot_re = r"\d{4,5}"
    rots = [t for t in toks if re.fullmatch(rot_re, t.text)]
    pairs = []
    for a in rots:
        if int(a.text) % 2 == 0:
            continue
        cands = [b for b in rots if int(b.text) == int(a.text) + 1 and abs(b.x0 - a.x0) < 4 and 0.6 * a.h < b.yc - a.yc < 2.6 * a.h]
        if cands:
            pairs.append((a, cands[0]))
    rows, dropped = [], []
    for a, b in pairs:
        y0, y1, mid = a.y0 - 0.3 * a.h, b.y1 + 0.3 * a.h, (a.yc + b.yc) / 2
        right = min([p[0].x0 for p in pairs if p[0].x0 > a.x1 + 5 and abs(p[0].yc - a.yc) < a.h] + [612])
        cell = sorted([t for t in toks if a.x1 < t.x0 < right - 1 and y0 - 2 < t.yc < y1 + 2], key=lambda t: t.x0)
        names = [t for t in cell if re.search(r"[A-Za-z]", t.text) and t.text.upper() not in ("EVEN", "EV")]
        nums = [t for t in cell if t not in names]
        if not names or not nums:
            continue
        name_x1 = max(t.x1 for t in names)
        big = [t for t in nums if t.x0 >= name_x1 - 1 and abs(t.yc - mid) < 0.6 * (b.yc - a.yc)]
        if not big:
            continue
        hmax = max(t.h for t in big)
        big = [t for t in big if t.h > 0.85 * hmax]
        lt = sorted(big, key=lambda t: t.x0)[0]
        if not _clean(lt) or num(lt.text) is None:
            dropped.append((page, a.text, " ".join(t.text for t in names), lt.text)); continue
        small = [t for t in nums if t.x0 >= lt.x1 - 1 and t.h <= 0.85 * lt.h]
        up = [t for t in small if t.yc < mid]
        lo = [t for t in small if t.yc > mid]
        name = " ".join(t.text for t in names)
        m = re.search(r"\(([A-Z]{2,4})\)", name)
        team = norm_team(m.group(1)) if m else ""
        player = re.sub(r"\s*\([^)]*\)\s*", " ", name).strip()
        sec = ""
        for (sy, st, sx0, sx1) in secs:
            if sy < a.y0:
                sec = st
        prop_type = sec
        group = ""
        for (sy, st, sx0, sx1) in secs:
            if sy < a.y0 and "PROPS" in st.upper():
                group = st
        for side, p, rt in (("over", up, a), ("under", lo, b)):
            ok = [t for t in p if _clean(t) and price(t.text) is not None]
            if p and not ok:
                dropped.append((page, rt.text, player, [t.text for t in p])); 
            if kind == "team_total":
                base = dict(layout="pairs", page=page, section=sec or "team totals", game_date="", away_rot=None, home_rot=None,
                            away="", home="", period="FG", market="team_total", prop="team total points", player="", team=player)
            else:
                base = dict(layout="pairs", page=page, section=group, game_date="", away_rot=None, home_rot=None,
                            away="", home="", period="FG", market="player_prop", prop=prop_type, player=player, team=team)
            rows.append(Row(**base, side=side, side_rot=int(rt.text), line=num(lt.text), price=price(ok[0].text) if ok else None,
                            price_printed=bool(ok), line_derived=False,
                            side_basis="odd rotation = over, even = under; upper stacked price = over", y=round(mid, 1)))
    return rows, dropped


NFL_TEAMS = {"ARI", "ATL", "BAL", "BUF", "CAR", "CHI", "CIN", "CLE", "DAL", "DEN", "DET", "GB", "HOU", "IND", "JAX", "KC", "LV",
             "LAC", "LAR", "MIA", "MIN", "NE", "NO", "NYG", "NYJ", "PHI", "PIT", "SF", "SEA", "TB", "TEN", "WAS"}


def norm_team(code: str) -> str:
    """OCR reads this font's I as T ('CHT', 'PHT', 'ART'). Repair only when the repaired code is a real team and the
    raw one is not; otherwise return the raw code prefixed with '?' so it is visibly unverified."""
    c = (code or "").upper().strip("() ")
    if c in NFL_TEAMS:
        return c
    for cand in {c.replace("T", "I"), c[:-1] + "I" if c.endswith("T") else c}:
        if cand in NFL_TEAMS:
            return cand
    return "?" + c


def parse_yesno_page(tokens, page, prop="anytime touchdown"):
    """'WILL [PLAYER] SCORE A TOUCHDOWN?' grid: NAME (TEAM)  yes-rot yes-price  no-rot no-price, two columns."""
    toks = [T(t) for t in tokens if _g(t, "page") == page]
    rows, dropped = [], []
    lines = {}
    for t in toks:
        lines.setdefault(round(t.yc / 2.5), []).append(t)
    keys = sorted(lines)
    merged, seen = [], set()
    for k in keys:
        if k in seen:
            continue
        grp = lines[k] + lines.get(k + 1, [])
        seen.update({k, k + 1})
        merged.append(sorted(grp, key=lambda t: t.x0))
    for ln in merged:
        i = 0
        while i < len(ln):
            # a block: names... rot price rot price
            j = i
            names = []
            while j < len(ln) and re.search(r"[A-Za-z]", ln[j].text) and ln[j].text.upper() not in ("EV", "EVEN"):
                names.append(ln[j]); j += 1
            if not names or j + 3 >= len(ln) + 0:
                i = j + 1
                continue
            seq = ln[j:j + 4]
            if len(seq) < 4 or not (re.fullmatch(r"\d{4}", seq[0].text) and re.fullmatch(r"\d{4}", seq[2].text)):
                i = j + 1
                continue
            name = " ".join(t.text for t in names)
            m = re.search(r"\(([A-Z]{2,4})\)", name)
            team = norm_team(m.group(1)) if m else ""
            player = re.sub(r"\s*\([^)]*\)\s*", " ", name).strip()
            for side, rt, pt in (("yes", seq[0], seq[1]), ("no", seq[2], seq[3])):
                pr = price(pt.text) if _clean(pt) else None
                if pr is None:
                    dropped.append((page, rt.text, player, pt.text))
                    continue
                rows.append(Row(layout="yesno", page=page, section="WILL [PLAYER] SCORE A TOUCHDOWN?", game_date="", away_rot=None,
                                home_rot=None, away="", home="", period="FG", market="player_prop", prop=prop, player=player,
                                team=team, side=side, side_rot=int(rt.text), line=None, price=pr, price_printed=True,
                                line_derived=False, side_basis="printed YES / NO columns", y=round(rt.yc, 1)))
            i = j + 4
    return rows, dropped


def parse_early_page(tokens, page=1):
    """'Week N (Early Lines)': rotation, team, full-game spread (with optional price), total between rows. No ML."""
    toks = [T(t) for t in tokens if _g(t, "page") == page]
    headers = _date_headers(toks)
    rots = sorted([t for t in toks if re.fullmatch(r"\d{3}", t.text) and t.x0 < 200], key=lambda t: t.yc)
    rows, dropped = [], []
    i = 0
    while i + 1 < len(rots):
        a, b = rots[i], rots[i + 1]
        if int(b.text) != int(a.text) + 1 or int(a.text) % 2 == 0 or not (0.8 * a.h < b.yc - a.yc < 4 * a.h) or abs(a.x0 - b.x0) > 5:
            i += 1
            continue
        i += 2
        ya, yb, mid = a.yc, b.yc, (a.yc + b.yc) / 2
        date = ""
        for (hy, hd) in headers:
            if hy < ya:
                date = hd
        team, cells = {}, {}
        for side, y in (("away", ya), ("home", yb)):
            rt = sorted([t for t in toks if abs(t.yc - y) < 0.45 * a.h * 2 and t.x0 > a.x1], key=lambda t: t.x0)
            names = [t for t in rt if re.search(r"[A-Z]{2}", t.text) and t.text.upper() not in ("EVEN", "EV", "PK")]
            team[side] = " ".join(t.text for t in names)
            nx = max([t.x1 for t in names] + [a.x1])
            cells[side] = [t for t in rt if t.x0 > nx and abs(t.yc - y) < 0.6 * a.h]
        kick = " ".join(t.ocr_full for t in sorted([t for t in toks if abs(t.yc - ya) < 0.6 * a.h and t.x1 < a.x0], key=lambda t: t.x0)).strip()
        base = dict(layout="early", page=page, section="early lines", game_date=date, away_rot=int(a.text), home_rot=int(b.text),
                    away=team["away"], home=team["home"], prop="", player="", team="", kickoff_raw=kick, period="FG")
        # total: number vertically centred between the two rows, rightmost column
        tots = [t for t in toks if abs(t.yc - mid) < 0.35 * a.h * 2 and t.x0 > a.x1 + 100 and _clean(t) and num(t.text) is not None
                and price(t.text) is None and t not in cells["away"] + cells["home"]]
        sp = {}
        for s in ("away", "home"):
            line_t = [t for t in cells[s] if t.text.upper() == "PK" or (num(t.text) is not None and price(t.text) is None and t not in tots)]
            pr_t = [t for t in cells[s] if price(t.text) is not None]
            bad = [t for t in cells[s] if not _clean(t)]
            if bad:
                dropped.append((page, a.text, [t.text for t in bad]))
            sp[s] = (line_t, pr_t)
        fav = [s for s in sp if sp[s][0]]
        if len(fav) == 1:
            f = fav[0]; d = "home" if f == "away" else "away"
            lt = sp[f][0][0]
            fl = 0.0 if lt.text.upper() == "PK" else num(lt.text)
            for s, line, der in ((f, fl, False), (d, -fl if fl else 0.0, True)):
                ps = sp[s][1]
                rows.append(Row(**base, market="spread", side=team[s], side_rot=int((a if s == "away" else b).text), line=line,
                                price=price(ps[0].text) if ps else None, price_printed=bool(ps), line_derived=der,
                                side_basis=("PK printed" if lt.text.upper() == "PK" else "favourite row prints the line; other side negated") if der else "printed",
                                y=round(ya if s == "away" else yb, 1)))
        if tots:
            for side in ("over", "under"):
                rows.append(Row(**base, market="total", side=side, side_rot=int((a if side == "over" else b).text), line=num(tots[0].text),
                                price=None, price_printed=False, line_derived=False, side_basis="single total printed, no price",
                                y=round(mid, 1)))
    return rows, dropped


def page_kind(tokens, page):
    txt = " ".join(_g(t, "text") for t in tokens if _g(t, "page") == page).upper()
    if "SCORE A TOUCHDOWN" in txt or ("YES" in txt.split() and "NO" in txt.split() and "TOUCHDOWN" in txt):
        return "yesno"
    if "TEAM TOTALS" in txt or ("TEAM" in txt and "TOTALS" in txt):
        return "team_total"
    if "PLAYER" in txt and "PROPS" in txt:
        return "player_prop"
    if "EARLY" in txt and "LINES" in txt:
        return "early"
    if "HALF" in txt and "QUARTER" in txt:
        return "game"
    return "unknown"


def parse_tokens(tokens):
    """-> rows, report {page: {kind, rows, dropped}}"""
    rows, report = [], {}
    for page in sorted({_g(t, "page") for t in tokens}):
        kind = page_kind(tokens, page)
        if kind == "game":
            r, d = parse_game_page(tokens, page)
        elif kind == "early":
            r, d = parse_early_page(tokens, page)
        elif kind in ("team_total", "player_prop"):
            r, d = parse_pair_page(tokens, page, kind)
        elif kind == "yesno":
            r, d = parse_yesno_page(tokens, page)
        else:
            r, d = [], []
        rows.extend(r)
        report[page] = {"kind": kind, "rows": len(r), "dropped": [list(map(str, x)) for x in d]}
    return rows, report


def updated_stamp(tokens):
    """the sheet's own printed 'Updated MM/DD/YY HH:MM AM' footer, as OCR'd (kept raw; the PDF CreationDate is the
    machine-readable publish time)."""
    for page in sorted({_g(t, "page") for t in tokens}):
        ts = sorted([T(t) for t in tokens if _g(t, "page") == page], key=lambda t: (round(t.yc), t.x0))
        for t in ts:
            if (t.ocr_full or t.text).lower().startswith("updated"):
                line = [x for x in ts if abs(x.yc - t.yc) < 2]
                return " ".join((x.ocr_full or x.text) for x in sorted(line, key=lambda x: x.x0))
    return ""
