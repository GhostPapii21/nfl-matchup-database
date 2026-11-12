# Defender regrade, Sun Nov 1 2026 (built ~1:30 AM ET). Candidates for Ghost6 vetting, NOT picks.
Defender source: PFR advanced defense, cached Oct 29 6:02 AM ET (fresh pull 403). ESPN Wk8 WR/CB sheet (alignment and likely defender). Sharp schemes (updated Oct 27) for man/zone/MOF, with StatRankings (Oct 30) as a cross-check. FTN blitz. PFF per-defender data: NOT used (paywalled).
Model p: sims_summary.csv "cons" (FD pull Oct 31 6:49 PM ET; alts 8:18 PM ET). p' = 0.5+0.7(p-0.5). Prices need a refresh before vetting.

## Task A: leg grades
| Slip | Leg | Defender / scheme | p -> p' | Grade |
|---|---|---|---|---|
| PP40 | Higgins 14.5 FS | Cordale Flott (TEN) 9-6-83, 9.2 Y/T, rating 96.1; TEN 11.8 YPT to the slot (#1), Sharp man 16.5 / MOFO 51 | FS: unconfirmed; 70+ yds .79 | ok |
| PP40 | Lamb 4.5 rec | Denzel Burke (ARI) 15-10-114-2TD, rating 101; ARI man 9.1 / zone 70.9 / MOFC 22 / MOFO 57 | .855 -> .80 | strong |
| PP40 | Bowers 8.5 tgt | D'Angelo Ponds: 0 PFR targets (thin sample). LB Jamien Sherwood 18-15-163, rating 122.9; NYJ zone 67 / MOFO 50, blitz ~38-40% | no FD targets line; 10.4 tpg | ok/weak (unconfirmed) |
| PP40 | St. Brown 5.5 rec | Byron Murphy (MIN) 26-18-231, 8.9 Y/T, 3 INT, rating 57; MIN zone 86.5 / MOFO 61, blitz 68% (#1) means quick slot throws | .686 -> .63 | ok (up) |
| PP40 | Stafford 22.5 comp | Not a defender-specific leg; LAC scheme only | unconfirmed | ok? |
| PP40 | Walker 97.5 rush | Run leg. Sims cons ~.64, but the regressed-YPC median is ~99 | ~coin flip | weak |
| UD20 | Puka 69.5 | Donte Jackson (Q) 9-6-69, rating 89.6; backup Cam Hart 16-10-167. LAC man 10.6 / zone 58 | .75 -> .67 | strong (Puka was DNP-rest Friday) |
| UD20 | Bowers 49.5 | Same as above | .954 -> .87 | strong |
| UD20 | Walker 69.5 | Run leg | .877 -> .81 | strong |
| UD20 | London 5.5 rec | Jacob Parrish (TB) 28-17-230, 8.2 Y/T, rating 83.9; TB zone 78 / MOFC 59, blitz 40% | .55 -> .535 | weak/ok |
| UD20 | Flowers 49.5 | Dee Alford (BUF slot) 20-11-175, 8.8 Y/T, rating 80.2 | .96 -> .87 | strong |
| UD20 | St. Brown 49.5 | Murphy, as above | .80 -> .71 | strong |
| UD20 | Lamb 4.5 rec | As above | .80 | strong |
| UD20 | D. Boston 29.5 | ROLE: 21% target share, 49% LWR; KC Concepcion 22%, Jeudy 13%. Boston is a real #2, not a #3. vs Jamel Dean 18-12-160, 8.9 Y/T, rating 94.7. PIT scheme unconfirmed. FD main line 48.5 | crude ~.79 | ok |
| PP20 | Higgins 68.5 | Flott, as above | ~.79 -> .70 | ok/strong |
| PP20 | Bowers 2H 25+ | Halves rarely both hit (3/5 in 2026, 2/12 in 2025) | .36-.40 | cut |
| PP20 | Walker+Kyren 1.5 TD | TD leg in a main slip (breaks the rule) | n/a | cut (rule) |
| PP20 | Mahomes 0.5 pass yds | Free if he plays | ~1 | strong (filler) |
| PP25 | Flowers 6 rec | Alford, as above | .829 -> .78 | strong |
| PP25 | Bijan 3.5 rec | No sim at this rung; TB RB receiving context only | unconfirmed | ok? |
| PP25 | Lamb 6.5 rec | Burke, as above; FD 7+ at -106 | .643 -> .60 | ok |
| PP25 | St. Brown 7 rec | Murphy, as above | .52 -> .51 | weak |
| PP25 | J. Warren 69.5 R+R | Cut by Ghost6's pressure check; CLE man 42% / MOFC 73 | unconfirmed | weak |
| PP25 | Kyren anytime TD | TD leg in a main slip | n/a | cut (rule) |

Changed reads: St. Brown improves (Murphy allows 8.9 Y/T, and MIN plays heavy zone and blitzes a lot). Boston is now confirmed as a real secondary target. Lamb 6.5 moves from risky to ok. Bowers' targets lean on Sherwood, not Ponds (thin sample).

## Task B: new candidates (crude model, NOT the 3-sim engine)
Model: mean = 0.7*ypg + 0.3*ypg*(defender Y/T / 7.0), normal with sd = 0.6*mean. FD main lines at -113/-113, so no-vig is 50%.
| Player | FD line | Defender (PFR) | Scheme | p | p' | Edge |
|---|---|---|---|---|---|---|
| Keenan Allen (IND) o35.5 yds | -113 | Jarrian Jones (JAX) 31-17-256, 8.3 Y/T | JAX man 26 / MOFC 50; D. Jones 3.75 yds/db vs blitz | .64 | .60 | +10 |
| Jordan Addison (MIN) o37.5 | -113 | D.J. Reed (DET) 23-15-287-2TD, 12.5 Y/T, rating 137.4 | DET man 5 / zone 87 | .61 | .58 | +8 (18% share; 0 yds in one of 5 games) |
| D.J. Moore (BUF) o53.5 | -113 | Marlon Humphrey (BAL) 23-15-215, 9.3 Y/T, rating 110 | unconfirmed | .62 | .58 | +8 (only 3 BUF games) |
| Pickens (DAL) o65.5 yds | -113 | Max Melton (ARI) 17-10-137, 8.1 Y/T | ARI MOFO 57 | .565 | .545 | +4.5 (not the barred 4+ rec prop) |
| Parker Washington (JAX) o67.5 | -113 | Justin Walley (IND) 27-19-227, 8.4 Y/T, rating 108 | IND slot YPT 10.7 (#4 allowed) | .555 | .54 | +3.9 |
| Germie Bernard o43.5 | -113 | Myles Harden 25-14-230 | CLE man 42 | .54 | .53 | 2.8: FAILS |
All need a fresh price, an inactives check and the full sim before Ghost6 sees them.
