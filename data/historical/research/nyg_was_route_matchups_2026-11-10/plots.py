import pandas as pd, numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
rng=np.random.default_rng(7)
W=53.3; COL={'Malik Nabers':'#1f77ff','Isaiah Likely':'#ff7f0e','Malachi Fields':'#2ca02c'}
FOOT='ESTIMATE, NOT CHARTED COVERAGE. Zones = generic two-high (Cover 2/6 family, WAS 61.8% two-high per StatRankings) responsibilities filled by snap-share/depth-chart roles. Target spots: nflverse pbp air yards + gamebook pass_location (left/middle/right, offense view); x-position within a third is jittered.'
def field(ax,title):
    ax.set_facecolor('#24563a'); ax.set_xlim(0,W); ax.set_ylim(-6,40)
    for y in range(0,41,5): ax.axhline(y,color='white',lw=.5,alpha=.35)
    ax.axhline(0,color='#3d7dff',lw=2.5); ax.text(.5,.4,'LOS',color='white',fontsize=8)
    for x in (17.8,35.5): ax.axvline(x,color='white',ls=':',lw=.8,alpha=.6)
    ax.set_xticks([8.9,26.65,44.4]); ax.set_xticklabels(["Offense's LEFT","MIDDLE","Offense's RIGHT"],fontsize=9)
    ax.set_ylabel('Air yards from LOS'); ax.set_title(title,fontsize=11,fontweight='bold')
def zone(ax,x0,y0,w,h,txt,c='#ffd700'):
    ax.add_patch(Rectangle((x0,y0),w,h,fc=c,ec='white',alpha=.16,lw=1.2,ls='--'))
    ax.text(x0+w/2,y0+h-1.2,txt,ha='center',va='top',fontsize=7.3,color='white',fontweight='bold',
            bbox=dict(fc='black',alpha=.45,ec='none',pad=1.5))
def xpos(side):
    return {'left':rng.uniform(3,15.5),'middle':rng.uniform(20,33),'right':rng.uniform(38,50.5)}[side]
ZW5=[(0,15,26.6,25,'DEEP 1/2 (L): Reaves or Martin\n(Sainristil deep-zone snaps per DC)','#87ceeb'),
     (26.7,15,26.6,25,'DEEP 1/2 (R): Martin or Reaves','#87ceeb'),
     (0,-5,11,15,'OUTSIDE L: Robertson\n(Douglas when shadowing\nNabers)','#ffd700'),
     (42.3,-5,11,15,'OUTSIDE R: Douglas /\nMoreau (both ~61-64%\noffense-right per SR)','#ffd700'),
     (11,-5,11,14,'HOOK L: Styles\n(RILB)','#ff6961'),(31.3,-5,11,14,'HOOK R: Luvu\n(LILB)','#ff6961'),
     (22,8,9.3,6,'MID/NICKEL: Sainristil\n48% + Styles/Luvu','#dda0dd')]
ZTH=[(0,15,26.6,25,'DEEP 1/2 (L): Cross or Reaves\n(Martin rotates in)','#87ceeb'),
     (26.7,15,26.6,25,'DEEP 1/2 (R): Reaves or Cross','#87ceeb'),
     (0,-5,11,15,'OUTSIDE L: Trey Amos\n(RCB, 97% W9)\nNOT in Week 5','#ffd700'),
     (42.3,-5,11,15,'OUTSIDE R: Robertson /\nDouglas (24% W9)','#ffd700'),
     (11,-5,11,14,'HOOK L: Styles','#ff6961'),(31.3,-5,11,14,'HOOK R: Luvu','#ff6961'),
     (22,-5,9.3,13,'NICKEL/3rd S:\nMartin / Robertson\nRobber: Cross','#dda0dd')]
# ---------- (a) Week 5 ----------
m=pd.read_csv('wk5_target_zone_map.csv'); m=m[m.official_target==True]
fig,ax=plt.subplots(figsize=(12,9)); field(ax,'Week 5 (Oct 11, NYG 27-27 WAS OT): Nabers / Likely / Fields targets vs likely WAS zone defenders')
for z in ZW5: zone(ax,*z)
INI=lambda s: ' / '.join(n.split()[-1] for n in str(s).split('; ') if n and n!='nan')
for _,r in m.iterrows():
    x=xpos(r.side); y=r.air_yards_pbp if not np.isnan(r.air_yards_pbp) else 5
    td='touchdown' in r.result; comp=r.result in('complete','touchdown','touchdown_after_replay_reversal')
    ax.scatter(x,y,s=170 if td else 70,marker='*' if td else 'o',c=COL[r.receiver] if comp else 'none',edgecolors=COL[r.receiver],linewidths=2,zorder=5)
    lab=INI(r.official_credit_full) or ('('+r.media_attribution.split()[-1]+', media)' if isinstance(r.media_attribution,str) and r.media_attribution else '')
    if lab: ax.text(x+.6,y+.5,lab,fontsize=6.5,color='white',zorder=6)
