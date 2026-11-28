"""Join executed component outputs. Methods stay separate; nothing is averaged."""
from __future__ import annotations

from sunday import PROJECTION_READY, SCHEMA
from sunday.context import git_revision
from sunday.jsonutil import sha256_obj


def _arr(trials: dict | None, key: str):
    import numpy as np

    if not trials or key not in trials:
        return None
    return np.asarray(trials[key], dtype=float)


def settle(home, away, line: float, market: str) -> dict | None:
    import numpy as np

    if home is None or away is None or line is None:
        return None
    home = np.asarray(home, dtype=float)
    away = np.asarray(away, dtype=float)
    if home.size == 0 or home.size != away.size:
        return None
    if market == "spread":
        adj = (home - away) + float(line)
    elif market == "total":
        adj = (home + away) - float(line)
    else:
        return None
    push = np.abs(adj) < 1e-9
    win = (adj > 0) & ~push
    p_win = float(win.mean())
    p_push = float(push.mean())
    p_lose = float((~win & ~push).mean())
    decisive = 1.0 - p_push
    return {
        "n": int(home.size),
        "p_win": round(p_win, 4),
        "p_push": round(p_push, 4),
        "p_lose": round(p_lose, 4),
        "p_win_decisive": round(p_win / decisive, 4) if decisive > 0 else None,
        "line": float(line),
        "market": market,
    }


def partition_scripts(trials: dict | None, home: str, away: str, home_spread) -> dict:
    """Split possession trials into three script buckets. A trial is in one bucket.

    The rule uses the pregame home spread only to name the favorite. It does not
    refit the trials. Play counts, pass/run mix, and per-player opportunity are
    not on these arrays, so those fields stay unsupported.
    """
    import numpy as np

    base = {
        "entrypoint": "sunday.assemble:partition_scripts",
        "source_engine": "possession_engine_v0",
        "pooled": False,
        "play_pass_run": "NOT_SUPPORTED",
        "player_opportunity": "NOT_SUPPORTED",
        "td_opportunity": "NOT_SUPPORTED",
        "rule": (
            "Favorite is the side laid the points (home spread < 0 means home is favored). "
            "underdog_chases: favorite led by 8+ at half and the final favorite margin is 3 or less. "
            "favorite_controls: favorite led by 7+ at half and won by 7+. "
            "competitive: final favorite margin within 7 and halftime margin within 10, and not already classed. "
            "other_unclassified: the rest. Regulation scores. Buckets do not overlap."
        ),
    }
    needed = ("h1_home", "h1_away", "reg_home", "reg_away")
    if not trials or any(k not in trials for k in needed):
        return {**base, "status": "NOT_RUN", "ran": False,
                "reason": "Possession trials were not returned, so script buckets were not built."}
    if home_spread is None or float(home_spread) == 0:
        return {**base, "status": "NOT_SUPPORTED", "ran": False,
                "reason": "No favorite on the pregame home spread, so the three named scripts are not assigned."}
    h1_h, h1_a = _arr(trials, "h1_home"), _arr(trials, "h1_away")
    reg_h, reg_a = _arr(trials, "reg_home"), _arr(trials, "reg_away")
    n = int(reg_h.size)
    home_favored = float(home_spread) < 0
    favorite = home if home_favored else away
    dog = away if home_favored else home
    fav_h1 = h1_h if home_favored else h1_a
    dog_h1 = h1_a if home_favored else h1_h
    fav_reg = reg_h if home_favored else reg_a
    dog_reg = reg_a if home_favored else reg_h
    half = fav_h1 - dog_h1
    final = fav_reg - dog_reg
    underdog = (half >= 8) & (final <= 3)
    controls = (~underdog) & (half >= 7) & (final >= 7)
    competitive = (~underdog) & (~controls) & (np.abs(final) <= 7) & (np.abs(half) <= 10)
    other = ~(underdog | controls | competitive)
    masks = {
        "underdog_chases": underdog,
        "favorite_controls": controls,
        "competitive": competitive,
        "other_unclassified": other,
    }
    if int(sum(int(m.sum()) for m in masks.values())) != n:
        raise RuntimeError("script buckets overlap or drop trials")
    branches = {}
    for name, mask in masks.items():
        idx = np.flatnonzero(mask)
        branches[name] = {
            "n": int(idx.size),
            "share": round(float(idx.size / n), 4) if n else None,
            "regulation": {
                "home": _summ(reg_h[idx]),
                "away": _summ(reg_a[idx]),
                "favorite_margin": _summ(final[idx]),
            },
            "half": {
                "home": _summ(h1_h[idx]),
                "away": _summ(h1_a[idx]),
            },
        }
    return {
        **base,
        "status": "OK",
        "ran": True,
        "n": n,
        "favorite": favorite,
        "underdog": dog,
        "home_spread": float(home_spread),
        "branches": branches,
    }


