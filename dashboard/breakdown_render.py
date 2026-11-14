"""Render a breakdown JSON (from dashboard.breakdown) and an analyst notes JSON into one HTML page body.

    python3 -m dashboard.breakdown_render dashboard/results/breakdown_X.json notes.json out.html
"""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

E = html.escape


def pct(x, d=0):
    return "—" if x is None else f"{x * 100:.{d}f}%"


def num(x, d=1):
    return "—" if x is None else (f"{x:.{d}f}" if isinstance(x, float) else str(x))


def amer(a):
    return "—" if a is None else (f"+{a}" if a > 0 else str(a))


def chip(text, kind="mute"):
    return f'<span class="chip {kind}">{E(str(text))}</span>'


def status_chip(s):
    if not s:
        return chip("Healthy", "good")
    k = {"out": "bad", "injured reserve": "bad", "doubtful": "bad", "questionable": "warn"}.get(s.lower(), "mute")
    return chip(s, k)


def bars(log, line=80):
    """Yards per game, a dashed line at 80, a dot for each 20+ yard catch."""
    if not log:
        return ""
    w, h, pad = 300, 92, 16
    top = max(170, max(g["yards"] for g in log) + 10)
    n = len(log)
    bw = (w - 8) / n
    y = lambda v: h - pad - (v / top) * (h - pad - 6)
    out = [f'<svg viewBox="0 0 {w} {h}" class="bars" role="img" aria-label="Yards by game">']
    out.append(f'<line x1="0" x2="{w}" y1="{y(line):.1f}" y2="{y(line):.1f}" class="ref"/>')
    out.append(f'<text x="{w - 2}" y="{y(line) - 3:.1f}" class="reflab" text-anchor="end">80</text>')
    for i, g in enumerate(log):
        x = 4 + i * bw
        cls = "b100" if g["yards"] >= 100 else "b80" if g["yards"] >= 80 else "b"
        top_y = y(max(g["yards"], 0))
        out.append(f'<rect x="{x + 2:.1f}" y="{top_y:.1f}" width="{bw - 4:.1f}" height="{max(h - pad - top_y, 1):.1f}" class="{cls}" rx="2">'
                   f'<title>Wk {g["week"]} vs {g["opp"]}: {g["targets"]} tgt, {g["rec"]} rec, {g["yards"]} yds, {g["explosive"]} catches of 20+</title></rect>')
        for k in range(g["explosive"]):
            out.append(f'<circle cx="{x + bw / 2:.1f}" cy="{top_y - 5 - k * 6:.1f}" r="2.4" class="exdot"/>')
        out.append(f'<text x="{x + bw / 2:.1f}" y="{h - 3}" text-anchor="middle" class="xlab">{E(g["opp"])}</text>')
    out.append("</svg>")
    return "".join(out)


def cov_fit(r, shell):
    c = r.get("coverage_2025") or {}
    if not c or not shell:
        return ""
    rows = []
    for key, lab, rate in (("vs_man", "Man", shell.get("man_rate")), ("vs_zone", "Zone", shell.get("zone_rate")),
                           ("vs_mofo", "Two-high (MOFO)", shell.get("mofo_rate")), ("vs_mofc", "One-high (MOFC)", shell.get("mofc_rate"))):
        v = c.get(key)
        if not v:
            continue
        rows.append(f"<tr><td>{lab}</td><td>{pct(rate)}</td><td>{v['targets']}</td><td>{pct(v['catch_rate'])}</td><td>{num(v['yards_per_target'])}</td></tr>")
    return ('<div class="scroll"><table class="mini"><thead><tr><th>Coverage</th><th>Defense uses</th><th>His tgts</th><th>Catch</th><th>Yds/tgt</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>')


