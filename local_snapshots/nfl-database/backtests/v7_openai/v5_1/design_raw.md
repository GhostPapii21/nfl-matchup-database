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

```python
#!/usr/bin/env python3
"""Frozen v5.1 selector/execution policy. No outcomes read or grading performed."""
import argparse
import hashlib
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent
KEY = ["week", "game_id", "gsis", "market", "side", "line"]
PICK_COLS = ["week", "game", "game_id", "player", "gsis", "market",
             "side", "line", "price", "stake", "reason_kept"]
SLIP_COLS = ["slip_id", "week", "leg_no", "game_id", "gsis",
             "market", "side", "line", "price"]


def load(path):
    df = pd.read_csv(path, dtype={"game_id": str, "gsis": str})
    for c in ["game_id", "gsis", "market", "side"]:
        df[c] = df[c].astype("string").str.strip()
    for c in ["market", "side"]:
        df[c] = df[c].str.lower()
    df["week"] = pd.to_numeric(df["week"], errors="raise").astype(int)
    df["line"] = pd.to_numeric(df["line"], errors="raise")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    return df


def decimal(price):
    return 1 + price / 100 if price > 0 else 1 + 100 / (-price)


def primary(df):
    tags = df["tag"].astype("string").str.strip().str.upper()
    known = {"PRIMARY", "SAVED_READ", "RECONSTRUCTED", "GROK_ON_SAVED_GAME"}
    if tags.isna().any() or not tags.isin(known).all():
        raise ValueError("Unexpected tag; resolve PRIMARY semantics explicitly.")
    # An explicitly labeled PRIMARY dataset takes precedence if supplied.
    if tags.eq("PRIMARY").any():
        return df.loc[tags.eq("PRIMARY")].copy()
    saved = set(map(tuple, df.loc[
        tags.eq("SAVED_READ"), ["week", "game_id"]].to_numpy()))
    on_saved = pd.Series(
        [(w, g) in saved for w, g in zip(df.week, df.game_id)],
        index=df.index)
    keep = tags.eq("SAVED_READ") | (tags.eq("RECONSTRUCTED") & ~on_saved)
    return df.loc[keep].copy()


def make_slips(picks):
    rows = []
    for week, group in picks.groupby("week", sort=True):
        pool = group.loc[group.price.notna()].sort_values(
            ["game_id", "gsis", "market", "side", "line"],
            kind="mergesort")
        for number in range(1, 6):
            chosen, games, players = [], set(), set()
            for idx, row in pool.iterrows():
                if row.game_id in games or row.gsis in players:
                    continue
                chosen.append(idx)
                games.add(row.game_id)
                players.add(row.gsis)
                if len(chosen) == 4:
                    break
            if len(chosen) < 3:
                break
            for leg_no, idx in enumerate(chosen, 1):
                row = pool.loc[idx]
                rows.append({
                    "slip_id": f"v5_1_w{week}_{number}", "week": week,
                    "leg_no": leg_no, "game_id": row.game_id,
                    "gsis": row.gsis, "market": row.market,
                    "side": row.side, "line": row.line, "price": row.price})
            pool = pool.drop(index=chosen)
    return pd.DataFrame(rows, columns=SLIP_COLS)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--week", type=int)
    parser.add_argument("--reads", type=Path, default=BASE / "data/v5_reads.csv")
    parser.add_argument("--lines", type=Path, default=BASE / "data/lines_noact.csv")
    args = parser.parse_args()
    reads, lines = load(args.reads), load(args.lines)
    if args.week is not None:
        reads = reads.loc[reads.week.eq(args.week)].copy()
        lines = lines.loc[lines.week.eq(args.week)].copy()
        if reads.empty:
            raise ValueError("No reads for requested week.")
    reads = primary(reads)
    required = KEY + ["player", "game"]
    if reads[required].isna().any().any():
        raise ValueError("PRIMARY identity/line fields must be complete.")
    if reads.duplicated(KEY).any():
        raise ValueError("Duplicate PRIMARY selection.")
    if not reads.market.isin(["rushyds", "recyds", "rushrecyds"]).all():
        raise ValueError("Unexpected market.")
    if not reads.side.isin(["over", "under"]).all():
        raise ValueError("Unexpected side.")
    confidence = reads.confidence.astype("string").str.strip().str.lower()
    verdict = reads.verdict.astype("string").str.strip().str.lower()
    picks = reads.loc[
        (confidence.eq("strong") & verdict.eq("agree")).fillna(False)].copy()
    snap = pd.to_datetime(lines["snap"], utc=True, errors="coerce")
    kickoff = pd.to_datetime(lines["kickoff"], utc=True, errors="coerce")
    valid_price = np.isfinite(lines.price) & lines.price.ne(0)
    valid = snap.notna() & kickoff.notna() & snap.lt(kickoff) & valid_price
    quotes = lines.loc[valid].dropna(subset=KEY + ["book"]).copy()
    quotes["decimal"] = quotes.price.map(decimal)
    quotes["book"] = quotes.book.astype(str)
    quotes = quotes.sort_values(
        KEY + ["decimal", "book"], ascending=[True] * len(KEY) + [False, True],
        kind="mergesort").drop_duplicates(KEY)
    best = {tuple(row[k] for k in KEY): row
            for row in quotes.to_dict("records")}
    prices, reasons = [], []
    for row in picks.to_dict("records"):
        price = row["price"]
        if pd.notna(price) and (not np.isfinite(price) or price == 0):
            raise ValueError("Invalid original saved price.")
        source = "original_saved" if pd.notna(price) else "unpriced"
        quote = best.get(tuple(row[k] for k in KEY))
        if quote is not None:
            if pd.isna(price) or decimal(quote["price"]) > decimal(price):
                price, source = quote["price"], "saved_book:" + quote["book"]
        prices.append(price)
        reasons.append("strong+agree;same_line;" + source)
    picks["price"], picks["reason_kept"], picks["stake"] = prices, reasons, 10.0
    picks = picks.sort_values(
        ["week", "game_id", "gsis", "market", "side", "line"],
        kind="mergesort").reset_index(drop=True)
    out = BASE / "out"
    out.mkdir(parents=True, exist_ok=True)
    files = [(out / "v5_1_picks.csv", picks[PICK_COLS]),
             (out / "v5_1_slips.csv", make_slips(picks))]
    for path, frame in files:
        frame.to_csv(path, index=False, float_format="%.10g", lineterminator="\n")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        path.with_suffix(path.suffix + ".sha256").write_text(
            f"{digest}  {path.name}\n", encoding="utf-8")
        print(f"{path}: {len(frame)} rows; sha256={digest}")


if __name__ == "__main__":
    main()
```

Forward invocation:

```bash
python v5_1.py --week 10 --reads data/week10_reads.csv --lines data/week10_lines.csv
```

The hashes establish file identity; externally timestamping and archiving them before kickoff establishes the pre-kick lock.