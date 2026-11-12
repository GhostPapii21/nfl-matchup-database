# Ghost6 — Phase 6 Live monitoring plan — Sun Nov 1 2026
Applicability (per GAME_SCRIPT Phase 6):
- This walk does **not** restart the canceled 15-minute game checks, change weekly audits, or create schedules.
- Monitoring runs only through the already-authorized routines in the parent conversation: the 6:10 AM refresh, the 7:05 AM re-vet, the 8:00 AM Betting Hub agreement, and the 11:30 AM inactives check.

| Time (ET) | Check | Action |
|---|---|---|
| 6:10 AM (BetGuru routine) | Re-pull PFR/FTN, final card | Diff vs this snapshot. Any changed defender number goes in a new file |
| 7:05 AM (Ghost6 routine) | Independent re-vet | Re-run Phases 1–4 deltas. Confirm Lamb/Gibbs stack decisions are queued for Rico |
| 8:00 AM | Betting Hub agreement | Rico decides. No action without his explicit approval |
| **11:30 AM** | Inactives/injury report | Bowers, Puka, Gibbs active? Pickens (Ticket 1 and 2), Donte Jackson, DJ Glaze, Elijah Wilkinson, Dee Winters replacement. Recheck line moves (>0.5 or 20 cents → reprice) |
| **11:30 AM (90 min pre 1:00 kick)** | **Approval gate** | Ask Rico to approve each Q/inactive that matters: Pickens (Lamb volume ↑ if out), Glaze (Bowers), Jackson (Puka, 4:05 game) |
| 2:35 PM (90 min pre 4:05 LAC@LAR) | Puka / Donte Jackson final | If Puka is out → leg voids or drops. If Jackson is out → Hart/Still mapping, keep 70 |
| In-game | None (canceled polling stays canceled) | Grading only after final |

Kill/drop rules at inactives:
- Bowers out: drop. Glaze out: keep 5+, no move up.
- Puka out: drop. Gibbs out: drop. If Gibbs is limited in-week, use the 50 alt.
- Pickens out: Lamb keeps 5+ (more volume).
- Winters' replacement LB in coverage: map him with PFR. If he allows <60% comp, McBride drops to 6+.