def _summ(values) -> dict:
    import numpy as np

    arr = np.asarray(values, dtype=float)
    if arr.size == 0:
        return {"n": 0}
    return {
        "n": int(arr.size),
        "mean": round(float(arr.mean()), 4),
        "p50": round(float(np.median(arr)), 4),
    }


def _method_trials(receipts: dict) -> list[dict]:
    found = []
    poss = (receipts.get("possession") or {}).get("output") or {}
    if poss.get("ran") and poss.get("trials"):
        found.append({
            "engine_id": "possession_engine_v0",
            "method": "simulate_games",
            "scope": "regulation",
            "seed": poss.get("seed"),
            "n": poss.get("n_completed"),
            "trials": poss["trials"],
            "home_key": "reg_home",
            "away_key": "reg_away",
        })
    period = (receipts.get("period") or {}).get("output") or {}
    for name, method in (period.get("methods") or {}).items():
        if not method.get("ran"):
            continue
        for scope, home_key, away_key in (
            ("regulation", "reg_home", "reg_away"),
            ("final_including_ot", "fg_home", "fg_away"),
        ):
            found.append({
                "engine_id": "period_engine_v0",
                "method": name,
                "scope": scope,
                "seed": method.get("seed"),
                "n": method.get("n"),
                "trials": method.get("trials") or {},
                "home_key": home_key,
                "away_key": away_key,
            })
    return found


def thresholds(receipts: dict) -> dict:
    quotes = ((receipts.get("market_lines") or {}).get("output") or {}).get("quotes") or []
    methods = _method_trials(receipts)
    comparisons = []
    for quote in quotes:
        market = quote.get("market")
        kind = "spread" if market == "spread" else ("total" if market == "total" else None)
        line = quote.get("line")
        no_vig = quote.get("no_vig") if isinstance(quote.get("no_vig"), dict) else {}
        row = {
            "market": market,
            "book": quote.get("book"),
            "line": line,
            "prices": quote.get("prices"),
            "no_vig": quote.get("no_vig"),
            "last_update": quote.get("last_update"),
            "source": quote.get("source"),
            "models": [],
        }
        if kind is None or line is None:
            row["edge"] = None
            row["reason"] = "No executed player-prop engine. Documented sim_v6 did not run, so no model probability or edge is attached."
            comparisons.append(row)
            continue
        target = None
        if kind == "spread":
            # Home cover probability uses the home team's no-vig at this line.
            prices = quote.get("prices") or {}
            # The home abbreviation is not on the quote; callers compare by key later.
            target = no_vig
        else:
            target = no_vig.get("Over")
        for method in methods:
            settled = settle(
                _arr(method["trials"], method["home_key"]),
                _arr(method["trials"], method["away_key"]),
                float(line),
                kind,
            )
            if settled is None:
                continue
            entry = {
                "engine_id": method["engine_id"],
                "method": method["method"],
                "scope": method["scope"],
                "seed": method["seed"],
                "n": method["n"],
                "probability": settled,
            }
            if kind == "total" and target is not None:
                entry["no_vig_reference"] = "Over"
                entry["edge"] = round(settled["p_win"] - float(target), 4)
            else:
                entry["edge"] = None
                entry["edge_reason"] = "Spread no-vig is stored by team. The home-team edge is attached in disagreement using the packet home abbreviation."
            row["models"].append(entry)
        comparisons.append(row)
    return {
        "status": "OK" if methods else "NOT_RUN",
        "ran": bool(methods),
        "entrypoint": "sunday.assemble:thresholds",
        "pooled": False,
        "note": "Each engine and method keeps its own probability. Edges are model minus that book's no-vig at the same line. Methods are not averaged.",
        "comparisons": comparisons,
    }


