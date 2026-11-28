"""Human-readable decision board. Numbers are formatted; they are not rounded into a pick."""

from __future__ import annotations

SECTIONS = (
    ("strong_reads", "Strong Reads"),
    ("soft_leans", "Soft Leans"),
    ("avoids", "Avoids"),
    ("no_plays", "No Plays"),
)


def _num(value, digits=4):
    if value is None:
        return "—"
    if isinstance(value, float):
        return f"{value:.{digits}f}"
    return str(value)


def _projection(value) -> str:
    if not isinstance(value, dict) or not value:
        return "not published"
    parts = []
    for key in ("mean", "median", "mean_margin_home", "sd", "p_home_win", "p_away_win", "p_tie"):
        if key in value:
            parts.append(f"{key}={_num(value[key])}")
    return ", ".join(parts) if parts else "not published"


def render_markdown(report: dict) -> str:
    lines = [
        f"# Decision board — {report.get('game_id')}",
        "",
        "RESEARCH ONLY. projection_ready=false. Not a validated projection, not a pick, no stakes.",
        "An edge figure, when present, is model probability minus the two-way no-vig price. It is not an edge claim.",
        "This board does not target a number of picks and does not compute a hit rate. Empty sections stay empty.",
        "",
        f"- Kickoff (UTC): {report.get('kickoff_utc')}",
        f"- projection_ready: {str(report.get('projection_ready')).lower()}",
        f"- edge_claim_allowed: {str(report.get('edge_claim_allowed')).lower()}",
        f"- Section counts: {report.get('section_counts')}",
        "",
        "## Market snapshots",
        "",
        "Book, market, line, price, timestamp and missing-line status are recorded for every comparison. Implied probability and edge are blank when either input is missing.",
        "",
        "| subject | market | side | book | line | price | timestamp | missing line | model P | implied | no-vig | edge | edge status |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for comparison in report.get("market_snapshots") or []:
        for snapshot in comparison.get("snapshots") or []:
            lines.append(
                "| {subject} | {market} | {side} | {book} | {line} | {price} | {timestamp} | {missing} | {model} | {implied} | {novig} | {edge} | {status} |".format(
                    subject=snapshot.get("subject"),
                    market=snapshot.get("market"),
                    side=snapshot.get("side"),
                    book=snapshot.get("book") or "—",
                    line=_num(snapshot.get("line"), 1) if snapshot.get("line") is not None else "—",
                    price=_num(snapshot.get("price"), 0) if snapshot.get("price") is not None else "—",
                    timestamp=snapshot.get("timestamp_utc") or "—",
                    missing="yes" if snapshot.get("missing_line") else "no",
                    model=_num(snapshot.get("model_probability")),
                    implied=_num(snapshot.get("implied_probability")),
                    novig=_num(snapshot.get("no_vig_probability")),
                    edge=_num(snapshot.get("edge")),
                    status=snapshot.get("edge_status"),
                )
            )
    lines.extend(["", "## Model probabilities", ""])
    for comparison in report.get("market_snapshots") or []:
        lines.append(
            f"### {comparison.get('thesis_id')} — consensus {comparison.get('model_consensus')}"
        )
        lines.append(
            f"Threshold probability: {_num(comparison.get('threshold_probability'))} ({comparison.get('threshold_basis')}). "
            f"Disagreement: {_num(comparison.get('model_disagreement'))}."
        )
        if not comparison.get("models"):
            lines.append("No model probability was published.")
        for view in comparison.get("models") or []:
            lines.append(
                f"- {view.get('model_id')}: P={_num(view.get('probability'))}, n={view.get('n')}, "
                f"calibration={view.get('calibration_status')}, seed={view.get('seed')}"
            )
        if comparison.get("model_consensus") == "disagree":
            lines.append("Disagreement withheld the threshold. The probabilities above were not averaged.")
        lines.append("")
    lines.extend(["## Adversarial review", ""])
    for review in report.get("adversarial_reviews") or []:
        red = review["red_team"]
        lines.append(f"### {review.get('thesis_id')} — {review.get('decision')} / {review.get('section')}")
        lines.append("Supporting evidence:")
        support = red["supporting_evidence"] or [{"text": "none supplied"}]
        for item in support:
            lines.append(f"- {item.get('text')} ({item.get('source', 'unspecified')})")
        lines.append("Contradicting evidence:")
        contra = red["contradicting_evidence"] or [{"text": "none supplied"}]
        for item in contra:
            lines.append(f"- {item.get('text')} ({item.get('source', 'unspecified')})")
        lines.append("Red-team checks:")
        suppression = red["defensive_suppression"] or [{"path": "none supplied", "material": False}]
        for item in suppression:
            lines.append(
                f"- Defensive suppression: {item.get('path') or item.get('detail') or 'none supplied'}; "
                f"material={item.get('material')}"
            )
        role = red["role_volume_fragility"]
        lines.append(
            f"- Role/volume fragility: tag={role.get('tag')}, fragile={role.get('fragile')}. {role.get('reason')}"
        )
        efficiency = red["efficiency_dependence"]
        lines.append(
            f"- Efficiency dependence: depends={efficiency.get('depends_on_efficiency')}, "
            f"support cited={efficiency.get('support_cited')}"
        )
        for label, key in (("Injury", "injury"), ("Weather", "weather"), ("Game script", "game_script")):
            block = red[key]
            detail = block.get("detail") or block.get("reason") or ""
            lines.append(f"- {label} contingency: {detail}".rstrip())
        sample = red["sample_quality"]
        lines.append(
            f"- Sample quality: n={sample.get('n')}, withheld={sample.get('withheld')}, "
            f"blocks_reads={sample.get('blocks_reads')}. {sample.get('limitation') or ''}".rstrip()
        )
        for reason in review.get("reasons") or []:
            lines.append(f"- Decision: {reason}")
        lines.append("")
    lines.extend([
        "## Final board",
        "",
        "Columns: player/team, market, projection, threshold probability, role tag, confidence, model consensus, warnings.",
        "",
    ])
    for key, title in SECTIONS:
        rows = (report.get("board") or {}).get(key) or []
        lines.append(f"### {title}")
        lines.append("")
        if not rows:
            lines.append("None.")
            lines.append("")
            continue
        lines.append("| player/team | market | side | projection | threshold probability | role tag | confidence | model consensus | warnings |")
        lines.append("|---|---|---|---|---|---|---|---|---|")
        for row in rows:
            warning = "; ".join(row.get("warnings") or [])
            lines.append(
                f"| {row.get('player_or_team')} | {row.get('market')} { _num(row.get('line'), 1) if row.get('line') is not None else '' } | "
                f"{row.get('side')} | {_projection(row.get('projection'))} | {_num(row.get('threshold_probability'))} | "
                f"{row.get('role_tag') or '—'} | {row.get('confidence')} | {row.get('model_consensus')} | {warning} |"
            )
            for reason in row.get("reasons") or []:
                lines.append(f"| | | | | | | | | {reason} |")
        lines.append("")
    lines.extend(["## Abstentions", ""])
    for item in report.get("abstentions") or []:
        lines.append(f"- {item.get('thesis_id')} ({item.get('decision')}): {' '.join(item.get('reasons') or [])}")
    lines.extend(["", "## Boundaries", ""])
    for note in report.get("notes") or []:
        lines.append(f"- {note}")
    lines.append("")
    return "\n".join(lines)
