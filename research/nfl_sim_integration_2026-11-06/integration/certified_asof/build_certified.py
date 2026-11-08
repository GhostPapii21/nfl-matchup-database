"""Offline diagnostic packet builder. No forecast, network, credentials or spend."""
from collections import Counter
import copy
import csv
from datetime import datetime, timezone
import importlib.util
import io
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
RESEARCH = ROOT.parents[1]
CORE = Path('/workspace/wt-nfl-sim-core-2026-11-06')
DB = Path('/workspace/nfl-database')
GATE = RESEARCH / 'source_run_gate'
sys.path.insert(0, str(GATE))
from provenance import digest, verified_copy, espn_athletes, join_players, inspect_quotes, utc
import readiness
CUTOFF = '2026-11-06T01:15:00Z'
NOW = datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')
provenance = []


def write(name, obj):
    path = ROOT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True, allow_nan=False) + '\n')


def snapshot(path, name=None, expected=None, usage='SAVED_ONLY'):
    path = Path(path)
    name = name or 'snapshots/' + path.name
    checked = verified_copy(path, ROOT / name, expected)
    provenance.append({'original_path': str(path), 'path': name, **checked,
                       'local_read_at_utc': NOW, 'external_pull_this_pass': False,
                       'mtime_used_as_availability': False, 'usage': usage})
    return name


def load(name):
    return json.loads((ROOT / name).read_text())


def record(name, objects):
    write('records/' + name + '.json', objects)
    return 'records/' + name + '.json'


