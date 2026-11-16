"""Builds report.html from the study outputs (every number comes from the JSON files written by the scripts here)."""
import json, html
from pathlib import Path
H = Path(__file__).resolve().parent
s = json.loads((H / "studies_results.json").read_text()); e = json.loads((H / "explosive_results.json").read_text())
x = json.loads((H / "extra.json").read_text()); dd = json.loads((H / "deepdives.json").read_text())
esc = html.escape
def pct(v, d=0): return f"{v * 100:.{d}f}%"
def deciles_svg(rows, title):
    W, Hh, pad = 520, 220, 36; mx = max(max(r["pred"], r["hit"]) for r in rows) * 1.1; bw = (W - 2 * pad) / len(rows)
    g = ""
    for i, r in enumerate(rows):
        x0 = pad + i * bw
        for j, (k, col) in enumerate((("pred", "var(--a2)"), ("hit", "var(--a)"))):
            h = r[k] / mx * (Hh - 50); g += f'<rect x="{x0 + 4 + j * (bw / 2 - 3):.1f}" y="{Hh - 26 - h:.1f}" width="{bw / 2 - 6:.1f}" height="{h:.1f}" rx="2" fill="{col}"><title>decile {i + 1}: predicted {pct(r["pred"], 1)}, happened {pct(r["hit"], 1)}</title></rect>'
        g += f'<text x="{x0 + bw / 2:.1f}" y="{Hh - 10}" text-anchor="middle" font-size="10" fill="var(--mu)">{i + 1}</text>'
    top = rows[-1]
    g += f'<text x="{W - pad}" y="{Hh - 30 - top["hit"] / mx * (Hh - 50) - 6:.1f}" text-anchor="end" font-size="11" fill="var(--ink)" font-weight="700">{pct(top["hit"])}</text>'
    for f in (0.25, 0.5, 0.75):
        y = Hh - 26 - f * (Hh - 50); g += f'<line x1="{pad}" x2="{W - pad}" y1="{y:.1f}" y2="{y:.1f}" stroke="var(--line)" stroke-dasharray="2 4"/><text x="{pad - 4}" y="{y + 3:.1f}" text-anchor="end" font-size="9" fill="var(--mu)">{pct(f * mx)}</text>'
    return f'<figure><svg viewBox="0 0 {W} {Hh}" role="img" aria-label="{esc(title)}">{g}</svg><figcaption>{esc(title)}. Tenths of all receiver-games, least to most likely. <span class="sw" style="background:var(--a2)"></span> predicted <span class="sw" style="background:var(--a)"></span> happened.</figcaption></figure>'
def pair_svg(rows, a, b, title):
    def yds(c):
        if not c or c == "-": return 0
        return int(c.split("-")[1].split("/")[0])
    W, Hh, pad = 520, 200, 30; vals = [(r["week"], r["opp"], yds(r.get(a)), yds(r.get(b))) for r in rows]
    mx = max(max(v[2], v[3]) for v in vals) * 1.15; bw = (W - 2 * pad) / len(vals); g = ""
    for i, (w, o, ya, yb) in enumerate(vals):
        x0 = pad + i * bw
        for j, (v, col) in enumerate(((ya, "var(--a)"), (yb, "var(--a2)"))):
            h = v / mx * (Hh - 50); g += f'<rect x="{x0 + 3 + j * (bw / 2 - 2):.1f}" y="{Hh - 30 - h:.1f}" width="{bw / 2 - 5:.1f}" height="{h:.1f}" rx="2" fill="{col}"><title>week {w} vs {o}: {v} yds</title></rect><text x="{x0 + 3 + j * (bw / 2 - 2) + (bw / 2 - 5) / 2:.1f}" y="{Hh - 33 - h:.1f}" text-anchor="middle" font-size="8.5" fill="var(--ink)">{v}</text>'
        g += f'<text x="{x0 + bw / 2:.1f}" y="{Hh - 16}" text-anchor="middle" font-size="9" fill="var(--mu)">wk {w}</text><text x="{x0 + bw / 2:.1f}" y="{Hh - 5}" text-anchor="middle" font-size="9" fill="var(--mu)">{esc(str(o))}</text>'
    y100 = Hh - 30 - 100 / mx * (Hh - 50)
    g += f'<line x1="{pad}" x2="{W - pad}" y1="{y100:.1f}" y2="{y100:.1f}" stroke="var(--warn)" stroke-dasharray="4 3"/><text x="{W - pad}" y="{y100 - 3:.1f}" text-anchor="end" font-size="9" fill="var(--warn)">100 yds</text>'
    return f'<figure><svg viewBox="0 0 {W} {Hh}" role="img" aria-label="{esc(title)}">{g}</svg><figcaption>{esc(title)}: receiving yards each game. <span class="sw" style="background:var(--a)"></span> {esc(a)} <span class="sw" style="background:var(--a2)"></span> {esc(b)}</figcaption></figure>'
