import json
L={ # key: (player,market,rung,price,sims,defline,t2,flags)
'HIG':('Tee Higgins','Receptions','5+',-166,(.736,.774,.684),'Cordale Flott 9-6 66.7% 83y 9.2YPT 96.1 | TEN man16.5/zone77.2 MOFC45.6/MOFO51.2','',''),
'FLO':('Ryan Flournoy','Receptions','3+',-240,(.765,.758,.870),'Garrett Williams 6-4 66.7% 21y 3.5YPT 72.2 | ARI man9.1/zone70.9 MOFC21.9/MOFO56.7','','low-YPT CB -> rec only, yds cut'),
'MET':('DK Metcalf','Receiving Yds','40+',-225,(.768,.676,.722),'Campbell 12-9 75% 179y 14.9 116.7; Ward shadow risk 25-10 40% 142y 5.7 82.0 | CLE man42.4/zone54.0 MOFC72.6/MOFO24.4','','CONDITIONAL_FILM (fails 8A if Ward shadows)'),
'PUK':('Puka Nacua','Receiving Yds','70+',-290,(.638,.787,.819),'Donte Jackson(Q) 9-6 66.7% 69y 7.7 89.6 | LAC man10.6/zone58.0 MOFC33.9/MOFO40.7','','LOW VALUE (<-250); conditional Puka + D.Jackson status 11:30 ET'),
'DOW':('Josh Downs','Receptions','3+',-225,(.778,.758,.890),'Jourdan Lewis 18-10 55.6% 108y 6.0 52.3 | JAX man21.0/zone73.4 MOFC46.0/MOFO51.1','','8A borderline comp%; cleared by 6.6 tgt/g'),
'TR2':('Laquon Treadwell','Receptions','2+',-245,(.756,.726,.853),'Travis Hunter 19-12 63.2% 142y 7.5 63.9 | JAX same','',''),
'TRY':('Laquon Treadwell','Receiving Yds','20+',-178,(.694,.672,.835),'Travis Hunter as above | JAX same','',''),
'AWI':('Antonio Williams','Receptions','3+',-200,(.654,.628,.781),'Q.Mitchell 20-13 65% 140y 7.0 64.6 (alignment mismatch: AW 50% slot) | PHI man15.1/zone72.8 MOFC49.1/MOFO43.4','','defender map uncertain -> PENDING_FILM'),
'BOW':('Brock Bowers','Receptions','6+',-158,(.629,.636,.756),"D'Angelo Ponds (0 tgt, thin) / LB Sherwood 18-15 83.3% 163y 9.1 122.9 | NYJ man23.8/zone66.6 MOFC45.2/MOFO50.0",'',''),
'GIB':('Jahmyr Gibbs','Rushing Yds','70+',-250,(.765,.686,.778),'n/a rushing | MIN man5.3/zone86.5 MOFC31.6/MOFO61.2','T2 Gibbs 5+ rec (same player, positive correlation)','at -250 boundary'),
'TUT':('Bhayshul Tuten','Rushing Yds','60+',-158,(.654,.635,.768),'n/a rushing | IND','','JAX -10, carry share .65'),
}
G={'Group 1 (value, ~-170 avg)':['HIG','BOW','TUT','TRY','AWI','DOW'],
   'Group 2 (higher hit, conditional)':['GIB','FLO','MET','PUK','HIG','BOW'],
   'Group 3 (mix)':['TR2','TUT','DOW','AWI','GIB','FLO']}
dec=lambda a:1+(100/-a if a<0 else a/100)
out={}
for g,ks in G.items():
  D=1;P=1
  for k in ks: D*=dec(L[k][3]);P*=sum(L[k][4])/3
  am=round((D-1)*100)
  out[g]={'legs':[dict(zip(['player','market','rung','price','sims','defender_scheme','ticket2','flags'],L[k]),route_type='PENDING_FILM',alignment='PENDING_FILM') for k in ks],'combined_american':f'+{am}','bonus_profit_on_125':round(125*(D-1),2),'indep_sim_hit':round(P,3)}
  print(g,'+%d'%am,'profit $%.2f'%(125*(D-1)),'p=%.3f'%P)
json.dump(out,open('betguru_2026-11-01_raw/groups_1031.json','w'),indent=1)
