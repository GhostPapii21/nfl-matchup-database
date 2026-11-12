"""Fails (exit 1) if any saved game play log is missing from defender_ledger.csv (Ghost6/Rico, Nov 3 2026)."""
import csv,glob,os,re,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
led={r['game'] for r in csv.DictReader(open(os.path.join(ROOT,'defender_ledger.csv')))}
miss=[]
for f in glob.glob(os.path.join(ROOT,'playlogs','2026_wk*','*.csv')):
    m=re.fullmatch(r'([A-Z]{2,3})_([A-Z]{2,3})\.csv',os.path.basename(f))
    if m and f"{m[1]}@{m[2]}" not in led: miss.append(f"{m[1]}@{m[2]} ({os.path.relpath(f,ROOT)})")
print("LEDGER COVERAGE: " + ("OK, every logged game is in the ledger" if not miss else "FAIL, logged but not in ledger: " + ", ".join(sorted(miss))))
sys.exit(1 if miss else 0)