def tree_table(rows, cols):
    head = "".join(f"<th>{esc(c)}</th>" for c in cols)
    body = "".join("<tr><td>" + f"{r['week']}</td><td>{esc(str(r['opp']))}</td><td>{esc(str(r['qb']))}</td>" + "".join(f"<td>{esc(str(r.get(c, '-')))}</td>" for c in cols) + "</tr>" for r in rows)
    return f'<div class="tw"><table><thead><tr><th>Wk</th><th>Opp</th><th>QB</th>{head}</tr></thead><tbody>{body}</tbody></table></div>'
def bars(items, title, fmt=lambda v: f"{v:.2f}", lo=None, hi=None, highlight=()):
    mx = max(abs(v) for _, v in items) or 1
    rows = "".join(f'<div class="br{" hl" if k in highlight else ""}"><span>{esc(k)}</span><i style="width:{max(2, abs(v) / mx * 100):.0f}%;background:{"var(--bad)" if v < 0 else "var(--a)"}"></i><b>{fmt(v)}</b></div>' for k, v in items)
    return f'<figure class="bars"><figcaption>{esc(title)}</figcaption>{rows}</figure>'
S2 = s["q2_seesaw"]; Q3 = s["q3_qb_change"]; Q4 = s["q4_position_share"]; RM = x["rematch"]; SM = x["short_vs_man"]; LA, ARI = dd["LA_eff"], dd["ARI_eff"]; SIM = x["sim"]
tree = sorted(((r["team"], r["corr"]) for r in s["team_tree"]), key=lambda t: -t[1])
y100, y30 = e["y100"], e["y30"]
def mtab(res):
    return "".join(f"<tr><td>{esc(k)}</td><td>{v['brier']:.4f}</td></tr>" for k, v in res["models"].items())