h=[Line2D([],[],marker='o',ls='',mfc=c,mec=c,label=k,markersize=8) for k,c in COL.items()]+[
   Line2D([],[],marker='o',ls='',mfc='none',mec='gray',label='incomplete (hollow)',markersize=8),
   Line2D([],[],marker='*',ls='',mfc='gray',mec='gray',label='touchdown',markersize=12),
   Rectangle((0,0),1,1,fc='#ffd700',alpha=.3,label='likely zone owner (est.)')]
ax.legend(handles=h,loc='upper center',bbox_to_anchor=(.5,-.035),ncol=6,fontsize=8,frameon=False)
ax.text(.5,-0.115,'Small white text = official gamebook tackler/PD credit on that play (not a coverage assignment). 35 official targets: Nabers 20, Likely 13, Fields 2.',transform=ax.transAxes,ha='center',va='top',fontsize=8,color='black')
fig.text(.5,.01,FOOT,ha='center',fontsize=7.2,wrap=True,color='darkred'); fig.subplots_adjust(bottom=.16,top=.95)
fig.savefig('wk5_targets_vs_was_zones.png',dpi=150); plt.close()
# ---------- (b) Thursday ----------
z=pd.read_csv('target_zone_profile.csv'); z=z[z.scope=='season W1-9']
th=pd.read_csv('thursday_projection.csv'); th=th[th.scope.str.startswith('season')]
XS={'left':(0,17.8),'middle':(17.8,17.7),'right':(35.5,17.8)}; YS={'short (<=9 air yds)':(-5,15),'intermediate (10-19)':(10,10),'deep (20+)':(20,20)}
fig,axs=plt.subplots(1,3,figsize=(21,12))
for ax,pl in zip(axs,COL):
    field(ax,f'{pl}: season W1-9 target heat')
    g=z[z.player==pl]; tot=g.targets.sum()
    for _,r in g.iterrows():
        x0,w=XS[r.side_offense_view]; y0,h=YS[r.depth_band]
        if r.depth_band.startswith('short'): y0,h=-5,15
        a=min(.85,.12+r.share_of_player_targets_pct/45)
        ax.add_patch(Rectangle((x0,y0),w,h,fc=COL[pl],alpha=a,ec='none',zorder=1))
        ax.text(x0+w/2,y0+h/2-1.5,f"{r.targets} tgt\n{r.share_of_player_targets_pct:.0f}%",ha='center',va='center',fontsize=9,color='white',fontweight='bold',zorder=7)
    for zz in ZTH: zone(ax,*zz[:5],c='none')
    top=th[th.receiver==pl].head(4)
    ax.text(.0,-.07,'Most likely WAS defenders (est. share of target-time crossings):\n'+'\n'.join(f"  {r.defender}: {r.est_share_pct:.0f}% ({r.confidence})" for _,r in top.iterrows()),
            transform=ax.transAxes,va='top',fontsize=9,color='black',bbox=dict(fc='white',alpha=.9),zorder=9)
    ax.set_title(f'{pl}: {tot} season targets (W1-9) heat',fontsize=11,fontweight='bold'); ax.set_xlabel(f'{tot} season targets (nflverse pbp, W1-9; NYG bye W8)',fontsize=8)
fig.suptitle('Thursday Nov 12 projection: WAS current personnel (W8-9 snaps, Nov 9 depth chart) in likely zones over Giants season target heat',fontsize=13,fontweight='bold')
fig.text(.5,.01,FOOT+' Thursday personnel assumes W8-9 usage; Moreau uncertain; inactives not posted.',ha='center',fontsize=7.5,color='darkred',wrap=True)
fig.subplots_adjust(bottom=.2,top=.92,wspace=.12); fig.savefig('thursday_projection_was_zones.png',dpi=130); plt.close()
print('ok')
