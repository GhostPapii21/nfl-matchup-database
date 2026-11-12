"""v5.1 CODEX arm (OpenAI model swap only; prompts/packs/validator identical to fresh/reads_v51.py). v5.1 fresh-read arm (copy of v5 reads.py; only SYS prompt additions, validator additions, cost guard, 3 threads). v5 Stage A: Grok reads from frozen v4 as-of packs (808dc89). No outcomes loaded. Key read from env only."""
import os,json,re,time,difflib,urllib.request,sys
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parent;PK=Path('/workspace/nfl-database/backtests/yardage_markets_wk3_8/v4/packs')
OUT=ROOT/'reads';OUT.mkdir(exist_ok=True)
KEY=os.environ.get('OPENAI_API_KEY_RICO') or os.environ.get('OPENAI_API_KEY');MODEL=os.environ.get('CODEX_MODEL','gpt-6.1-sol');EFFORT='medium'
import threading as _t;LK0=_t.Lock()
usage={'requests':0,'prompt_tokens':0,'completion_tokens':0,'reasoning_tokens':0,'errors':0}
PIN,POUT=float(os.environ.get('PIN','5')),float(os.environ.get('POUT','40'))  # assumed $/1M tokens (conservative)
COST=[sum(json.loads(x).get('est_usd',0) for x in open(ROOT/'usage_log.jsonl'))] if (ROOT/'usage_log.jsonl').exists() else [0.0];CAP=38.0
def call(msgs):
    if COST[0]>=CAP:raise RuntimeError('COST_CAP')
    inp=[{'role':m['role'] if m['role']!='system' else 'developer','content':m['content']} for m in msgs]
    body=json.dumps({'model':MODEL,'input':inp,'reasoning':{'effort':EFFORT},'text':{'format':{'type':'json_object'}},'max_output_tokens':32000}).encode()
    for a in range(5):
        try:
            r=urllib.request.Request('https://api.openai.com/v1/responses',body,{'Authorization':'Bearer '+KEY,'Content-Type':'application/json'})
            with urllib.request.urlopen(r,timeout=900) as resp:d=json.load(resp)
            t=''.join(c.get('text','') for o in d['output'] if o['type']=='message' for c in o['content'])
            u=d.get('usage') or {};it,ot=u.get('input_tokens',0),u.get('output_tokens',0);est=it*PIN/1e6+ot*POUT/1e6
            with LK0:
                usage['requests']+=1;usage['prompt_tokens']+=it;usage['completion_tokens']+=ot
                usage['reasoning_tokens']+=(u.get('output_tokens_details') or {}).get('reasoning_tokens',0)
                COST[0]+=est;open(ROOT/'usage_log.jsonl','a').write(json.dumps({'model':d.get('model'),'usage':u,'est_usd':est})+'\n');print(f'cost ${COST[0]:.2f}',flush=True)
            return t
        except Exception as e:
            if getattr(e,'code',0) in (401,402,403,429) and 'quota' in (getattr(e,'read',lambda:b'')().decode()+str(e)).lower() or getattr(e,'code',0) in (401,402,403) or 'COST_CAP' in str(e):raise SystemExit('STOP '+str(getattr(e,'code',e)))
            usage['errors']+=1;print('API error',type(e).__name__,getattr(e,'code',''),file=sys.stderr);open(ROOT/'usage_log.jsonl','a').write(json.dumps({'error':type(e).__name__})+'\n');time.sleep(10*(a+1))
    raise SystemExit('OpenAI API failed; stopping')
