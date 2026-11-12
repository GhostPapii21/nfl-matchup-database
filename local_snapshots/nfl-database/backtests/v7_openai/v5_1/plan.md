## A) PLAN — pre-registration

**Freeze this specification before inspecting per-pick outcomes.** This is a conservative candidate, not a demonstrated improvement.

### Changes

1. **Actionability gate: retain only `confidence=strong` AND `verdict=agree`.**  
   A narrative lean is not sufficient justification for paying bookmaker margin. A flagged read has unresolved contradictory evidence; v5 preserved those reads, but v5.1 will not stake them. Missing/unrecognized values fail the gate. Apply uniformly across markets and sides—no rush-under exclusion or overs preference.

2. **Same-line execution improvement.**  
   Use the highest decimal payout among the original saved price and saved quotes matching week, game, GSIS, market, side, and exact line. Replacement quotes must have valid timestamps strictly before kickoff. Never change the line or use later prices. If no price exists, retain the unpriced selection under v5’s grading convention.

3. **Reproducible slip allocation.**  
   Because original slip membership is not supplied, construct fresh slips deterministically: at most five per week, three or four priced legs, one leg/game and one leg/player per slip, no reused selection. Alphabetical/key ordering—not estimated probability—determines allocation. Slips are secondary, descriptive results.

### Success criterion

Primary comparison: **Weeks 3–6**, using the shared harness and unchanged scoring.

Declare success only if v5.1:
- retains at least **40 settled, priced legs**;
- has **positive ROI**;
- improves both ROI and dollar profit over v5 PRIMARY.

Otherwise classify as failure or insufficient coverage—not a reason to revise thresholds. Report Weeks 7–8 separately, including counts, profit, ROI, hit rate, and uncertainty; do not tune against them. Neither historical split is a fresh confirmatory test.

### Unchanged

Locked reads and PRIMARY precedence; player, market, side, and line; $10 flat singles; push/settlement conventions; unpriced-leg treatment. No `PRO_EDGE`, zone labels, outcome-derived features, or player-game data are used. No new LLM calls.

### Week 10+ shadow protocol

Use the same read schema and frozen code. Before each included game’s kickoff, archive code/input hashes and an externally timestamped picks/slips SHA-256 manifest. Maintain an append-only ledger: selection ID, read tag/confidence/verdict, original and executed price, quote book/snapshot/kickoff, stake, exclusion reason, manifest hash, then separately settlement and closing price.

Judge only after **100 settled priced singles spanning at least eight weeks**, against concurrent frozen v5 PRIMARY. Review once at that endpoint; promotion requires positive ROI and higher dollar profit than v5. Operational kill: any as-of/hash violation. Performance kill: cumulative singles loss reaches **$200**; stop prospectively and count that stop in reporting.

**Forward-only prompt proposals:** make missing information explicit rather than inventing injury fallout; structure `must_be_true` and `kills_it`; distinguish data contradiction from missing data. These are a separate shadow arm, not part of this backtest.

## B) `v5_1.py`



Forward invocation:

```bash
python v5_1.py --week 10 --reads data/week10_reads.csv --lines data/week10_lines.csv
```

The hashes establish file identity; externally timestamping and archiving them before kickoff establishes the pre-kick lock.