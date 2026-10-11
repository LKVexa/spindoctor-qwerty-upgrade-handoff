# E2E results: spindoctor-qwerty-upgrade-handoff 1.1.0

This repo is a kit, not a plugin, so its end-to-end gate is: every tool and test script runs from a clean clone
per the README, every JSON/YAML file parses, and every link resolves. `python3 tools/check_kit.py` does all three.

Run on 2026-10-10 (PT) in a fresh empty folder with a minimal environment (`env -i`, fresh HOME), Python 3.13,
following only the README:

| Check | Result |
|---|---|
| JSON/YAML parse | PASS (24 JSON, 0 YAML) |
| `engine/examples/theory/make_sample_pdfs.py` | PASS |
| `tests/functions_test.py` | PASS, 168 examples, 0 failures |
| `tests/theory_test.py` | PASS, 43/43 |
| `tests/theory_test.py --no-pypdf` | PASS, 43/43 |
| `tests/validate.py` | PASS, 32/32 with NumPy (22/22 without NumPy, also run) |
| `tests/wide_parity.py` (C# 3.1.2-298 replay) | PASS, 0 differences |
| `tests/wide298_example_parity.py` | PASS |
| `tests/e2e_mcp.py` over stdio against `engine/scripts/spindoctor_mcp.py` | PASS, 12/12 (function table, 241 presets listed, one script per command family, 298-qubit mcx7 circuit, q.folder on a mixed folder, theory from a file, a chat summary with excerpts and an exported transcript, presets qc-001..qc-025 vs the updated-3.1.2 reference, 255 TXT+PDF reports valid) |
| `tools/repokit.py scan` (strict scan) | PASS, clean (also clean with the private deny list kept outside the repo) |
| Links in Markdown | 59 of 60 resolved before the push; the 60th is this repo's own URL, checked again after the push |

SpinDoctor 3.1.2 base: the updated build's own suite passes 18/18 with the three 29-qubit checks adapted to the
298 limit. Russell approved publishing on that basis.

Post-push: the repo was cloned back from GitHub into a fresh folder and `tools/check_kit.py` was run again,
including the link check (see the publish report and `results_3.1.2/PUBLISH_LOG.csv` in later updates).