def spread_edges(receipts: dict, home: str) -> list[dict]:
    """Home-cover edge for each executed method against each spread quote, same line."""
    out = []
    block = thresholds(receipts)
    for row in block["comparisons"]:
        if row.get("market") != "spread" or row.get("line") is None:
            continue
        no_vig = row.get("no_vig") or {}
        ref = no_vig.get(home)
        for model in row.get("models") or []:
            prob = (model.get("probability") or {}).get("p_win")
            edge = None if ref is None or prob is None else round(float(prob) - float(ref), 4)
            out.append({
                "engine_id": model["engine_id"],
                "method": model["method"],
                "scope": model["scope"],
                "book": row["book"],
                "line": row["line"],
                "last_update": row.get("last_update"),
                "model_p_home_cover": prob,
                "no_vig_home": ref,
                "edge": edge,
            })
    return out


def disagreement(receipts: dict, home_spread) -> dict:
    rows = []
    if home_spread is None:
        return {"status": "NOT_RUN", "ran": False, "reason": "no home spread", "methods": []}
    for method in _method_trials(receipts):
        if method["scope"] not in ("regulation",):
            continue
        settled = settle(
            _arr(method["trials"], method["home_key"]),
            _arr(method["trials"], method["away_key"]),
            float(home_spread),
            "spread",
        )
        if settled is None:
            continue
        rows.append({
            "engine_id": method["engine_id"],
            "method": method["method"],
            "scope": method["scope"],
            "seed": method["seed"],
            "n": method["n"],
            "p_home_cover": settled["p_win"],
            "p_push": settled["p_push"],
            "line": float(home_spread),
        })
    probs = [r["p_home_cover"] for r in rows]
    span = None if len(probs) < 2 else round(max(probs) - min(probs), 4)
    return {
        "status": "OK" if rows else "NOT_RUN",
        "ran": bool(rows),
        "line": None if home_spread is None else float(home_spread),
        "methods": rows,
        "span": span,
        "material": bool(span is not None and span >= 0.08),
        "pooled": False,
        "note": "Span is the max minus min home-cover probability across executed methods. It is not a blended probability.",
    }


