# spindoctor-qwerty-upgrade-handoff

A handoff kit for the **SpinDoctor Qwerty** plugin family: everything another assistant (ChatGPT/Codex, Claude,
or a person) needs to keep building, auditing, and publishing the per-host plugin repos on the
**updated SpinDoctor 3.1.2 base** (update `3.1.2-298-20261010`) with the bundled **engine 1.1.0**.

This is a kit, not a plugin. It does not install into any host app.

## Status

| Item | Status |
|---|---|
| Base | SpinDoctor 3.1.2, updated build `3.1.2-298-20261010` (298 logical qubits, 59 per entangled factor, new `mcx7` gate, prepared-factor Born-Z sampling above 29 qubits) |
| Engine 1.1.0 ("SpinDoctor 3.1.2 parity") | **DONE.** Bundled in `engine/`. 241/241 presets match the updated-3.1.2 reference outcome, phase and step count; chug series 40/41 (the cancel case does not apply, see STATE.md); all kit tests pass |
| 1.1.0 features: in-chat function table, theory testing from files, pasted text and chat history | **DONE**, and shipped in every published plugin repo below |
| Plugin repos | 5 of 41 published. The rest are queued in Russell's order (see STATE.md) |

Published so far (public, `main`, version 1.1.0, each passed the strict scan and a clean-room end-to-end gate before and after the push):

| Folder | Repo |
|---|---|
| zed | https://github.com/LKVexa/spindoctor-qwerty-zed |
| amp | https://github.com/LKVexa/spindoctor-qwerty-amp |
| antigravity | https://github.com/LKVexa/spindoctor-qwerty-antigravity |
| anythingllm | https://github.com/LKVexa/spindoctor-qwerty-anythingllm |
| augment-auggie | https://github.com/LKVexa/spindoctor-qwerty-augment-auggie |

## What's inside

| Path | Purpose |
|---|---|
| `MASTER_PROMPT.md` | One pasteable prompt: goal, constraints, the per-repo spec, the end-to-end gate, and the report format |
| `WORKFLOW.md` | Ordered steps for each repo, each with an acceptance check |
| `STATE.md` | Where things stand: Phase A results, published repos, the queue, engine facts, documented differences, per-host caveats, schema drift |
| `FEATURE_SPEC_1.1.0.md` | The function-table and theory-testing spec (implemented; kept as the reference) |
| `ACCEPTANCE_CHECKLIST.md` | What gets checked before and after every push |
| `DOCS_LINKS.md` | Links to each host's official plugin documentation (replaces the old local doc snapshots) |
| `engine/` | The SpinDoctor Qwerty engine 1.1.0: pure Python 3.8+ standard library (NumPy optional), MCP server, CLI, 241 presets, theory examples |
| `tests/` | Engine tests and the generic MCP end-to-end harness (`e2e_mcp.py`) used for every repo's gate |
| `reference/` | Updated-3.1.2 reference outputs used by the tests (presets qc-001..qc-025, the 298-qubit command replay, the 11-file 298-qubit example folder) |
| `tools/repokit.py` | Bundle the engine, write LICENSE/NOTICE/COPYRIGHT, add SPDX headers, run the strict pre-push scan |
| `tools/skill_template.md` | The shared SKILL.md/instructions template used across the repos |
| `tools/check_kit.py` | Self-check: parse every JSON/YAML, run every test, run the scan, check every link |
| `schemas/` | Upstream JSON schemas for offline manifest checks (Agent Plugins 1.0.0/1.1.0, MCPB v0.3/v0.4/latest, AnythingLLM), with their licenses |
| `results_3.1.2/` | `PHASE_A_RESULTS.md`, `DIFF_312_updated.md` (what the 298-qubit update changed), chug results, the publish log |
| `history/` | Older material, kept for context only: the v1.0.0 validation snapshot, the 3.0.3 parity audit, the partial 3.0.3 to 3.0.4 diff, and the 1.1.0 work-in-progress results on the 3.0.3 base |

## Quick start (from a clean clone)

Needs Python 3.8 or newer. No packages are required; `pypdf`, `jsonschema`, `pyyaml` and `numpy` are used if present.

