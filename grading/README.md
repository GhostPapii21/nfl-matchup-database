# Post-game grading loop (work order item 6)

Research only. Nothing here sets `projection_ready`, changes a model weight or formula, or calls a paid API.

## Run it after each game

    python -m grading.grade --game 2026_10_WAS_NYG            # dry run, prints a summary
    python -m grading.grade --game 2026_10_WAS_NYG --write    # writes grading/results/<game>.jsonl + .summary.json

Then commit `grading/results/`. The command refuses (exit 2, nothing written) when the game isn't final in
nflverse yet, or when no pregame packet was generated before kickoff. nflverse usually posts final
play-by-play the morning after a game, so run it the next day. `--offline` reuses cached nflverse files.

To read the freezes from another branch, for example Blitz's closing freeze, use `--freeze-ref`:

    git fetch origin research/multibook-price-feed-2026-11-12
    python -m grading.grade --game 2026_10_WAS_NYG --freeze-ref origin/research/multibook-price-feed-2026-11-12 --write

`--freeze-ref` takes any git ref. By default the grader reads freezes from the current working tree. Files are
listed with `git ls-tree` and read with `git show`. They're data only, so no code from that ref is imported or
run. A ref that can't be read stops the command with exit 2. Each quote's source is recorded as
`git:<ref>@<sha>:<path>`.

## What gets graded

Everything comes from the **pregame packet committed before kickoff**. The grader walks git history for
`pregame/packets/<game>/packet.json` and takes the newest version whose `generated_utc` is before kickoff, so a
packet refresh after the game can't leak in.

| Kind | Where in the packet | Graded against |
| --- | --- | --- |
| `flagged_prop` | every `books.prop_check` row. The side is the sign of `baseline_minus_line` | actual stat, win/loss/push, closing line, CLV, edge rule |
| `player_projection` | `matchup.*.player_baselines` (weighted mean, per stat) | actual stat, error |
| `team_projection` | `team_projection.samplers.*` points, margin, total | final score, error |
| `team_market` | sampler probabilities (`home_covers_market_spread`, `over_market_total`, `home_win`) | result, closing line, CLV, edge rule |

**Actual results** come from nflverse public releases (games, play-by-play, weekly rosters, snap counts). These
are the same free URLs `pregame/sources.py` uses. Player stats are summed from play-by-play by nflverse player
id. Checked against nflverse's own weekly player stats for 2026_09_BUF_MIN, 223 of 224 stat values matched. The
one miss (5 receiving yards) is the kind of gap a lateral or a stat correction causes. Players are matched by
**full name plus team** through the nflverse roster. Packet short names (`M.Nabers`) are matched by initial,
surname and team. Anything other than exactly one match is `unknown`.

**Closing line** means the latest snapshot this repo saved **before kickoff** from the same book. It comes from
the packet's book section, `pregame/line_history/<game>.jsonl`, or a saved freeze in
`pregame/price_freezes/*_<AWAY>@<HOME>/freeze_*.json`, which is read as data and never run. Each row records the
snapshot source, its pull time and how many minutes before kickoff it was taken. Both freeze formats are
parsed: schema 1 (`freeze_*.json`, a `rows` list) and schema 2 (`freeze_v2_*.json`, `markets` plus `consensus`).
When a v1 and a v2 file share a pull time, the v2 quote wins. A book marked `"no props"` doesn't count as a quote.

**Grading is per book.** A prop's closing line and CLV come only from the **same book's** own pre-kickoff
quotes. No other book's line and no consensus line is ever substituted. The freeze consensus is copied into
`closing_consensus_reference_only` for reference. When a market's consensus says `"no consensus"`, that field's
value is `"unknown"` and the reason is kept. It's never treated as missing data to fill in or as zero, and the
per-book lines in that market are still used. If no snapshot exists, the
closing line is `unknown` and is never estimated. CLV is only measured against a snapshot saved **after** the bet
quote. Otherwise it is `unknown`, because comparing a quote with itself would count as a fake tie.

CLV sign conventions: an Over gains when the close is higher than the bet line, an Under when it's lower, and a
spread side when its own handicap at the close is worse than the one it got. Spread lines are stored as the
home handicap. When the line didn't move, CLV is the closing no-vig probability minus the bet-time no-vig
probability from the same book.

## The edge-label rule (exactly as ordered)

A prop is labelled `edge` only when **all three** hold:

1. **Model beats best retail break-even.** The model probability is greater than the lowest break-even among
   retail books quoting the same line for that side. Reference books (`pinnacle`) are excluded. The packet
   carries **no per-prop model probability** today, so this condition fails for every prop until the packet adds
   `model_prob_over` / `model_prob_under` to a `prop_check` row.
2. **Projected volume supports the number.** It uses the packet's volume field for the market (targets for
   receiving and receptions, carries for rushing, pass attempts for passing). Rate is the player's stat weighted
   mean divided by the volume weighted mean, and the volume needed is line ÷ rate. An Over passes only if the
   player's median game volume (`p50`) is above that, and an Under only if it's below. A missing field, or fewer
   than `min_volume_games` games, fails.
3. **Positive closing-line record over a holdout.** The holdout is props of the same market type graded in
   **earlier** games only, one entry per (game, market, side), using the best-priced quote. The record is
   positive when at least `min_holdout_props_per_market_type` props (default **30**) have a known CLV **and**
   more beat the close than didn't. A 50/50 split doesn't count as positive.

Labels: `edge` when all three pass. `research only, not validated` when that market type has no holdout yet,
which is every market type today. `not an edge` when a holdout exists but the rule fails. Player and team
projections are always `research only, not validated`. Team markets can't pass condition 2, because the volume
test applies to player props only.

Settings live in `grading/config.json`. Changing them is a reviewed change.

## Output format (`grading/results/<game>.jsonl`)

There is one JSON object per graded item. Each figure (`projection`, `model_prob`, `bet_line`, `bet_price`,
`best_retail_break_even`, `actual`, `closing_line`, `closing_price`) is stored as
`{"value", "source", "pulled_utc", ...}`. Missing data is the string `"unknown"`, never 0 and never null. A
player who's on the roster but has no snaps and no plays is `unknown`, because that could be a did-not-play. A
stat counts as a real 0 only when snaps or plays show the player was in the game. Every row carries
`projection_ready: false`.

## Limits

- The packet has no calibrated per-prop probability, so no prop can be an `edge` yet, even after a holdout exists.
- CLV needs a snapshot saved after the packet's last pre-kickoff refresh, such as the T-60 to T-90 freeze in
  work order item 2. Without one, CLV is `unknown` and that prop doesn't count toward the holdout.
- Nothing runs this on a schedule yet. Workflow files can't be added by the bot. Run it by hand or from a
  routine the day after each game.
- Prop markets the packet doesn't carry (pass attempts, completions, rush attempts) are graded once the packet
  or a freeze includes them. The grader already supports those stat types.