def props_table(r):
    p = r.get("props") or {}
    if not p:
        return '<p class="muted small">No FanDuel or DraftKings prop posted in this pull.</p>'
    rows = []
    for stat, lab in (("receptions", "Receptions"), ("receiving_yards", "Rec yards")):
        for b in ("fanduel", "draftkings"):
            q = p.get(stat, {}).get(b)
            if not q:
                continue
            gap = None if q.get("sim_over") is None or q.get("break_even") is None else q["sim_over"] - q["break_even"]
            k = "good" if gap is not None and gap >= 0.03 else "bad" if gap is not None and gap <= -0.05 else "mute"
            rows.append(f"<tr><td>{lab}</td><td>{'FD' if b == 'fanduel' else 'DK'}</td><td>O {q['line']}</td><td>{amer(q['over'])}</td>"
                        f"<td>{pct(q.get('break_even'))}</td><td>{pct(q.get('sim_over'))}</td><td>{chip(('+' if gap and gap > 0 else '') + pct(gap) if gap is not None else '—', k)}</td></tr>")
    return ('<div class="scroll"><table class="mini"><thead><tr><th>Prop</th><th>Book</th><th>Line</th><th>Over</th><th>Needs</th><th>Sim</th><th>Gap</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>')


def receiver_card(r, side, note):
    p = r.get("profile") or {}
    hits = p.get("hits", {})
    g = p.get("games", 0)
    e8 = p.get("eight_plus", {})
    soft, hard = p.get("vs_explosive_friendly", {}), p.get("vs_explosive_stingy", {})
    py = r.get("p_yards") or {}
    inp = r.get("inputs") or {}
    stats = [("Proj. targets", num(r.get("targets_mean"))), ("Proj. catches", num(r.get("receptions_mean"))),
             ("Median yds", num(r.get("yards_median"), 0)), ("80+ chance", pct(py.get("80"))), ("100+ chance", pct(py.get("100"))),
             ("Target share, season / last 3", f"{pct(inp.get('target_share_window'))} / {pct(inp.get('target_share_last3'))}")]
    stat_html = "".join(f'<div class="stat"><span>{E(k)}</span><b>{v}</b></div>' for k, v in stats)
    hit_html = " ".join(f'<span class="hit"><b>{hits.get(k, 0)}/{g}</b> {k}+</span>' for k in ("50", "60", "80", "100"))
    eight = (f"<b>{e8['games']}</b> games with 8+ targets: {num(e8.get('rec_avg'))} catches, {num(e8.get('yds_avg'), 0)} yds avg, "
             f"80+ in {e8.get('hit80', 0)}, 100+ in {e8.get('hit100', 0)}" if e8.get("games") else "No 8+ target games yet")
    split = (f"Vs defenses in the top 12 for explosives allowed: <b>{num(soft.get('yds_avg'), 0)}</b> yds, {num(soft.get('ex_pg'))} explosive/g "
             f"({soft.get('games', 0)} g) · vs the rest: <b>{num(hard.get('yds_avg'), 0)}</b> yds, {num(hard.get('ex_pg'))} explosive/g ({hard.get('games', 0)} g)")
    verdict = note.get("verdict") if note else None
    vk = note.get("kind", "mute") if note else "mute"
    return f'''<article class="rc" id="{E(r['player_id'] or '')}">
  <header><div><h4>{E(r['player'])}</h4><span class="muted">{E(r['pos'])} · {E(side['offense'])}</span></div>{chip(verdict, vk) if verdict else ''}</header>
  <div class="stats">{stat_html}</div>
  <div class="rc-grid">
    <div class="rc-col">
      <p class="lab">This season, yards by game <span class="muted">(dots = catches of 20+)</span></p>
      {bars(p.get('log', []))}
      <p class="hits">{hit_html}</p>
      <p class="small">{p.get('explosive_total', 0)} explosive catches in {g} games ({num(p.get('explosive_pg'), 2)}/g); at least one in {p.get('games_with_explosive', 0)} games.</p>
      <p class="small">{eight}.</p>
      <p class="small">{split}.</p>
    </div>
    <div class="rc-col">
      <p class="lab">FanDuel and DraftKings against the sim</p>
      {props_table(r)}
      <p class="lab">Coverage fit <span class="muted">({r.get('coverage_season') or '2025'} charting, last season)</span></p>
      {cov_fit(r, side.get('shell')) or '<p class="muted small">No charted routes last season.</p>'}
    </div>
  </div>
  {f'<p class="note">{note["text"]}</p>' if note and note.get("text") else ''}
</article>'''


