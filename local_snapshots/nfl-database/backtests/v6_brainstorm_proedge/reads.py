"""v6 Stage A: Grok reads. Both skills' full steps are IN the system prompt; pro-edge features are computed pre-read and fed IN.
As-of data only; no outcomes loaded. Key from env only (never printed). Hard stop at $40 spend."""
import os,json,re,time,sys,difflib,urllib.request,threading,math
from concurrent.futures import ThreadPoolExecutor
import pandas as pd,numpy as np
from common import *
OUT=ROOT/'reads';OUT.mkdir(exist_ok=True)
KEY=os.environ.get('GROK_API_KEY') or os.environ.get('XAI_API_KEY');MODEL='grok-4.7';CAP=1e9
WEEKS=[int(x) for x in sys.argv[1:]] or list(range(1,9))
LK=threading.Lock();ULOG=ROOT/'usage_log.jsonl'
def spent():
    if not ULOG.exists():return 0.0
    return sum(json.loads(l).get('cost_in_usd_ticks',0) for l in open(ULOG))/1e10
def call(msgs):
    with LK:
        s=spent()
        if s>=CAP-0.5:raise SystemExit(f'HARD STOP: spend ${s:.2f} at cap')
    body=json.dumps({'model':MODEL,'messages':msgs,'temperature':0.3,'response_format':{'type':'json_object'},'stream':True,'stream_options':{'include_usage':True}}).encode()
    for a in range(5):
        try:
            r=urllib.request.Request('https://api.x.ai/v1/chat/completions',body,{'Authorization':'Bearer '+KEY,'Content-Type':'application/json'})
            out=[];u={}
            with urllib.request.urlopen(r,timeout=180) as resp:
                t0=time.time()
                for line in resp:
                    if time.time()-t0>1000:raise TimeoutError('wall')
                    line=line.decode().strip()
                    if not line.startswith('data:'):continue
                    p=line[5:].strip()
                    if p=='[DONE]':break
                    ch=json.loads(p)
                    if ch.get('usage'):u=ch['usage']
                    for c in ch.get('choices',[]):out.append((c.get('delta') or {}).get('content') or '')
            with LK:open(ULOG,'a').write(json.dumps(u)+'\n')
            return ''.join(out)
        except Exception as e:
            print('API error',type(e).__name__,getattr(e,'code',''),file=sys.stderr);
            body_=''
            try:body_=e.read().decode()[:300]
            except Exception:pass
            if getattr(e,'code',0) in (402,) or re.search(r'credit|quota|spending limit|exhausted|billing',body_,re.I):
                open(ROOT/'QUOTA_STOP','w').write(f'{getattr(e,"code","")} {body_[:200]}');os._exit(3)
            with LK:open(ULOG,'a').write(json.dumps({'error':type(e).__name__})+'\n')
            time.sleep(10*(a+1))
    raise SystemExit('Grok API failed; stopping')