def red_team(ctx: dict, pre: dict, receipts: dict, scripts: dict, disagree: dict) -> dict:
    challenges = []
    roster = (receipts.get("engine_roster") or {}).get("output") or {}
    sim_v6 = roster.get("documented_sim_v6") or {}
    if not sim_v6.get("ran"):
        challenges.append({
            "id": "sim_v6_absent",
            "severity": "no_play",
            "claim": "The required three-method sim_v6 triad did not run.",
            "evidence": sim_v6.get("reason"),
        })
    if not (roster.get("lightning") or {}).get("ran"):
        challenges.append({
            "id": "lightning_absent",
            "severity": "gap",
            "claim": "Lightning was not executed.",
            "evidence": (roster.get("lightning") or {}).get("reason"),
        })
    challenges.append({
        "id": "uncalibrated",
        "severity": "no_play",
        "claim": "Probabilities are not a fitted calibration.",
        "evidence": "known_flags calibration_fitted_claim is false. Period bias is UNIMPLEMENTED. Possession is an empirical resample.",
    })
    gate = ((receipts.get("sim100k_preflight") or {}).get("output") or {}).get("gate") or {}
    if not gate.get("ok"):
        challenges.append({
            "id": "sim100k_refused",
            "severity": "gap",
            "claim": "The gated 100k entry point refused this game.",
            "evidence": (gate.get("reasons") or [])[:8],
        })
    freshness = ((receipts.get("phase_ledger") or {}).get("output") or {}).get("freshness") or []
    stale = [f"{r.get('source')} {r.get('status')}" for r in freshness if r.get("status") not in ("FRESH", "NOT_REQUIRED")]
    if stale:
        challenges.append({
            "id": "freshness_gaps",
            "severity": "gap",
            "claim": "One or more packet sources are not fresh at this as-of.",
            "evidence": stale,
        })
    fields = ((receipts.get("matchup_fields") or {}).get("output") or {}).get("fields") or {}
    missing_fields = [name for name, row in fields.items() if row.get("status") == "MISSING"]
    if missing_fields:
        challenges.append({
            "id": "matchup_fields_missing",
            "severity": "gap",
            "claim": "Defender assignment or route fields have no accepted source.",
            "evidence": missing_fields,
        })
    research = (receipts.get("packet_research") or {}).get("output") or {}
    shells = research.get("coverage_shells") or {}
    if not shells.get("ran_shell_model"):
        challenges.append({
            "id": "coverage_shells",
            "severity": "gap",
            "claim": "Coverage shells were not produced by a shell model.",
            "evidence": shells.get("note"),
        })
    prior = research.get("prior_packet_projection") or {}
    if prior.get("includes_prior_season"):
        challenges.append({
            "id": "prior_projection_season_mix",
            "severity": "fragility",
            "claim": "The packet's stored team projection includes a prior season. This command's period run does not use that object.",
            "evidence": prior.get("note"),
        })
    if disagree.get("material"):
        challenges.append({
            "id": "method_disagreement",
            "severity": "fragility",
            "claim": "Executed methods disagree by 8 points or more on the home cover probability.",
            "evidence": disagree.get("methods"),
        })
    market = (receipts.get("market_lines") or {}).get("output") or {}
    consensus_total = market.get("consensus_total")
    pinnacle_totals = [q.get("line") for q in market.get("quotes") or []
                       if q.get("market") == "total" and q.get("book") == "pinnacle"]
    if consensus_total is not None and pinnacle_totals and float(pinnacle_totals[0]) != float(consensus_total):
        challenges.append({
            "id": "total_line_sources_differ",
            "severity": "fragility",
            "claim": "The schedule consensus total and the timestamped Pinnacle total are different numbers.",
            "evidence": {"consensus_total": consensus_total, "pinnacle_total": pinnacle_totals[0]},
        })
    poss = (receipts.get("possession") or {}).get("output") or {}
    if poss.get("limitations"):
        challenges.append({
            "id": "possession_limitations",
            "severity": "fragility",
            "claim": "The possession engine published its own limitations on this run.",
            "evidence": poss.get("limitations"),
        })
    if scripts.get("play_pass_run") == "NOT_SUPPORTED":
        challenges.append({
            "id": "script_opportunity_unsupported",
            "severity": "gap",
            "claim": "Script buckets have scores only. They do not carry play, pass/run, or player-opportunity distributions.",
            "evidence": scripts.get("rule"),
        })
    challenges.append({
        "id": "projection_ready_false",
        "severity": "no_play",
        "claim": "projection_ready is false. This packet is research, not a pick.",
        "evidence": "Set by sunday.assemble and known_flags. This command does not flip it.",
    })
    return {
        "status": "OK",
        "ran": True,
        "entrypoint": "sunday.assemble:red_team",
        "as_of": ctx["as_of"].isoformat(),
        "leakage_check": pre.get("leakage"),
        "challenges": challenges,
        "no_play_ids": [c["id"] for c in challenges if c["severity"] == "no_play"],
    }


