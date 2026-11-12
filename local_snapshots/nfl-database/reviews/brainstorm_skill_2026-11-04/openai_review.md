# OpenAI review
Model: gpt-5-2025-08-07  
Usage: {"input_tokens": 3488, "input_tokens_details": {"cache_write_tokens": 0, "cached_tokens": 0}, "output_tokens": 5594, "output_tokens_details": {"reasoning_tokens": 2688}, "total_tokens": 9082}

Below is a tight review of SKILL.md against your scenario‑first philosophy, with concrete line-level edits you can paste, plus specific judgment-risk spots to shore up.

1) What’s strong (scenario-first elements already working)
- Lead with the read: The opening frames the read as a hypothesis and puts data second (good alignment).
- Receiving ladder discipline (Step 4c): Forces possession script → QB vs pressure/blitz → target ladder → route trees → coverage → shell/leaks before naming players. This is exactly the Parker-Washington style flow.
- Small-sample humility (Step 5b): Treats backup-QB throw logs as “a read, not a stat gate,” and disallows quiet cuts on missing data. This prevents game-log vetoes after a good scenario read.
- Red team and postmortem (Steps 10 and 12): Separates READ vs RESULT and requires a counter-case. This is the right scaffolding for a miss audit culture.
- Market mapping (Step 9): Connects scenario type to the right market (receptions vs yards, etc.), reducing mismatch errors.
- Cautions on model overconfidence (Step 8): Warns that 70–80% model “hits” have historically been ~50% in reality.

2) Concrete edits to make it stronger (exact replacements keyed to section/line)
A. Header description (top matter)
- Replace: “...then tests it with data, which can cut it.”
- With: “...then tests it with data, which sizes it and flags disagreements for manual review; only hard constraints can cut.”

B. The read comes first paragraph (first paragraph under “Betting game brainstorm”)
- Replace: “Data that clearly disagrees with a read can cut it; close calls get flagged. Data that agrees sizes it.”
- With: “Data that disagrees flags the read for manual review. Only hard constraints (snap caps, severe weather, clear role caps, bad price vs no‑vig) can cut. Data that agrees sizes it.”

C. Ground rules (bullet 3)
- Replace: “Data that clearly disagrees with a read can cut it; close calls get flagged.”
- With: “Data that disagrees flags the read (no auto‑cuts). Allowed hard cuts: (i) documented snap/rep limits, (ii) severe weather (sustained wind ≥20 mph), (iii) mispriced vs sharp no‑vig worse than −3% edge, (iv) role-cap evidence (e.g., RB1 <60% expected carries for a rush‑over). Document the hard-cut reason.”

- Add a new bullet after bullet 3:
  - “Recent box scores or ‘2-of-5 hit’ game logs are cross‑checks, not gates. They can’t veto a scenario read. Use them only in the miss audit (Step 12) to identify causes and whether those causes persist this week.”

D. Step 2. Game script hypothesis (end of section; add a controlling instruction)
- Add: “Quantify plays and dropbacks baseline vs flip scripts; commit to a single conservative plays band (e.g., 58–64) to avoid compounding later. If you project more plays due to opponent QB downgrade, explicitly reduce pass rate for positive-lead scripts—don’t multiply plays x pass rate x target share off the same root cause.”

E. Step 4c. Receiving matchup ladder (point 1 and new point 8)
- Replace point 1 (Possession script) with:
  - “Possession script: who has the ball more and why, with a plays estimate for each side (conservative band). If the opponent starts a backup/third‑string QB, write the expected impact on drive length and your plays band, plus any offsetting slower pace.”
- Add a new point 8 at the end:
  - “Edge arithmetic guardrail: Build receptions from one causal chain—Plays → Dropbacks → Target share → Catch rate—once. If pressure drives quick throws and target share up, don’t separately ‘add plays’ for the same pressure story.”

