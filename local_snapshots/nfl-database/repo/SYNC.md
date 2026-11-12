# Snapshot synchronization

The maintainer's local Codex automation checks the working database daily at **9:00 AM America/New_York**, after the Monday 8:00 AM external-source audit. It publishes a new snapshot only when the local database or data-gap report changes. This sync does not fetch new game data itself or restart canceled game polling.

This is a local automation: the maintainer's computer, Codex and GitHub access must be available. GitHub Actions cannot read a database on a personal computer. An unavailable local machine can delay a scheduled update; inspect `manifest.json` for the actual snapshot timestamp.

The exporter creates a consistent SQLite backup, rejects unexpected tables and credential-like content, removes local paths, verifies database integrity, and builds a compressed archive with checksums. The original database and append-only working history remain untouched. Only the curated public package is uploaded. The upload is verified through an unauthenticated download before being recorded as successful. Failed uploads are retried on a later scheduled run; the local export is not proof of publication.

## Pull the latest snapshot

```sh
git pull --ff-only
python3 prepare.py
python3 query.py --tables
```

## Build from another local database

```sh
python3 export_snapshot.py --source /path/to/nfl_matchups.sqlite --output /path/to/export --gaps /path/to/DATA_GAPS.md
```

`UNCHANGED` means no new export was needed; remote verification is still necessary to detect a previously failed upload. `READY_TO_PUBLISH` means an audited package was built, not that it reached GitHub. Keep private raw evidence, media, credentials and machine-specific configuration out of the public repository.

## Publication whitelist

Upload only these files together to the repository root: `nfl_matchups.sqlite.gz`, `manifest.json`, `schema.sql`, `DATA_GAPS.md`, `README.md`, `SOURCES.md`, `SYNC.md`, `prepare.py`, `query.py`, `export_snapshot.py`, `verify_publication.py`, `test_export.py`, `.gitignore`.

After publication run `python3 verify_publication.py`. A successful anonymous download must match both local and remote manifests. Local operational status is recorded outside the public package. Unexpected schema or credential-like content blocks publication for review.
