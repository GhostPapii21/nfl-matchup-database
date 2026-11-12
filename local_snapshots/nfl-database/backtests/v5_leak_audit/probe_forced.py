import json,random,pandas as pd
from grok import call,ROOT
sc=pd.read_csv(ROOT/'probe_scores.csv');st=pd.read_csv(ROOT/'probe_stats.csv')
SYS=("Answer only from memory, no tools. For each NFL game give your BEST GUESS of the final score even if unsure, plus confidence 0-100 that it is exactly right, and recall=true only if you genuinely remember the result (not inferred). "
 "If you believe the game never happened, set did_not_happen=true (still give a guess). JSON {\"answers\":[{\"id\":..,\"away_score\":int,\"home_score\":int,\"confidence\":int,\"recall\":bool,\"did_not_happen\":bool}]}")
q=sc[['id','season','week','game']].to_dict('records');random.seed(1);random.shuffle(q);A={}
for i in range(0,len(q),30):
    for a in json.loads(call([{'role':'system','content':SYS},{'role':'user','content':json.dumps(q[i:i+30])}],tag='scores_forced'))['answers']:A[a['id']]=a
def gs(r):
    a=A.get(r.id,{});ga,gh=a.get('away_score'),a.get('home_score')
    if r.kind=='fake':return 'flagged_fake' if a.get('did_not_happen') else ('HALLUCINATED' if a.get('recall') else 'guess_on_fake')
    if ga is None:return 'none'
    if (ga,gh)==(r.a,r.h):return 'exact'
    return 'winner_right' if (ga>gh)==(r.a>r.h) else 'winner_wrong'
sc['f_away']=sc.id.map(lambda i:A.get(i,{}).get('away_score'));sc['f_home']=sc.id.map(lambda i:A.get(i,{}).get('home_score'))
sc['f_recall']=sc.id.map(lambda i:A.get(i,{}).get('recall'));sc['f_conf']=sc.id.map(lambda i:A.get(i,{}).get('confidence'));sc['f_dnh']=sc.id.map(lambda i:A.get(i,{}).get('did_not_happen'))
sc['forced_result']=[gs(r) for r in sc.itertuples()];sc.to_csv(ROOT/'probe_scores.csv',index=False)
SYS2=("Answer only from memory, no tools. For each item give your BEST GUESS of the player's stat in that exact game even if unsure, confidence 0-100 that you are within 10 yards, and recall=true only if you genuinely remember this specific game's box score. "
 "If the game never happened set did_not_happen=true. JSON {\"answers\":[{\"id\":..,\"value\":int,\"confidence\":int,\"recall\":bool,\"did_not_happen\":bool}]}")
q=st[['id','season','week','game','player_id','team','stat']].to_dict('records');random.shuffle(q);B={}
for i in range(0,len(q),30):
    for a in json.loads(call([{'role':'system','content':SYS2},{'role':'user','content':json.dumps(q[i:i+30])}],tag='stats_forced'))['answers']:B[a['id']]=a
st['f_value']=st.id.map(lambda i:B.get(i,{}).get('value'));st['f_conf']=st.id.map(lambda i:B.get(i,{}).get('confidence'))
st['f_recall']=st.id.map(lambda i:B.get(i,{}).get('recall'));st['f_dnh']=st.id.map(lambda i:B.get(i,{}).get('did_not_happen'))
def r2(r):
    if r.kind=='fake':return 'flagged_fake' if r.f_dnh else ('HALLUCINATED' if r.f_recall else 'guess_on_fake')
    if pd.isna(r.f_value):return 'none'
    e=abs(r.f_value-r.truth);return 'exact' if e==0 else ('within10' if e<=10 else 'wrong')
st['forced_result']=[r2(r) for r in st.itertuples()]
st['f_side_hit']=[((r.f_value>r.line)==(r.side=='over')) if r.kind=='leg' and pd.notna(r.f_value) else None for r in st.itertuples()]
st['f_truth_side']=[((r.truth>r.line)==(r.side=='over')) if r.kind=='leg' else None for r in st.itertuples()]
st.to_csv(ROOT/'probe_stats.csv',index=False)
print(sc.groupby(['kind','forced_result']).size());print(sc.groupby('kind').f_recall.sum())
print(st.groupby(['kind','forced_result']).size());print(st.groupby('kind').f_recall.sum())
L=st[st.kind=='leg'];print('guess MAE',(L.f_value-L.truth).abs().mean(),'line MAE',(L.line-L.truth).abs().mean())
print('guess agrees w actual outcome vs line',(L.f_side_hit==L.f_truth_side).mean())