SK1=open('/home/box/agent-data/workflows/betting-game-brainstorm/SKILL.md').read()
SK2=open('/home/box/agent-data/workflows/pro-edge-scan/SKILL.md').read()
SYS=("You are Rico's NFL prop handicapper running a BLIND HISTORICAL BACKTEST. Run SKILL 1 (all 12 steps, brainstorm first) and THEN SKILL 2 (pro-edge scan) on this one game, BEFORE any data check. "
"The pro-edge script cannot run live here: its outputs (implied team totals, anchor no-vig fair, best saved price, lagging-line flags, OUT/Doubtful players for the sleeper check) are precomputed from saved pre-kick data in the PRO-EDGE INPUTS block; read them like the scan output (skill 2 'Read spreads/totals into a game script' and 'Hidden edges').\n\n"
"=== SKILL 1: betting-game-brainstorm ===\n"+SK1+"\n\n=== SKILL 2: pro-edge-scan ===\n"+SK2+
"\n\n=== BACKTEST CONSTRAINTS ===\nNO OUTCOME KNOWLEDGE: You must not use anything you may know about how this game, these players' later 2026 (or 2025) results, later trades/injuries or season narratives turned out. Pretend it is the morning of kickoff. Use ONLY the pack below (all data dated before kickoff). If you notice you 'remember' a result, ignore it and say nothing about it. "
"Where the pack lacks info (live weather, final inactives, coverage charting, sims, Pinnacle) say so and set step6_limited / step12_limited. "
"EDGE PLAYERS: max 2, ONLY (player,market,side) from AVAILABLE PROPS; markets rushyds|recyds|rushrecyds (no passing yards, no TDs, no receptions). Confidence 'pass' = no leg. Data disagreeing with a strong read => 'flag', not cut. Every section game-specific with names/numbers from the pack.\n"
"Return JSON: {\"game\":str,\"script\":{\"base\":str,\"flip1\":str,\"flip2\":str},\"injury_fallout\":str,\"matchup\":{\"shell\":str,\"pressure\":str,\"bleeds\":str,\"overlap\":str},\"form\":str,"
"\"pro_edge\":{\"implied_totals\":str,\"script_read\":str,\"best_price\":str,\"lagging\":str,\"sleepers\":str},"
"\"edge_players\":[{\"player\":id,\"market\":str,\"side\":\"over|under\",\"edge_sentence\":str,\"must_be_true\":str,\"kills_it\":str,\"confidence\":\"strong|lean|pass\",\"model_p\":float,"
"\"scheme\":{\"matchup\":{\"ok\":bool,\"source\":str},\"scheme_fit\":{\"ok\":bool,\"source\":str},\"script\":{\"ok\":bool,\"source\":str},\"form_trend\":{\"ok\":bool,\"source\":str}},"
"\"primary_defender\":{\"who\":str,\"source\":str},\"depth_script_pass\":bool,\"depth_defender_giving\":bool,\"pro_edge_support\":str}],"
"\"data_check\":{\"notes\":str,\"verdict\":\"agree|flag\"},\"market_rung_price\":str,\"pre_mortem\":str,\"slip_story\":str,\"step6_limited\":bool,\"step12_limited\":bool}")
def _s(x):return json.dumps(x) if isinstance(x,(dict,list)) else str(x or '')
def validate(j,game,cands,others):
    e=[]
    for k,n in {'game':5,'injury_fallout':8,'form':10,'market_rung_price':4,'pre_mortem':12,'slip_story':6}.items():
        if len(_s(j.get(k)).split())<n:e.append(f'{k} missing/short')
    sc=j.get('script') or {};m=j.get('matchup') or {};pe=j.get('pro_edge') or {}
    e+=[f'script.{k} missing' for k in['base','flip1','flip2'] if len(str(sc.get(k,'')).split())<8]
    e+=[f'matchup.{k} missing' for k in['shell','pressure','bleeds','overlap'] if len(str(m.get(k,'')).split())<5]
    e+=[f'pro_edge.{k} missing' for k in['implied_totals','script_read','best_price','lagging','sleepers'] if len(str(pe.get(k,'')).split())<3]
    if (j.get('data_check') or {}).get('verdict') not in('agree','flag'):e.append('data_check verdict')
    e+=[k+' missing' for k in['step6_limited','step12_limited'] if k not in j]
    p=[x for x in (j.get('edge_players') or []) if x.get('confidence')!='pass']
    if not 1<=len(p)<=2:e.append('edge player count (need 1-2 non-pass)')
    for x in p:
        if (x.get('player'),x.get('market'),x.get('side')) not in cands:e.append(f"not in props {x.get('player')} {x.get('market')} {x.get('side')}")
        e+=[f'edge.{k} missing' for k in['edge_sentence','must_be_true','kills_it'] if len(str(x.get(k,'')).split())<6]
        if not isinstance(x.get('model_p'),(int,float)):e.append('model_p missing')
        if not isinstance(x.get('scheme'),dict):e.append('scheme missing')
    if len({x.get('player') for x in p})<len(p):e.append('dup player')
    txt=_s(sc)+_s(m)
    if any(difflib.SequenceMatcher(None,txt,o).ratio()>0.6 for o in others):e.append('templated vs other read')
    return e
pl=pd.read_parquet(PLAYERS);POS=dict(zip(pl.gsis_id,pl.position));INJ_=pd.read_parquet(INJ)
def props(w):
    if w<=2:return pd.read_csv(ROOT/f'packs/w{w}/props_standin.csv'),pd.DataFrame()
    q=pd.read_csv(V4/f'w{w}/props_main.csv');q=q[q.market.isin(MK)&(q.tier=='main')];full=q.copy()
    q=q.sort_values(['snap','book','candidate_id']).drop_duplicates(['player','market','side'],keep='last');q['line_src']='saved main line ('+q.book+')'
    return q,full
