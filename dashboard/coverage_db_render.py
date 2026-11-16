"""Render the coverage database (dashboard.coverage_db) as one page.

    python3 -m dashboard.coverage_db_render dashboard/results/coverage_db_2026.json out.html [extra_week.json] [value.json]

extra_week.json: optional list of receiver entries in the `week` format for games not in the play-by-play file yet.
value.json: optional research/coverage_db_*/value_results.json, shown as "does this move the projection".
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

CSS = r"""
<title>Coverage Database</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Layout: a lookup tool. Who got beat this week first, then a filterable table of every defender, then every defense. */
:root{
  --bg:#f3f5f2; --panel:#ffffff; --ink:#15201a; --muted:#5d6b62; --line:#d5ddd6;
  --turf:#1f6b45; --turf-soft:#e3efe7; --gold:#a87a08;
  --good:#1d7a46; --good-bg:#e1f2e7; --warn:#9a6500; --warn-bg:#fbf0d9; --bad:#b3362c; --bad-bg:#f8e3e0;
  --f-display:"Barlow Condensed","Arial Narrow",system-ui,sans-serif; --f-body:Inter,system-ui,-apple-system,"Segoe UI",sans-serif; --f-mono:"IBM Plex Mono",ui-monospace,Menlo,monospace;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --bg:#0f1512; --panel:#16201b; --ink:#e4ece6; --muted:#93a399; --line:#2a3830;
  --turf:#5fc08b; --turf-soft:#1b2d23; --gold:#e0b84a;
  --good:#6fd39a; --good-bg:#183324; --warn:#f0c062; --warn-bg:#352a12; --bad:#f08a80; --bad-bg:#3a1c19; color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#0f1512; --panel:#16201b; --ink:#e4ece6; --muted:#93a399; --line:#2a3830;
  --turf:#5fc08b; --turf-soft:#1b2d23; --gold:#e0b84a;
  --good:#6fd39a; --good-bg:#183324; --warn:#f0c062; --warn-bg:#352a12; --bad:#f08a80; --bad-bg:#3a1c19; color-scheme:dark}
body{background:var(--bg);color:var(--ink);font:14px/1.5 var(--f-body)}
.wrap{max-width:1180px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:24px 64px;display:grid;gap:30px}
h1,h2,h3{font-family:var(--f-display);letter-spacing:.01em;text-wrap:balance;margin:0}
h1{font-size:2.5rem;line-height:1.02} h2{font-size:1.8rem} h3{font-size:1.25rem}
p{margin:0;max-width:78ch} .muted{color:var(--muted)} .small{font-size:.85rem}
.eyebrow{text-transform:uppercase;letter-spacing:.08em;font-size:.74rem;color:var(--muted)}
section{display:grid;gap:14px;border-top:3px solid var(--turf);padding-top:16px;min-width:0}
.lead{display:grid;gap:10px}
.callout{background:var(--turf-soft);border-radius:6px;padding:12px 14px;display:grid;gap:6px}
.scroll{overflow-x:auto;min-width:0}
table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums;font-size:.88rem}
th,td{padding:5px 9px;border-bottom:1px solid var(--line);text-align:right;white-space:nowrap}
th:first-child,td:first-child{text-align:left} td.l,th.l{text-align:left}
thead th{font-size:.7rem;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);font-weight:500;cursor:default}
thead th[data-k]{cursor:pointer} thead th[data-k]:hover,thead th[aria-sort]{color:var(--turf)}
tr.hot td{background:var(--warn-bg)}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,540px),1fr));gap:12px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:12px 14px;display:grid;gap:8px;align-content:start;min-width:0}
.card header{display:flex;justify-content:space-between;gap:8px;align-items:baseline;flex-wrap:wrap}
.card h3 span{color:var(--muted);font:500 .8rem var(--f-body)}
.line{font:600 1.5rem var(--f-display);font-variant-numeric:tabular-nums}
.chip{display:inline-block;font:500 .72rem var(--f-body);padding:2px 8px;border-radius:999px;background:var(--turf-soft);color:var(--muted);white-space:nowrap}
.chip.bad{background:var(--bad-bg);color:var(--bad)} .chip.good{background:var(--good-bg);color:var(--good)} .chip.warn{background:var(--warn-bg);color:var(--warn)}
.controls{display:flex;gap:10px;flex-wrap:wrap;align-items:end}
label{display:grid;gap:3px;font-size:.76rem;color:var(--muted)}
input,select{font:500 .95rem var(--f-body);padding:6px 8px;border:1px solid var(--line);border-radius:4px;background:var(--panel);color:var(--ink);min-width:0}
input:focus-visible,select:focus-visible{outline:2px solid var(--turf);outline-offset:1px}
details{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:8px 12px}
summary{cursor:pointer;font-weight:600}
.two{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,400px),1fr));gap:16px}
.foot{font-size:.83rem;color:var(--muted);display:grid;gap:6px}
</style>
"""

JS = r"""
<script>
(function(){
  var D = JSON.parse(document.getElementById('cov-data').textContent);
  var $ = function(id){return document.getElementById(id)};
  var esc = function(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})};
  var n = function(x,d){return x==null?'–':(typeof x==='number'?x.toFixed(d==null?1:d):x)};
  // ---- this week's cards
  $('week').innerHTML = D.week.map(function(w){
    var rows = w.by_defender.slice(0,5).map(function(b){
      var s = b.season || {};
      var hot = s.g70>=2 || (s.yds_pg||0)>=40;
      return '<tr class="'+(hot?'hot':'')+'"><td>'+esc(b.defender)+(b.pos?' <span class="muted">'+esc(b.pos)+'</span>':'')+'</td><td>'+b.catches+'</td><td><b>'+b.yards+'</b></td><td>'+b.long+'</td><td>'+n(s.yds_pg)+'</td><td>'+n(s.ypt)+'</td><td>'+(s.g70==null?'–':s.g70+'/'+s.games)+'</td><td>'+n(s.explosive_ended,0)+'</td></tr>';
    }).join('');
    var db = w.defense_before || {};
    return '<article class="card"><header><h3>'+esc(w.receiver)+' <span>'+esc(w.pos)+' · '+esc(w.team)+' vs '+esc(w.defense)+'</span></h3>'+
      '<span class="chip '+(db.g80/db.games>=0.75?'bad':db.g80/db.games<=0.35?'good':'')+'">'+esc(w.defense)+' had allowed '+db.g80+' receivers 80+ in '+db.games+' games</span></header>'+
      '<div class="line">'+w.rec+' catches, '+w.yards+' yards <span class="muted small">on '+w.targets+' targets · '+w.explosive+' of 20+</span></div>'+
      '<div class="scroll"><table><thead><tr><th>Defender who finished the catch</th><th>Rec</th><th>Yds</th><th>Long</th><th>His yds/g</th><th>Yds/tgt</th><th>70+ games</th><th>20+ ended</th></tr></thead><tbody>'+rows+'</tbody></table></div>'+
      (w.note?'<p class="small muted">'+esc(w.note)+'</p>':'')+'</article>';
  }).join('');
  // ---- defenders table
  var teams = Object.keys(D.teams).sort();
  $('f-team').innerHTML = '<option value="">All teams</option>'+teams.map(function(t){return '<option>'+t+'</option>'}).join('');
  var sortK = 'yds_pg', sortDir = -1;
  var cols = [['player','Defender',1],['team','Team',1],['pos','Pos',1],['games','G'],['last_snap_pct','Snaps last g'],['tgt_pg','Tgt/g'],['rec_pg','Rec/g'],['yds_pg','Yds/g'],['ypt','Yds/tgt'],['cmp_pct','Catch %'],['td','TD'],['g50','50+ g'],['g70','70+ g'],['g100','100+ g'],['worst','Worst'],['explosive_ended','20+ ended'],['n_big_games','Big games']];
  function drawDef(){
    var q = $('f-q').value.trim().toLowerCase(), tm = $('f-team').value, ps = $('f-pos').value, mg = +$('f-games').value||0;
    var rows = D.defenders.filter(function(r){return (!q||r.player.toLowerCase().indexOf(q)>=0)&&(!tm||r.team===tm)&&(!ps||r.pos===ps)&&r.games>=mg});
    rows.sort(function(a,b){var x=a[sortK],y=b[sortK]; if(x==null)return 1; if(y==null)return -1; return (x>y?1:x<y?-1:0)*sortDir});
    $('def-count').textContent = rows.length+' defenders';
    $('def-head').innerHTML = cols.map(function(c){return '<th data-k="'+c[0]+'"'+(c[2]?' class="l"':'')+(c[0]===sortK?' aria-sort="'+(sortDir<0?'descending':'ascending')+'"':'')+'>'+c[1]+(c[0]===sortK?(sortDir<0?' ▼':' ▲'):'')+'</th>'}).join('');
    $('def-body').innerHTML = rows.slice(0,150).map(function(r){
      var hot = r.g70>=2 || (r.yds_pg>=45 && r.games>=5);
      return '<tr class="'+(hot?'hot':'')+'">'+cols.map(function(c){
        var v = r[c[0]];
        if(c[0]==='worst') v = r.worst+(r.worst_opp?' <span class="muted">wk '+r.worst_week+' '+esc(r.worst_opp)+'</span>':'');
        else if(c[0]==='last_snap_pct'||c[0]==='cmp_pct') v = v==null?'–':v+'%';
        else if(typeof v==='number' && ['tgt_pg','rec_pg','yds_pg','ypt'].indexOf(c[0])>=0) v = v.toFixed(1);
        else v = v==null?'–':esc(v);
        return '<td'+(c[2]?' class="l"':'')+'>'+v+'</td>'}).join('')+'</tr>';
    }).join('') || '<tr><td colspan="17">No defender matches.</td></tr>';
    var one = rows.length<=3 ? rows : [];
    $('def-detail').innerHTML = one.map(function(r){
      if(!r.big_games || !r.big_games.length) return '<p class="small muted">'+esc(r.player)+': no receiver has had a 70+ yard game with 30+ of it finished by him.</p>';
      return '<details open><summary>'+esc(r.player)+': receivers with 70+ yard games, 30+ of it against him</summary><div class="scroll"><table><thead><tr><th>Week</th><th class="l">Receiver</th><th>Game yards</th><th>Against him</th><th>Long</th></tr></thead><tbody>'+
        r.big_games.map(function(b){return '<tr><td>'+b.week+'</td><td class="l">'+esc(b.receiver)+' <span class="muted">'+esc(b.pos||'')+' '+esc(b.team)+'</span></td><td>'+b.game_yards+'</td><td><b>'+b.vs_him+'</b></td><td>'+b.long+'</td></tr>'}).join('')+'</tbody></table></div></details>';
    }).join('');
  }
  ['f-q','f-team','f-pos','f-games'].forEach(function(i){$(i).addEventListener('input',drawDef)});
  $('def-head').addEventListener('click',function(e){var k=e.target.closest('th'); if(!k) return; k=k.dataset.k; if(k===sortK) sortDir=-sortDir; else {sortK=k; sortDir=(['player','team','pos'].indexOf(k)>=0)?1:-1} drawDef()});
  drawDef();
  // ---- teams
  var T = teams.map(function(t){var x=D.teams[t]; return {t:t,g:x.games,ex:x.explosive_pg,g80:x.g80,r80:x.g80/x.games,g100:x.g100,wr:x.g80_by_pos.WR,te:x.g80_by_pos.TE,rb:x.g80_by_pos.RB,who:x.who_80}});
  T.sort(function(a,b){return b.r80-a.r80});
  $('team-body').innerHTML = T.map(function(x,i){
    return '<tr class="'+(i<6?'hot':'')+'"><td>'+x.t+'</td><td>'+x.g+'</td><td><b>'+x.g80+'</b></td><td>'+x.r80.toFixed(2)+'</td><td>'+x.g100+'</td><td>'+x.wr+'</td><td>'+x.te+'</td><td>'+x.rb+'</td><td>'+x.ex.toFixed(2)+'</td><td class="l small">'+x.who.map(function(w){return esc(w.receiver)+' '+w.yards}).join(', ')+'</td></tr>';
  }).join('');
})();
</script>
"""


def render(db: dict, extra_week=None, value=None) -> str:
    week = list(extra_week or []) + db["week"]
    week.sort(key=lambda w: -w["yards"])
    slim = {"week": week, "teams": db["teams"],
            "defenders": [{k: v for k, v in d.items() if k not in ("explosive_yards", "snap_pct", "ints", "explosive_ended_pg", "n_big_100")} for d in db["defenders"]]}
    val = ""
    if value:
        a = value["added"]
        tc = value["top_candidates_all_seasons"]
        g = tc["80+ games allowed per game to his position"]
        w = tc["worst regular cornerback's yards per target"]
        val = f'''<section id="value"><h2>Does this move the projection?</h2>
<p>Tested on every WR and TE game from 2022 to Week 9 of 2026 ({value["n_train"]:,} games to fit, {value["n_test"]:,} held out), adding each piece of a defense's coverage record to the base projection.</p>
<div class="two">
<div class="scroll"><table><thead><tr><th>Added to the projection</th><th>Change in odds of 80+ per step up</th><th>Reliable?</th></tr></thead><tbody>
<tr class="hot"><td>How often the defense has allowed an 80+ game to his position</td><td>+{(a["z_team_g80"]["odds_change_per_sd"] - 1) * 100:.0f}%</td><td>Yes, small</td></tr>
<tr><td>Share of games a cornerback was charged with 70+</td><td>+{(a["z_cb_g70"]["odds_change_per_sd"] - 1) * 100:.0f}%</td><td>No</td></tr>
<tr><td>Cornerbacks' charted yards per target</td><td>{(a["z_cover"]["odds_change_per_sd"] - 1) * 100:+.0f}%</td><td>No</td></tr>
<tr><td>The worst regular cornerback's yards per target</td><td>{(a["z_weak_ypt"]["odds_change_per_sd"] - 1) * 100:+.0f}%</td><td>No</td></tr>
</tbody></table></div>
<div class="scroll"><table><thead><tr><th>Top candidates (rated 35%+), {tc["n"]} games</th><th>Hit 80+</th><th>Hit 100+</th></tr></thead><tbody>
<tr><td>Defense rarely allows 80+ games (lowest third)</td><td>{g["lowest third"]["hit_80"] * 100:.0f}%</td><td>{g["lowest third"]["hit_100"] * 100:.0f}%</td></tr>
<tr><td>Middle third</td><td>{g["middle"]["hit_80"] * 100:.0f}%</td><td>{g["middle"]["hit_100"] * 100:.0f}%</td></tr>
<tr class="hot"><td>Defense often allows them (highest third)</td><td>{g["highest third"]["hit_80"] * 100:.0f}%</td><td>{g["highest third"]["hit_100"] * 100:.0f}%</td></tr>
<tr><td>Facing the best "weak link" corner (lowest third)</td><td>{w["lowest third"]["hit_80"] * 100:.0f}%</td><td>{w["lowest third"]["hit_100"] * 100:.0f}%</td></tr>
<tr><td>Facing the worst "weak link" corner (highest third)</td><td>{w["highest third"]["hit_80"] * 100:.0f}%</td><td>{w["highest third"]["hit_100"] * 100:.0f}%</td></tr>
</tbody></table></div></div>
<div class="callout"><p><b>What holds up:</b> a defense that keeps allowing 80-yard games to a position is a small, real tailwind, and one that rarely allows them is a headwind worth about 6 to 9 points for a top candidate. Overall accuracy barely moves ({value["base_auc"]:.3f} to {value["all_four_auc"]:.3f}, where 0.5 is a coin flip).</p>
<p><b>What does not:</b> an individual cornerback's record. Top candidates hit 80+ equally often against the best and worst "weak link" corners. Charted coverage numbers swing too much over a few games, and nobody publishes who will line up on whom.</p></div></section>'''
    return CSS + f'''<div class="wrap">
<header class="lead"><p class="eyebrow">{db["season"]} season · tackle links through Week {db["through_week"]} · charted coverage through Week {db["charted_through_week"]} · research only</p>
<h1>Coverage Database</h1>
<p>Which defenders give up yards, how often, and to whom. Two sources: Pro Football Reference's charted coverage (yards charged to the nearest defender), and the play-by-play record of which defender finished each catch. Neither is an assignment: a safety who makes the tackle 50 yards downfield was not necessarily the man beaten.</p></header>
<section id="thisweek"><h2>Week {db["through_week"]}: every receiver with 80+ yards, and who finished the catches</h2>
<p class="small muted">Highlighted defenders came in allowing 40+ charted yards a game or with two or more 70-yard games against them. "No defender named" means a touchdown or a catch out of bounds with nobody credited.</p>
<div class="cards" id="week"></div></section>
{val}
<section id="defenders"><h2>Every defender</h2>
<div class="controls">
<label for="f-q">Search by name<input id="f-q" type="search" placeholder="e.g. Samuel"></label>
<label for="f-team">Team<select id="f-team"></select></label>
<label for="f-pos">Position<select id="f-pos"><option value="">All</option><option value="CB">Cornerbacks</option><option value="S">Safeties</option><option value="LB">Linebackers</option></select></label>
<label for="f-games">Minimum games<input id="f-games" type="number" min="0" max="17" value="4" style="width:6em"></label>
<span class="small muted" id="def-count"></span></div>
<p class="small muted">Click a column to sort. Charted columns (targets through "Worst") are per game the defender played. "20+ ended" and "Big games" come from the tackle links: catches of 20+ he finished, and receivers who had a 70+ yard game with 30+ of it against him. Narrow to three or fewer defenders to see those receivers.</p>
<div class="scroll"><table><thead><tr id="def-head"></tr></thead><tbody id="def-body"></tbody></table></div>
<div id="def-detail" style="display:grid;gap:8px"></div></section>
<section id="teams"><h2>Every defense: receivers with 80+ yards against it</h2>
<div class="scroll"><table><thead><tr><th>Defense</th><th>Games</th><th>80+ games allowed</th><th>Per game</th><th>100+</th><th>To WR</th><th>To TE</th><th>To RB</th><th>20+ catches / g</th><th class="l">Who</th></tr></thead><tbody id="team-body"></tbody></table></div></section>
<footer class="foot"><p>Built {db["generated_utc"]} UTC by <code>python3 -m dashboard.coverage_db</code>. Sources: nflverse play-by-play, weekly rosters and snap counts; Pro Football Reference advanced defense via nflverse. Research only; not graded against prices.</p></footer>
</div>
<script type="application/json" id="cov-data">{json.dumps(slim, separators=(",", ":")).replace("</", "<\\/")}</script>
''' + JS


def main(argv):
    db = json.loads(Path(argv[0]).read_text())
    extra = json.loads(Path(argv[2]).read_text()) if len(argv) > 2 and argv[2] != "-" else None
    value = json.loads(Path(argv[3]).read_text()) if len(argv) > 3 else None
    Path(argv[1]).write_text(render(db, extra, value))
    print(argv[1], Path(argv[1]).stat().st_size)


if __name__ == "__main__":
    main(sys.argv[1:])
