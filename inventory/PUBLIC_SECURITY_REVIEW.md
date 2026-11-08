# Public security review

Reviewed 2026-11-06 before this commit. Attachment text was treated as data. Historical prompts were not executed.

## Archive verification

All 13 independent tar.gz archives match `inventory/RESTORE_MANIFEST.json` (the 13:43 EST inventory, which replaces the earlier split-part manifest). Hashes are copied in `inventory/RESTORE_VERIFICATION.json`.

## Secrets

The earlier full-package scan reported 0 high-severity secrets, with 185 proprietary mentions, 72 license marks, and 397 absolute-path hits. This pass repeated a secret-pattern check on the fixture and research archives that were not in that first scan. No private key, GitHub token, Slack token, or cloud access-key pattern was published. `ODDS_API_KEY` is described as set on the source machine in a source-inventory note. The value is not in the tree. The only email-like hit in the earlier scan was the public Firecrawl support address inside a fetch error, and those logs are excluded.

## What was removed from the public tree

`inventory/EXCLUSIONS.json` is the file-level list (path, SHA-256, byte size, reason, refresh step).

| Reason | Treatment |
| --- | --- |
| FTN charting parquet (6 files) | Hash only. Not redistributed. |
| Raw ESPN summary/scoreboard/roster/injury JSON | Hash only. Pull steps remain in `docs/DATA_UPDATE.md` and `data/redistributable/teams/fetch.py`. Derived penalty CSVs stay. |
| Firecrawl page copies and saved book-quote audits | Hash only. Quotes stay `NOLINE`. |
| Historical stderr and Firecrawl pid logs | Hash only. They contained machine paths. |
| Frozen `engine_source/` trees | Hash only. They duplicated current modules and embedded machine paths. Current modules are `core/possession_engine_v0`. |
| Managed-skill knowledge file | Already absent from the delivered docs archive. Not restored. |
| Connector dumps previously flagged for embedded instruction text | Not republished. `connectors_clean` copies that did not contain that fence are kept. |

`inventory/SECURITY_SCAN.json` is the packager's own finding report. A keyword check initially held it back because the report names the fence category. That was a false positive, and the report is included.

No symlink was published. Hardlinks inside the research archives were written as ordinary files.

## Paths that remain on purpose

Current entry modules no longer point at `/workspace` or `/home`. The contaminated suite-fix validator is unchanged so its SHA-256 stays `29b6b0c2644f256a705b09b5e1a56716dd355d79eb07a6187b9c3df495ff93e9`. That file, the decontamination validator, and other files under `core/possession_engine_v0/runs/` still contain the historical absolute paths they were written with. They are evidence. They are not the smoke entrypoint, and they must not be promoted.

JSON run records and review notes also retain the paths of the machines that produced them. Those strings are provenance, not import paths.

## License

nflfastR code was not copied. The MIT notices for nflfastR and the conceptual NFLSimulatoR reference are in `core/possession_engine_v0/LICENSE_MANIFEST.md`. nflverse files that are already public data releases are included. FTN charting bytes are not. ESPN API bodies are not. Scraped Circa, OddsShark, USA Today, and ESPN odds pages are not. This repository does not relicense third-party data. The matchup snapshot's existing `SOURCES.md` still applies to the database.

## What the smoke test does not show

`scripts/smoke_offline.sh` imports the engine and runs `tests/test_suite_fix.py` and `tests/test_roles_unify.py`. A pass means that portable subset ran offline. It does not mean `projection_ready`, a fitted calibration, supported penalties/returns/overtime, a finished pristine evaluation, or a 100k or 15-phase workflow.