def board(ctx: dict, review: dict, disagree: dict) -> dict:
    home, away = ctx.get("home"), ctx.get("away")
    no_plays = [
        {"market": "spread", "selection": f"{home} cover", "role": "team",
         "reason": "research-only; projection_ready is false"},
        {"market": "spread", "selection": f"{away} cover", "role": "team",
         "reason": "research-only; projection_ready is false"},
        {"market": "total", "selection": "over", "role": "team",
         "reason": "research-only; projection_ready is false"},
        {"market": "total", "selection": "under", "role": "team",
         "reason": "research-only; projection_ready is false"},
        {"market": "player_props", "selection": "all listed props", "role": "player",
         "reason": "tools/sim_v6.py did not run, so no player threshold probability was executed"},
    ]
    avoids = []
    for item in review.get("challenges") or []:
        if item["severity"] in ("fragility", "gap"):
            avoids.append({
                "id": item["id"],
                "role": "warning",
                "claim": item["claim"],
                "action": "avoid treating this as a settled read",
            })
    return {
        "status": "OK",
        "ran": True,
        "entrypoint": "sunday.assemble:board",
        "projection_ready": False,
        "research_only": True,
        "wager_authorized": False,
        "strong_reads": [],
        "soft_leans": [],
        "avoids": avoids,
        "no_plays": no_plays,
        "model_agreement": {
            "span": disagree.get("span"),
            "material_disagreement": disagree.get("material"),
            "methods": disagree.get("methods"),
        },
        "withheld_reason": (
            "Strong reads and soft leans stay empty while projection_ready is false. "
            "Method probabilities stay on the model layer and are not promoted."
        ),
    }


def _component_rows(receipts: dict) -> list[dict]:
    rows = []
    for name, receipt in receipts.items():
        rows.append({
            "component": name,
            "status": receipt.get("status"),
            "ran": receipt.get("ran"),
            "entrypoint": receipt.get("entrypoint"),
            "duration_sec": receipt.get("duration_sec"),
            "error": receipt.get("error"),
            "output_sha256": receipt.get("output_sha256"),
        })
    return rows


def game_context(ctx: dict) -> dict:
    schedule = dict(ctx.get("schedule") or {})
    for key in ("away_score", "home_score", "result", "total", "overtime"):
        schedule.pop(key, None)
    kick = ctx.get("kickoff_utc")
    return {
        "game_id": ctx["game_id"],
        "season": ctx["season"],
        "week": ctx["week"],
        "away": ctx["away"],
        "home": ctx["home"],
        "kickoff_utc": None if kick is None else kick.isoformat(),
        "kickoff_source": ctx.get("kickoff_source"),
        "schedule_kickoff_utc": (ctx.get("schedule") or {}).get("kickoff_utc"),
        "as_of": ctx["as_of"].isoformat(),
        "schedule": schedule,
        "schedule_omits_final_scores": True,
        "packet_generated_utc": None if not ctx.get("packet") else ctx["packet"].get("generated_utc"),
        "listed_qbs": None if not ctx.get("packet") else (ctx["packet"].get("game") or {}).get("listed_qbs"),
        "coaches": None if not ctx.get("packet") else (ctx["packet"].get("game") or {}).get("coaches"),
        "roof": None if not ctx.get("packet") else (ctx["packet"].get("game") or {}).get("roof"),
    }


