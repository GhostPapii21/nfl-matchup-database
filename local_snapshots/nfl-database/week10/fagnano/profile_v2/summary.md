# Fagnano profile v2 + Rico 3&out rerun (2026-11-04 ~9:15 AM ET). All rates are ESTIMATES.
Profile: reuse runs/2026-11-05_JAX@BAL_r5/fagnano_profile.md. ESPN preseason boxes confirm 56/75, 509 yds (PHI 22/28 224, MIN 15/20 123 1 sk, WSH 19/27 162). The preseason games were vs backups. The sample is small: 1 regular-season relief game (24 dropbacks).
Wks 1-7: no Fagnano dropbacks in the nflverse pbp, so there are no mop-up or lead snaps. Wk 8 BUF is his only regular-season sample.
Reconcile: drive sim 16.0 = 10.4 drives x ~1.54 pts/drive (JAX allowed 1.54/drive over 72 drives, pbp). Projector 13.4 = average of BAL's last-3 pts (11) and JAX's pts allowed per game (15.9), with no Fagnano or drive model. Rico case (50% 3&outs) = 13.0. Suggested anchor: ~14-15 base, 13 Rico.
Rerun: rico_sim.py -> rico_sim.txt. This is a clock-linked drive model. I did not edit the projector branch (I read its params: share .209, catch .80).