def nm(s):return re.sub('[^a-z]','',str(s).lower())
def team_ctx(pb,ft,team,opp):
    off=pb[pb.posteam==team];de=pb[pb.defteam==opp];wk=sorted(off.week.unique())[-3:];l3=off[off.week.isin(wk)]
    rush=l3[l3.rush_attempt==1].groupby('rusher_player_name').agg(car=('rushing_yards','size'),yds=('rushing_yards','sum')).sort_values('car',ascending=False).head(4)
    tg=l3[l3.pass_attempt==1].dropna(subset=['receiver_player_name']).groupby('receiver_player_name').agg(tgt=('receiving_yards','size'),yds=('receiving_yards','sum'),airy=('air_yards','sum')).sort_values('tgt',ascending=False).head(7)
    n=len(wk) or 1
    pa=de[de.pass_attempt==1];loc=pa.groupby('pass_location').agg(att=('yards_gained','size'),ypa=('yards_gained','mean')).round(2)
    rr=de[de.rush_attempt==1]
    m=pb.merge(ft[['nflverse_game_id','nflverse_play_id','n_blitzers']],left_on=['game_id','play_id'],right_on=['nflverse_game_id','nflverse_play_id'],how='left')
    db=m[(m.posteam==team)&(m.qb_dropback==1)&m.n_blitzers.notna()];ob=m[(m.defteam==opp)&(m.qb_dropback==1)&m.n_blitzers.notna()]
    return (f"## {team} offense (last {n} games: weeks {list(map(int,wk))})\nRushers (carries/yds over L3): "+'; '.join(f"{i} {r.car}/{int(r.yds)}" for i,r in rush.iterrows())+
      "\nTargets (tgt/rec yds/air yds over L3): "+'; '.join(f"{i} {r.tgt}/{int(r.yds)}/{int(r.airy)}" for i,r in tg.iterrows())+
      f"\n{team} QB EPA/dropback vs blitz {db[db.n_blitzers>0].epa.mean():.2f} (n={int((db.n_blitzers>0).sum())}) vs no blitz {db[db.n_blitzers==0].epa.mean():.2f}"+
      f"\n## {opp} defense (season to date, {de.game_id.nunique()} games)\nRush YPC allowed {rr.yards_gained.mean():.2f}; 10+ yd runs allowed {int((rr.yards_gained>=10).sum())}; 20+ yd pass plays allowed {int((pa.yards_gained>=20).sum())}/{len(pa)} att"+
      f"\nPass YPA allowed by location: "+'; '.join(f"{i} {r.ypa} ({r.att} att)" for i,r in loc.iterrows())+
      f"\n{opp} blitz rate {(ob.n_blitzers>0).mean():.0%}")
