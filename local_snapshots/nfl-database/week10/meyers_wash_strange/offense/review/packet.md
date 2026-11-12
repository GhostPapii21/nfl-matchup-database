Review this NFL research report and the code that produced it for bugs, wrong denominators, misleading claims, unsupported numbers, and data-source problems. Be concrete; list issues by severity. Report:
# JAX offense half: Meyers / P. Washington / Strange vs BAL (TNF Thu Nov 5, 2026)
Built 2026-11-04 ~17:45 ET on branch mws-matchup-2026-11-04. Research inputs only, not picks. Scenario-first; game logs are a cross-check. Passing-yards legs are off slips.

**Sources (pull times ET)**
- [N] nflverse 2026 local snapshot (pbp, FTN charting, snap_counts, roster_weekly), CC-BY, pulled 2026-11-03 08:04 ET: `sources/nflverse/`. Computed by `runA/build_a.py` (Codex run A), outputs in `runA/*.csv`.
- [E] ESPN game logs, fetched 2026-11-04 17:10 ET: Meyers https://www.espn.com/nfl/player/gamelog/_/id/3916433/type/nfl/year/2026 , Washington .../id/4432620/... , Strange .../id/4430539/... ; schedule https://www.espn.com/nfl/team/schedule/_/name/jax/season/2026 (Codex run B, `runB/raw/`, `runB/fetch_log.csv`).
- [P] Free PFF matchup/player pages already in repo: `week10/pff_jax_bal/receiver_matchups.csv` (https://www.pff.com/tools/matchups), pulled Nov 3-4.
- [G] Existing NGS route-chart screenshots `week10/ngs/*.png` (capture time not recorded).
- Blocked this run: PFR (all pages HTTP 403 "Just a moment" challenge, 17:10 ET), NGS stat tables (404 or JS shell with no data, 17:10 ET).

## 1. Routes, alignment, field areas
NGS 2026 route-type counts (go/slant/out/curl/cross/screen) are **UNAVAILABLE**: NGS stat pages return a JS shell with no data, and nflverse 2026 participation (route field) was a 404/corrupt. What we have instead:

| Player | Alignment snaps 2026 [P] | Screen targets [N/FTN] | Target areas, Lawrence tgts (location/air yds) [N] | NGS chart, one game [G] |
|---|---|---|---|---|
| Washington | Wide 179 / Slot 145 | 2 of 48 | **Left side 29 of 48** (left 5-14: 15 tgt 11-114; left 15+: 10 tgt 4-84); middle 7; right 12 | Wk6: shallow crossers, intermediate breaks both sides, deep stems both sides |
| Meyers | Wide 229 / Slot 102 | 3 of 31 | Left 12 (left 15+: 3-3-88), **middle 10** (5-14: 7 tgt 5-71; 15+: 3 tgt 2-44), right 9 | Wk3 vs NE: crossers/in-breakers + outs, short/intermediate, TD intermediate middle |
| Strange | Inline 171 / Slot 80 / Wide 39 / Backfield 38 | 2 of 35 | Spread: left 14, **middle 5-14: 9 tgt 5-76**, right 11 (mostly short 1-14) | Wk4 vs CIN: flats/underneath, intermediate diagonals/crossers, outs |
Route types from screenshots are visual reads of one game each, not counts.

**NGS season aggregates, Weeks 1-6 (nflverse NGS file `week8/defense/raw/ngs_receiving.parquet` / `ngs_passing.parquet`, pulled 2026-10-29 06:04 ET, week 0 = season row).** Verified: NGS targets 46/33/28 equal nflverse pbp Wks 1-6 targets for Washington/Strange/Meyers exactly. No Week 8.
| Player | NGS tgt (Wk1-6) | Avg cushion | Avg separation | Intended air yds/tgt | Share of team intended air yds |
|---|---|---|---|---|---|
| Washington | 46 | 6.7 | **2.1 (lowest)** | 12.8 | **37.7%** |
| Meyers | 28 | 7.8 | **3.2** | 11.9 | 21.4% |
| Strange | 33 | 7.3 | 3.1 | 7.7 | 16.2% |
Lawrence NGS time to throw (Wk1-6, 184 att): **2.72 s**, aggressiveness 16.3%; by week 2.98/2.80/2.71/2.48/2.65/2.72. Not split by blitz/pressure (NGS doesn't publish that).

**Field-area map vs Blitz's defense read (BAL leakiest = middle; tightest = short outside).** Lawrence targets by area [N]:
| Player | Middle (any depth) | Outside short (<=4 air yds, L+R) | Outside 5-14 | Outside 15+ |
|---|---|---|---|---|
| Washington (48) | 7 (15%) | 7 | 20 | 14 |
| Meyers (31) | 10 (32%) | 5 | 13 | 3 |
| Strange (35) | 10 (29%) | 11 | 10 | 4 |
Meyers and Strange get the most middle work; Washington lives outside (left 5-14 and deep). Strange's 11 short-outside targets sit in BAL's tightest zone.

## 2. Snaps, Weeks 1-8 (7 games, Wk7 bye) [N snap_counts]
| Player | Wk1 | 2 | 3 | 4 | 5 | 6 | 8 | Avg snaps | Avg snap % |
|---|---|---|---|---|---|---|---|---|---|
| Meyers | 37 (65%) | 53 (90) | 50 (81) | 50 (82) | 61 (85) | 53 (75) | 29 (54) | 47.6 | 76.0% |
| Washington | 35 (61) | 48 (81) | 50 (81) | 49 (80) | 59 (82) | 52 (73) | 36 (67) | 47.0 | 75.0% |
| Strange | 39 (68) | 49 (83) | 48 (77) | 53 (87) | 58 (81) | 54 (76) | 28 (52) | 47.0 | 74.9% |
| B. Thomas Jr. (context) | 20 (35) | 32 (54) | 23 (37) | 38 (62) | 37 (51) | 15 (21) | 28 (52) | 27.6 | 44.6% |
Wk8 was a 42-7 blowout (backups late), so Wks 2-6 (~75-90%) is the better normal-game read.

## 3. Lawrence target share, Weeks 1-8 (192 targeted Lawrence attempts) [N], cross-checked vs [E]
| Rank | Receiver | Tgt | Rec | Yds | Share | aDOT |
|---|---|---|---|---|---|---|
| 1 | Parker Washington | 48 | 27 | 432 | 25.0% | 12.9 |
| 2 | Brenton Strange | 35 | 28 | 334 | 18.2% | 7.9 |
| 3 | Jakobi Meyers | 31 | 22 | 309 | 16.1% | 10.5 |
| 4 | Brian Thomas Jr. | 21 | 10 | 117 | 10.9% | 12.2 |
| 5 | Bhayshul Tuten | 16 | 15 | 181 | 8.3% | -3.1 |
| 6 | Josh Cameron | 12 | 8 | 117 | 6.3% | 4.9 |
| 7 | Nate Boerkircher | 9 | 7 | 83 | 4.7% | 6.6 |
| 8 | Travis Hunter | 7 | 6 | 76 | 3.6% | 4.3 |
| 9 | LeQuint Allen Jr. | 5 | 2 | 9 | 2.6% | 2.6 |
| 10= | Chris Rodriguez Jr. / Ameer Abdullah | 3 / 3 | 2 / 2 | 23 / 2 | 1.6% each | |
| 12 | Quintin Morris | 2 | 1 | 7 | 1.0% | |
Weekly targets (Wk1-6, 8): Washington 6,12,5,3,9,11,2; Strange 3,2,5,8,8,7,2; Meyers 2,1,8,4,3,10,3. **ESPN per-week targets/rec/yds match nflverse exactly for all three players (21 of 21 player-weeks).** All-QB version (incl. Ewers' 3 Wk8 attempts): 195 targets, same top 3.

## 4. BAL pressure and Lawrence under it [N: pbp + FTN charting]
| BAL defense, Wks 1-8 | BAL | League | N (BAL) |
|---|---|---|---|
| Blitz rate (FTN n_blitzers>0) | 33.0% | 31.8% | 99 / 300 charted dropbacks |
| 5+ rushers | 33.0% | 31.8% | 99 / 300 |
| Sack rate | 5.7% | 6.2% | 17 / 300 |
| QB hit (incl. sacks per pbp flag) | 17.0% | 15.2% | 51 / 300 |
PFR blitz%/pressure%/hurries and NGS pressure: UNAVAILABLE (PFR 403, NGS shell). BAL is about league average, slightly more blitz.

| Lawrence split | Dropbacks | Att | Cmp% | YPA | Sacks (rate) | EPA/db |
|---|---|---|---|---|---|---|
| All | 219 | 197 | 66.0% | 8.58 | 13 (5.9%) | +0.28 |
| vs blitz | 67 | 62 | 58.1% | 7.02 | 4 (6.0%) | +0.15 |
| no blitz | 152 | 135 | 69.6% | 9.30 | 9 (5.9%) | +0.34 |
| pressured (proxy) | 65 | 43 | 51.2% | 7.60 | 13 (20.0%) | -0.26 |
| clean (proxy) | 154 | 154 | 70.1% | 8.85 | 0 | +0.51 |
Pressure proxy = qb_hit OR sack OR FTN out-of-pocket OR scramble (nflverse pbp has no `was_pressure` field). Because sacks define the proxy, the pressured sack rate is circular. **Time to throw: UNAVAILABLE** (NGS only).

**Who he throws to** [N]
| Receiver | vs blitz (62 tgt) | Under pressure proxy (43 tgt) | Checkdowns, air yds <=2 (53 all / 18 pressured) |
|---|---|---|---|
| Washington | **17 (27.4%)** | **10 (23.3%)** | 5 / 2 |
| Strange | 13 (21.0%) | 5 (11.6%) | 6 / 1 |
| Meyers | 11 (17.7%) | 8 (18.6%) | 3 / 0 |
| Tuten | 5 | 5 (11.6%) | **16 (30.2%) / 5 (27.8%)** |
| Cameron | 6 | 2 | 5 / 2 |
| Al-Jay Henderson | 2 | 4 | 2 / 2 |
**Check-down guy = RB Tuten** (16 of 53 at-or-near-LOS targets). Tuten is questionable (3 straight DNPs); if out, that role likely spreads to Allen/Rodriguez/Henderson (hypothesis, tiny n).

## 5. Meyers' timing
Meyers is on JAX in every 2026 week of nflverse roster_weekly and pbp (Wks 1-6, 8), and ESPN labels his whole 2026 log "JAX". The LV->JAX trade happened in the 2025 season (from memory of public reporting, not re-fetched this run), so **there is no short 2026 JAX sample**: 7 games, same as the others. He had no injury designation on the final Wednesday report per the parent brief.

## Scenario notes (hypotheses, not picks)
- Washington: the clear WR1 and the top target both vs blitz and under pressure; left-side intermediate/deep. Pairs with the defense half (Wiggins Q -> Awuzie outside; Hamilton from the slot).
- Meyers: the middle-of-field guy (5-14 and 15+ middle), BAL's deep-middle area; steady 76% snaps; volume swingy (1-10 tgt).
- Strange: safest volume (top 3 in all 7 games), but mostly short/intermediate; under pressure his share drops (21% blitz -> 12% pressured). Check-downs go to the RB, not him.

## Gaps and flags
1. NGS route-type counts UNAVAILABLE (NGS pages JS shell/404 2026-11-04 17:10 ET). Separation/cushion/TTT come from the Oct 29 nflverse NGS file (Wks 1-6 only, no Wk8). Blitz's `scratch_offense_aborted/ws3/ngs_2026_receiving.parquet` is a 9-byte 'Not Found' body, not data; not used. Route reads use location x air-yards proxy + one screenshot per player.
2. PFR advanced (BAL blitz%/pressure%/hurries, Lawrence pressure%/bad throw%, player advanced receiving): UNAVAILABLE, HTTP 403 challenge. Not bypassed.
3. Pressure is a pbp/FTN proxy, not charted pressure; sack rate under "pressure" is definitional. Samples small: 65 pressured dropbacks, 43 targets; 62 blitz targets.
4. Alignment uses free PFF season splits (pulled Nov 3-4), not per-route data; no per-week alignment.
5. FTN has no route/alignment fields (column list in runA/ftn_columns.csv).
6. Wk8 blowout depresses snaps/targets; Ewers took 3 attempts.
7. nflverse snapshot is ~33 h old (pulled 2026-11-03 08:04 ET); fine for Wks 1-8, nothing newer exists.
8. ESPN schedule calls this game Week 9; directory naming retains week10.
9. Tuten (check-down RB) questionable; Wiggins Q recheck at Thu 6:50 PM ET inactives.
10. Al-Jay Henderson (4 pressured targets) identity/role not checked.
=== build_a.py ===
"""Recompute local nflverse analysis; write only beside this script. Python 3 + pandas."""
from pathlib import Path
import pandas as pd
import numpy as np

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
SRC = ROOT / 'sources/nflverse'

def save(df, name):
    df.to_csv(OUT / (name + '.csv'), index=False, float_format='%.6f')
    return df

def ratio(a, b):
    return a / b if b else np.nan

p0 = pd.read_csv(SRC / 'pbp_2026.csv.gz', low_memory=False)
f = pd.read_csv(SRC / 'ftn_charting_2026.csv', low_memory=False)
r = pd.read_csv(SRC / 'roster_weekly_2026.csv.gz', low_memory=False)
s = pd.read_csv(SRC / 'snap_counts_2026.csv.gz')
assert not p0.duplicated(['game_id', 'play_id']).any()
assert not f.duplicated(['nflverse_game_id', 'nflverse_play_id']).any()
fc = [c for c in f if c not in ['season', 'week']]
p = p0.merge(f[fc], left_on=['game_id','play_id'], right_on=['nflverse_game_id','nflverse_play_id'], how='left', validate='one_to_one', indicator='ftn_merge')
p = p[p.week.between(1,8) & p.season_type.eq('REG')].copy()
valid = p.two_point_attempt.ne(1) & p.play_type.ne('no_play') & p.play_deleted.ne(1)
j = p[valid & p.posteam.eq('JAX')].copy()
rr = r[r.week.between(1,8)]
names = ['Jakobi Meyers','Parker Washington','Brenton Strange','Brian Thomas Jr.']
ids = {n: rr.loc[rr.full_name.eq(n),'gsis_id'].dropna().unique().item() for n in names}
pfr = {n: rr.loc[rr.full_name.eq(n),'pfr_id'].dropna().unique().item() for n in names}
idnames = rr.drop_duplicates('gsis_id').set_index('gsis_id').full_name.to_dict()
p['receiver'] = p.receiver_player_id.map(idnames).fillna(p.receiver_player_name)
j['receiver'] = j.receiver_player_id.map(idnames).fillna(j.receiver_player_name)
games = j[['week','game_id']].drop_duplicates().sort_values('week')
assert games.week.tolist() == [1,2,3,4,5,6,8]
ss = s[s.team.eq('JAX') & s.week.between(1,8) & s.game_type.eq('REG') & s.pfr_player_id.isin(pfr.values())].copy()
ss['player'] = ss.pfr_player_id.map({v:k for k,v in pfr.items()})
assert not ss.duplicated(['game_id','player']).any()
ss['row_type']='game'; ss['games_n']=1
# Source percentage is rounded; exact team offensive-snap denominator isn't supplied.
ss['offense_pct_source_games_n'] = ss.offense_pct.notna().astype(int)
av = ss.groupby('player').agg(offense_snaps=('offense_snaps','mean'),offense_pct=('offense_pct','mean'),games_n=('game_id','nunique'),offense_pct_source_games_n=('offense_pct','count')).reset_index()
av['row_type']='average_games_played'
snaps=save(pd.concat([ss[['row_type','player','week','game_id','offense_snaps','offense_pct','games_n','offense_pct_source_games_n']],av],ignore_index=True),'snaps')

attempts = j[j.pass_attempt.eq(1) & j.sack.ne(1)].copy()
lt = attempts[attempts.passer_player_name.eq('T.Lawrence')]
def target_summary(a, scope):
    t=a[a.receiver_player_id.notna() | a.receiver_player_name.notna()]
    z=t.groupby(['receiver_player_id','receiver'],dropna=False).agg(targets=('play_id','size'),receptions=('complete_pass','sum'),yards=('receiving_yards','sum'),air_yards_sum=('air_yards','sum'),adot_n=('air_yards','count')).reset_index()
    z['scope']=scope; z['targets_n']=len(t); z['target_share']=z.targets / len(t)
    z['adot']=z.air_yards_sum.div(z.adot_n.replace(0,np.nan));z['rank']=z.targets.rank(method='min',ascending=False).astype(int)
    return z.sort_values(['rank','receiver'])
targets=save(pd.concat([target_summary(lt,'Lawrence'),target_summary(attempts,'team_all_QB')],ignore_index=True),'targets')
weekly=[]
for scope,a in [('Lawrence',lt),('team_all_QB',attempts)]:
    for w,g in games.itertuples(index=False):
        t=a[a.game_id.eq(g) & a.receiver_player_id.notna()]
        for n in names[:3]:
            x=t[t.receiver_player_id.eq(ids[n])]
            weekly.append(dict(scope=scope,week=w,game_id=g,player=n,targets=len(x),targets_n=len(t),target_share=ratio(len(x),len(t))))
save(pd.DataFrame(weekly),'targets_weekly')
# Roster membership is not proof of participation. PBP receiving involvement is affirmative evidence.
timing=[]
for w in sorted(r.week.dropna().unique()):
    rost=r[r.week.eq(w)&r.gsis_id.eq(ids[names[0]])]
    plays=p0[p0.week.eq(w)&p0.receiver_player_id.eq(ids[names[0]])]
    timing.append(dict(week=w,roster_teams='|'.join(sorted(rost.team.dropna().unique())),roster_rows_n=len(rost),pbp_posteams='|'.join(sorted(plays.posteam.dropna().unique())),pbp_receiving_plays_n=len(plays),jax_game_n=int(games.week.eq(w).sum())))
save(pd.DataFrame(timing),'meyers_timing')

db=p[valid & p.qb_dropback.eq(1)].copy()
pressure_rows=[]
for label,x in [('BAL',db[db.defteam.eq('BAL')]),('league',db),('league_ex_BAL',db[db.defteam.ne('BAL')])]:
    row=dict(row_type='defense',scope=label,dropbacks=len(x),games_n=x.game_id.nunique())
    for metric,col,threshold in [('blitz_rate','n_blitzers',0),('rush5plus_rate','n_pass_rushers',4),('sack_rate','sack',0),('qb_hit_rate','qb_hit',0)]:
        a=x[col].dropna();row[metric+'_n']=len(a);row[metric+'_count']=int((a>threshold).sum());row[metric]=ratio(row[metric+'_count'],len(a))
    pressure_rows.append(row)
lawrence_db = db.passer_player_name.eq('T.Lawrence') | (db.qb_scramble.eq(1) & db.rusher_player_name.eq('T.Lawrence'))
l=db[db.posteam.eq('JAX') & lawrence_db].copy()
l['receiver']=l.receiver_player_id.map(idnames).fillna(l.receiver_player_name)
l['blitz']=np.where(l.n_blitzers.isna(),'unknown',np.where(l.n_blitzers.gt(0),'blitz','no_blitz'))
proxycols=['qb_hit','sack','is_qb_out_of_pocket','qb_scramble']
positive=l[proxycols].eq(1).any(axis=1)
known=l[proxycols].notna().all(axis=1)
l['pressure_proxy']=np.where(positive,'pressure_proxy',np.where(known,'clean_proxy','unknown'))
if 'was_pressure' in p0:
    l['pressure']=np.where(l.was_pressure.isna(),'unknown',np.where(l.was_pressure.eq(1),'pressured','clean'))
else:
    l['pressure']=l.pressure_proxy
splits=[('all','all',l)]
for axis in ['blitz','pressure_proxy'] + (['pressure'] if 'was_pressure' in p0 else []):
    splits += [(axis,str(label),x) for label,x in l.groupby(axis)]
for axis,label,x in splits:
    a=x[x.pass_attempt.eq(1)&x.sack.ne(1)]
    pressure_rows.append(dict(row_type='QB',scope='T.Lawrence',split_axis=axis,split=label,dropbacks=len(x),att=len(a),completions=int(a.complete_pass.sum()),cmp_pct=ratio(a.complete_pass.sum(),a.complete_pass.count()),cmp_pct_n=int(a.complete_pass.count()),passing_yards=float(a.passing_yards.fillna(0).sum()),ypa=ratio(a.passing_yards.fillna(0).sum(),len(a)),ypa_n=len(a),sacks=int(x.sack.sum()),sack_rate=ratio(x.sack.sum(),x.sack.count()),sack_rate_n=int(x.sack.count()),epa=x.epa.mean(),epa_n=int(x.epa.count())))
pressure=save(pd.DataFrame(pressure_rows),'pressure')

def distribution(x, axis, label):
    t=x[x.pass_attempt.eq(1)&x.sack.ne(1)&x.receiver.notna()]
    z=t.groupby('receiver').size().rename('targets').reset_index()
    z['split_axis']=axis;z['split']=label;z['targets_n']=len(t);z['share']=z.targets/len(t);z['rank']=z.targets.rank(method='min',ascending=False).astype(int)
    return z.sort_values(['rank','receiver'])
dists=[distribution(x,axis,label) for axis,label,x in splits if axis!='all']
save(pd.concat(dists,ignore_index=True),'target_pressure_distribution')
checks=[]
for label,x in [('all',l),('pressure_proxy',l[l.pressure_proxy.eq('pressure_proxy')])]:
    checks.append(distribution(x[x.air_yards.le(2)],'air_yards_le_2',label))
check=save(pd.concat(checks,ignore_index=True),'checkdowns')

route=[];screen=[]
for scope,a in [('Lawrence',lt),('team_all_QB',attempts)]:
    for n in names[:3]:
        x=a[a.receiver_player_id.eq(ids[n])].copy()
        x['depth']=pd.cut(x.air_yards,[-np.inf,0,4,14,np.inf],labels=['at_or_behind_LOS','1_to_4','5_to_14','15_plus']).astype('object').fillna('unknown')
        x['location']=x.pass_location.fillna('unknown')
        z=x.groupby(['location','depth'],observed=True).agg(targets=('play_id','size'),receptions=('complete_pass','sum'),yards=('receiving_yards','sum')).reset_index()
        z['player']=n;z['scope']=scope;z['targets_n']=len(x);z['share']=z.targets/len(x);route.append(z)
        chart=x.is_screen_pass.dropna()
        screen.append(dict(scope=scope,player=n,targets=len(x),screen_charted_n=len(chart),screen_pass_targets=int(chart.eq(1).sum()),screen_rate=ratio(chart.eq(1).sum(),len(chart))))
save(pd.concat(route,ignore_index=True),'route_area_proxy');save(pd.DataFrame(screen),'screens')
save(pd.DataFrame({'column':f.columns,'dtype':[str(f[c].dtype) for c in f]}),'ftn_columns')
# Any receiver alignment / route data would be summarized generically if supplied.
route_fields=[c for c in f if any(k in c.lower() for k in ['alignment','route'])]
if route_fields:
    rows=[]
    for c in route_fields:
        x=j[j.receiver_player_id.isin([ids[n] for n in names[:3]]) & j.pass_attempt.eq(1)]
        z=x.groupby(['receiver',c],dropna=False).size().rename('targets').reset_index().rename(columns={c:'value'})
        z['field']=c;rows.append(z)
    save(pd.concat(rows,ignore_index=True),'ftn_route_fields')

assert targets.groupby('scope').targets.sum().eq(targets.groupby('scope').targets_n.first()).all()
assert targets.groupby('scope').target_share.sum().sub(1).abs().lt(1e-9).all()
assert len(ss)==28 and av.games_n.eq(7).all()
assert sum(len(x) for _,x in l.groupby('blitz'))==len(l)
notes=[]
notes += ['# JAX offense, Weeks 1–8, 2026', '', 'Source: local nflverse CC-BY snapshot, pulled 2026-11-03 08:04 ET. Recomputed from the four supplied files; reference build.py informed the join and split logic, with no copied results. Run: `python3 week10/meyers_wash_strange/offense/runA/build_a.py`.', '', 'Seven JAX games: Weeks 1–6 and 8; Week 7 bye. Regular season only. PBP excludes two-point attempts, no-play rows and deleted plays. Attempts exclude sacks; named/identified receivers define targets, excluding untargeted throwaways/spikes. Lawrence attribution uses passer T.Lawrence for throws/sacks or rusher T.Lawrence for scrambles; no other-QB sacks are assigned to him. QB splits use qb_dropback=1, which excludes one Lawrence clock spike; the attempt/target tables retain official pass attempts including that untargeted spike.', '', 'All rates are fractions, with denominator `_n` columns (or att/dropbacks/targets_n); counts appear alongside rates. aDOT uses non-null air yards; YPA treats null passing yards on incomplete passes as zero. EPA is mean per dropback with epa_n. Receiving yards are summed. Snap averages are arithmetic means of source game percentages over source appearances (games played), not snap-weighted percentages. Source offense_pct is rounded and has no exact team-snap denominator; games_n and offense_pct_source_games_n accompany it.', '', '## Snap averages', av.to_markdown(index=False), '', '## Targets', targets[['scope','receiver','rank','targets','receptions','yards','targets_n','target_share','adot','adot_n']].to_markdown(index=False), '', '## Meyers timing', 'Meyers is JAX in every available roster week (1–6, 8), and receiving PBP posteam is JAX in those same seven games. There is no within-2026 team transition in this snapshot. A trade to JAX may predate this sample, but these files cannot establish a transaction or trade date. Week 7 has no roster/receiving entry and is JAX’s bye; it is not evidence of a team change. Only seven JAX games are observed.', '', '## Pressure', 'FTN n_blitzers > 0 and n_pass_rushers >= 5 are distinct measures, each using its own non-null charted dropback denominator. Sack and QB-hit rates use all eligible dropbacks with known respective PBP flags. League includes BAL; league_ex_BAL is also supplied.', pressure.to_markdown(index=False), '', f'PBP was_pressure column present: {"was_pressure" in p0}. Proxy = qb_hit OR sack OR FTN is_qb_out_of_pocket OR qb_scramble. Positive known signals establish proxy pressure; clean requires all four known and false. Otherwise unknown. This proxy includes movement and is not a direct pressure measure. If was_pressure exists it additionally supplies the primary pressure split; proxy remains separately available.', '', 'Time to throw is not in PBP. qb_location/read_thrown are not time-to-throw or receiver alignment/route measurements.', '', '## Shallow target / check-down proxy', 'air_yards <= 2 includes designed screens and short throws; it does not prove a progression check-down. Targets with null air yards cannot qualify. All tied rank-1 receivers below are leaders.', check[check['rank'].eq(1)].to_markdown(index=False), '', '## Route-area proxy and FTN coverage', 'route_area_proxy.csv uses pass_location × depth: <=0, 1–4, 5–14, >=15 air yards, plus unknowns. These are targeted-pass areas, not routes run or slot/outside alignments. Both Lawrence and team-all-QB versions are supplied. screens.csv counts FTN screen-target flags with charted N. FTN alignment/route fields found: '+(', '.join(route_fields) or 'none')+'.', '', 'FTN columns: '+', '.join(f.columns)+'.', '', '## Verification', 'Assertions passed: unique PBP/FTN join keys; one-to-one join; seven expected JAX weeks; 28 selected snap rows and seven appearances per player; target shares/counts reconcile; Lawrence blitz groups partition all dropbacks.', '', '## Anomalies and limitations (final audit)']
notes += ['- Brian Thomas Jr. is Brian Thomas in snaps and '+', '.join(sorted(j.loc[j.receiver_player_id.eq(ids[names[3]]),'receiver_player_name'].dropna().unique()))+' in PBP. IDs distinguish him from DE Bryan Thomas Jr.; identities are normalized using GSIS/PFR IDs.']
notes += [f'- QB attempt counts: {attempts.groupby("passer_player_name").size().to_dict()}; all-QB and Lawrence target tables therefore differ.']
notes += [f'- JAX target nulls: air_yards={int(attempts.loc[attempts.receiver_player_id.notna(),"air_yards"].isna().sum())}; pass_location={int(attempts.loc[attempts.receiver_player_id.notna(),"pass_location"].isna().sum())}; attempts without named/identified receiver={int((attempts.receiver_player_id.isna() & attempts.receiver_player_name.isna()).sum())}.']
notes += [f'- Lawrence dropbacks={len(l)}; FTN unmatched={int(l.ftn_merge.ne("both").sum())}; missing n_blitzers={int(l.n_blitzers.isna().sum())}; missing n_pass_rushers={int(l.n_pass_rushers.isna().sum())}; missing out-of-pocket={int(l.is_qb_out_of_pocket.isna().sum())}; pressure-proxy unknown={int(l.pressure_proxy.eq("unknown").sum())}.']
notes += [f'- JAX dropbacks with null passer: {int((db.posteam.eq("JAX") & db.passer_player_name.isna()).sum())}; all nine are Lawrence scrambles attributed using rusher identity and included in his dropbacks.', '- Snap and PBP game counts match for all four players (7 each); roster has no Week 7 JAX entries. Snapshot cannot answer later weeks or establish an exact historical trade date.', '- Missing FTN observations are never interpreted as no blitz. Small split samples and seven-game player samples limit conclusions. No receiver route/alignment or time-to-throw data supplied.']
(OUT/'notes_a.md').write_text('\n\n'.join(notes)+'\n')
print(f'Wrote {len(list(OUT.glob("*.csv")))} CSVs and notes_a.md; assertions passed.')
=== independent recompute ===
was_pressure in pbp: False []
192
                       t     r      y
receiver_player_name                 
P.Washington          48  27.0  432.0
B.Strange             35  28.0  334.0
J.Meyers              31  22.0  309.0
Bri.Thomas            21  10.0  117.0
B.Tuten               16  15.0  181.0
J.Cameron             12   8.0  117.0
                   g      snaps       pct
player                                   
Brenton Strange    7  47.000000  0.748571
Jakobi Meyers      7  47.571429  0.760000
Parker Washington  7  47.000000  0.750000
BAL db 303 blitz 0.333 sack 0.056 games 8
week
1    2026_01_BAL_IND
2     2026_02_NO_BAL
3    2026_03_BAL_DAL
4    2026_04_TEN_BAL
5    2026_05_BAL_ATL
6    2026_06_BAL_CLE
7    2026_07_CIN_BAL
8    2026_08_BAL_BUF
Name: game_id, dtype: str