F. Step 5. Box score and recent-form edges (first bullet)
- Replace: “The last 3–4 games’ role: snaps, routes, targets, carries, air yards, red‑zone looks.”
- With: “The last 3–4 games’ role (snaps, routes, targets, carries, air yards, RZ looks). Do not use raw ‘hit/miss’ game-log counts as a gate. Role only.”

G. Step 5b. QB throw log (last sentence)
- Replace: “A small sample (one or two games) is a read, not a stat gate. Flag it as a small sample and leave the call to the user instead of quietly cutting the leg as missing data.”
- With: “A small sample (one or two games) is a read, not a stat gate. Flag it as small‑sample and escalate for manual review; do not auto‑cut.”

H. Step 7. Write the edge (add explicit constraints and price realism)
- Add after “Confidence: strong, lean, or pass.”:
  - “Price realism: map ‘strong’ to a fair no‑vig of roughly −120 or better and ‘lean’ to −105 to −115. If the best available price is worse than the fair, pass (the read can be right while the bet is wrong).”

I. Step 8. Data check (overhaul bullets to enforce flag-not-cut and house gates)
- Replace the entire bullet list with:
  - “- Run the projection and sims; compare to no‑vig at the sharp book (Pinnacle).
     - Agree: size it and pick the rung.
     - Disagree on a strong read: flag for manual review (no auto‑cut). Note exactly which inputs disagree (plays, pass rate, target share, catch rate).
     - Disagree on a lean: usually pass unless a clear pricing edge remains.
     - Hard‑cut only for: (i) snap/rep cap, (ii) severe weather (sustained wind ≥20 mph), (iii) mispriced worse than −3% EV vs no‑vig, (iv) role-cap evidence (e.g., RB1 <60% expected carries for a rush‑over).
     - Treat model probabilities >70% with suspicion; down‑weight unless multiple independent drivers support the read.”

- Add a new Step 8a. House gates (integration, and which are flags vs cuts):
  - “Apply house gates as labeled:
     - 3‑of‑4 line check: flag only.
     - Last‑2 downgrade: flag only.
     - N1 under‑60%‑carry rush‑over: hard‑cut (role‑cap).
     - Edge tiers: flag only.
     - Best‑price shop: pass if you can’t get within 1% of the sharp no‑vig (pricing hard‑cut).
     - Limit slips to 3–4 legs.”

J. Step 9. Choose the market (add rush‑under prior and avoid short alts)
- Add at end: “Calibration prior: rush unders have outperformed historically; weigh them slightly more when script/role/defense align. Avoid short‑priced alts unless used as correlated anchors and still +EV vs no‑vig.”

K. Step 10. Pre‑mortem and red team (strengthen falsification)
- Replace: “For each leg and slip, argue the opposite side for one paragraph: ‘It’s Monday and this lost. Why?’”
- With: “For each leg, produce at least two disconfirming facts (not narratives) that would sink the read (e.g., ‘Opp blitz rate was 12% last 4, not 30%; primary slot CB returned to full snaps’). If either is plausible today, downgrade or pass.”

L. Step 11. Build slips (clarify single‑story rule)
- Add: “Single‑story enforcement: each leg must explicitly list the same base script. Drop any leg that needs the opposite script.”

M. Step 12. Log it and postmortem it (add explicit miss audit and scenario tracking)
- Replace: “Save the written read with its timestamp before kickoff. After the game, grade the READ (was the script right? was the edge right?) separately from the RESULT (did the leg hit?). Note which brainstorm step would have caught each miss, and feed that into the team and player files.”
- With:
  - “Lock the read and timestamp it before kickoff. After the game:
     - Grade the READ (script right/wrong; edge mechanism right/wrong) separately from the RESULT.
     - Miss audit: record the primary cause (role cap, pressure mismatch, shell mismatch, wrong plays band, injury/snap cap, weather, price). Next week, only veto if the same cause is present again; otherwise the prior miss cannot veto a new read.
     - Track scenario drivers: list the 2–3 drivers you claimed (e.g., ‘opponent 3rd‑string QB → +6 plays; heavy blitz → RB/slot targets’) and grade each driver as right/wrong. Aggregate these driver grades across weeks to calibrate the framework.
     - Update calibration: map Strong/Lean labels to realized edges vs no‑vig and maintain hit rates by label.”

