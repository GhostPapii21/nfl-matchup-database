# BetGuru consensus re-price, Sun Nov 1, 2026, ~6:15 AM ET
FD pull: sbapi event-page (fd_pull_ts.py copy), 06:12:58 ET -> fd_refresh.csv (13,534 rows, 12 games). Compared vs locked FD 7:37 PM snapshot. Sims: corrected v4 (runs/betguru_audit_20261031T195019/sims_v4.json; YPC regressed to league 4.17, k=100, full opp YPC allowed), seed 20261101, 100k x 3. No re-sim needed (no inputs changed). write_card.py NOT run. Odds API not used. No keys printed.
See edges.txt for the arithmetic. ESPN injuries: espn_inj_20261101_0615.json. NWS Denver hourly: nws_den_hourly.json. PFR fresh pulls 403 -> Oct 29 cache used for 8A.
Walker 80+ rush -144 no-vig 0.556 sims (0.67647, 0.55195, 0.64041) avg 0.623 raw +6.7 p' 0.586 shrink +3.0 -> PASS
Puka 8+ rec -140 no-vig 0.545 sims (0.62169, 0.53059, 0.62639) avg 0.593 raw +4.8 p' 0.565 shrink +2.0 -> PASS
Gibbs 70+ rush -250 no-vig 0.673 sims (0.78554, 0.66839, 0.72287) avg 0.726 raw +5.2 p' 0.658 shrink -1.5 -> FAIL
Cook 70+ rush -210 no-vig 0.638 sims (0.66083, 0.51774, 0.62514) avg 0.601 raw -3.7 p' 0.571 shrink -6.8 -> FAIL
combined dec 2.905 american +190
joint (indep) v4 0.369