def main():
    # Verify staged bytes before using them. Probe hashes without retained bodies
    # remain declarations, explicitly distinct from verified snapshot hashes.
    meta = load('snapshots/espn_summary_401873037_public_pull_2026-11-06.meta.json')
    espn_path = snapshot(ROOT / 'snapshots/espn_summary_401873037_public_pull_2026-11-06.json',
        'snapshots/espn_summary_401873037_public_pull_2026-11-06.json', meta['sha256'], 'EVIDENCE_ONLY_POSTGAME')
    espn = load(espn_path)
    batch = load('connectors_clean/CONNECTOR_BATCH_META.json')
    for item in batch['artifacts']:
        path = Path(item['path'])
        snapshot(path, str(path.relative_to(ROOT)), item['sha256'], 'DIAGNOSTIC_IDENTITY')
    staged = load('aliases/jax_bal_canonical_aliases_v1.json')
    roster = snapshot(staged['source_roster'], 'snapshots/nflverse_roster_2026.csv', staged['source_roster_sha256'], 'DIAGNOSTIC_IDENTITY')
    snapshot(RESEARCH / 'SOURCE_INVENTORY_BETGURU_2026-11-06.md', 'snapshots/SOURCE_INVENTORY_BETGURU_2026-11-06.md', usage='ACCESS_ATTEMPT_EVIDENCE')
    snapshot(RESEARCH / 'PREFLIGHT_BETGURU_2026-11-06.json', 'snapshots/PREFLIGHT_BETGURU_2026-11-06.json', usage='ACCESS_ATTEMPT_EVIDENCE')
    workflow_names = ['nfl-projection-source-preflight', 'betting-game-brainstorm', 'nfl-game-script-run', 'nfl-betting-script', 'football-period-game-flow']
    workflows = []
    for name in workflow_names:
        path = Path('/home/box/sand-data/workflows') / name / 'SKILL.md'
        rel = snapshot(path, 'workflows/' + name + '.SKILL.md', usage='WORKFLOW_DEFINITION')
        workflows.append({'name': name, 'path': rel, 'sha256': digest((ROOT / rel).read_bytes()),
                          'declared_version': None, 'definition_status': 'PRESENT',
                          'version_status': 'UNVERIFIED_NO_EXPLICIT_VERSION_TAG'})
    for name in ['GAME_SCRIPT_2026-10-29.md', 'PHASE_SCRIPT.md']:
        snapshot(DB / name, 'workflows/' + name, usage='WORKFLOW_CONTEXT')
    snapshot(DB / 'postmortems/2026-11-05_code_notes_for_ghost6.md', 'workflows/latest_postmortem_context.md', usage='HELD_CONTEXT_NOT_FORECAST_INPUT')
    write('workflow_definitions.json', {'definitions': workflows, 'workflow_status': 'NOT_COMPLETE',
        'reason': 'Definitions located and retained; no explicit version tags in skill bodies; dated rule text is not current cut approval.',
        'authority_order': workflow_names[:3] + ['source_run_gate/REQUIREMENT.md'],
        'consolidated_workflow': {'contract': 'workflow-v1', 'accepted_revision': '20261028T132748605447',
                                 'source': 'workflows/GAME_SCRIPT_2026-10-29.md',
                                 'note': 'These are consolidated document labels, not invented skill versions.'}})

    # Validate v1 aliases against the actual roster rows, preserving opaque IDs.
    raw_roster = list(csv.DictReader((ROOT / roster).open()))
    roster_index = {(r['gsis_id'], r['team']): r for r in raw_roster if r['gsis_id']}
    columns = {'espn':'espn_id', 'pfr':'pfr_id', 'pff':'pff_id', 'sleeper':'sleeper_id',
               'yahoo':'yahoo_id', 'sportradar':'sportradar_id', 'rotowire':'rotowire_id'}
    for player in staged['players']:
        raw = roster_index[(player['canonical_id'], player['team'])]
        for alias in player['aliases']:
            if raw[columns[alias['namespace']]] != str(alias['id']):
                raise ValueError('staged player alias does not match roster bytes')
    observations = []
    for filename in staged['espn_roster_files_parsed']:
        path = Path(filename)
        rel = snapshot(path, 'snapshots/availability/' + path.name, usage='SAVED_AVAILABILITY_ASOF_UNVERIFIED')
        document = load(rel)
        team = 'JAX' if 'jax' in path.name else 'BAL'
        observations.extend({**item, 'team': team, 'source_path': rel} for item in espn_athletes(document))
    joined, unmatched = join_players(observations, staged['players'])
    write('aliases/player_aliases_certified_v2.json', {
        'document_type': 'diagnostic_player_aliases', 'classification': 'DIAGNOSTIC_IDENTITY',
        'source_roster': roster, 'source_roster_sha256': staged['source_roster_sha256'],
        'players': staged['players'], 'matched': joined, 'unmatched': unmatched,
        'counts': {'players':len(staged['players']), 'athlete_observations':len(observations),
                   'unique_team_espn_ids':len({(o['team'],o['espn_id']) for o in observations}),
                   'matched_observations':len(joined), 'unmatched_observations':len(unmatched)},
        'join_method': 'EXACT_ESPN_ID_AND_TEAM; ambiguous joins rejected; no name fallback',
        'usable_for_frozen_pregame': False, 'roster_source_available_timestamp': None,
        'correction': 'v1 recursively counted college/position IDs as player candidates. v2 only reads athletes.items and entries.playerId; v1 retained unchanged.'})
    identity = load('aliases/game_identity_401873037.json')
    competition = espn['header']['competitions'][0]
    games = load('connectors_clean/balldontlie_nfl_get_games_2026_wk9_10.json')['data']
    game = next(g for g in games if g['id'] == identity['balldontlie_game']['id'])
    lines = load('connectors_clean/open_leagues_getGameLines_2026_wk9.json')
    line = next(g for g in lines if g['gameId'] == identity['nflverse_line_row']['gameId'])
    assert espn['header']['id'] == '401873037'
    assert utc(competition['date']) == utc(game['date']) == utc(CUTOFF)
    assert {c['team']['abbreviation'] for c in competition['competitors']} == {'JAX','BAL'}
    assert game['visitor_team']['abbreviation'] == line['away'] == 'JAX'
    assert game['home_team']['abbreviation'] == line['home'] == 'BAL'
    assert espn['header']['week'] == line['week'] == game['week'] == 9
    write('aliases/game_aliases_certified_v2.json', {
        'classification':'DIAGNOSTIC_IDENTITY', 'aliases':identity['aliases'],
        'canonical_game_id':None, 'canonical_game_id_namespace':None,
        'registry_join_status':'UNVERIFIED_NO_FROZEN_SCHEDULE_PBP_REGISTRY',
        'match_checks':{'teams':'PASS','kickoff':'PASS','season_week':'PASS'},
        'kickoff_utc':CUTOFF, 'season':2026, 'week':9,
        'provider_team_ids':{'espn':{c['team']['abbreviation']:str(c['team']['id']) for c in competition['competitors']},
                             'balldontlie':{'JAX':str(game['visitor_team']['id']),'BAL':str(game['home_team']['id'])}},
        'week_label_conflict':{'espn':9,'balldontlie':9,'open_leagues_nflverse_alias':9,'some_local_odds_data_week':10},
        'unmatched':[{'namespace':'oddsapi_event','id':'c75744790b7acf6260c78ba5e739c0e5',
                      'reason':'Matchup text agrees but commence_utc=01:20Z conflicts with official 01:15Z; no verified canonical crosswalk.'}],
        'usable_for_frozen_pregame':False,
        'source_paths':['aliases/game_identity_401873037.json',espn_path,
                        'connectors_clean/balldontlie_nfl_get_games_2026_wk9_10.json',
                        'connectors_clean/open_leagues_getGameLines_2026_wk9.json'],
        'discrepancy':'open-leagues spread=-8.5 has ambiguous team perspective; preserved raw, not normalized or used as executable quote.'})
    held = DB / 'runs/2026-11-05_JAX_BAL/inactives'
    availability = []
    for name in ['sum_401873037_meta.json','sum_401873037_1855.json','espn_jax_injuries_1855.json',
                 'espn_bal_injuries_1855.json','phase15_inactives.md','jaguars_inactives.png','ravens_inactives.jpg']:
        availability.append(snapshot(held / name, 'snapshots/availability/' + name, usage='SAVED_AVAILABILITY_ASOF_UNVERIFIED'))
    weather = []
    for name in ['weather_recheck_meta.json','forecast_2026-11-05_1855.json',
                 'nws_hourly_20261105T1855.json','open_meteo_20261105T1855.json']:
        weather.append(snapshot(held / name, 'snapshots/weather/' + name, usage='SAVED_FORECAST_ASOF_UNVERIFIED'))
    audits = []
    for name in ['actual_role_coverage_audit.md','notes/te_usage_comparison.md',
                 'notes/evidence_nov5/nfl_gamebook_JAX_at_BAL_20261105.txt',
                 'notes/evidence_nov5/nfl_gamebook_JAX_at_BAL_20261105.pdf']:
        audits.append(snapshot(DB / 'live/2026-11-05_JAX_BAL' / name, usage='EVIDENCE_ONLY_POSTGAME'))
    for name in ['tools/weather_forecast.py','manifest.json','DATA_GAPS.md','schema.sql']:
        if (DB / name).is_file():
            snapshot(DB / name, 'snapshots/local/' + Path(name).name, usage='ENGINEERING_CONTEXT_ONLY')

    # Only original raw quotes enter records, never postgame grades or scores.
    odds_checks, quotes = [], {}
    for label, folder, stem in [
        ('close',DB/'runs/line_movement_wk10','odds_20261105_JAXBAL_close'),
        ('open',DB/'runs/line_movement_wk10','odds_20261105_JAXBAL_open'),
        ('r6',DB/'runs/2026-11-05_JAX@BAL_r6/odds','odds_r6')]:
        csv_path = folder / (stem + '_game.csv')
        if label=='r6': csv_path = folder / 'odds_jaxbal_game.csv'
        meta_path = folder / (stem + '_meta.json')
        if not meta_path.exists():
            odds_checks.append({'snapshot':label,'status':'SAVED_ONLY','reason':'No paired meta at explicit path','meta_path':str(meta_path)})
            continue
        raw_path = snapshot(csv_path, 'snapshots/odds/' + csv_path.name)
        meta_rel = snapshot(meta_path, 'snapshots/odds/' + meta_path.name)
        rows = list(csv.DictReader((ROOT / raw_path).open()))
        declaration = load(meta_rel)
        checks = inspect_quotes(rows, declaration, CUTOFF, 9)
        odds_checks.append({'snapshot':label,'source_path':raw_path,'meta_path':meta_rel,
                            'raw_sha256':digest((ROOT/raw_path).read_bytes()), **checks})
        for number, row in enumerate(rows, 2):
            quotes.setdefault(row['book'],[]).append({'raw_quote_fields':row, 'source_path':raw_path,
                'source_sha256':digest((ROOT/raw_path).read_bytes()), 'source_row_number':number,
                'snapshot':label, 'status':'SAVED_ONLY','actionable_status':'NOLINE',
                'canonical_game_id':None,'usable_for_run':False})
    write('odds_verification.json', {'cutoff_utc':CUTOFF,'checks':odds_checks,
        'promotion_decision':'NO_SUCCESS: timestamp evidence alone does not resolve week/kickoff/game identity and settlement conflicts.',
        'freshness_policy':'Use saved meta max_quote_age_min for quote-to-pull checks; no new executable-price tolerance invented.',
        'raw_only':True, 'no_new_odds_requests':True})
    paths = {}
    paths['ESPN'] = record('ESPN_postgame', [{'event_alias':'401873037','season':2026,'week':9,
        'kickoff_utc':competition['date'],'final_scores':{c['team']['abbreviation']:c['score'] for c in competition['competitors']},
        'source_snapshot':espn_path,'usage':'EVIDENCE_ONLY_POSTGAME','usable_for_frozen_pregame':False}])
    paths['nflverse'] = record('nflverse_identity', staged['players'])
    for provider, book in [('FD','fanduel'),('DK','draftkings'),('Pinnacle','pinnacle')]:
        paths[provider] = record(provider+'_saved_quotes', quotes[book])
    paths['OddsAPI'] = record('OddsAPI_saved_pull_assessment', odds_checks)
    paths['ESPN availability/depth'] = record('ESPN_saved_availability', [{'source_paths':availability,
        'scope':'Saved pregame declarations and roster/injury bytes; completeness/as-of not independently certified',
        'usable_for_frozen_pregame':False}])
    for provider in ['official injury/depth','official X']:
        paths[provider] = record(provider.replace('/','_').replace(' ','_'), [{'source_paths':availability[-3:],
            'scope':'Saved note and images with official attribution; full practice/depth and original post provenance unverified',
            'usable_for_frozen_pregame':False}])
    for provider in ['NWS','OpenMeteo','stadium tools','weather_forecast.py']:
        paths[provider] = record(provider, [{'source_paths':weather,
            'scope':'Saved forecast/venue declarations; no promotion of postgame probe to historical forecast',
            'usable_for_frozen_pregame':False}])
    paths['gamebooks'] = record('gamebooks', [{'source_paths':audits[2:], 'usage':'EVIDENCE_ONLY_POSTGAME'}])
    paths['local DB'] = record('local_evidence', [{'source_paths':audits,'coverage':'UNKNOWN','routes':'MISSING',
        'personnel_11':'MISSING','personnel_12':'MISSING','personnel_13':'MISSING',
        'allows_sim_effect':False,'usage':'EVIDENCE_ONLY_POSTGAME','receiving_credit_discrepancy':'RETAINED_IN_AUDIT'}])
    source_notes = {
        'ESPN':'Verified final summary bytes/hash; postgame only. Public home 200 is not field coverage. Probe and meta pull times differ by 2 seconds.',
        'nflverse':'Verified saved roster hash and exact player IDs. Release homepage 200/roster HEAD 302 do not establish pregame PBP/snaps/participation.',
        'PFR':'Observed public probe HTTP 403 challenge, not proven login requirement. No advanced-defense records retrieved.',
        'NGS':'Public shell HTTP 200 only; no required route/separation/time-to-throw records retrieved.',
        'PFF':'Coordinator public shell 200; paid grades/matchups not retrieved. No observed login challenge to justify LOGIN_REQUIRED.',
        'NFLPro':'Coordinator note says signed out; no authenticated required-field retrieval. Access barrier remains per saved note, not a fresh diagnosis.',
        'OddsAPI':'Saved raw quote bytes/meta verified; no keyed network request. Week10/kickoff01:20 conflict; canonical mapping and settlement unverified.',
        'FD':'Public shell 403 in coordinator evidence. Saved quote fields exist; as-of/conflict and settlement checks block promotion.',
        'DK':'Public shell 200 not quotes. Saved quote fields exist; as-of/conflict and settlement checks block promotion.',
        'Pinnacle':'Public shell 200 not quotes. Saved quote fields exist; as-of/conflict and settlement checks block promotion.',
        'NWS':'Staged current /points 200 is grid discovery only. Held dated forecast saved; no certified complete kickoff weather freeze.',
        'OpenMeteo':'Staged postgame temperature-only forecast does not cover historic game weather; held dated response saved.',
        'gamebooks':'Saved PDF/text verified; postgame score/stat evidence only. Staged operations URL 404 does not negate saved book.',
        'FTN via nflverse':'No verified cutoff-eligible FTN/PBP join or man/zone, MOF, rushers and conditional targets. Saved registry reference is not retrieved scoped charting.',
        'Sharp':'No dated schemes/positional coverage retrieved and no second-source corroboration; no Sharp-dependent effect.',
        'StatRankings':'No per-defender or OL tables retrieved with dated scope, denominators and source availability.',
        'PropsMadness':'No authorized scoped coverage/routes/matchup records retained; no login or account entitlement inferred.',
        'SumerSports':'No dated team advanced metrics or denominator/sample records retrieved for this cutoff.',
        'FantasyPoints':'No dated crosscheck records retrieved; cannot supply sole-source scheme evidence.',
        'official injury/depth':'Saved official-attributed inactive note/images only; full official depth, practice trends and original publication chain unverified.',
        'ESPN availability/depth':'Saved roster and injury JSON inspected. Athlete ID scope is explicit; complete depth/workload and original pull certification absent.',
        'Ourlads':'No dated depth-chart snapshot retrieved for this game/cutoff.',
        'AP':'No dated game-specific practice/news article retained in scoped evidence.',
        'RotoWire':'No dated practice/workload reporting retrieved; access entitlement unverified.',
        'official X':'Saved official-attributed inactive images/note held; original post bytes, publication chain and complete scope unverified.',
        'stadium tools':'Held forecast venue/roof labels only; no authoritative dated roof/rest/travel tool output certified.',
        'weather_forecast.py':'Saved weather runner output and source bytes inspected; script presence/output is not complete historical source certification.',
        'Outlier':'Coordinator reports saved cache but no scoped original quote records were selected/verified here; partial coverage note is not complete retrieval.',
        'PP':'No scoped pick-em lines/rules/timestamps retrieved. Catalog mentions older PrizePicks book only; no required-fields claim.',
        'Polymarket':'No exact scoped market/outcomes/settlement records retrieved; optional future scope does not establish present availability.',
        'official film reconciled to PBP':'Saved highlight audit says TE catches omitted and no personnel/coverage proof; no official film-to-PBP event reconciliation completed.',
        'local DB':'Retained actual-role audit preserves missingness and receiving-credit discrepancy. No current complete database query verified.'}
    rows = copy.deepcopy(json.loads((GATE/'MANIFEST.json').read_text())['source_inventory'])
    attempts = []
    probe_map = {'ESPN':['espn_nfl_home','espn_summary_public'],'nflverse':['nflverse_releases','nflverse_roster_release'],
        'PFR':['pfr_home'],'NGS':['ngs_home'],'NWS':['nws_points_mtbank'],'OpenMeteo':['open_meteo'],'gamebooks':['operations_gamebooks']}
    for row in rows:
        name = row['source_tool']
        reason = source_notes.get(name, 'Required scoped fields not retrieved in staged/explicit local evidence; no provider outage or login inference. Public current material cannot recreate an absent frozen input.')
        row.update(season=2026,week=9,cutoff_utc=CUTOFF,status='MISSING',assessment='attempted',
            status_reason=reason, fields_retrieved=[],data_through_timestamp=None,pull_timestamp=None,
            source_available_timestamp=None,attempt_timestamp=NOW,artifact_path=None,artifact_sha256=None,
            usable_for_run=False,asof_status='ASOF_UNVERIFIED',freshness_status='not_assessed',
            scope='JAX@BAL source/readiness audit; historical cutoff eligibility required for any forecast input',
            unknown_reasons={k:'No verified provider '+k+' for this scoped input; local audit time is not a retrieval/publication clock.'
                             for k in ['data_through_timestamp','pull_timestamp','source_available_timestamp','artifact_path','artifact_sha256']},
            fallback={'kind':'blocked','detail':'Retain missingness. No inferred measured feature, price or forecast; research only.',
                      'source_refs':['attempts.json','SOURCE_INVENTORY_CORE_2026-11-06.md']})
        if name in paths:
            path = paths[name]
            row.update(status='SAVED_ONLY',assessment='retrieved',artifact_path=path,
                artifact_sha256=digest((ROOT/path).read_bytes()),fields_retrieved=list(load(path)[0]))
            for field in ['artifact_path','artifact_sha256']: row['unknown_reasons'].pop(field)
        elif name in ['local sim','local engines']:
            row.update(status='NOT_APPLICABLE', reason='Scoped offline source audit produces no model forecasts and executes no simulation engines; engine readiness remains unverified for future projections.',
                       status_reason='No simulation or engine output is required to inspect retained source bytes.')
        elif name=='PFR': row.update(status='ERROR',assessment='attempted')
        elif name in probe_map or name=='PFF': row['assessment']='attempted'
        if name in ('FD','DK','Pinnacle','OddsAPI'):
            latest = {'FD':'25','DK':'01','Pinnacle':'24','OddsAPI':'25'}[name]
            row.update(data_through_timestamp='2026-11-06T01:12:'+latest+'Z',
                pull_timestamp='2026-11-06T01:12:42Z',source_available_timestamp=None)
            # These timestamps describe the selected close observation, not every
            # earlier quote in the attached array; retain exact per-row times.
            for field in ['data_through_timestamp','pull_timestamp']:
                row['unknown_reasons'].pop(field)
            row['status_reason'] += ' Row clocks describe selected close snapshot envelope; individual raw times retained. No SUCCESS declared.'
        attempts.append({'source_tool':name,'local_assessment_at_utc':NOW,
            'external_retrieval_this_pass':False,'staged_probe_ids':probe_map.get(name,[]),
            'staged_access_evidence':'snapshots/PREFLIGHT_BETGURU_2026-11-06.json',
            'staged_public_attempts':'public_probe_attempts.json',
            'artifact_path':row['artifact_path'],'decision':row['status'],'reason':row['status_reason'],
            'fallback':row['fallback'],'assessment_scope':'Staged exact attempts plus bounded local inspection; unattempted providers are not exhausted access claims.'})
        errors = list(readiness.VALIDATOR.iter_errors(row))
        if errors: raise ValueError([e.message for e in errors])
    write('attempts.json', {'generated_at_utc':NOW,'sources':attempts,
        'tool_discovery':{'matching_callable_balldontlie_open_leagues_odds_bridge_tools':[],
                          'result':'No matching callable tools in active list; staged coordinator connector results used.'},
        'odds_bridge':{'status':'LOGIN_REQUIRED','basis':'Saved coordinator GetMcpServerStatus authentication_required','bypass':False},
        'external_requests_this_pass':0,'spend_this_pass':0,
        'timing_conflicts':['ESPN probe pulled_et 07:06:20 vs snapshot meta 07:06:22; both postgame; exact network instant unverified.'],
        'attempt_hash_policy':'Probe-declared body hashes without retained bodies are unverified; provenance.json lists byte-verified files.'})
    write('source_ledger.json',rows)
    write('provenance.json', {'artifacts':provenance,'generated_at_utc':NOW,'projection_ready':False,
        'clock_policy':'Local read time is never substituted for provider pull/data-through/source availability.',
        'external_requests_this_pass':0,'spend_this_pass':0})
    write('feature_availability.json', {k:{'status':'UNKNOWN' if k=='coverage' else 'MISSING',
        'value':None,'allows_sim_effect':False,'usage':'EVIDENCE_ONLY_POSTGAME',
        'source_ref':'records/local_evidence.json'} for k in ['coverage','routes','personnel_11','personnel_12','personnel_13']})
    blockers = ['NOT_COMPLETE: skill definitions present but explicit authoritative skill version tags absent; no full workflow execution or final vet.',
        'No usable SUCCESS source rows; saved odds retain week/kickoff/canonical identity and settlement conflicts.',
        'Required pregame PBP/snaps/participation, defender coverage, route/personnel charting, pressure splits and QB grade cards not certified.',
        'Saved injury/weather/roster declarations are incomplete as-of evidence; postgame ESPN/gamebook/audit cannot repair a frozen forecast.',
        'Canonical game registry join UNVERIFIED; exact player aliases diagnostic only; unmatched IDs explicit.',
        'BetGuru binding for DIRECT wire pending; Ghost final acceptance not claimed.',
        'Forecast/model/market impact NOT_MEASURED; no before/after forecast evidence or untouched TNF holdout.']
    phase_names = re.findall(r'^\*\*\d+\. (.*?)\*\*$', (ROOT/'workflows/nfl-game-script-run.SKILL.md').read_text(), re.M)
    assert len(phase_names)==15
    phase_status = ['UNVERIFIED','MISSING','MISSING','MISSING','MISSING','MISSING','MISSING','UNVERIFIED','MISSING','UNVERIFIED','UNVERIFIED','FAIL','UNVERIFIED','MISSING','UNVERIFIED']
    gaps = ['Pregame PBP/box/snaps/participation and credit reconciliation missing; saved final box only.',
        'No last-3 share/attempt or carry model, efficiency denominator or eligible priced leg.',
        'Both-team positional/slot/outside YPT, RB-only YPC, explosive and money-down denominators missing.',
        'No per-defender targets/completions/YPT/rating or charted alignment/routes; coverage UNKNOWN.',
        'No certified blitz/pressure denominators, QB splits or conditional target samples; no proxy invented.',
        'No current-QB percentile reference set or sourced component grades.',
        'No certified current-QB role history, last-4 carry shares or RB receiving efficiency.',
        'Saved injury/inactive notes/images and roster bytes held; complete practice/depth provenance unverified.',
        'NGS shell response only; no separation, route, RYOE or time-to-throw tables.',
        'Saved gamebook/highlight audit is postgame; no official film-to-PBP reconciliation completed.',
        'Held dated weather responses; source availability/completeness and roof/rest/travel review unverified.',
        'All 34 providers assessed in inventory; required usable categories absent, so source gate FAIL.',
        'Conditional base/flip hypotheses only; no certified spread/EPA/Sharp profile or modeled minutes.',
        'SIMULATION NOT RUN; no model p/median/no-vig/edge; quote settlement and joins unverified: NOLINE.',
        'Held 18:55/18:56 declarations cannot prove complete pre-kick refresh, live price or final vet.']
    versions = {w['name']:None for w in workflows if w['name']!='nfl-projection-source-preflight'}
    write('audit_config.json', {'mode':'OFFLINE_DIAGNOSTIC_SOURCE_AUDIT','cutoff_utc':CUTOFF,
        'event_alias_espn':'401873037','season':2026,'provider_week':9,
        'network':False,'spend':0,'simulation':False,'automatic_cuts':'DISABLED'})
    input_files = sorted(set(item['path'] for item in provenance) | {
        'public_probe_attempts.json','aliases/jax_bal_canonical_aliases_v1.json',
        'aliases/game_identity_401873037.json','aliases/player_aliases_certified_v2.json',
        'aliases/game_aliases_certified_v2.json','workflow_definitions.json','audit_config.json',
        'odds_verification.json','source_ledger.json','attempts.json','feature_availability.json'} |
        {str(path.relative_to(ROOT)) for path in (ROOT/'records').glob('*.json')})
    inputs = [{'path':name,'sha256':digest((ROOT/name).read_bytes())} for name in input_files]
    inputs += [{'path':str(path),'sha256':digest(path.read_bytes())} for path in
        [Path(__file__),GATE/'provenance.py',GATE/'readiness.py',GATE/'source_ledger.schema.json',GATE/'REQUIREMENT.md']]
    write('input_manifest.json', {'classification':'DIAGNOSTIC_INPUT_LINEAGE_NOT_FORECAST',
        'inputs':inputs,'code_commit_scope':'engine_version is base CORE HEAD, not a clean-tree claim; actual source helper hashes retained.'})
    input_hash = 'sha256:' + digest((ROOT/'input_manifest.json').read_bytes())
    manifest = dict(document_type='run_manifest',schema_version='1.0.0',
        run_id='core-jax-bal-certified-source-diagnostic-2026-11-06',run_kind='diagnostic_evaluation',
        season=2026,week=9,game_id=None,game_id_namespace=None,cutoff_utc=CUTOFF,
        frozen_at_utc=NOW,generated_at_utc=NOW,
        engine_version=subprocess.check_output(['git','rev-parse','HEAD'],cwd=CORE,text=True).strip(),
        config_id='OFFLINE_SOURCE_AUDIT_NO_MODEL',input_content_hash=input_hash,workflow_versions=versions,
        checklist_path='checklist.md',report_path='report.md',brainstorm_path='brainstorm.md',source_ledger=rows,
        source_gate={'status':'BLOCKED','evidence':'SOURCE_INVENTORY_CORE_2026-11-06.md',
                     'permitted_scope':'DIAGNOSTIC/evaluation evidence audit and conditional research only; no projections/picks/placement',
                     'blockers':blockers},scenario_first={'status':'BLOCKED','evidence':'brainstorm.md'},
        phases=[{'number':i,'authoritative_name':name,'status':'BLOCKED','evidence':'checklist.md','reason':gaps[i-1]}
                for i,name in enumerate(phase_names,1)],
        supplemental_workflows={n:{'status':'BLOCKED','evidence':'brainstorm.md',
            'reason':'Definition retained; applicable to QB/prop or period research, but mandatory inputs and execution absent; NOT_COMPLETE.'}
            for n in ['nfl-betting-script','football-period-game-flow']},
        projection_execution_status='NOT_RUN',engineering_checks=[],blockers=blockers,
        projection_ready=False,synthetic=False,validation_basis='infrastructure_only',
        automatic_cuts=copy.deepcopy(json.loads((GATE/'MANIFEST.json').read_text())['automatic_cuts']))
    write('run_manifest.json',manifest)
    errors = list(readiness.VALIDATOR.iter_errors(manifest))
    if errors: raise ValueError([e.message for e in errors])
    inventory = ['# CORE source inventory — 2026-11-06', '',
        'DIAGNOSTIC/evaluation only. projection_ready=false. Cutoff: '+CUTOFF+'. ESPN week 9; local data_week 10 conflict retained.',
        'Every mandatory provider is assessed below. Source status uses the exact contract enum. No saved source is promoted to SUCCESS.',
        'Attempts: attempts.json and public_probe_attempts.json. Exact copied bytes: provenance.json. Original staged files preserved.',
        'Attempts SHA-256: '+digest((ROOT/'attempts.json').read_bytes())+'; public_probe_attempts.json SHA-256: '+digest((ROOT/'public_probe_attempts.json').read_bytes())+'.',
        'Families assessed: foundational; advanced/charting; availability/depth; environment; markets; official film; local engineering. Each provider below has a corresponding attempts.json record; missing data artifact hashes remain null.',
        'Fields/timestamps/null reasons/scope/fallback are retained in source_ledger.json; local audit time is separate from provider pull time.',
        'No fresh historic success inferred from homepage/HEAD/library/account presence. No new network, spend, keyed Odds API calls, auth bypass or heavy sims.', '',
        '| Provider | Status | Attempt / retained fields / blocker | Artifact SHA-256 | Fallback |','| --- | --- | --- | --- | --- |']
    for row in rows:
        inventory.append('| '+ ' | '.join([row['source_tool'],row['status'],row['status_reason'],row['artifact_sha256'] or 'null — no retained scoped data',row['fallback']['detail']])+' |')
    inventory += ['', 'SAVED_ONLY includes pre-cutoff quote declarations and byte-verified raw records. Current quote fields do not establish canonical event or book settlement compatibility.',
        'PFR ERROR refers to observed HTTP 403. NFLPro remains MISSING: a signed-out note is not proof of a specific login barrier. Odds-bridge LOGIN_REQUIRED is auxiliary connector evidence, not invented entitlement for every book.',
        'NGS/PFF shells are not advanced fields. Missing providers were not network-probed in this pass; access is not claimed exhausted. Fallback remains missing evidence or held diagnostic source, never fabricated coverage.',
        'Hashed JSON record arrays exist for every SAVED_ONLY row. SUCCESS count is zero; there are no SUCCESS rows needing further arrays.',
        'Unsupported features: coverage UNKNOWN; routes and personnel 11/12/13 MISSING; allows_sim_effect=false. Postgame records: EVIDENCE_ONLY_POSTGAME.',
        'Workflow bodies found in /home/box/sand-data/workflows and frozen under workflows/. Explicit skill version tags absent; workflow_definitions.json retains exact hashes; NOT_COMPLETE.',
        'Impact: NOT_MEASURED. Source readiness blocks projection. Waiting BetGuru binding for DIRECT wire; no Ghost final.']
    (ROOT/'SOURCE_INVENTORY_CORE_2026-11-06.md').write_text('\n'.join(inventory)+'\n')
    checklist = ['# JAX@BAL diagnostic checklist — NOT_COMPLETE', '',
        'No candidate legs, projections or picks. All 15 authoritative phase names are copied from the retained skill body; version tags UNVERIFIED.',
        'Cutoff '+CUTOFF+'; generated/frozen packet clock '+NOW+' is postgame, not a frozen forecast.',
        'Per-phase status is below; manifest status BLOCKED records the corresponding execution gate. No phase box is falsely checked.', '',
        '| Done | Phase | Authoritative name | Status | Evidence / missing input |','| --- | --- | --- | --- | --- |']
    for i,name in enumerate(phase_names,1):
        checklist.append(f'| [ ] | {i:02} | {name} | {phase_status[i-1]} | {gaps[i-1]} |')
    checklist += ['', 'Source inventory documentation: PASS (34 providers covered); source usability gate: FAIL.',
        'betting-game-brainstorm conditional research: documented in brainstorm.md; frozen-pregame execution: BLOCKED.',
        'nfl-betting-script and football-period-game-flow: applicable definitions retained; NOT_COMPLETE, inputs missing.',
        'Model trials, seeds and probabilities: N/A for this source audit; SIMULATION NOT RUN.',
        'Automatic weather/WR/edge cuts DISABLED; latest dated approval MISSING. Final vet UNVERIFIED.',
        'Engineering tests and live readiness command results are in logs/ and SOURCE_READINESS_EVIDENCE.json; tests are not phase completion.']
    (ROOT/'checklist.md').write_text('\n'.join(checklist)+'\n')
    report = ['# JAX@BAL source readiness diagnostic — NOT_COMPLETE', '',
        'projection_ready=false; source gate BLOCKED; research/NOLINE. SIMULATION NOT RUN; no forecasts or picks released.',
        'Game alias ESPN 401873037; kickoff 2026-11-05 20:15 ET / '+CUTOFF+'. Provider season 2026/week 9; local odds data_week 10 retained.',
        'run_kind=diagnostic_evaluation; synthetic=false. The packet freeze occurs after kickoff; no claim of a pregame-authored read or forecast.',
        'Inventory: SOURCE_INVENTORY_CORE_2026-11-06.md; ledger: source_ledger.json; attempt details: attempts.json; byte hashes: provenance.json.',
        'Source ledger statuses: '+str(dict(Counter(r['status'] for r in rows)))+'. No usable SUCCESS rows.',
        'Foundational: final ESPN summary and gamebook saved, postgame only; nflverse roster used for diagnostic IDs. PFR HTTP 403; PBP/snaps/participation not certified.',
        'Coverage/charting and NGS: required records missing. Availability: saved roster/inactive/injury evidence held, incomplete provenance. Environment: saved dated NWS/Open-Meteo responses held; current probes cannot replace frozen forecast evidence.',
        'Markets: FD/DK/Pinnacle raw saved quote fields/meta verified; kickoff/time/week conflicts block promotion. OddsAPI no network; PP/Outlier/Polymarket scoped records missing. Official film not reconciled.',
        'Local engineering: original actual-role audit retained with receiving-credit discrepancy. No new engine run or engine changes by this source pass.', '',
        'Brainstorm: brainstorm.md provides conditional base and two flip scripts, falsifiers and missing dependencies; no model effects, assumed rates or numeric projections.',
        'All 15 phases: see checklist.md; '+str(dict(Counter(phase_status)))+'. Every phase remains execution BLOCKED. Definitions located; explicit skill versions absent, so NOT_COMPLETE.',
        'Exact player joins use ESPN athlete IDs and team, validated against saved nflverse roster bytes. Full unmatched list retained; nested college/position false positives corrected without name joins.',
        'Game provider aliases reconcile teams/kickoff/season/week for diagnostic identity only. Frozen schedule/PBP canonical registry join remains UNVERIFIED; odds event alias not force-joined.',
        'Postgame ESPN final JAX 33, BAL 10 and gamebook/actual-role audit remain EVIDENCE_ONLY_POSTGAME. TNF is inspected evidence; not untouched holdout.',
        'Coverage UNKNOWN; routes/personnel 11/12/13 MISSING; allows_sim_effect=false. Targets, position and depth do not supply charted measurements.',
        'frozen_at_utc/generated_at_utc identify this diagnostic packet only; cutoff_utc is the requested historical boundary. Input/source/code hashes retained; no model config/seed/trial output exists.',
        'Automatic weather/WR/edge cuts remain DISABLED regardless of older rule text. No betting placement, keyed odds request, new spend, cloud jobs, calibration edits or heavy simulations.',
        'Engineering verification is separate: captured source_run_gate pytest and readiness.py live logs are referenced by SOURCE_READINESS_EVIDENCE.json. Passing tests cannot make projection_ready true.', '',
        'Phase evidence (source: retained nfl-game-script-run skill; no phase is execution COMPLETE):', '',
        '| Phase | Authoritative name | Status | Missing input / evidence |',
        '| --- | --- | --- | --- |'] + [f'| {i:02} | {name} | {phase_status[i-1]} | {gaps[i-1]} |'
            for i,name in enumerate(phase_names,1)] + ['', 'Blockers:', ''] + ['- '+b for b in blockers] + ['',
        'Next handoff: supply an authorized versioned workflow binding, review eligible original pregame sources and resolve identity/settlement discrepancies; preserve existing freeze and missingness. No impossible historic re-pull is required or claimed.',
        'Impact/model improvement, calibration, accuracy and ROI: NOT_MEASURED; genuine before/after forecast evidence absent.',
        'GHOST_ACCEPTANCE_PACKET addendum: source readiness still blocks projection; waiting BetGuru binding for DIRECT wire; Ghost final UNVERIFIED.']
    (ROOT/'report.md').write_text('\n'.join(report)+'\n')
    print(json.dumps({'status':'DIAGNOSTIC_PACKET_BUILT','providers':len(rows),
        'source_status_counts':dict(Counter(r['status'] for r in rows)),
        'player_identity_counts':load('aliases/player_aliases_certified_v2.json')['counts'],
        'manifest_schema_errors':[], 'projection_ready':False}))


if __name__=='__main__':
    main()