SKILL=open('/home/box/agent-data/workflows/betting-game-brainstorm/SKILL.md').read()
SYS=("You are Rico's NFL prop handicapper. Follow this skill exactly (all 12 steps), brainstorm first, data second:\n\n"+SKILL+
"\n\nV5.1 RULES (in addition to the skill): (1) INJURY FALLOUT: if the pack has no injury/inactive info for a player or team, write 'MISSING: <what is missing>' and do NOT guess absences, returns or next-man-up from usage dips. (2) must_be_true MUST use the fixed format '<player or team> <stat> <>= or <=> <number> [because <pack fact>]'; kills_it MUST use 'IF <specific event> THEN <leg> fails'. (3) DATA CHECK separates two things: data_check.disagrees = pack numbers that contradict the read (verdict 'flag' ONLY for this), data_check.missing = information not in the pack (missing data alone never makes verdict 'flag'; keep 'agree' if nothing present disagrees). Data_check JSON = {\"notes\":str,\"disagrees\":str (or 'none'),\"missing\":str (or 'none'),\"verdict\":\"agree|flag\"}."
"\n\nBACKTEST CONSTRAINTS: Use ONLY the as-of pack data given (all pre-kickoff); no live weather/news. Where the pack lacks info (e.g. weather, final inactives, coverage charting, no-vig/sim), say so and mark step6_limited / step12_limited true. "
"EDGE PLAYERS: max 2, ONLY from the AVAILABLE PROPS list, markets rushyds|recyds|rushrecyds (NO passing yards, NO TDs, NO receptions). Confidence 'pass' means no leg. Data disagreeing with a strong read => verdict 'flag', not cut. "
"Every section must be game-specific (names, numbers from the pack). Return JSON with keys: "
"{\"game\":\"kickoff/spread/total/weather line\",\"script\":{\"base\":str,\"flip1\":str,\"flip2\":str},\"injury_fallout\":str,"
"\"matchup\":{\"shell\":str,\"pressure\":str,\"bleeds\":str,\"overlap\":str},\"form\":str,"
"\"edge_players\":[{\"player\":id,\"market\":str,\"side\":\"over|under\",\"edge_sentence\":str,\"must_be_true\":str,\"kills_it\":str,\"confidence\":\"strong|lean|pass\"}],"
"\"data_check\":{\"notes\":str,\"disagrees\":str,\"missing\":str,\"verdict\":\"agree|flag\"},\"market_rung_price\":str,\"pre_mortem\":str,\"slip_story\":str,\"step6_limited\":bool,\"step12_limited\":bool}")
def _s(x):return json.dumps(x) if isinstance(x,(dict,list)) else str(x or '')
def validate(j,game,cands,others):
    errs=[]
    req={'game':5,'injury_fallout':8,'form':10,'market_rung_price':4,'pre_mortem':12,'slip_story':6}
    for k,n in req.items():
        if len(_s(j.get(k)).split())<n:errs.append(f'{k} missing/short')
    sc=j.get('script') or {}
    for k in ['base','flip1','flip2']:
        if len(str(sc.get(k,'')).split())<8:errs.append(f'script.{k} missing')
    m=j.get('matchup') or {}
    for k in ['shell','pressure','bleeds','overlap']:
        if len(str(m.get(k,'')).split())<5:errs.append(f'matchup.{k} missing')
    if (j.get('data_check') or {}).get('verdict') not in ('agree','flag'):errs.append('data_check verdict')
    for k in ['disagrees','missing']:
        if not str((j.get('data_check') or {}).get(k,'')).strip():errs.append('data_check.'+k+' missing')
    for k in ['step6_limited','step12_limited']:
        if k not in j:errs.append(k+' missing')
    teams=game.split('@')
    if not any(t in _s(sc)+_s(m) for t in teams):errs.append('no team named')
    p=[x for x in (j.get('edge_players') or []) if x.get('confidence')!='pass']
    if not 1<=len(p)<=2:errs.append('edge player count (need 1-2 non-pass)')
    for x in p:
        if (x.get('player'),x.get('market'),x.get('side')) not in cands:errs.append(f"not in props {x.get('player')} {x.get('market')} {x.get('side')}")
        for k in ['edge_sentence','must_be_true','kills_it']:
            if len(str(x.get(k,'')).split())<6:errs.append(f'edge.{k} missing')
        if not re.search(r'\d',str(x.get('edge_sentence',''))+str(x.get('must_be_true',''))):errs.append('edge no numbers')
        if not re.search(r'(>=|<=|≥|≤)\s*\d',str(x.get('must_be_true',''))):errs.append('must_be_true format (<stat> >=|<= <number>)')
        if not re.match(r'\s*IF\b.*\bTHEN\b',str(x.get('kills_it','')),re.S):errs.append('kills_it format (IF ... THEN ...)')
    if len({x.get('player') for x in p})<len(p):errs.append('dup player')
    txt=_s(sc)+_s(m)
    for o in others:
        if difflib.SequenceMatcher(None,txt,o).ratio()>0.6:errs.append('templated vs other read')
    if re.search(r'TBD|<player>|XX|lorem',txt):errs.append('placeholder')
    return errs
