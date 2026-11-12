# Generate Key Takeaways + Game Overview carousel — status

**POSTGAME ONLY.** Do not invent AI takeaways.

## Generate Key Takeaways
| Attempt | Result |
|---|---|
| Firecrawl markdown | Button/control text only: `Generate Key Takeaways▾` — **no expanded AI text** |
| Author github.io mirror | Section titles `Biggest Team Differences` / `Box Score Standouts` visible as labels — **no generated body text captured** |
| curl HTML | No `articleBody`; interactive widgets |

**BROWSER_NEEDED (parent):** click **Generate Key Takeaways** in a real browser, save rendered output + screenshot. Until then: takeaways = **NOT_RETRIEVED** (not “unavailable forever”).

Treat any future AI takeaways as **secondary generated commentary**, not verified coverage / personnel / scheme.

## Game Overview carousel
Firecrawl **did** capture public carousel panel text (score timeline, plays/yards/EPA, first downs, downs efficiency, drives, red zone, etc.) without clicking each slide — widget text was in the DOM/render.

User/parent-attested UI values (Rico 9:03) that **match** Firecrawl public extraction:
- Q3 cumulative **20–3**; Q3 period **3–0**
- Gross pass **242 vs 57**; expl. pass yards **168 vs 0**; air yards **155 vs −1**
- Net yards **319 vs 227**; rush **77 vs 163**

## Screenshots from latest parent/agent context
Copied under `screenshots/` from `/cursor/stores/user/grok-bot/agents/0bcd66da-bca8-4d8c-80f0-a827a79ab95b/assets/`.

**Inventory (visual ID):** these files are mostly **NFL Next Gen Stats / NFL Pro / PFR** panels — **not** the PFF Game Overview carousel screenshots described in the message. Paths preserved for provenance of what was in the turn; PFF carousel screenshots still needed from parent browser if distinct.

| File | Identified UI |
|---|---|
| user_shot_01_* | NFL Pro homepage / subscribe |
| user_shot_02–09,11–12 | Next Gen Stats charts/highlights/receiving |
| user_shot_04 | NGS Mark Andrews |
| user_shot_13 | PFR Advanced Defense through week 8 |
| user_shot_10,14 | small / unclear — see files |

PFF numeric reconciliation uses Firecrawl/mirror text + Rico attestation, not those NGS shots.