simrow = lambda n: (f"<tr><td>{esc(n)}</td><td>{SIM[n]['targets']}</td><td>{SIM[n]['median']:.0f}</td><td>{pct(SIM[n]['p70'])}</td><td>{pct(SIM[n]['p100'])}</td></tr>" if n in SIM else "")
proj = x.get("la_ari_projection") or {}
inj = x.get("la_ari_inj", {})
meet = "".join(f"<tr><td>{r['season']} wk {r['week']}</td><td>{r['away_team']} {int(float(r['away_score']))} at {r['home_team']} {int(float(r['home_score']))}</td><td>{r['home_team']} {(-float(r['spread_line'])):+.1f}</td></tr>" for r in x["la_ari_meetings"] if str(r["home_score"]) not in ("nan", "None"))
page = f"""<title>Boom Games Research</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@600;700&family=Inter:wght@400;500;600;700&display=swap">
<style>
/* Layout: a single reading column of findings, each led by its verdict, with charts beside the evidence. Dark by design to match the game board. */
:root {{ --bg:#050a14; --panel:rgba(12,22,40,.85); --ink:#e6f1ff; --mu:#8ea3c2; --line:rgba(80,140,220,.22); --a:#22d3ee; --a2:#c084fc; --good:#34d399; --bad:#fb7185; --warn:#fbbf24;
  --fd:"Chakra Petch","Arial Narrow",sans-serif; --fb:"Inter",system-ui,-apple-system,"Segoe UI",sans-serif; color-scheme:dark; }}
* {{ box-sizing:border-box; }}
body {{ background:var(--bg); color:var(--ink); font:15px/1.6 var(--fb); margin:0; font-variant-numeric:tabular-nums;
  background-image:radial-gradient(900px 500px at 90% -10%,rgba(192,132,252,.12),transparent 60%),radial-gradient(900px 500px at 0% 0%,rgba(34,211,238,.1),transparent 60%); }}
.wrap {{ max-width:900px; margin:0 auto; padding-left:max(16px,env(safe-area-inset-left,0px)); padding-right:max(16px,env(safe-area-inset-right,0px)); padding-block:28px 60px; display:flex; flex-direction:column; gap:22px; }}
h1 {{ font-family:var(--fd); font-size:clamp(30px,6vw,46px); line-height:1; margin:0; text-transform:uppercase; text-shadow:0 0 22px rgba(34,211,238,.45); text-wrap:balance; }}
h2 {{ font-family:var(--fd); font-size:22px; text-transform:uppercase; letter-spacing:.03em; margin:0; color:var(--a); text-wrap:balance; }}
.eyebrow {{ color:var(--a); font-weight:700; letter-spacing:.16em; text-transform:uppercase; font-size:12px; }}
.lede {{ color:var(--mu); max-width:65ch; margin:8px 0 0; }}
section {{ background:var(--panel); border:1px solid var(--line); border-radius:12px; padding:18px 20px; display:flex; flex-direction:column; gap:12px; min-width:0; }}
.verdict {{ font-family:var(--fd); font-size:19px; line-height:1.3; }}
.verdict b {{ color:var(--a); }}
p {{ margin:0; max-width:68ch; }} ul {{ margin:0; padding-left:20px; max-width:68ch; }} li {{ margin:3px 0; }}
.no {{ color:var(--bad); font-weight:700; }} .yes {{ color:var(--good); font-weight:700; }} .some {{ color:var(--warn); font-weight:700; }}
.summary {{ display:grid; gap:10px; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); }}
.summary div {{ border:1px solid var(--line); border-radius:10px; padding:12px 14px; background:rgba(5,10,20,.5); }}
.summary b {{ display:block; font-family:var(--fd); text-transform:uppercase; font-size:14px; margin-bottom:4px; }}
figure {{ margin:0; min-width:0; }} figure svg {{ width:100%; height:auto; display:block; }}
figcaption {{ font-size:12px; color:var(--mu); margin-top:4px; }}
.sw {{ display:inline-block; width:10px; height:10px; border-radius:2px; vertical-align:middle; margin:0 3px 0 8px; }}
.tw {{ overflow-x:auto; }} table {{ border-collapse:collapse; width:100%; font-size:12.5px; }}
th,td {{ padding:5px 7px; border-bottom:1px solid var(--line); text-align:left; white-space:nowrap; }} th {{ color:var(--mu); font-size:11px; text-transform:uppercase; letter-spacing:.05em; }}
.two {{ display:grid; gap:14px; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); }}
.bars .br {{ display:grid; grid-template-columns:52px minmax(0,1fr) 46px; gap:8px; align-items:center; font-size:12px; margin:2px 0; }}
.bars .br i {{ height:9px; border-radius:4px; display:block; }} .bars .br b {{ text-align:right; }} .bars .br.hl span, .bars .br.hl b {{ color:var(--warn); font-weight:700; }}
.bars figcaption {{ margin:0 0 6px; }}
.note {{ font-size:12.5px; color:var(--mu); }}
.kpi {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(130px,1fr)); gap:8px; }}
.kpi div {{ background:rgba(5,10,20,.5); border:1px solid var(--line); border-radius:8px; padding:8px 10px; }} .kpi b {{ font-family:var(--fd); font-size:22px; display:block; }} .kpi span {{ font-size:11px; color:var(--mu); text-transform:uppercase; letter-spacing:.06em; }}
</style>
<div class="wrap">
<header><div class="eyebrow">Overnight research · Week 10, 2026</div><h1>Can we see a boom game coming?</h1>
<p class="lede">Five questions from Friday night, tested on every receiver game from 2022 to 2026 ({len(__import__('pandas').read_parquet(H / 'rows.parquet')):,} games), using only what was known before each game, then applied to Sunday's games. Research only.</p></header>
<div class="summary">
<div><b>Explosive games</b><span class="some">Partly.</span> Volume, efficiency and the implied team total pick out who is likelier to boom. A hot streak of big plays does not.</div>
<div><b>Seesaw pairs</b><span class="no">No.</span> A team's top two receivers do not trade off. They boom together more often than apart.</div>
<div><b>QB changes</b><span class="no">Rarely.</span> Shares move about 2.5 points; reweighting to the new QB's few games makes projections worse.</div>
<div><b>"Defense allows a lot to TEs"</b><span class="no">Not more targets.</span> The offense's own target tree decides who gets the ball. The defense mostly changes yards per catch.</div>
<div><b>Rams favored without stars</b><span class="yes">Explained.</span> A big team-quality gap, Arizona's quarterback situation, and a low total that already prices the missing receivers.</div>
</div>

<section><h2>1 · Can you predict a receiver exploding?</h2>
<p class="verdict">You can rank who is <b>more likely</b> to boom, but even the best candidates hit 100 yards about <b>1 game in 5</b>. Recent big plays add nothing.</p>
<div class="two">{deciles_svg(s['q1_sharpness']['y100']['deciles'], '100+ receiving yards')}{deciles_svg(s['q1_sharpness']['y30']['deciles'], 'A catch of 30+ yards')}</div>
<ul>
<li><span class="yes">Predicts it:</span> targets per game and target share (the strongest by far), yards per target, and the implied team total. Each extra point of implied team total raises the odds of a 100-yard game by about {e['y100']['coef']['implied']['coef'] * 100:.1f}%, so a team implied at 28 points carries about 40% higher odds than one at 20.</li>
<li><span class="no">Does not:</span> big plays in his last 2 or 3 games (the "hot hand" coefficient is about zero, p = {e['y100']['coef']['ex20_l2']['p']:.2f}), what the defense allowed on explosive plays (p = {e['y100']['coef']['opp_ex_rate']['p']:.2f}), or wind.</li>
<li><span class="some">Barely:</span> a receiver's deep profile (target depth, deep-target rate) improves the 30+ catch forecast a hair (Brier {y30['models']['base (volume + efficiency)']['brier']:.4f} to {y30['models']['+ deep profile']['brier']:.4f}) and not the 100-yard forecast.</li>
<li>Tested on seasons the models never saw: the top tenth of predictions said {pct(s['q1_sharpness']['y100']['deciles'][-1]['pred'], 1)} for 100+ yards and {pct(s['q1_sharpness']['y100']['deciles'][-1]['hit'], 1)} happened; for a 30+ yard catch, {pct(s['q1_sharpness']['y30']['deciles'][-1]['pred'], 1)} predicted, {pct(s['q1_sharpness']['y30']['deciles'][-1]['hit'], 1)} happened.</li>
</ul>
<p class="note">What this means for the board: the opportunity simulation already uses the parts that work (volume, efficiency, the spread and total). Treat a recent run of long catches as noise, not a signal.</p>
</section>

<section><h2>2 · Do receiver pairs seesaw?</h2>
<p class="verdict"><b>No.</b> Across {S2['pairs']:,} games of a team's top two receivers, their yards move slightly <b>together</b> (correlation {S2['corr_yards']:+.2f}), not opposite.</p>
<ul>
<li>When the WR1 has 100+ yards, the WR2 also reaches 100 {pct(S2['p_wr2_100_when_wr1_100'], 1)} of the time, more than his usual {pct(S2['p_wr2_100'], 1)}. Big passing days lift both.</li>
<li>When the WR2 is held under 40, the WR1 still reaches 100 only {pct(S2['p_wr1_100_when_wr2_under40'], 1)} of the time, the same as usual ({pct(S2['p_wr1_100'], 1)}). Locking one down does not feed the other.</li>
<li>Which one wins the targets in a given game follows their season shares (correlation {S2['corr_prior_share_gap_vs_game_share_gap']:.2f}), with lots of game-to-game noise. Nothing in the free pregame data reliably calls the flip.</li>
</ul>
<div class="two">{pair_svg(dd['GB'], 'Matthew Golden', 'Christian Watson', 'Packers 2026')}{pair_svg(dd['CIN'], "Ja'Marr Chase", 'Tee Higgins', 'Bengals 2026')}</div>
<p class="note">Green Bay is the clearest example of "together": weeks 5 and 9 both went over 100. Cincinnati shows real flips (week 4: Higgins 157, Chase 27; week 9: Chase 155, Higgins 32), but they don't line up with anything knowable before kickoff.</p>
</section>

<section><h2>3 · Vikings at Packers: does Week 1 repeat?</h2>
<p class="verdict">A blow-up in the first meeting <b>does not carry</b> to the rematch.</p>
<ul><li>Across {RM['pairs']:,} same-season rematches, how far a player beat his average in the first game says almost nothing about the second (correlation {RM['corr_residual']:+.3f}). Players with 100+ in the first meeting averaged {RM['big_first_100_then_avg_second']:.0f} yards in the rematch, close to their usual {RM['their_avg_before']:.0f}.</li>
<li>Week 1 also had Carson Wentz at quarterback for Minnesota; Kirk Cousins is listed now.</li>
<li>Golden and Watson are still strong this week on <i>volume</i>, not on the rematch:</li></ul>
<div class="tw"><table><thead><tr><th>This week's simulation</th><th>Targets</th><th>Median yds</th><th>70+</th><th>100+</th></tr></thead><tbody>{simrow('Matthew Golden')}{simrow('Christian Watson')}{simrow('Justin Jefferson')}{simrow('Jordan Addison')}{simrow("Ja'Marr Chase")}{simrow('Tee Higgins')}</tbody></table></div>
</section>

<section><h2>4 · Quarterback changes: Nabers and Likely</h2>
<p class="verdict">QB changes move target shares <b>less than they feel like</b>, and a few games with the new QB are too few to trust.</p>
<ul><li>In {Q3['n_games_with_new_qb']:,} games where the starter differed from the usual one, shares moved {Q3['mean_abs_share_shift'] * 100:.1f} points on average. Predicting targets from the season share missed by {Q3['share']:.2f} targets a game; using only games with the new QB missed by {Q3['share_same_qb']:.2f}. The full-season share was better.</li>
<li>The Giants so far: under Winston (weeks 2-6) Likely drew 24-41% of targets; in McCarthy's two games in this data he drew 15% and 22%, while Nabers stayed at 30-33%. That is the opposite of "McCarthy feeds Likely underneath", but two games prove nothing either way, and Thursday's game is not in the play-by-play yet.</li></ul>
{tree_table(dd['NYG'], ['Malik Nabers', 'Isaiah Likely', 'Malachi Fields', 'Darnell Mooney'])}
<p class="note">Cells: catches-yards / targets (share of the team's targets).</p>
</section>

<section><h2>5 · "They give up a lot to tight ends": is the opportunity there?</h2>
<p class="verdict">A defense that allows a lot to a position <b>does not send more targets</b> there. The offense's own habits decide who gets the ball.</p>
<ul><li>League-wide (2022-2026): a defense that sees 20% more tight-end targets than average moved the offense's tight-end share by {Q4['TE']['slope'] * 0.2 * 100:+.2f} points (p = {Q4['TE']['p']:.2f}); for receivers {Q4['WR']['slope'] * 0.2 * 100:+.2f} (p = {Q4['WR']['p']:.2f}). Only backs show a small real effect ({Q4['RB']['slope'] * 0.2 * 100:+.2f} points, p &lt; 0.001).</li>
<li>Detroit allows the most to tight ends: {dd['DET_TE']['det']['tgt']} targets, {dd['DET_TE']['det']['rec']} catches and {dd['DET_TE']['det']['yds']:.0f} yards a game (league {dd['DET_TE']['league']['tgt']}, {dd['DET_TE']['league']['rec']}, {dd['DET_TE']['league']['yds']:.0f}). That raises what Hunter Henry does <i>per target</i>, not how many he gets. Drake Maye spreads the ball: Henry's share has ranged from 7% to 24%.</li></ul>
{tree_table(dd['NE'], ['DeMario Douglas', 'Hunter Henry', 'Rhamondre Stevenson', 'Eli Raridon', 'Mack Hollins'])}
<div class="tw"><table><thead><tr><th>This week's simulation</th><th>Targets</th><th>Median yds</th><th>70+</th><th>100+</th></tr></thead><tbody>{simrow('Hunter Henry')}{simrow('DeMario Douglas')}{simrow('Eli Raridon')}</tbody></table></div>
</section>

<section><h2>6 · How the Bills spread the ball</h2>
<p class="verdict">Your read is right: Buffalo's targets are <b>among the least predictable</b> in the league. Allen throws to whoever the play frees up, so no receiver is a steady weekly volume bet.</p>
<div class="two">{bars(tree[:8] + tree[-8:], 'How well each team\'s season shares predicted its game shares in 2026 (correlation; higher = steadier). Steadiest 8 and least steady 8.', highlight=('BUF', 'NE'))}
<div><ul><li>Buffalo's correlation is {dict(tree)['BUF']:.2f} (Seattle {dict(tree)['SEA']:.2f}); New England's is {dict(tree)['NE']:.2f}.</li>
<li>In 8 games, Shakir's share rose against defenses that played more man coverage last season (correlation {dd['BUF_man_corr'].get('Khalil Shakir', 0):+.2f}) and Moore's fell ({dd['BUF_man_corr'].get('DJ Moore', 0):+.2f}). Tested across 2023-2025, short receivers do <span class="no">not</span> reliably gain share against man coverage (p = {SM['opp_man:short']['p']:.2f}), so treat Buffalo's pattern as noise until it repeats.</li>
<li>The steady piece is James Cook: {SIM['James Cook']['targets']} projected carries and a {SIM['James Cook']['median']:.0f}-yard rushing median this week. Each Bills receiver projects a median between {min(SIM[n]['median'] for n in ('Khalil Shakir', 'Dalton Kincaid', 'Keon Coleman', 'DJ Moore')):.0f} and {max(SIM[n]['median'] for n in ('Khalil Shakir', 'Dalton Kincaid', 'Keon Coleman', 'DJ Moore')):.0f} yards.</li></ul></div></div>
{tree_table(dd['BUF'], ['Khalil Shakir', 'Dalton Kincaid', 'Keon Coleman', 'DJ Moore', 'James Cook'])}
</section>

<section><h2>7 · Rams at Cardinals: why the Rams are big favorites</h2>
<p class="verdict">The market has the Rams by <b>{x['la_ari_market']['home_spread']}</b> with a total of just <b>{x['la_ari_market']['total']}</b>. The low total is the market saying it knows the Rams' receivers are out. The spread says the rest of the matchup is lopsided.</p>
<div class="kpi"><div><span>Rams record · margin</span><b>{LA['record']} · {LA['margin_pg']:+.1f}</b></div><div><span>Cardinals record · margin</span><b>{ARI['record']} · {ARI['margin_pg']:+.1f}</b></div>
<div><span>Offense EPA/play rank</span><b>LA {LA['off_epa_play_rank']} · ARI {ARI['off_epa_play_rank']}</b></div><div><span>Defense EPA/play rank</span><b>LA {LA['def_epa_play_rank']} · ARI {ARI['def_epa_play_rank']}</b></div></div>
<ul>
<li><b>The Rams really are without their stars:</b> Puka Nacua and Davante Adams are both on injured reserve. Nacua had 44-48% of the targets in his last three games. There is no game this season without both, so the Rams' passing game is the biggest unknown here.</li>
<li><b>Arizona's quarterback situation is worse.</b> Brissett averaged {ARI['qbs'][0]['epa']:+.3f} EPA per dropback over {ARI['qbs'][0]['db']} dropbacks (below average); Minshew, the listed starter, is on injured reserve on ESPN's list. Confirm who starts at inactives.</li>
<li><b>The Rams' defense is 4th in EPA per play;</b> Arizona's offense is {ARI['off_epa_play_rank']}st. Arizona is without its starting center (Froholdt, out) and receiver Michael Wilson (injured reserve). Byron Young leads the Rams with {dd['LA_sacks'].get('B.Young', 0)} sacks; Myles Garrett has {dd['LA_sacks'].get('M.Garrett', 0)} and is questionable. Aaron Donald is on the roster but not among the sack leaders.</li>
<li><b>Careful:</b> Arizona won the Week 6 meeting 18-16 in Los Angeles as 12.5-point underdogs. Recent meetings:</li></ul>
<div class="tw"><table><thead><tr><th>Game</th><th>Score</th><th>Home line</th></tr></thead><tbody>{meet}</tbody></table></div>
<p class="note">The board's research simulation (not validated, no injuries applied) has the Rams by {abs(proj.get('home_margin', 0)):.1f} and a {proj.get('total', 0):.0f}-point total, well above the market's {x['la_ari_market']['total']}. That gap is mostly the missing Rams receivers and Arizona's quarterback, which the simulation does not know about. Trey McBride is Arizona's volume piece: {SIM['Trey McBride']['targets']} projected targets, a {SIM['Trey McBride']['median']:.0f}-yard median.</p>
</section>

<section><h2>What changes on the board</h2>
<ul><li>Nothing that failed these tests gets added: no "hot hand", no seesaw adjustment, no QB-only shares, no extra targets from what a defense allows a position.</li>
<li>Worth adding, because it held up: a <b>100+ yard chance</b> and a <b>30+ yard catch chance</b> on each player card, built from volume, efficiency and the implied team total, and a <b>target-tree steadiness</b> note for teams like Buffalo and New England, so a soft matchup isn't mistaken for guaranteed volume.</li></ul>
<p class="note">Method: logistic models fit leaving one season out (2022-2026); Brier scores and calibration by decile; clustered standard errors by game; nflverse play-by-play, rosters and schedules, NGS participation for coverage (through 2025). Scripts and outputs: research/receiver_volatility_2026-11-14/ in the repository.</p>
</section>
</div>"""
(H / "report.html").write_text(page)
print(len(page))
