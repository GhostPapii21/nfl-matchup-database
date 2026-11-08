"""Snapshot established local evidence only; never retrieve or certify a forecast."""
from collections import Counter
import copy
import csv
from datetime import datetime, timezone
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parent
RESEARCH = ROOT.parents[1]
CORE = Path('/workspace/wt-nfl-sim-core-2026-11-06')
LIVE = Path('/workspace/nfl-database/live/2026-11-05_JAX_BAL')
ODDS = Path('/workspace/nfl-database/runs/2026-11-05_JAX@BAL_r6/odds')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def save_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + '\n')


def main():
    stamp = datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')
    package = json.loads((RESEARCH / 'source_run_gate/MANIFEST.json').read_text())
    spec = importlib.util.spec_from_file_location('local_source_readiness', RESEARCH / 'source_run_gate/readiness.py')
    gate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gate)
    provenance = []

    def snapshot(path, use):
        # Fixed caller-supplied paths only. No directory crawling, URLs or auth.
        data = path.read_bytes()
        target = ROOT / 'snapshots' / path.name
        if target.exists() and target.read_bytes() != data:
            raise ValueError(f'snapshot conflict: {target}')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        provenance.append(dict(original_path=str(path), snapshot_path=str(target.relative_to(ROOT)),
            sha256=sha(data), byte_size=len(data), local_read_at_utc=stamp,
            original_mtime_utc=datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(),
            mtime_is_availability_evidence=False, intended_use=use,
            external_retrieval_this_pass=False))
        return data

    espn = json.loads(snapshot(LIVE / 'raw/espn_summary_401873037.json', 'EVIDENCE_ONLY_POSTGAME'))
    live_meta = json.loads(snapshot(LIVE / 'live_meta.json', 'Saved retrieval declaration; not certified availability'))
    audit = snapshot(LIVE / 'actual_role_coverage_audit.md', 'EVIDENCE_ONLY_POSTGAME; missingness retained')
    snapshot(LIVE / 'notes/te_usage_comparison.md', 'EVIDENCE_ONLY_POSTGAME; receiving does not establish personnel/routes')
    snapshot(LIVE / 'notes/evidence_nov5/nfl_gamebook_JAX_at_BAL_20261105.txt', 'EVIDENCE_ONLY_POSTGAME')
    snapshot(LIVE / 'notes/evidence_nov5/nfl_gamebook_JAX_at_BAL_20261105.pdf', 'EVIDENCE_ONLY_POSTGAME; official-source saved bytes, no new fetch')
    quote_inputs = [ODDS / 'odds_jaxbal_game.csv', LIVE / 'period_q1_q2_q3_fd_dk_cleared.csv', LIVE / 'period_line_grades.csv']
    quote_files = [(path, list(csv.DictReader(io.StringIO(snapshot(path, 'SAVED_ONLY; scores/grades are hindsight').decode('utf-8-sig'))))) for path in quote_inputs]
    competition = espn['header']['competitions'][0]
    records = [dict(source_event_id=espn['header']['id'], source_event_namespace='ESPN',
        provider_season=espn['header']['season']['year'], provider_week=espn['header']['week'],
        scheduled_start_raw=competition['date'], status=competition['status'],
        competitors=[dict(source_team_id=c['id'], abbreviation=c['team']['abbreviation'],
                          home_away=c['homeAway'], score=c.get('score')) for c in competition['competitors']],
        provider_timestamps=espn['meta'], saved_retrieval_declaration=live_meta,
        canonical_game_id=None, canonical_crosswalk_status='MISSING', intended_use='EVIDENCE_ONLY_POSTGAME',
        source_snapshot='snapshots/espn_summary_401873037.json')]
    save_json(ROOT / 'records/espn_summary.json', records)
    # These are statements from an existing local audit, not measured charting.
    for token in ('UNKNOWN', 'MISSING'):
        assert token in audit.decode('utf-8')
    save_json(ROOT / 'records/role_coverage_audit.json', [dict(
        source_event_alias='401873037', coverage='UNKNOWN', routes='MISSING',
        personnel_11='MISSING', personnel_12='MISSING', personnel_13='MISSING',
        receiving_yard_discrepancy='RETAINED; see original audit',
        intended_use='EVIDENCE_ONLY_POSTGAME', source_snapshot='snapshots/actual_role_coverage_audit.md')])
    save_json(ROOT / 'records/gamebook_notes.json', [dict(
        source_event_alias='401873037', intended_use='EVIDENCE_ONLY_POSTGAME',
        canonical_game_id=None, source_snapshots=[
            'snapshots/nfl_gamebook_JAX_at_BAL_20261105.txt',
            'snapshots/nfl_gamebook_JAX_at_BAL_20261105.pdf', 'snapshots/te_usage_comparison.md'],
        asof_certification='NOT_CERTIFIED; no pregame source-availability evidence')])
    # Preserve saved quote identity/timestamps and original row numbers. Hindsight
    # result/score/grade columns stay in snapshots and never enter quote records.
    quote_columns = set('game_id snapshot_id line_timing is_in_play_line book market period side selection selection_team player point line_point price price_american last_update_utc pulled_utc snapshot_pulled_utc snapshot_last_update_utc source_file source_note reconstruction absent_flag'.split())
    for tool, book in [('FD', 'fanduel'), ('DK', 'draftkings'), ('Pinnacle', 'pinnacle')]:
        quotes = [dict(book=book, source_row_number=i, source_snapshot='snapshots/' + path.name,
                       raw_quote_fields={k: v for k, v in row.items() if k in quote_columns},
                       status='SAVED_ONLY', usable_for_run=False,
                       source_event_alias='401873037', canonical_game_id=None)
                  for path, rows in quote_files for i, row in enumerate(rows, 2) if row.get('book') == book]
        assert quotes, f'No saved rows for {book}'
        save_json(ROOT / f'records/{tool}_saved_quotes.json', quotes)

    mappings = {
        'ESPN': ('espn_summary.json', list(records[0]), 'Saved final ESPN summary, provider week 9. Postgame only; no certified pregame availability.'),
        'local DB': ('role_coverage_audit.json', ['coverage', 'routes', 'personnel_11', 'personnel_12', 'personnel_13'], 'Saved local postgame audit; coverage UNKNOWN, routes and personnel MISSING; receiving discrepancy retained.'),
        'gamebooks': ('gamebook_notes.json', ['source_snapshots', 'intended_use', 'asof_certification'], 'Saved gamebook and TE usage notes; no pregame certification or measured route/personnel assertion.'),
    }
    for tool in ('FD', 'DK', 'Pinnacle'):
        mappings[tool] = (f'{tool}_saved_quotes.json', ['book', 'source_row_number', 'source_snapshot', 'raw_quote_fields'],
                         'SAVED_ONLY quotes from the three exact handoff files; original timestamps retained; no new pull, fresh-line claim or sportsbook-rule verification.')
    rows = copy.deepcopy(package['source_inventory'])
    for row in rows:
        row.update(scope='Local JAX/BAL evidence inventory only; no forecast/canonical join/cutoff established',
                   status_reason='MISSING within the bounded established artifact selection; no network/auth attempt and no outage/login inference.')
        if row['source_tool'] in mappings:
            filename, fields, reason = mappings[row['source_tool']]
            artifact = 'records/' + filename
            row.update(status='SAVED_ONLY', assessment='retrieved', fields_retrieved=fields,
                status_reason=reason, season=2026, week=None, pull_timestamp=stamp,
                attempt_timestamp=stamp, artifact_path=artifact,
                artifact_sha256=sha((ROOT / artifact).read_bytes()), asof_status='ASOF_UNVERIFIED',
                unknown_reasons={
                    'week': 'No canonical week assigned; ESPN header says 9, some local planning references use week10.',
                    'data_through_timestamp': 'Not certified as an observation-complete dataset; original provider times retained in snapshots/records.',
                    'source_available_timestamp': 'No certified historical publication/availability evidence; mtime is not proof.',
                    'cutoff_utc': 'No projection cutoff selected or certified in this inventory.',
                    'pull_timestamp_semantics': 'Local read/snapshot timestamp only; original external pull strings retained separately, never replaced with a claimed live pull.'})
            row['fallback'] = dict(kind='blocked', detail='Saved evidence only; as-of certification, crosswalk and workflow incomplete', source_refs=[artifact, 'provenance.json'])
            if row['source_tool'] == 'ESPN':
                row['data_through_timestamp'] = espn['meta']['lastPlayWallClock']
                row['unknown_reasons'].pop('data_through_timestamp')
        elif row['source_tool'] in {'local sim', 'local engines'}:
            row.update(status='NOT_APPLICABLE', reason='This pass inventories saved sources and runs engineering regressions only; no projection/model input is generated.')
        errors = list(gate.VALIDATOR.iter_errors(row))
        if errors:
            raise ValueError([e.message for e in errors])

    blockers = [
        'NOT_COMPLETE: authoritative workflow definitions/versions and phase names absent; no 15-phase completion.',
        'Saved postgame data is EVIDENCE_ONLY_POSTGAME, not a pregame forecast input; source availability/cutoff certification absent.',
        'Canonical game/player/team crosswalk missing; ESPN provider week 9 differs from some local week10 planning labels.',
        'Saved quotes remain SAVED_ONLY and unusable for run; book rules unverified; no new odds pulls.',
        'Coverage UNKNOWN; routes/personnel MISSING; receiving-yard source discrepancy retained.',
        'No projection run, predictive validation, fitted Bias or measured improvement.']
    manifest = dict(document_type='run_manifest', schema_version='1.0.0',
        run_id='core-established-local-source-scaffold-2026-11-06', run_kind='engineering_test',
        season=2026, week=None, game_id=None, game_id_namespace=None, cutoff_utc=None,
        frozen_at_utc=None, generated_at_utc=stamp,
        engine_version=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=CORE, text=True).strip(),
        config_id=None, input_content_hash=None,
        workflow_versions={name: None for name in ('betting-game-brainstorm', 'nfl-game-script-run', 'nfl-betting-script', 'football-period-game-flow')},
        checklist_path='checklist.md', report_path='report.md', brainstorm_path='brainstorm.md',
        source_ledger=rows,
        source_gate=dict(status='BLOCKED', evidence='report.md', permitted_scope='Local saved-evidence inventory only', blockers=blockers),
        scenario_first=dict(status='BLOCKED', evidence='brainstorm.md'),
        phases=[dict(number=n, authoritative_name=None, status='BLOCKED', evidence=None,
                     reason='NOT_COMPLETE; authoritative workflow definition and name absent') for n in range(1, 16)],
        supplemental_workflows={name: dict(status='BLOCKED', reason='NOT_COMPLETE; authoritative workflow definition absent', evidence=None) for name in ('nfl-betting-script', 'football-period-game-flow')},
        projection_execution_status='NOT_RUN', engineering_checks=[], blockers=blockers,
        projection_ready=False, synthetic=False, validation_basis='infrastructure_only',
        automatic_cuts=copy.deepcopy(package['automatic_cuts']))
    errors = list(gate.VALIDATOR.iter_errors(manifest))
    if errors:
        raise ValueError([e.message for e in errors])
    save_json(ROOT / 'source_ledger.json', rows)
    save_json(ROOT / 'run_manifest.json', manifest)
    save_json(ROOT / 'provenance.json', dict(local_inventory_at_utc=stamp,
        external_requests=0, projection_ready=False, artifacts=provenance,
        search_scope='Only explicit paths in this builder; MISSING is scoped to this selection, not a provider availability diagnosis.',
        timestamp_policy='pull_timestamp on saved rows means local read; saved original times remain in exact snapshots. No mtime-as-availability inference.',
        source_identity_policy='ESPN aliases/provider labels only; canonical crosswalk unresolved',
        reference_documents=[dict(path=str(p), sha256=sha(p.read_bytes())) for p in [
            RESEARCH / 'SOURCE_INVENTORY_BETGURU_2026-11-06.md',
            Path('/workspace/wt-market-calibration/research/market_calibration/tracking/GHOST_HANDOFF_MARKET_ADAPTER.md')]]))
    print(json.dumps(dict(schema_valid=True, source_rows=len(rows), statuses=dict(Counter(r['status'] for r in rows)),
                          snapshot_files=len(provenance), projection_ready=False), indent=2))


if __name__ == '__main__':
    main()