def defense_block(side):
    ex, lg = side.get("defense_explosive") or {}, side.get("league_explosive") or {}
    da, rk = side.get("defense_allowed") or {}, side.get("defense_rank") or {}
    sh = side.get("shell") or {}
    cp = side.get("coverage_profile") or {}
    tiles = [("20+ yd catches allowed / g", f"{num(ex.get('ex20_pg'), 2)}", f"#{ex.get('rank')} most of 32 · league {num(lg.get('ex20_pg'), 2)}"),
             ("Explosive yards allowed / g", num(ex.get("explosive_yards_pg"), 0), f"40+ yd catches: {num(ex.get('ex40_pg'), 2)}/g"),
             ("Explosives by position / g", f"WR {num(ex.get('by_pos_pg', {}).get('WR'), 1)} · TE {num(ex.get('by_pos_pg', {}).get('TE'), 1)}",
              f"League WR {num(lg.get('by_pos_pg', {}).get('WR'), 1)} · TE {num(lg.get('by_pos_pg', {}).get('TE'), 1)}"),
             ("Pass yds allowed / g", num(da.get("pass_yards_pg"), 0), f"{num(da.get('yards_per_pass_attempt'), 2)} per att · rank {rk.get('pass_yards_pg', {}).get('rank')} (1 = fewest)"),
             ("WR / TE yds allowed rank", f"{rk.get('wr_rec_yards_pg', {}).get('rank')} / {rk.get('te_rec_yards_pg', {}).get('rank')}", "1 = allows the fewest"),
             ("Pressure / sack rate rank", f"{rk.get('pressure_rate', {}).get('rank')} / {rk.get('sack_rate', {}).get('rank')}", "1 = most pressure")]
    tile_html = "".join(f'<div class="tile"><span>{E(a)}</span><b>{b}</b><small>{E(c)}</small></div>' for a, b, c in tiles)
    shells = ", ".join(f"{s['shell']} {pct(s['rate'])}" for s in (cp.get("shells") or []))
    va = lambda k: sh.get(k) or {}
    cov = (f'<p class="small"><b>Last season&rsquo;s coverage:</b> zone {pct(sh.get("zone_rate"))}, man {pct(sh.get("man_rate"))}; '
           f'two-high {pct(sh.get("mofo_rate"))}, one-high {pct(sh.get("mofc_rate"))}. Top shells: {E(shells)}. '
           f'Allowed {num(va("vs_man").get("yards_per_attempt"), 2)} yds/att vs man, {num(va("vs_zone").get("yards_per_attempt"), 2)} vs zone, '
           f'{num(va("vs_mofo").get("yards_per_attempt"), 2)} vs two-high, {num(va("vs_mofc").get("yards_per_attempt"), 2)} vs one-high. '
           f'5+ rushers on {pct(cp.get("five_plus_rushers_rate"))} of dropbacks.</p>') if sh else ""
    base = side.get("defender_league_median") or {}
    rows = []
    for c in side.get("coverage_personnel", []):
        hot = c.get("yds_pg") is not None and base.get("yds_pg") and c["yds_pg"] >= base["yds_pg"] * 1.2 and (c.get("tgt_pg") or 0) >= 2
        rows.append(f"<tr class=\"{'hot' if hot else ''}\"><td>{E(c['player'])}</td><td>{E(c['pos'])}</td><td>{status_chip(c.get('status'))}</td>"
                    f"<td>{num(c.get('snap_last'), 0)}%</td><td>{num(c.get('tgt_pg'))}</td><td>{num(c.get('rec_pg'))}</td><td>{num(c.get('yds_pg'))}</td>"
                    f"<td>{num(c.get('ypt'))}</td><td>{c.get('td', 0)} / {c.get('ints', 0)}</td></tr>")
    listed = {c["player"] for c in side.get("coverage_personnel", [])}
    extra = [x for x in side.get("coverage_injured", []) if x["player"] not in listed]
    extra_html = ("<p class=\"small\"><b>Also on the report:</b> " + "; ".join(f"{E(x['player'])} ({E(x['pos'])}, {E(x['status'])}, {E(x.get('injury') or '')})" for x in extra) + "</p>") if extra else ""
    big = side.get("big_games_allowed", [])
    big_html = "".join(f"<tr><td>{b['week']}</td><td>{E(b['player'])}</td><td>{E(b['team'])}</td><td>{E(b['pos'] or '')}</td><td>{b['targets']}</td><td>{b['rec']}</td><td><b>{b['yards']}</b></td><td>{b['explosive']}</td><td>{b['long']}</td></tr>" for b in big)
    return f'''<div class="tiles">{tile_html}</div>
{cov}
<h4 class="sub">Who covers: CB, S and LB who played 25%+ of snaps in weeks {", ".join(map(str, side.get("coverage_weeks", [])))}</h4>
<div class="scroll"><table class="data"><thead><tr><th>Defender</th><th>Pos</th><th>Status</th><th>Snaps last g</th><th>Tgt/g</th><th>Rec/g</th><th>Yds/g</th><th>Yds/tgt</th><th>TD / INT</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>
<p class="muted small">Typical defender (5+ games, 20+ targets, n={base.get('n')}): {num(base.get('rec_pg'))} rec, {num(base.get('yds_pg'))} yds a game, {num(base.get('ypt'))} yds/target. Highlighted rows allow 20%+ more yards than that. Allowed stats credit the nearest charted defender (PFR) and are noisy over 8 games.</p>
{extra_html}
<h4 class="sub">Receivers who reached 80+ yards against this defense</h4>
<div class="scroll"><table class="data"><thead><tr><th>Wk</th><th>Player</th><th>Team</th><th>Pos</th><th>Tgt</th><th>Rec</th><th>Yds</th><th>20+</th><th>Long</th></tr></thead><tbody>{big_html or '<tr><td colspan="9">None this season.</td></tr>'}</tbody></table></div>'''