N. Output format (DATA CHECK line)
- Replace: “DATA CHECK: model, sim median, no‑vig, agree / flag / cut / drop”
- With: “DATA CHECK: model, sim median, no‑vig, AGREE / FLAG (manual review) / PASS (hard constraint or price) + reason”

O. New micro-guardrails (insert these one-liners where appropriate, e.g., Step 7 or Step 4c)
- Add: “Do not reverse a ladder‑built edge based on a ‘2‑of‑5 hits’ game log. If you’re tempted, write the miss audit cause and check whether it applies this week; if not, proceed or flag, but do not veto on the log.”

3) Parts that could hurt judgment (and where they appear)
- Auto-cuts that violate scenario-first:
  - Ground rules bullet 3 and Step 8 currently allow data to “cut” a strong read. This is how a 2‑of‑5 game log can creep back in as a veto. Fix with the edits above.
- Confirmation bias and unfalsifiable stories:
  - Step 2/Step 4c write rich narratives but don’t force disconfirming evidence. Tighten Step 10 to require two concrete falsifiers. Also require explicit plays band and pressure/blitz rates with sources to avoid slippery stories.
- Double-counting multipliers:
  - Nowhere does the file forbid compounding the same cause into plays x pass rate x target share x catch rate. Add the “Edge arithmetic guardrail” (Step 4c point 8) and Step 2 quantification note. Require one causal chain and conservative offsets (e.g., more plays if leading often reduces pass rate).
- Game-log veto risk:
  - Step 5 references “last 3–4 games’ role” but doesn’t explicitly ban “2‑of‑5 hits” logic. Your Parker-Washington reversal is exactly this failure mode. Fix via Step 5 edit and the new Ground rules bullet on game logs as cross-check only.
- Overconfidence without calibration:
  - “Strong/Lean” aren’t tied to pricing. Add the price realism mapping (Step 7) and require no‑vig comparison in Step 8 to tether confidence to edge size. Step 12’s calibration expansion makes this measurable.
- Missing scenario driver tracking:
  - Step 12 currently grades read vs result but not the component drivers (possession, blitz, shell). Without this, the miss audit can become an excuse machine. Add the driver‑level grading and the “only veto if the same cause reappears” rule.
- Conflicts with house stat gates:
  - House rules say gates flag, not cut, except for the RB1 under‑60% carry share rush‑over. SKILL.md currently treats disagreements as potential cuts. Add Step 8a to encode which gates are flags vs hard cuts and integrate best‑price shopping as a cut for price only.
- Price discipline gaps:
  - Step 9 cautions on short alts but doesn’t enforce passing on bad price. Add explicit “pass if >−3% EV vs no‑vig” in Step 8 and “within 1% of sharp no‑vig” in Step 8a.
- Weather hard stop clarity:
  - Step 6 flags 15+ mph but doesn’t define hard constraints. Promote severe weather (≥20 mph sustained) to a hard‑cut list in Step 8 and Ground rules to standardize.
- Slip mixing risk:
  - Step 11 advises one story but doesn’t enforce it. Add a check that each leg explicitly shares the same base script; otherwise drop.

Bottom line: Does SKILL.md, as written, implement scenario‑first?
- Partially. It starts with a scenario and builds a coverage/pressure-led ladder, which is correct. But the “data can cut” language (Ground rules, Step 8, Output) and the lack of an explicit “game logs are cross‑checks only” clause allow the very failure you flagged (reversing a sound scenario read due to a 2‑of‑5 log).
- Apply the edits above—especially the flag‑not‑cut policy, the miss‑audit veto rule, and the anti‑double‑counting guardrails—to lock the file into your philosophy and prevent future Parker‑Washington reversals.