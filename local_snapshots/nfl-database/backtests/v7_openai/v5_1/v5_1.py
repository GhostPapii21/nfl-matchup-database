
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
