# Slip vet. Tag: fixed-model, copies only. sim_v6_fix, 3x100k, seed 20261101. Shaheed-out boost per loeb_followups (JSN & Kupp).
import sys,json;sys.path.insert(0,'/workspace/nfl-database/tools/sim_v6_fix')
import sim_v6 as V
class E(V.Engine):
    tb={}
    def player(self,name,*a,**k):
        r=list(super().player(name,*a,**k)); b=self.tb.get(name,1.0)
        if b!=1.0: r[1]=r[1].copy(); r[1]['tgt']=r[1]['tgt']*b; r[1]['rec']=r[1]['rec']*b
        return tuple(r)
e=E();out={}
legs=[('Colston Loveland','CHI','SEA','rec',3.0,[2.5,3.5,4.5],'Caleb Williams',1.0),
      ('Luther Burden III','CHI','SEA','recyds',3.0,[29.5,39.5,51.5],'Caleb Williams',1.0)]
for b in (1.0,1.07,1.144):
    legs+=[('Cooper Kupp','SEA','CHI','recyds',-3.0,[14.5,19.5,29.5],'Sam Darnold',b),
           ('Jaxon Smith-Njigba','SEA','CHI','rec',-3.0,[5.5,6.5,7.5],'Sam Darnold',b)]
for pl,t,o,mk,sp,r,cq,b in legs:
    E.tb={pl:b}; L=dict(player=pl,team=t,opp=o,market=mk,spread=sp,rungs=r,current_qb=cq)
    s,info=e.sim(L); key=f'{pl}|{mk}|x{b}'; out[key]=dict(sims=s,info=info)
    print(key,'n',info['n_games'],{m:(round(s[m]['median'],1),{k:round(v,3) for k,v in s[m]['rungs'].items()}) for m in ('mc','bias','gr')})
json.dump(dict(tag='fixed-model, copies only',src=V.SRC,seed=V.SEED,n=V.N,out=out),open('raw_sims.json','w'),indent=1,default=float)
