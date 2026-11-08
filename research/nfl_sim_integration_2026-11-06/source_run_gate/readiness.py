"""Local file-backed preflight; no retrieval, simulation, or engineering-test promotion."""
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re

from jsonschema import Draft202012Validator, FormatChecker

PACKAGE = Path(__file__).resolve().parent
SCHEMA = json.loads((PACKAGE / 'source_ledger.schema.json').read_text())
VALIDATOR = Draft202012Validator(SCHEMA, format_checker=FormatChecker())
REQUIRED_SOURCES = {r['source_tool'] for r in json.loads((PACKAGE / 'MANIFEST.json').read_text())['source_inventory']}


def assess(manifest, run_dir, *, allow_synthetic=False):
    """Return fail-closed readiness. Synthetic acceptance never grants live readiness.

    Full fixtures exercise the artifact contract only. A live caller still owns
    source truth, freshness policy, dependency scope and dated approval review.
    """
    errors = [f'schema: {e.message}' for e in VALIDATOR.iter_errors(manifest)]
    cuts = manifest.get('automatic_cuts')
    if isinstance(cuts, dict):
        for cut in ('weather', 'WR', 'edge'):
            settings = cuts.get(cut)
            if isinstance(settings, dict) and settings.get('enabled') is not False:
                errors.append(f'automatic cuts: {cut} must remain DISABLED; '
                              'dated approval evidence and a separately reviewed contract change '
                              'are required before future enablement')
    synthetic = manifest.get('synthetic') is True
    if errors:
        return {'projection_ready': False, 'synthetic_fixture_ready': False, 'errors': errors}
    if not manifest['projection_ready']:
        errors.append('projection_ready was not requested; engineering PASS cannot set it')
    if manifest['validation_basis'] != 'full_source_run':
        errors.append('infrastructure/schema-only checks cannot establish readiness')
    if synthetic and not allow_synthetic:
        errors.append('synthetic evidence is forbidden for live readiness')
    root = Path(run_dir).resolve()

    def artifact(relative):
        path = (root / relative).resolve()
        if not path.is_relative_to(root):
            raise ValueError('artifact escapes run directory')
        data = path.read_bytes()
        if not data.strip():
            raise ValueError(f'empty artifact: {relative}')
        return path, data

    def text(relative):
        return artifact(relative)[1].decode('utf-8')

    try:
        if Path(manifest['checklist_path']).name != 'checklist.md':
            errors.append('checklist.md required')
        if Path(manifest['report_path']).name != 'report.md':
            errors.append('report.md required')
        checklist = text(manifest['checklist_path'])
        marked = re.findall(r'^\|\s*\[x\]\s*\|\s*(\d{1,2})\s*\|', checklist, re.M | re.I)
        if sorted(map(int, marked)) != list(range(1, 16)):
            errors.append('checklist must mark all 15 distinct phases')
        report = text(manifest['report_path'])
        brainstorm = text(manifest['brainstorm_path'])
        if 'betting-game-brainstorm' not in brainstorm:
            errors.append('brainstorm marker missing')
        if not synthetic and any('SYNTHETIC' in t for t in (checklist, report, brainstorm)):
            errors.append('synthetic workflow artifacts cannot support live readiness')
        if synthetic and any('SYNTHETIC' not in t for t in (checklist, report, brainstorm)):
            errors.append('fixture artifacts must be labeled SYNTHETIC')
        text(manifest['scenario_first']['evidence'])
        text(manifest['source_gate']['evidence'])
        for phase in manifest['phases']:
            if phase['status'] == 'COMPLETE':
                text(phase['evidence'])
        for workflow in manifest['supplemental_workflows'].values():
            if workflow['status'] == 'COMPLETE':
                text(workflow['evidence'])
    except (OSError, ValueError, TypeError) as exc:
        errors.append(f'workflow artifact: {exc}')

    rows = manifest['source_ledger']
    if {r['source_tool'] for r in rows} != REQUIRED_SOURCES:
        errors.append('complete mandatory source inventory required')
    if len({r['source_id'] for r in rows}) != len(rows) or len({r['source_tool'] for r in rows}) != len(rows):
        errors.append('duplicate source ledger records')
    usable = 0
    for row in rows:
        if row['status'] == 'NOT_APPLICABLE':
            continue  # explicit scoped reason is schema-required
        if row['status'] != 'SUCCESS' or not row['usable_for_run']:
            errors.append(f"{row['source_id']}: source is not usable SUCCESS; exclude scope explicitly with NOT_APPLICABLE reason")
            continue
        usable += 1
        try:
            _, data = artifact(row['artifact_path'])
            if hashlib.sha256(data).hexdigest() != row['artifact_sha256']:
                errors.append(f"{row['source_id']}: artifact hash mismatch")
            records = json.loads(data)
            if not isinstance(records, list) or not records or not all(
                isinstance(record, dict) and all(field in record and record[field] is not None for field in row['fields_retrieved'])
                for record in records
            ):
                errors.append(f"{row['source_id']}: real-shaped populated source records required")
            if not synthetic and any(record.get('synthetic') is True for record in records if isinstance(record, dict)):
                errors.append('synthetic source records cannot support live readiness')
            if synthetic and not all(record.get('synthetic') is True for record in records if isinstance(record, dict)):
                errors.append('source fixture records must be labeled synthetic')
            if any(row[key] != manifest[key] for key in ('season', 'week', 'cutoff_utc')):
                errors.append('source scope/cutoff differs from run')
            times = {k: datetime.fromisoformat(row[k].replace('Z', '+00:00')) for k in (
                'data_through_timestamp', 'source_available_timestamp', 'pull_timestamp', 'cutoff_utc')}
            if not times['data_through_timestamp'] <= times['source_available_timestamp'] <= times['cutoff_utc']:
                errors.append('source observation/availability exceeds cutoff or is inconsistent')
            if times['pull_timestamp'] < times['source_available_timestamp']:
                errors.append('pull precedes source availability')
        except (OSError, ValueError, TypeError) as exc:
            errors.append(f'source artifact: {exc}')
    if not usable:
        errors.append('no usable source records; empty/template ledger cannot establish readiness')
    return {'projection_ready': not errors and not synthetic,
            'synthetic_fixture_ready': not errors and synthetic and allow_synthetic,
            'errors': errors}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--synthetic-fixture', action='store_true', help='accept labeled full fixtures; never grants live readiness')
    args = parser.parse_args(argv)
    try:
        result = assess(json.loads(args.manifest.read_text()), args.manifest.parent,
                        allow_synthetic=args.synthetic_fixture)
    except (OSError, ValueError) as exc:
        result = {'projection_ready': False, 'synthetic_fixture_ready': False, 'errors': [str(exc)]}
    print(json.dumps(result, indent=2))
    return 0 if result['projection_ready'] or result['synthetic_fixture_ready'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
