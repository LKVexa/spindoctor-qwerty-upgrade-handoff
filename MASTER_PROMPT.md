# MASTER PROMPT: publish the remaining SpinDoctor Qwerty plugin repos (engine 1.1.0, SpinDoctor 3.1.2 base)

Paste everything below the line into the assistant, and give it this repository.

---

You are continuing the SpinDoctor Qwerty plugin project for RUSSELL PHILIP SMITHSON. The kit you've been given
(`spindoctor-qwerty-upgrade-handoff`) contains the finished engine, the tests, the end-to-end harness, the scan tool
and the current state. Read `README.md`, `STATE.md`, `WORKFLOW.md` and `ACCEPTANCE_CHECKLIST.md` first.

## What is already done (don't redo it)
- Engine 1.1.0 at parity with the **updated SpinDoctor 3.1.2** (`3.1.2-298-20261010`): 298 logical qubits, 59 per
  entangled factor, `mcx7`, prepared-factor Born-Z sampling above 29 qubits (basis z only), `q.folder` with 3.1.2
  semantics (`.txt .csv .json .qasm .qasm2 .circuit .pdf`, skipped-file listing, compact status, 128 files, 4 MiB per
  file, 128 commands per file, 4096 characters per command, first failure aborts), CSV report copies,
  measurement-CSV fitting equations.
- The 1.1.0 features: the in-chat function table (`spindoctor_functions`) and theory testing from a file, pasted
  text or the chat (`spindoctor_test_theory`, `source=file|text|chat`). Spec: `FEATURE_SPEC_1.1.0.md`.
- Published repos (public, on GitHub account LKVexa): see the table in `README.md` / `STATE.md`.

## Goal
Publish each remaining host folder as its own public GitHub repo, **one at a time, in the order in STATE.md**,
finishing each completely before starting the next. Every repo bundles `engine/` from this kit unchanged.

## Per repo
1. Re-read the host's current official plugin docs (`DOCS_LINKS.md`) and check for format drift: manifest fields,
   root-path variables, hooks, MCP config, packaging. Fix anything stale. Note what you couldn't verify.
2. Audit and fix the folder against the 3.1.2 base: limits text (298/59, basis z above 29), tool names, paths,
   Windows `python` vs `python3`, and the platform caveats in `STATE.md`. Hooks must never run engine commands or
   touch the network.
3. Version 1.1.0 everywhere. Bundle `engine/` with `python3 tools/repokit.py bundle <repo>/<engine-dir>`.
4. Add README.md (what it is, which host, install steps for that host, the function table, theory testing, a
   testing section, honest limits: classical simulation, qubit cap, Python 3.8+, and an Author section),
   LICENSE (full GPL-3.0 text, verbatim), NOTICE and COPYRIGHT (`python3 tools/repokit.py license <repo> "<title>"`),
   SPDX `GPL-3.0-or-later` headers in source files, and the license and author fields in every manifest.
   Author: RUSSELL PHILIP SMITHSON <russellsmithson77@outlook.com>. That email is the only one allowed.
5. Rebuild any binaries or archives the host needs. If the push tool can't carry binaries, commit the source and
   build scripts and say so in the README.
6. Run the strict scan: `python3 tools/repokit.py scan <repo> --deny <private-patterns-file>` (keep the deny file
   outside the repo). Zero findings, or no push.
7. End-to-end gate (all of it must pass, or no push):
   - Copy the staged repo into a fresh empty folder, follow ONLY its README install steps, and launch it through the
     host's real entry point (MCP server over stdio, JS/TS module, Python tool class, exe, SK class, Dify tool, ...).
   - Through that entry point: show the function table, run one script per command family, run a preset, run
     `q.folder` on a small mixed folder, test a theory from a file and from a chat summary/transcript, and generate
     TXT+PDF reports. Validate the PDFs and compare results with `reference/`. `tests/e2e_mcp.py` does all of this
     for anything that speaks MCP or can be bridged to it.
   - Where the real host app installs for free without a login (npm/pip/official installer), install it in an
     isolated HOME and check it loads the plugin and lists its tools. Never sign in, never add API keys, never call
     the LLM. Where that isn't possible, use a stand-in host and mark the result `host-simulated` in the README and
     the log.
   - Write `E2E_RESULTS.md` into the repo. Record that SpinDoctor 3.1.2's own suite passed 18/18 with the three
     29-qubit checks adapted to the 298 limit (Russell approved publishing on that basis).
8. Create the repo (name `spindoctor-qwerty-<host>`; check it's free first), PUBLIC, push straight to `main` in
   small batches. Add a description (and topics if the tooling allows).
9. Read the tree back and compare it with the staged files. Clone it into a fresh folder and rerun a quick E2E. If
   that fails, fix it at once or make the repo private, and report.
10. Append a row to `results_3.1.2/PUBLISH_LOG.csv`: folder, repo URL, version, commit sha, file count, binaries
    status, E2E status, audit findings, time (PT).

## Hard rules
- Never use a password, token you weren't given, or start any sign-in or device-code flow.
- No secrets, machine paths, user names or other emails in anything you publish.
- A repo that fails its scan or its gate is NOT pushed. Log it and move on to the next folder.
- Don't change the engine's results. If you find an engine bug, fix it here first, rerun every test in this kit,
  and note it in `CHANGELOG.md`.
- Don't claim quantum advantage. SpinDoctor is a classical simulator.

## Report after each repo
Folder, repo URL, version, commit sha, key fixes, binaries status, a one-line E2E result, and the next folder.