def lines(w,game):
    away,home=game.split('@')
    if w<=2:
        g=pd.read_csv(ROOT/f'packs/w{w}/game_lines.csv');g=g[g.game==game].iloc[0]
        s=-g.spread_line;t=g.total_line;return s,t,None,f"{home} spread {s:+g}, total {t:g} (nflverse games.csv closing line), roof {g.roof}, kickoff {g.gameday} {g.gametime} ET. Weather forecast not saved."
    gl=pd.read_csv(V4/f'w{w}/game_lines.csv');gl=gl[gl.game==game]
    sp=gl[(gl.market=='spreads')&(gl.name==home)].sort_values('timestamp');to=gl[gl.market=='totals'].sort_values('timestamp')
    we=pd.read_csv(V4/f'w{w}/weather.csv');wx=we[we.game==game];wxs=f"Weather: wind {wx.iloc[-1].wind}, temp {wx.iloc[-1].temp}" if len(wx) else 'Weather: not saved.'
    if len(sp) and len(to):
        S=sp.groupby('timestamp').point.median();T=to.groupby('timestamp').point.median()
        return S.iloc[-1],T.iloc[-1],(S.iloc[-1]-S.iloc[0],T.iloc[-1]-T.iloc[0]) if len(S)>1 else None,f"{home} spread {S.iloc[-1]:+g}, total {T.iloc[-1]:g} (saved pre-kick books). {wxs}"
    return None,None,None,"Spread/total NOT saved; infer script from form. "+wxs
def pro_edge_inputs(w,game,g,full,s,t,mv):
    away,home=game.split('@');out=[]
    if s is not None:out.append(f"Implied team totals: {home} {(t-s)/2:.1f}, {away} {(t+s)/2:.1f}"+(f"; game line moved spread {mv[0]:+g} / total {mv[1]:+g} across saved snapshots" if mv else ''))
    else:out.append('Implied team totals: N/A (no saved spread/total)')
    for r in g.itertuples():
        if r.side!='over':continue
        q=full[(full.player==r.player)&(full.market==r.market)&(full.line==r.line)] if len(full) else full
        fair=None
        for b in['pinnacle','circa','betonlineag','consensus']:
            if not len(q):break
            qb=q[q.book==b].sort_values('snap');o=qb[qb.side=='over'];u=qb[qb.side=='under']
            if len(o) and len(u) and o.price.notna().iloc[-1] and u.price.notna().iloc[-1]:
                po,pu=imp(o.price.iloc[-1]),imp(u.price.iloc[-1]);fair=(po/(po+pu),b);break
        lag=''
        if len(full) and mv and (abs(mv[0])>=1 or abs(mv[1])>=1) and full[(full.player==r.player)&(full.market==r.market)].line.nunique()<=1:lag=' LAG: prop static while game line moved'
        bo=q[q.side=='over'].price.max() if len(q) else np.nan;bu=q[q.side=='under'].price.max() if len(q) else np.nan
        out.append(f"{r.player} {r.market} {r.line:g}: "+(f"anchor {fair[1]} no-vig over {fair[0]:.3f} / under {1-fair[0]:.3f}; best over {bo:+g}, best under {bu:+g}" if fair else 'no two-sided price saved (no-vig N/A)')+lag)
    io=INJ_[(INJ_.week==w)&INJ_.team.isin([away,home])&INJ_.report_status.notna()]
    out.append('Official injury report (pre-game, nflverse injuries): '+('; '.join(f"{r.team} {r.position} {r.full_name} {r.report_status} ({r.report_primary_injury})" for r in io.itertuples()) or 'none listed'))
    return '\n'.join(out)