def game_section(g, notes):
    gm = g["game"]
    gid = gm["game_id"]
    gn = notes.get(gid, {})
    imp = g.get("implied_points") or {}
    m = g.get("market") or {}
    wx = (g.get("weather") or {}).get("at_kickoff") or {}
    ctx = g.get("context") or {}
    flags = []
    for t in (gm["away"], gm["home"]):
        c = ctx.get(t, {})
        lg = c.get("last_game") or {}
        flags.append(f"<li><b>{t}</b>: {c.get('rest_days')} days rest; last game {lg.get('weekday', '')} vs {lg.get('opponent', '')} at {E(lg.get('stadium', ''))} ({lg.get('score', '')})"
                     + "".join(f" · {E(f['text'])}" for f in c.get("flags", [])) + "</li>")
    head = f'''<section class="game" id="{gid}">
<div class="ghead">
  <div><p class="eyebrow">{E(gm['weekday'])} {E(gm['date'])} · {E(gm['kickoff_et'])} ET · {E(gm['slot'])}</p>
  <h2>{E(gm['away'])} @ {E(gm['home'])}</h2></div>
  <div class="line">
    <div><span>Total</span><b>{num(m.get('total'))}</b></div>
    <div><span>Spread</span><b>{E(gm['home'])} {num(m.get('home_spread'))}</b></div>
    <div><span>Implied</span><b>{E(gm['home'])} {num(imp.get(gm['home']))} · {E(gm['away'])} {num(imp.get(gm['away']))}</b></div>
    <div><span>Kickoff weather</span><b>{wx.get('temp_f', '—')}°F · wind {num(wx.get('wind_mph'), 0)} mph · rain {wx.get('precip_chance_pct', 0)}%</b></div>
  </div>
</div>
<ul class="ctx">{''.join(flags)}<li>{E(gm['stadium_id'])} · {E(gm['roof'])} · {E(gm['surface'])}{' · division game' if gm.get('division_game') else ''}</li></ul>
{f'<div class="read"><p class="lab">The read</p>{gn.get("read", "")}</div>' if gn.get("read") else ''}'''
    body = []
    for side in g["sides"]:
        sn = gn.get(side["offense"], {})
        cards = "".join(receiver_card(r, side, sn.get("players", {}).get(r["player"])) for r in side["receivers"])
        injs = side.get("offense_injuries_own") or []
        inj_html = "; ".join(f"{E(x['player'])} ({E(x['pos'])}, {E(x['status'])})" for x in injs) or "None listed"
        body.append(f'''<div class="side">
<h3>{E(side['offense'])} passing game vs {E(side['defense'])} defense <span class="muted">· implied {num(side.get('implied'))} · projected {num(side.get('team_pass_attempts'))} pass attempts</span></h3>
<p class="small"><b>{E(side['offense'])} injuries:</b> {inj_html}</p>
{f'<p class="note">{sn["summary"]}</p>' if sn.get("summary") else ''}
<h4 class="sub">{E(side['defense'])} pass defense</h4>
{defense_block(side)}
<h4 class="sub">{E(side['offense'])} receivers</h4>
<div class="cards">{cards}</div>
</div>''')
    return head + "".join(body) + "</section>"


