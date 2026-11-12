#!/bin/bash
# usage: gate_compare.sh <outdir>  — runs gate on temp copies of the 16 Nov 1 runs (never touches runs/*/gate_output.txt)
OUT=$1; mkdir -p $OUT; DB=/workspace/nfl-database; T=$(mktemp -d)
for f in $DB/audits/2026-11-01_lessons/gate_after2/*.txt; do r=$(basename $f .txt)
  now=$(head -1 $f | sed -E 's/.*checked_at=([0-9-]+) ([0-9:]+).*/\1T\2/')
  cp -r "$DB/runs/$r" "$T/$r"; (cd $DB/tools && python3 run_gate.py "$T/$r" --now $now >/dev/null 2>&1)
  sed "s#$T#$DB/runs#" "$T/$r/gate_output.txt" > "$OUT/$r.txt"; done; rm -rf $T