def manifest(ctx: dict, pre: dict, receipts: dict, run_id: str) -> dict:
    market = (receipts.get("market_lines") or {}).get("output") or {}
    home_spread = market.get("consensus_home_spread")
    if home_spread is None and ctx.get("packet"):
        home_spread = (ctx["packet"].get("market") or {}).get("home_spread")
    poss_trials = ((receipts.get("possession") or {}).get("output") or {}).get("trials")
    scripts = partition_scripts(poss_trials, ctx.get("home"), ctx.get("away"), home_spread)
    disagree = disagreement(receipts, home_spread)
    prices = thresholds(receipts)
    review = red_team(ctx, pre, receipts, scripts, disagree)
    card = board(ctx, review, disagree)
    edges = spread_edges(receipts, ctx.get("home"))
    failed = [name for name, rec in receipts.items() if rec.get("status") == "FAILED"]
    if failed:
        status = "PARTIAL"
    elif not (receipts.get("possession") or {}).get("ran") or not (receipts.get("period") or {}).get("ran"):
        status = "PARTIAL"
    else:
        status = "COMPLETE"
    body = {
        "schema": SCHEMA,
        "run_id": run_id,
        "game_id": ctx["game_id"],
        "status": status,
        "projection_ready": PROJECTION_READY,
        "research_only": True,
        "wager_authorized": False,
        "command": ctx.get("spec", {}).get("command"),
        "code_revision": git_revision(ctx["root"]),
        "trials_requested": ctx.get("trials"),
        "preflight": pre,
        "layers": {
            "1_game_context": game_context(ctx),
            "2_fanout": _component_rows(receipts),
            "3_matchup": {
                "fields": (receipts.get("matchup_fields") or {}).get("output"),
                "team_sides": (receipts.get("packet_research") or {}).get("output"),
            },
            "4_players": {
                "sides": {
                    team: {
                        "players": (side or {}).get("players"),
                        "injuries": (side or {}).get("injuries"),
                        "snap_note": "snap_share is set only on an exact name match to offense_snap_share",
                    }
                    for team, side in (((receipts.get("packet_research") or {}).get("output") or {}).get("sides") or {}).items()
                },
                "possession_player_box": ((receipts.get("possession") or {}).get("output") or {}).get("player_box_summary"),
            },
            "5_game_scripts": scripts,
            "6_models": {
                "roster": (receipts.get("engine_roster") or {}).get("output"),
                "possession": (receipts.get("possession") or {}).get("output"),
                "period": (receipts.get("period") or {}).get("output"),
                "sim100k_preflight": (receipts.get("sim100k_preflight") or {}).get("output"),
                "prior_packet_projection_not_this_process": (
                    ((receipts.get("packet_research") or {}).get("output") or {}).get("prior_packet_projection")
                ),
            },
            "7_distributions_and_market": {
                "disagreement": disagree,
                "spread_edges": edges,
                "quotes": prices,
            },
            "8_red_team": review,
            "9_board": card,
            "10_execution": {
                "components": _component_rows(receipts),
                "phase_summary": ((receipts.get("phase_ledger") or {}).get("output") or {}).get("summary"),
                "phase15": ((receipts.get("phase_ledger") or {}).get("output") or {}).get("phase15"),
            },
        },
    }
    # Full component payloads live beside the manifest. The layer hash covers the joined body.
    body["output_sha256"] = sha256_obj(body)
    return body


def refusal_manifest(ctx: dict, pre: dict, run_id: str) -> dict:
    body = {
        "schema": SCHEMA,
        "run_id": run_id,
        "game_id": ctx["game_id"],
        "status": "REFUSED",
        "projection_ready": False,
        "research_only": True,
        "wager_authorized": False,
        "command": (ctx.get("spec") or {}).get("command"),
        "code_revision": git_revision(ctx["root"]),
        "preflight": pre,
        "layers": {"1_game_context": game_context(ctx)},
        "note": "Critical preflight failed. Simulators were not started.",
    }
    body["output_sha256"] = sha256_obj(body)
    return body


