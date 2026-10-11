# WORKFLOW: one repo at a time

Each step has an acceptance check. Don't start the next step until the check passes. Don't start the next folder
until the current one is pushed and verified, or logged as skipped.

| # | Step | Acceptance check |
|---|---|---|
| 0 | Check the kit: `python3 tools/check_kit.py` | `KIT CHECK n/n passed` |
| 1 | Pick the next folder from the queue in `STATE.md`; check `results_3.1.2/PUBLISH_LOG.csv` and the account's repo list so nothing half-pushed is redone | The folder isn't already logged; the repo name is free (or the existing repo is yours and incomplete) |
| 2 | Re-read the host docs (`DOCS_LINKS.md`); list format drift since v1.0.0 | Every manifest field, root variable, hook and MCP setting is confirmed against current docs, or flagged as unverifiable |
| 3 | Stage the repo in a scratch folder: copy the v1.0.0 folder, bundle `engine/` (`tools/repokit.py bundle`) | The bundled engine is byte-identical to `engine/` apart from the SPDX headers |
| 4 | Fix and harden: 3.1.2 limits text, tool names, paths, hooks, Windows notes, caveats from `STATE.md` | No `29-qubit cap` wording left except "basis z above 29"; hooks are harmless; no absolute paths |
| 5 | Version 1.1.0; license files; SPDX headers; manifest license and author fields; README; CHANGELOG | `grep -r 1.0.0` finds only history; every manifest has `GPL-3.0-or-later` and the author |
| 6 | Validate manifests offline against the documented schema (`schemas/` or the host's own) | 0 schema errors; JSON/YAML/TOML parse |
| 7 | Rebuild binaries/archives where the host needs them | Built artifacts validate (e.g. `wasm-tools validate`, zip == folder); hashes recorded |
| 8 | Strict scan: `tools/repokit.py scan <repo> --deny <private file>` | `SCAN CLEAN` |
| 9 | Clean-room E2E through the host's real entry point (see `MASTER_PROMPT.md` step 7) | `tests/e2e_mcp.py` (or the host's equivalent) all PASS; the real host loads the plugin, or the result is marked `host-simulated` with the reason |
| 10 | Write `E2E_RESULTS.md` (including the 18/18-with-3-adapted note) | The file states each check, the host version or stand-in, and the date |
| 11 | Create the public repo and push to `main` in small batches | Every staged file is in the repo |
| 12 | Read the tree back | File list and sizes match the staged repo (line-ending differences only in reference text, documented) |
| 13 | Clone into a fresh folder; rerun the quick E2E | PASS; otherwise fix at once or make the repo private |
| 14 | Log the row in `PUBLISH_LOG.csv` and report | Row has URL, version, sha, files, binaries, E2E, findings, time (PT) |

## Push tooling notes (what worked so far)
- The GitHub connector's `push_files` takes text files only and at most 4 file references per call, so push in
  batches of 4. It doesn't keep executable bits: document `sh build.sh` / `python3 x.py` instead of `./x`.
- Binary files (PDF, WASM, ZIP) can't go through it. Sample PDFs are shipped as a small generator
  (`engine/examples/theory/make_sample_pdfs.py`); WASM, exe and archives are built from the committed source.
- Commits show the connected account as committer; the author name and email are recorded in every file instead.
- There is no connector call for repo topics; note that in the log if topics couldn't be set.
