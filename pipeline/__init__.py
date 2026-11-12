"""NFL-56: repo-as-source-of-truth layer over the pregame packets.

freshness.py  max-age policy for every pregame input and the check that applies it
hooks.py      fail-closed hooks for pieces other owners are building (NFL-43, rocket, four-book feed, inactives)
phases.py     one command per phase of the 15-phase ledger, recording filled / missing / stale inputs
sim100k.py    the single 100k-trial entry point (NFL-43 possession engine); refuses (exit 2) unless every gate passes
slate.py      what the scheduled workflow runs: phases + the 100k gate for every game in the slate

Research only. Nothing here sets projection_ready to true.
"""