def render_report(body: dict) -> str:
    ctx = (body.get("layers") or {}).get("1_game_context") or {}
    lines = [
        f"# {body.get('game_id')} research packet",
        "",
        "RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.",
        "",
        f"- Status: {body.get('status')}",
        f"- Run: `{body.get('run_id')}`",
        f"- Command: `{body.get('command')}`",
        f"- Code: {(body.get('code_revision') or {}).get('commit')} dirty={(body.get('code_revision') or {}).get('dirty')}",
        f"- As of: {ctx.get('as_of')}",
        f"- Kickoff: {ctx.get('kickoff_utc')}",
        f"- {ctx.get('away')} at {ctx.get('home')}, season {ctx.get('season')} week {ctx.get('week')}",
        "",
        "## Fan-out",
        "",
        "| Component | Status | Ran | Seconds |",
        "| --- | --- | --- | --- |",
    ]
    for row in (body.get("layers") or {}).get("2_fanout") or []:
        lines.append(
            f"| {row.get('component')} | {row.get('status')} | {row.get('ran')} | {row.get('duration_sec')} |"
        )
    pre = body.get("preflight") or {}
    if pre.get("critical"):
        lines += ["", "## Critical refusal", ""]
        lines += [f"- {item}" for item in pre["critical"]]
    scripts = (body.get("layers") or {}).get("5_game_scripts") or {}
    lines += ["", "## Game scripts", "", scripts.get("rule") or scripts.get("reason") or ""]
    branches = scripts.get("branches") or {}
    if branches:
        lines += ["", f"Favorite {scripts.get('favorite')}, underdog {scripts.get('underdog')}, n={scripts.get('n')}.",
                  "", "| Script | Trials | Share | Home reg mean | Away reg mean |", "| --- | --- | --- | --- | --- |"]
        for name, branch in branches.items():
            reg = branch.get("regulation") or {}
            lines.append(
                f"| {name} | {branch.get('n')} | {branch.get('share')} | "
                f"{(reg.get('home') or {}).get('mean')} | {(reg.get('away') or {}).get('mean')} |"
            )
        lines.append("")
        lines.append("Play, pass/run, and player-opportunity distributions: NOT_SUPPORTED on these buckets.")
    models = (body.get("layers") or {}).get("6_models") or {}
    roster = models.get("roster") or {}
    sim_v6 = roster.get("documented_sim_v6") or {}
    lines += [
        "",
        "## Models",
        "",
        f"- Documented sim_v6 (`tools/sim_v6.py`): ran={sim_v6.get('ran')}. {sim_v6.get('reason')}",
        f"- Lightning: ran={(roster.get('lightning') or {}).get('ran')}.",
        f"- Main: no separate entrypoint. Possession is not relabeled Main.",
        f"- simv56 scratch: ran={(roster.get('simv56_scratch') or {}).get('ran')} (not used as sim_v6).",
    ]
    poss = models.get("possession") or {}
    if poss:
        reg = poss.get("regulation") or {}
        lines.append(
            f"- Possession `{poss.get('config_id')}` n={poss.get('n_completed')} seed={poss.get('seed')} "
            f"status={poss.get('status')}. Regulation mean home {(reg.get('home') or {}).get('mean')}, "
            f"away {(reg.get('away') or {}).get('mean')}."
        )
    period = models.get("period") or {}
    for name, method in (period.get("methods") or {}).items():
        summary = ((method.get("summaries") or {}).get("reg") or {})
        lines.append(
            f"- Period `{name}` n={method.get('n')} seed={method.get('seed')} ran={method.get('ran')} "
            f"reg home mean {summary.get('home_mean')} away mean {summary.get('away_mean')}."
        )
    if period.get("bias"):
        lines.append(f"- Period bias: {period['bias'].get('status')} ran={period['bias'].get('ran')}.")
    disagree = ((body.get("layers") or {}).get("7_distributions_and_market") or {}).get("disagreement") or {}
    lines += ["", "## Disagreement", "",
              f"Home-cover span across methods: {disagree.get('span')} (material={disagree.get('material')}). Methods are listed, not blended."]
    for row in disagree.get("methods") or []:
        lines.append(
            f"- {row.get('engine_id')} {row.get('method')} p_home_cover={row.get('p_home_cover')} n={row.get('n')} seed={row.get('seed')}"
        )
    review = (body.get("layers") or {}).get("8_red_team") or {}
    lines += ["", "## Red team", ""]
    for item in review.get("challenges") or []:
        lines.append(f"- [{item.get('severity')}] {item.get('claim')}")
    card = (body.get("layers") or {}).get("9_board") or {}
    lines += ["", "## Board", "", card.get("withheld_reason") or "", "",
              f"Strong reads: {len(card.get('strong_reads') or [])}. Soft leans: {len(card.get('soft_leans') or [])}. "
              f"Avoids: {len(card.get('avoids') or [])}. No plays: {len(card.get('no_plays') or [])}."]
    for row in card.get("no_plays") or []:
        lines.append(f"- No play: {row.get('market')} {row.get('selection')} — {row.get('reason')}")
    lines += ["", "## Reproducible", "", f"Manifest sha256 `{body.get('output_sha256')}`.", ""]
    return "\n".join(lines)