import threading
from concurrent.futures import ThreadPoolExecutor
picks=[];rej=[];others=[];LK=threading.Lock()
done={f.stem for f in OUT.glob('*.json')}
jobs=[]
for w in range(3,9):
    d=PK/f'w{w}';pb=pd.read_parquet(d/'pbp_prior.parquet');ft=pd.read_parquet(d/'ftn_prior.parquet')
    assert (pb.week<w).all()
    pb=pb[(pb.season_type=='REG')&pb.play_type.isin(['run','pass'])]
    pr=pd.read_csv(d/'props_main.csv');gl=pd.read_csv(d/'game_lines.csv');we=pd.read_csv(d/'weather.csv')
    idx=pd.read_csv(d/'saved_reads/INDEX.csv') if (d/'saved_reads/INDEX.csv').exists() else pd.DataFrame(columns=['path','games'])
    pr=pr[pr.market.isin(['rushyds','recyds','rushrecyds'])&(pr.tier=='main')].sort_values(['snap','book','candidate_id']).drop_duplicates(['player','market','side'],keep='last')
    for game,g in pr.groupby('game'):
        stem=f'w{w}_{game}';away,home=game.split('@')
        lines=gl[gl.game==game]
        sp=lines[(lines.market=='spreads')&(lines.name==home)].sort_values('timestamp');to=lines[lines.market=='totals'].sort_values('timestamp')
        env=f"{home} spread {sp.iloc[-1].point:+g}, total {to.iloc[-1].point:g}" if len(sp) and len(to) else "Spread/total NOT saved for this game; infer script only from team form, say so."
        wx=we[we.game==game];wxs=f"Weather: wind {wx.iloc[-1].wind}, temp {wx.iloc[-1].temp}" if len(wx) else 'Weather: not saved.'
        sv=idx[idx.games.astype(str).str.replace('LAR','LA').str.split(';').map(lambda L:game in L)]
        svt=('\n# SAVED PREGAME CHECKLIST (excerpt)\n'+(d/sv.iloc[0].path).read_text()[:5000]) if len(sv) else ''
        props='\n'.join(f"{r.player} ({r.team}) {r.market} {r.side} {r.line:g} {r.price:+g}" for r in g.itertuples())
        cands={(r.player,r.market,r.side) for r in g.itertuples()}
        ctx=f"# Week {w} {game}\n{env}\n{wxs}\n"+team_ctx(pb,ft,away,home)+"\n"+team_ctx(pb,ft,home,away)+svt+"\n# AVAILABLE PROPS (main line)\n"+props
        (OUT/f'{stem}.prompt.txt').write_text(ctx)
        jobs.append((w,game,stem,g,cands,ctx,len(sv)))
if os.environ.get('ONLY'):jobs=[j for j in jobs if j[2]==os.environ['ONLY']]
def run(job):
    w,game,stem,g,cands,ctx,hassv=job
    if stem in done:
        j=json.loads((OUT/f'{stem}.json').read_text())
    else:
        msgs=[{'role':'system','content':SYS},{'role':'user','content':ctx}];j=None
        for att in range(3):
            raw=call(msgs)
            try:jj=json.loads(raw)
            except Exception:jj={}
            with LK:e=validate(jj,game,cands,list(others))
            if not e:j=jj;break
            with LK:rej.append({'week':w,'game':game,'attempt':att,'errors':e});open(ROOT/'rejects_log.jsonl','a').write(json.dumps(rej[-1])+'\n')
            msgs+= [{'role':'assistant','content':raw},{'role':'user','content':'Rejected: '+'; '.join(e)+'. Redo with game-specific reasoning and valid picks.'}]
        if j is None:print('DROPPED',stem,flush=True);return
        j['_tag']='SAVED_READ_CONTEXT' if hassv else 'RECONSTRUCTED';(OUT/f'{stem}.json').write_text(json.dumps(j,indent=1))
    with LK:
        others.append(_s(j.get('script'))+_s(j.get('matchup')))
        for x in [x for x in j['edge_players'] if x.get('confidence')!='pass']:
            r=g[(g.player==x['player'])&(g.market==x['market'])&(g.side==x['side'])].iloc[0]
            picks.append(dict(week=w,game=game,player=r.player,team=r.team,opp=r.opp,market=r.market,side=r.side,line=r.line,price=r.price,model_ctx=j['_tag'],confidence=x['confidence'],verdict=j['data_check']['verdict'],why=x['edge_sentence']))
    print(stem,'ok',flush=True)
def safe(job):
    try:run(job)
    except BaseException as e:print('STOPPED',job[2],repr(e)[:120],flush=True)
with ThreadPoolExecutor(int(os.environ.get('THREADS','4'))) as ex:list(ex.map(safe,jobs))
picks=sorted(picks,key=lambda p:(p['week'],p['game'],p['player']))
pd.DataFrame(picks).to_csv(ROOT/'codex_picks.csv',index=False)
old=json.loads((ROOT/'usage.json').read_text()) if (ROOT/'usage.json').exists() else {}
for k in usage:usage[k]+=old.get(k,0) if k!='model' else 0
usage['model']=MODEL;(ROOT/'usage.json').write_text(json.dumps(usage,indent=1))
oldr=json.loads((ROOT/'rejects.json').read_text()) if (ROOT/'rejects.json').exists() else []
(ROOT/'rejects.json').write_text(json.dumps(oldr+rej,indent=1));print(usage,len(rej),'rejects')
