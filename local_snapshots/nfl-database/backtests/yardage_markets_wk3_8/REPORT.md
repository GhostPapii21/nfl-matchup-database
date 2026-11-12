# Yardage markets Wk3-8: Phase 1 (TEST ONLY, zero Odds API credits)
Rules lock commit 593ec21 (made before holdout grading). Detail: results.md, GAPS.md, RULES.md, slip_method.md, traits.md, grading_*.csv.
Coverage: priced quotes exist ONLY for Wk6-8 rush yds + rec yds (main + alt). Wk3-5 all markets and rush+rec all weeks: missing (~1,820 credits min main-only to fill; not pulled). So train = Wk6 only, holdout = Wk7-8.
Rules (train only): rec yds UNDER main line when prior-weeks avg is >=20 yds below line; rush yds UNDER main line, same >=20 yd edge. Everything else abstains (all overs and all alts lost in train).
Holdout singles (one per player, frozen): 56 legs 53.6%, -$105.90 (-18.9%). All correlated quotes: 198, 59.1%, +$116 (+5.9%). Train frozen: 30, 60%, -$19.54.
Slips 3-4 legs: train 3/7 +$114; holdout 0/14 -$140.
Sharp Oct27 (hindsight) ON only modestly better; still negative on frozen picks.
Verdict: no rule passes the holdout. Proposed target: holdout, one leg per player, n>=100, hit% >= break-even of avg price (~53.5% at -115) + 3.5 pts = 57%, ROI >= +3%, both holdout weeks non-negative.
