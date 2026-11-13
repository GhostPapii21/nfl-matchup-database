# Depth signal: forcing stale charted players (W10 fit, data through 2026 W9)

Training DM log likelihood (higher is better), other parameters at the frozen W10 fit:

| slot | K | force=False (fitted) | force=top (RB2/WR3/TE1) | force=True |
|---|---|---|---|---|
| carry | 0 | -24377.7 | -24460.0 | -24985.4 |
| carry | 1 | -24802.1 | -24817.2 | -25184.8 |
| carry | 99 | -25694.0 | -25694.0 | -25694.0 |
| target | 0 | -73143.1 | -73618.0 | -75783.7 |
| target | 1 | -75371.0 | -75507.2 | -76642.7 |
| target | 99 | -78328.4 | -78328.4 | -78328.4 |

WAS Week 10 base shares (before availability), fitted rule vs force=True (sensitivity, not fitted):

| slot | player | depth chart | share fitted | share force=True |
|---|---|---|---|---|
| carry | R.White | RB1 | 0.571 | 0.371 |
| carry | A.Ekeler | RB2 | 0.357 | 0.232 |
| carry | J.Croskey-Merritt | RB4 | 0.000 | 0.226 |
| carry | J.McNichols | RB5 | 0.000 | 0.099 |
| target | S.Diggs | WR1 | 0.177 | 0.136 |
| target | C.Okonkwo | TE1 | 0.163 | 0.126 |
| target | A.Williams | WR2 | 0.140 | 0.108 |
| target | T.Burks | WR3 | 0.111 | 0.085 |
| target | R.White | RB1 | 0.104 | 0.080 |
| target | V.Jefferson | WR4 | 0.100 | 0.077 |
| target | T.McLaurin | WR7 | 0.000 | 0.051 |
| target | A.Ekeler | RB2 | 0.059 | 0.046 |
| target | D.Brown | WR6 | 0.000 | 0.040 |
| target | J.Croskey-Merritt | RB4 | 0.000 | 0.034 |
| target | B.Sinnott | TE2 | 0.000 | 0.031 |
| target | J.Bates | TE3 | 0.000 | 0.026 |
| target | C.Yankoff | TE4 | 0.022 | 0.017 |
| target | L.McCaffrey | WR5 | 0.022 | 0.017 |
| target | J.McNichols | RB5 | 0.000 | 0.015 |
| target | J.Lane | WR8 | 0.000 | 0.013 |
| target | J.Bradley | not charted | 0.006 | 0.004 |