```
git clone https://github.com/LKVexa/spindoctor-qwerty-upgrade-handoff
cd spindoctor-qwerty-upgrade-handoff
python3 tools/check_kit.py              # everything, about 3 minutes; the link check needs internet
python3 tools/check_kit.py --offline    # same, without the link check
```

On Windows use `python` instead of `python3`.

Run the pieces one by one (each takes the bundled `engine/` and `reference/` by default):

```
python3 engine/examples/theory/make_sample_pdfs.py      # writes the two sample theory PDFs (run this first)
python3 tests/functions_test.py                         # every function-table example runs (168 examples, 0 failures)
python3 tests/theory_test.py                            # theory testing, 43 checks
python3 tests/theory_test.py --no-pypdf                 # same, forcing the built-in PDF text extractor
python3 tests/validate.py                               # statistics, guardrails, reports, scaling (22 checks; 32 with NumPy)
python3 tests/wide_parity.py                            # replays the C# 3.1.2-298 wide-register reference
python3 tests/wide298_example_parity.py                 # the 11-file 298-qubit example folder vs C#
python3 tests/e2e_mcp.py --server python3 engine/scripts/spindoctor_mcp.py --examples engine/examples/theory
python3 tools/repokit.py scan .                         # strict pre-push scan
```

Use the engine directly:

```
python3 engine/scripts/spindoctor_cli.py functions
python3 engine/scripts/spindoctor_cli.py run "q.circuit new bell 2" "q.circuit add h 0" "q.circuit add cx 0 1" "q.circuit run shots 1000 basis z"
```

To hand the work to another assistant, paste `MASTER_PROMPT.md` and give it this repo.

## The function table and theory testing

Every plugin exposes `spindoctor_functions`, which returns a Markdown table of every command (grouped by family,
each row with a runnable example) plus the 241 presets on request. `spindoctor_test_theory` tests a hypothesis
from a file (`.txt .md .pdf .py .json .csv .q`), pasted text, or the chat: the AI summarizes the theory from the
conversation, the user confirms it, and the tool runs a `q.*` script and writes a TXT+PDF theory test report with a
verdict (supported / not supported / inconclusive). A plugin can't read chat history itself; only the AI sees it.
Details: `FEATURE_SPEC_1.1.0.md`.

## What was left out, and why

- **Host documentation snapshots** (the old `tools/doc_snapshots/`, 57 files copied from vendor sites): third-party
  documentation without a clear redistribution license. Replaced by links in `DOCS_LINKS.md`.
- **The v1.0.0 41-format build scripts, format tests, JS test harness, Zed source and companion source**: they built
  and tested the old single-folder v1.0.0 delivery from machine-specific paths and can't run from a clean clone.
  Each published repo now carries its own sources, build scripts and tests.
- **Raw C# source diffs** for 3.0.3 to 3.0.4: superseded by the 3.1.2 base. `results_3.1.2/DIFF_312_updated.md`
  covers the current base.
- **The chug test series** (folder-ingest tests, about 11 MB of generated files): delivered to Russell separately.
  Only its results are here.
- Machine paths, user names and other emails have been removed throughout.

## Honest limits

- SpinDoctor is a **classical** simulator: FP64 arithmetic on an ordinary computer. It is not a quantum computer,
  doesn't connect to quantum hardware, and claims no quantum speed-up or advantage.
- Up to 298 logical qubits, but at most 59 qubits in any one entangled factor, plus the memory budget. Registers
  wider than 29 qubits sample in basis z only. Full joint query analysis is limited to 16 qubits.
- The Python engine matches SpinDoctor 3.1.2 results. It doesn't reproduce GPU/OpenCL timing fields or the C#
  work-accounting counters (see STATE.md). `q.folder` runs synchronously, so `q.folder cancel` has nothing to cancel.
- Python 3.8+ is required wherever a plugin runs the engine.

## Author and license

Author: RUSSELL PHILIP SMITHSON <russellsmithson77@outlook.com>

Copyright (C) 2026 RUSSELL PHILIP SMITHSON. Licensed under the GNU General Public License v3.0 or later
(`GPL-3.0-or-later`); see `LICENSE`, `NOTICE` and `COPYRIGHT`.

Third-party material: only the JSON schemas in `schemas/` (Apache-2.0, MIT/Apache-2.0 and MIT; see `NOTICE` and
`schemas/LICENSES/`). Host names are trademarks of their owners and are used only to describe compatibility.
