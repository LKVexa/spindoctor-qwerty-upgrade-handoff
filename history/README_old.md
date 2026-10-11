# PARTIAL_RESULTS — read the labels

| Folder | What | Status |
|---|---|---|
| `parity_303_cartridge100/` | Feature parity audit: SpinDoctor **3.0.3** vs cartridge **1.0.0** across 41 formats (FEATURE_PARITY.md, feature_parity.csv, probe_compare.json = 163-command direct probe diff, fam_py.json / fam_js.json = 31-command family sweep through every entry point) | COMPLETE for 3.0.3, but **SECONDARY / superseded**: the 3.0.4-based audit was never started |
| `303_304_diff/` | Raw 3.0.3→3.0.4 diff: file list, per-file stats, unified C# diff, catalogue/presets/README diff, DIFF_303_304_PARTIAL.md | **PARTIAL**: text-level only, not semantically mapped, nothing ported, no 3.0.4 presets run |
| `v110_wip_tests/` | Test results of the 1.1.0 build **on the 3.0.3-based engine** (formats_results110.json 405/405, v110_wrappers.json 78/78 Python entry points, js_results.json 11/11, v110_js.json 11/11, fam_js110.json 11/11) | **PARTIAL / WIP**: proves the 1.1.0 design works, but it must be rebuilt on 3.0.4 and revalidated. The 241-preset parity replay, `validate.py`, and the Python family sweep were **stopped before finishing** for the 1.1.0 WIP |
