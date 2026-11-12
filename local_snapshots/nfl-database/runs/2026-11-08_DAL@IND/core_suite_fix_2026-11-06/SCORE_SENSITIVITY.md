# Paired score sensitivity
The reported DAL 27.2 to 18.8 comparison did not hold random draws fixed: the previous trial seed hashed all input bytes, including rotation weights. It is therefore confounded by RNG reseeding and does not identify a true role-efficiency effect. No fitted efficiency coupling exists in these tables.

Version 2 derives a common game/trial seed independently of input contents. A fixed draw splits off a player-attribution RNG, so role sampling cannot consume team terminal, catch, yard, clock, or scoring randomness. Explicit role-efficiency coupling is rejected as unfitted; role-identity-conditioned usage/outcome tables are rejected too. Input/source hashes remain in forecast identity.

paired_runs.json compares equal_depth (equal eligible), empirical MLE, and selected robust rotation weights. Usage/outcome distributions, target-depth distributions, availability, seed 20261108 and all non-rotation model content are identical; half overrides are consistently removed in all three variants. Each has n=5 and an exact seeded repeat. Team period stats (including play counts and points) are identical in every paired trial. IDs/provenance differ as required by changed inputs. Means: DAL 21.8, IND 13.6 for all three. Player attribution may differ; the synthetic invariant test explicitly requires it to differ.

This establishes engineering invariance, not forecast accuracy. The original 8.4-point difference is not promoted as a causal efficiency estimate.