def history_block(h):
    if not h:
        return ""
    pre = h["pregame"]
    tb = ["<5", "5-6.5", "6.5-8", "8-9.5", "9.5+"]
    ib = ["<20", "20-24", "24-28", "28+"]
    cell = {(x["targets_pg"], x["implied"]): x for x in pre}
    rows = []
    for t in tb[1:]:
        tds = "".join((f'<td style="--v:{cell[(t, i)]["p80"] / 70:.2f}"><b>{cell[(t, i)]["p80"]:.0f}%</b><small>{cell[(t, i)]["p100"]:.0f}% · n {cell[(t, i)]["n"]}</small></td>'
                       if (t, i) in cell else "<td>—</td>") for i in ib)
        rows.append(f"<tr><th>{t}</th>{tds}</tr>")
    act = [x for x in h["actual_targets"] if x["pos"] == "WR"]
    act_te = {x["targets"]: x for x in h["actual_targets"] if x["pos"] == "TE"}
    arows = "".join(f"<tr><td>{x['targets']}</td><td>{num(x['median'], 0)}</td><td>{x['p70']:.0f}%</td><td>{x['p80']:.0f}%</td><td>{x['p100']:.0f}%</td>"
                    f"<td>{num(act_te.get(x['targets'], {}).get('median'), 0)} / {act_te.get(x['targets'], {}).get('p80', 0):.0f}%</td><td>{x['n']}</td></tr>" for x in act)
    return f'''<section class="rules" id="rules">
<h2>What it takes to reach 80</h2>
<p>Every WR and TE game from 2022 to Week 9 of 2026, after his third game of the season. Left: how often a receiver got 80+ yards, by the targets per game he came in averaging and his team&rsquo;s implied total. Right: what actually happened once he got a given number of targets in the game.</p>
<div class="two">
  <div class="scroll"><table class="heat"><caption>Chance of 80+ yards (100+ below)</caption><thead><tr><th>Targets/g coming in</th>{''.join(f'<th>Implied {i}</th>' for i in ib)}</tr></thead><tbody>{''.join(rows)}</tbody></table></div>
  <div class="scroll"><table class="data"><caption>WRs by targets in that game</caption><thead><tr><th>Targets</th><th>Median yds</th><th>70+</th><th>80+</th><th>100+</th><th>TE median / 80+</th><th>n</th></tr></thead><tbody>{arows}</tbody></table></div>
</div>
</section>'''


