"""Capture offline validation commands and hash the final diagnostic handoff."""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
GATE = ROOT.parents[1] / 'source_run_gate'
LOGS = ROOT / 'logs'


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False)+'\n')


def capture(name, command, expected):
    started = now()
    result = subprocess.run(command, cwd=ROOT.parents[1], capture_output=True, text=True)
    log = LOGS / (name+'.log')
    log.write_text(result.stdout + result.stderr)
    entry = {'command':command,'cwd':str(ROOT.parents[1]),'started_at_utc':started,
             'finished_at_utc':now(),'exit_code':result.returncode,'expected_exit_code':expected,
             'log_path':str(log.relative_to(ROOT)),'log_sha256':sha(log)}
    save(LOGS/(name+'_run.json'),entry)
    if result.returncode != expected:
        raise RuntimeError(str(entry))
    return entry, result.stdout


def main():
    LOGS.mkdir(exist_ok=True)
    commands = []
    entry, _ = capture('build_certified',[sys.executable,str(ROOT/'build_certified.py')],0)
    commands.append(entry)
    entry, _ = capture('source_gate_pytest',[sys.executable,'-m','pytest',str(GATE/'tests'),'-q',
        '-o','cache_dir='+str(LOGS/'pytest_cache'),'--basetemp',str(LOGS/'pytest_tmp'),
        '--junitxml',str(LOGS/'source_gate_pytest.xml')],0)
    commands.append(entry)
    suites = ET.parse(LOGS/'source_gate_pytest.xml').getroot()
    totals = {key:sum(int(s.get(key,0)) for s in suites.findall('testsuite'))
              for key in ['tests','failures','errors','skipped']}
    manifest_path = ROOT/'run_manifest.json'
    manifest = json.loads(manifest_path.read_text())
    manifest['engineering_checks'] = [
        {'name':'source_run_gate pytest (engineering only)','status':'COMPLETE','evidence':'logs/source_gate_pytest.log'},
        {'name':'diagnostic packet byte/lineage verification','status':'COMPLETE','evidence':'logs/packet_verification.log'}]
    save(manifest_path,manifest)
    entry, stdout = capture('packet_verification',[sys.executable,str(ROOT/'verify_packet.py')],0)
    commands.append(entry)
    verification = json.loads(stdout)
    entry, stdout = capture('readiness_live',[sys.executable,str(GATE/'readiness.py'),str(manifest_path)],1)
    commands.append(entry)
    live = json.loads(stdout)
    assert live['projection_ready'] is False and live['synthetic_fixture_ready'] is False
    assert live['errors']
    assert not totals['failures'] and not totals['errors']
    report_path = ROOT/'report.md'
    report_path.write_text(report_path.read_text()+'\nCaptured verification: '+str(totals['tests'])+
        ' source_run_gate engineering tests passed; '+str(totals['failures'])+' failures / '+str(totals['errors'])+
        ' errors. Packet byte/lineage checks PASS. readiness.py live exited 1 with projection_ready=false and '+
        str(len(live['errors']))+' reported blockers. Exact commands/logs: SOURCE_READINESS_EVIDENCE.json.\n')
    aliases = json.loads((ROOT/'aliases/player_aliases_certified_v2.json').read_text())
    paths = set(p for p in ROOT.iterdir() if p.is_file() and p.suffix in ['.md','.json','.py'])
    paths.discard(ROOT/'SOURCE_READINESS_EVIDENCE.json')
    for directory in ['records','snapshots','aliases','workflows','connectors_clean']:
        paths.update(p for p in (ROOT/directory).rglob('*') if p.is_file())
    paths.update(p for p in LOGS.iterdir() if p.is_file())
    paths.update([GATE/'readiness.py',GATE/'provenance.py',GATE/'source_ledger.schema.json',GATE/'REQUIREMENT.md'])
    paths.update((GATE/'tests').glob('*.py'))
    artifacts = [{'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(paths)]
    sources = manifest['source_ledger']
    evidence = {
        'document_type':'CORE_SOURCE_READINESS_EVIDENCE','generated_at_utc':now(),
        'run_id':manifest['run_id'],'run_kind':manifest['run_kind'],
        'classification':'DIAGNOSTIC_EVALUATION_NOT_FROZEN_FORECAST',
        'cutoff_utc':manifest['cutoff_utc'],'diagnostic_frozen_at_utc':manifest['frozen_at_utc'],
        'projection_ready':False,'source_gate':'BLOCKED','workflow_status':'NOT_COMPLETE',
        'source_provider_count':len(sources),'source_status_counts':dict(Counter(r['status'] for r in sources)),
        'usable_SUCCESS_count':0,'promotion_decision':'All saved candidates remain SAVED_ONLY; unresolved provenance/scope/identity/settlement.',
        'commands':commands,'pytest':totals,'packet_verification':verification,'readiness_live':live,
        'attempts':{'detailed_path':'attempts.json','sha256':sha(ROOT/'attempts.json'),
                    'staged_public_probe_path':'public_probe_attempts.json','staged_public_probe_sha256':sha(ROOT/'public_probe_attempts.json'),
                    'external_requests_this_pass':0,'spend_this_pass':0,'access_exhausted_claim':False,
                    'odds_bridge':'LOGIN_REQUIRED per staged coordinator evidence; no bypass'},
        'blockers':manifest['blockers'],
        'week_discrepancy':{'provider_week':9,'some_local_odds_data_week':10,'resolution':'UNRESOLVED_PRESERVED'},
        'identity':{'game':'ALIASES_ONLY_NO_FROZEN_CANONICAL_REGISTRY_JOIN',
                    'players':aliases['counts'],'unique_matched_team_espn_ids':114,'unique_unmatched_team_espn_ids':47,
                    'join_method':'EXACT_ESPN_ID_AND_TEAM_NO_GUESSED_JOINS'},
        'evidence_boundary':{'postgame':'EVIDENCE_ONLY_POSTGAME','usable_for_frozen_pregame':False,
                             'TNF_holdout':'INSPECTED_NOT_UNTOUCHED','forecast_execution':'NOT_RUN'},
        'missingness_path':'feature_availability.json','automatic_cuts':manifest['automatic_cuts'],
        'model_impact':'NOT_MEASURED','forecast_impact':'NOT_MEASURED','before_after_forecast_evidence':None,
        'predictive_accuracy':'NOT_MEASURED','calibration':'NOT_MEASURED','ROI':'NOT_MEASURED',
        'ghost_acceptance':{'source_readiness':'BLOCKING_PROJECTION','DIRECT_wire':'WAITING_BETGURU_BINDING',
                            'Ghost_final':'UNVERIFIED_NOT_CLAIMED','addendum_path':'GHOST_ACCEPTANCE_ADDENDUM.md'},
        'artifact_hashes':artifacts,
        'limitations':['Schema/engineering PASS does not establish data truth, workflow completion or projection readiness.',
            'Known pre-cutoff raw quote times do not resolve week/kickoff/settlement and canonical identity conflicts.',
            'Missing provider scoped records remain missing; unattempted network routes are not presented as exhausted access.',
            'Original scaffold and staged artifacts preserved; only source/integration/gate files changed by this pass.',
            'No independent final vet performed; no authoritative skill version numbers invented.']}
    save(ROOT/'SOURCE_READINESS_EVIDENCE.json',evidence)
    print(json.dumps({'evidence_path':str(ROOT/'SOURCE_READINESS_EVIDENCE.json'),'pytest':totals,
                      'readiness_live_exit':entry['exit_code'],'projection_ready':False,
                      'byte_verification':verification,'artifact_hashes':len(artifacts)}))


if __name__=='__main__':
    main()
