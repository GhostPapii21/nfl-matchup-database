import time,json
exec(open('deep.py').read().split('b=open')[0])
M="gpt-6.1-sol"
b=open('brief_deep.md').read(); c=b[69000:]
revs=open('section_reviews.md').read()
q="You are a senior sports-betting quant and experimental-design reviewer. This is the final chunk (4/4) of a brief on an amateur NFL player-prop (yardage, 3-4 leg slips) backtest program. Write a detailed, frank section review of THIS chunk: what the evidence shows, design flaws, leakage/overfitting risks, what should have been done, and concrete fixes. Cite numbers/files from the chunk. Note uncertainties. Compact Markdown, <=1200 words.\n\n"+c
t,m=call(M,q,"high",3300); revs+="\n\n## Section review 4/4\n\n"+(t or "(empty)")
open('section_reviews.md','w').write(revs); time.sleep(70)
share=open('chatgpt_share_rico_2026-11-03.md').read()
ctx="""Our backtest evidence: confidence check: every sim version Brier worse than market (0.248) and coin flip; NO-SHRINK (no shrink toward market) made calibration worse. v6 (Grok brainstorm+pro-edge) 2026 wk3-8: READS 66-90 42.3% ROI -19.1%, overs 53-76 41.1% -22.0% (overs-heavy, 113 of 139 priced), slips 0/30; GATED 41.5% -21.6%. Only steady positive: every main rush-yds under 296-229 56.4% +2.8% (5 of 6 weeks positive or flat). Rico-approved rules: N1, N2, the #3/#4 receiver rule (depth-receiver rule), the -250-or-shorter price flag, §7 3-of-4, +3 vs no-vig, SCHEME_EDGE flag, mirror overs, no TDs, no passing yards."""
q2="Below is a ChatGPT audit (written for the user) of missed MNF CHI@SEA legs, plus our backtest evidence. Review each proposal: (a) does our data support or contradict it, (b) would it undo a Rico-approved rule (explicitly check N1, N2, the #3/#4 rule, the -250 flag) — mark YES/NO per proposal, (c) keep / test-first / reject. Watch for proposals that push more overs or less shrink. <=900 words, Markdown table plus notes.\n\n"+ctx+"\n\n=== ChatGPT audit ===\n"+share
t2,_=call(M,q2,"high",3000)
revs+="\n\n## Review of Rico's ChatGPT MNF audit (vs backtest data)\n\n"+(t2 or "(empty)")
open('section_reviews.md','w').write(revs); time.sleep(70)
s="Using ONLY these section reviews of an NFL player-prop backtest program (constraints: free data only, no PFF/film/coverage data, Odds API ~250 credits/week, no historical odds pulls until Dec; plays FanDuel/PrizePicks 3-4 leg yardage slips, no TDs, no passing yards), write the complete deep-dive: 1) statistical design fix list (sample size/power, overfitting, leakage protocol, CLV, calibration); 2) per-version review: v1 100k sims, rulebook replays wk6-8, Rico method wk8, v5, v6; 3) verdict on the ChatGPT MNF audit proposals, marking which would undo Rico-approved rules (N1, N2, #3/#4 rule, -250 flag); 4) per-game reasoning checklist; 5) slip/correlation advice; 6) top-5 plan under constraints; 7) uncertainties. Markdown, <=2200 words.\n\n"+revs
for eff in ["high","medium"]:
  t,m=call(M,s,eff,3800)
  if t and len(t)>1000: break
  time.sleep(70)
open('response_deep.md','w').write(f"# Deep-dive review ({m}; per-chunk reviews in section_reviews.md)\n\n"+(t or "(empty)"))
print("DONE",flush=True)