def team_ctx(pb,ft,team,opp,L,w):
    off=pb[pb.posteam==team];de=pb[pb.defteam==opp]
    if w==1:return f"## {team}/{opp}: week 1 - no 2026 games yet; player logs below are 2025 (prior season, possibly different team/QB)."
    wk=sorted(off.week.unique())[-3:];l3=off[off.week.isin(wk)]
    rush=l3[l3.rush_attempt==1].groupby('rusher_player_name').agg(car=('rushing_yards','size'),yds=('rushing_yards','sum')).sort_values('car',ascending=False).head(4)
    tg=l3[l3.pass_attempt==1].dropna(subset=['receiver_player_name']).groupby('receiver_player_name').agg(tgt=('receiving_yards','size'),yds=('receiving_yards','sum'),airy=('air_yards','sum')).sort_values('tgt',ascending=False).head(7)
    pa=de[de.pass_attempt==1];loc=pa.groupby('pass_location').agg(att=('yards_gained','size'),ypa=('yards_gained','mean')).round(2);rr=de[de.rush_attempt==1]
    s=(f"## {team} offense (weeks {list(map(int,wk))})\nRushers car/yds L3: "+'; '.join(f"{i} {r.car}/{int(r.yds)}" for i,r in rush.iterrows())+
      "\nTargets tgt/yds/air L3: "+'; '.join(f"{i} {r.tgt}/{int(r.yds)}/{int(r.airy)}" for i,r in tg.iterrows())+
      f"\n## {opp} defense ({de.game_id.nunique()} games): rush YPC {rr.yards_gained.mean():.2f}; 10+ runs {int((rr.yards_gained>=10).sum())}; 20+ pass {int((pa.yards_gained>=20).sum())}/{len(pa)}; YPA by location: "+'; '.join(f"{i} {r.ypa} ({r.att})" for i,r in loc.iterrows()))
    if ft is not None and len(ft):
        m=pb.merge(ft[['nflverse_game_id','nflverse_play_id','n_blitzers']],left_on=['game_id','play_id'],right_on=['nflverse_game_id','nflverse_play_id'],how='left')
        ob=m[(m.defteam==opp)&(m.qb_dropback==1)&m.n_blitzers.notna()];db=m[(m.posteam==team)&(m.qb_dropback==1)&m.n_blitzers.notna()]
        s+=f"\n{opp} blitz rate {(ob.n_blitzers>0).mean():.0%}; {team} EPA/db vs blitz {db[db.n_blitzers>0].epa.mean():.2f} vs none {db[db.n_blitzers==0].epa.mean():.2f}"
    return s
def plog(L,gsis,m):
    x=L[L.gsis==gsis].tail(4);return ','.join(f"{int(v)}" for v in x[m]) if len(x) else 'no prior games'
jobs=[];META={}
for w in WEEKS:
    pb,lab=prior_pbp(w);ft=prior_ftn(w);L=logs(pb);q,full=props(w)
    for game,g in q.groupby('game'):
        stem=f'w{w}_{game}';away,home=game.split('@');s,t,mv,env=lines(w,game)
        pr='\n'.join(f"{r.player} ({r.team}) {r.market} {r.side} {r.line:g} {('%+g'%r.price) if pd.notna(r.price) else 'no price'} [{r.line_src}] last4 {r.market}: {plog(L,r.gsis,r.market)}" for r in g.itertuples())
        ctx=(f"# Week {w} 2026 {game} (stats source: {lab})\n{env}\n"+team_ctx(pb,ft,away,home,L,w)+"\n"+team_ctx(pb,ft,home,away,L,w)+
             "\n# PRO-EDGE INPUTS (precomputed from saved pre-kick data)\n"+pro_edge_inputs(w,game,g,full,s,t,mv)+"\n# AVAILABLE PROPS (main line)\n"+pr)
        (OUT/f'{stem}.prompt.txt').write_text(ctx)
        jobs.append((w,game,stem,{(r.player,r.market,r.side) for r in g.itertuples()},ctx))
others=[];rej=[]
def run(job):
    w,game,stem,cands,ctx=job
    if (OUT/f'{stem}.json').exists():return
    msgs=[{'role':'system','content':SYS},{'role':'user','content':ctx}];j=None
    for att in range(3):
        raw=call(msgs)
        try:jj=json.loads(raw)
        except Exception:jj={}
        with LK:e=validate(jj,game,cands,list(others))
        if not e:j=jj;break
        with LK:open(ROOT/'rejects_log.jsonl','a').write(json.dumps({'week':w,'game':game,'attempt':att,'errors':e})+'\n')
        msgs+=[{'role':'assistant','content':raw},{'role':'user','content':'Rejected: '+'; '.join(e)+'. Redo with game-specific reasoning and valid picks.'}]
    if j is None:print('DROPPED',stem,flush=True);return
    j['_meta']={'model':MODEL,'ts':time.strftime('%Y-%m-%dT%H:%M:%S%z')};(OUT/f'{stem}.json').write_text(json.dumps(j,indent=1))
    with LK:others.append(_s(j.get('script'))+_s(j.get('matchup')))
    print(stem,'ok',f'${spent():.2f}',flush=True)
if os.environ.get('DRY'):print(len(jobs),'jobs');sys.exit()
with ThreadPoolExecutor(8) as ex:list(ex.map(run,jobs))
print('spent',round(spent(),2))