CSS = r"""
<title>Week 10 Receiver Breakdown</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Layout: one long scouting report; a sticky game switcher, then per game the line, the read, and each offense against the other defense. */
:root{
  --bg:#f3f5f2; --panel:#ffffff; --ink:#15201a; --muted:#5d6b62; --line:#d5ddd6;
  --turf:#1f6b45; --turf-soft:#e3efe7; --gold:#b9860b;
  --good:#1d7a46; --good-bg:#e1f2e7; --warn:#9a6500; --warn-bg:#fbf0d9; --bad:#b3362c; --bad-bg:#f8e3e0;
  --bar:#9fb3a6; --bar80:#2f8a58; --bar100:#155c36; --heat:31,107,69;
  --f-display:"Barlow Condensed","Arial Narrow",system-ui,sans-serif; --f-body:Inter,system-ui,-apple-system,"Segoe UI",sans-serif; --f-mono:"IBM Plex Mono",ui-monospace,Menlo,monospace;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --bg:#0f1512; --panel:#16201b; --ink:#e4ece6; --muted:#93a399; --line:#2a3830;
  --turf:#5fc08b; --turf-soft:#1b2d23; --gold:#e0b84a;
  --good:#6fd39a; --good-bg:#183324; --warn:#f0c062; --warn-bg:#352a12; --bad:#f08a80; --bad-bg:#3a1c19;
  --bar:#3e5246; --bar80:#4fae78; --bar100:#8fe0b2; --heat:95,192,139; color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#0f1512; --panel:#16201b; --ink:#e4ece6; --muted:#93a399; --line:#2a3830;
  --turf:#5fc08b; --turf-soft:#1b2d23; --gold:#e0b84a;
  --good:#6fd39a; --good-bg:#183324; --warn:#f0c062; --warn-bg:#352a12; --bad:#f08a80; --bad-bg:#3a1c19;
  --bar:#3e5246; --bar80:#4fae78; --bar100:#8fe0b2; --heat:95,192,139; color-scheme:dark}
body{background:var(--bg);color:var(--ink);font:14px/1.5 var(--f-body)}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:var(--panel)}
.wrap{max-width:1180px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:20px 60px;display:grid;gap:28px}
h1,h2,h3,h4{font-family:var(--f-display);letter-spacing:.01em;text-wrap:balance;margin:0}
h1{font-size:2.4rem;line-height:1.05} h2{font-size:1.9rem} h3{font-size:1.35rem;margin-top:8px} h4{font-size:1.1rem}
h4.sub{margin:18px 0 8px;color:var(--turf);text-transform:uppercase;letter-spacing:.06em;font-size:.95rem}
p{margin:0} .muted{color:var(--muted)} .small{font-size:.86rem} .eyebrow{text-transform:uppercase;letter-spacing:.08em;font-size:.75rem;color:var(--muted)}
.lab{font-size:.74rem;text-transform:uppercase;letter-spacing:.07em;color:var(--muted);margin:10px 0 4px}
nav.jump{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--panel);border-bottom:1px solid var(--line);margin:0 calc(-1*max(16px,env(safe-area-inset-left,0px)));padding:8px max(16px,env(safe-area-inset-left,0px));display:flex;gap:8px;flex-wrap:wrap}
nav.jump a{color:var(--ink);text-decoration:none;font:600 .95rem var(--f-display);letter-spacing:.04em;padding:4px 10px;border:1px solid var(--line);border-radius:4px}
nav.jump a:hover,nav.jump a:focus-visible{border-color:var(--turf);color:var(--turf);outline:none}
.intro{display:grid;gap:10px;max-width:72ch}
.chip{display:inline-block;font:500 .74rem var(--f-body);padding:2px 8px;border-radius:999px;white-space:nowrap;background:var(--turf-soft);color:var(--muted)}
.chip.good{background:var(--good-bg);color:var(--good)} .chip.warn{background:var(--warn-bg);color:var(--warn)} .chip.bad{background:var(--bad-bg);color:var(--bad)}
section.game,section.rules{display:grid;gap:14px;border-top:3px solid var(--turf);padding-top:16px}
.ghead{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;align-items:flex-end}
.line{display:flex;gap:10px;flex-wrap:wrap}
.line div{background:var(--panel);border:1px solid var(--line);padding:6px 12px;border-radius:4px;display:grid;min-width:0}
.line span,.tile span,.stat span{font-size:.72rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}
.line b{font:600 1.15rem var(--f-display);font-variant-numeric:tabular-nums}
.ctx{margin:0;padding-left:18px;font-size:.88rem;color:var(--muted)}
.read,.note{background:var(--turf-soft);padding:12px 14px;border-radius:4px;max-width:90ch}
.read p+p{margin-top:8px} .note{font-size:.9rem;margin-top:10px}
.side{display:grid;gap:4px;background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:14px 16px 18px;min-width:0}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:8px}
.tile{border:1px solid var(--line);border-radius:4px;padding:8px 10px;display:grid;gap:2px;min-width:0}
.tile b{font:600 1.3rem var(--f-display);font-variant-numeric:tabular-nums} .tile small{color:var(--muted);font-size:.76rem}
.scroll{overflow-x:auto;min-width:0}
table{border-collapse:collapse;font-variant-numeric:tabular-nums;width:100%}
caption{text-align:left;font-size:.74rem;text-transform:uppercase;letter-spacing:.07em;color:var(--muted);padding-bottom:4px}
.data th,.data td,.mini th,.mini td{padding:5px 8px;border-bottom:1px solid var(--line);text-align:right;white-space:nowrap}
.data th:first-child,.data td:first-child,.mini th:first-child,.mini td:first-child{text-align:left}
.data td:nth-child(2){text-align:left}
.data thead th,.mini thead th{font-size:.72rem;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);font-weight:500}
.mini{font-size:.82rem}
tr.hot td{background:var(--warn-bg)}
.cards{display:grid;grid-template-columns:1fr;gap:12px}
.rc{border:1px solid var(--line);border-radius:6px;padding:12px 14px;display:grid;gap:8px;min-width:0;background:var(--bg)}
.rc header{display:flex;justify-content:space-between;gap:8px;align-items:flex-start;flex-wrap:wrap}
.rc h4{font-size:1.35rem}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(92px,1fr));gap:6px}
.stat{display:grid;border-left:2px solid var(--turf);padding-left:8px;min-width:0}
.stat b{font:600 1.15rem var(--f-display);font-variant-numeric:tabular-nums}
.rc-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr));gap:12px}
.rc-col>*{min-width:0} .rc-col{min-width:0;display:grid;gap:4px;align-content:start}
.bars{width:100%;height:auto;max-width:100%}
.bars .b{fill:var(--bar)} .bars .b80{fill:var(--bar80)} .bars .b100{fill:var(--bar100)}
.bars .ref{stroke:var(--gold);stroke-dasharray:4 3;stroke-width:1} .bars .reflab{fill:var(--gold);font:10px var(--f-mono)}
.bars .exdot{fill:var(--gold)} .bars .xlab{fill:var(--muted);font:9px var(--f-mono)}
.hits{display:flex;gap:10px;flex-wrap:wrap;font-size:.82rem} .hit b{font-family:var(--f-mono)}
.two{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr));gap:16px}
.heat th,.heat td{padding:6px 8px;border:1px solid var(--line);text-align:center}
.heat td{background:rgba(var(--heat),calc(var(--v,0)*.55))} .heat td b{display:block;font:600 1.1rem var(--f-display)} .heat td small{color:var(--muted);font-size:.72rem}
.heat thead th{font-size:.72rem;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);font-weight:500}
.foot{font-size:.82rem;color:var(--muted);max-width:90ch;display:grid;gap:6px}
@media (prefers-reduced-motion: no-preference){html{scroll-behavior:smooth}}
</style>
"""


def render(data, notes):
    games = data["games"]
    nav = "".join(f'<a href="#{g["game"]["game_id"]}">{E(g["game"]["away"])} @ {E(g["game"]["home"])}</a>' for g in games) + '<a href="#rules">What it takes to reach 80</a>'
    intro = notes.get("_intro", "")
    foot = notes.get("_foot", "")
    return (CSS + f'''<div class="wrap">
<nav class="jump" aria-label="Jump to">{nav}</nav>
<header class="intro"><p class="eyebrow">Week 10 · Research only, not graded against prop prices</p><h1>Week 10 Receiver Breakdown</h1>{intro}</header>
{''.join(game_section(g, notes) for g in games)}
{history_block(data.get('history'))}
<footer class="foot">{foot}<p>Built {E(data.get('generated_utc', ''))} UTC from the board data in the repo.</p></footer>
</div>''')


def main(argv):
    data = json.loads(Path(argv[0]).read_text())
    notes = json.loads(Path(argv[1]).read_text()) if len(argv) > 1 and Path(argv[1]).exists() else {}
    out = Path(argv[2] if len(argv) > 2 else "breakdown.html")
    out.write_text(render(data, notes))
    print(out)


if __name__ == "__main__":
    main(sys.argv[1:])
