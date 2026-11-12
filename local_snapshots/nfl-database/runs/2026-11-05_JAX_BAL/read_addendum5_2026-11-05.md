# Read addendum 5 — TNF JAX @ BAL, written 2026-11-05 ~16:55 ET (pre-kick, locks before pricing the final card)
Builds on the locked read runs/2026-11-05_JAX@BAL_r2/brainstorm_read.md (sha256 on file) and r5 addenda 1-4. Only what changed is written here.

## What changed since the Nov 4 read
1. WEATHER (new, decisive). NWS hourly for M&T Bank Stadium (api.weather.gov, update 2026-11-05 15:53 ET): 8 PM 76%, 9 PM 75%,
   10 PM 52% showers and thunderstorms, wind 5 mph, 67 F. tools/weather_forecast.py 16:43 ET: precip 75% (NWS) -> WEATHER FLAG.
   Morning runs had 34-45% (no flag). Open-air game -> every passing/receiving OVER in this game is cut by rule; rushing first.
2. Injuries (ESPN API 16:43 ET): Lamar Jackson and Tyler Huntley now officially on IR; Fagnano starts; Hawkins (S) OUT;
   Wiggins (CB) Q (illness); JAX Tuten Q (ankle/foot, DNP all week), Travon Walker Q; Meyers and Rodriguez no designation.
3. Market (Odds API 16:50 ET, FD/DK/Pinnacle): JAX -9.5/-10, total 39.5 (no move), Henry 71.5 FD / 68.5 Pin, Lawrence rush 12.5 FD/Pin,
   Meyers 38.5, Strange 32.5, Washington 60.5 FD. Tuten has no rush line (off the board while Q).

## Script with rain
BASE (unchanged, firmer): JAX leads by halftime; rain plus a UDFA QB means BAL cannot throw its way back; both teams lean run;
JAX kills clock in the 2H. Total pressure is DOWN.
FLIP A (slog) is now MORE likely: rain + two run-first plans -> 17-10 type game.
FLIP B (BAL close via Henry volume) is also a bit more likely than Nov 4: rain raises BAL's run share, so Henry's carry count
may NOT fall even if BAL trails. This is the main risk to the Henry under (edge player 1).

## Edge players (max 2) after the weather
1. Derrick Henry rush UNDER stays the read, but weakened: rain + run-first BAL plan pushes his carries up (Flip B). Flag, not a reversal.
2. Trevor Lawrence rush UNDER 12.5 (moves up from the Nov 3 slip story): JAX leads, run-heavy rain script, Lawrence's designed runs
   are rare (27 of 80 yds), so the under needs him to avoid one long scramble. Kills it: BAL pressure (24% PROXY, 7.3% scramble rate
   allowed) flushes him into one 15+ yd scramble. Script-dependent on JAX leading.
(Justice Hill receptions OVER stays a read but is not on this run: not on key_players.md.)

## Receivers
- Strange / Washington overs: CUT by the weather rule, not by the read. If the rain clears by kickoff, they re-enter at the Phase 15 recheck.
- Meyers: rain + JAX run lean argues for the under; he is also Lawrence's top target when pressured (7 of 23 pressured attempts, LOW-SAMPLE).
  Under only if the price/models agree; no over (weather).

## Pre-mortem
- Lawrence U12.5 loses on a single broken-play scramble, most likely on 3rd down in the 1H while the game is still close.
- Henry U loses if BAL keeps it within one score into Q4 and feeds him 20+ in the rain.
- The whole JAX-controls story loses if Fagnano's turnovers do not come and JAX's own offense stalls in the rain (Flip A
  hurts JAX spread legs, helps every under).
