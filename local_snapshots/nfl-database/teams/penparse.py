import re
ALIAS = {"ARZ":"ARI","BLT":"BAL","CLV":"CLE","HST":"HOU","LA":"LAR","WAS":"WSH"}
NORM = [(r"false start|offensive offside", "False Start/Offside"), (r"offensive holding", "Offensive Holding"),
        (r"illegal formation|illegal shift|illegal motion", "Illegal Formation/Shift/Motion"), (r"offensive pass interference", "OPI"),
        (r"defensive pass interference", "DPI"), (r"roughing the passer", "Roughing the Passer"), (r"face ?mask", "Face Mask"),
        (r"defensive holding", "Defensive Holding"), (r"illegal contact", "Illegal Contact"), (r"delay of game", "Delay of Game"),
        (r"unnecessary roughness", "Unnecessary Roughness"), (r"neutral zone|encroachment|defensive offside", "Defensive Offside/NZI/Encroach"),
        (r"intentional grounding", "Intentional Grounding"), (r"illegal block|chop block|clipping", "Illegal Block"),
        (r"taunting|unsportsmanlike", "Unsportsmanlike/Taunting"), (r"too many men|12 men", "Too Many Men"), (r"holding", "Holding (other)")]
def norm(t):
    tl = t.lower()
    for rx, n in NORM:
        if re.search(rx, tl): return n
    return t.strip()
PEN = re.compile(r"PENALTY on\s+([A-Z]{2,3})(?:-([^,]+?))?,\s*([^,]+?),\s*(?:(\d+)\s*yards?|declined|(?=offsetting)|(?=placed at))", re.I)
def parse_penalties(text):
    t = re.sub(r"\s+", " ", text or "")
    off = bool(re.search(r"penalties offset|offsetting", t, re.I))
    out = []
    for m in PEN.finditer(t):
        seg = t[m.start(): m.start() + 250].split("PENALTY on", 2)
        seg = "PENALTY on" + seg[1] if len(seg) > 1 else t[m.start():]
        dec = bool(re.match(r"[^.]*?,\s*declined", seg.split(",", 1)[1] if "," in seg else "", re.I)) or (m.group(4) is None and "declined" in m.group(0).lower())
        status = "offsetting" if off else ("declined" if dec else "accepted")
        out.append(dict(team=ALIAS.get(m.group(1).upper(), m.group(1).upper()), player=(m.group(2) or "").strip(), type=m.group(3).strip(), type_norm=norm(m.group(3)),
                        yards=int(m.group(4)) if (m.group(4) and status == "accepted") else 0, status=status,
                        no_play=bool(re.search(r"no play", seg, re.I))))
    return out
