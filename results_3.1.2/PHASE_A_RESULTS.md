# Phase A results: engine 1.1.0 vs the updated SpinDoctor 3.1.2

Parity target: SpinDoctor 3.1.2, updated build `3.1.2-298-20261010`, built from a fresh scratch copy of Russell's
updated folder (read-only). What changed in that update: `DIFF_312_updated.md`.

## SpinDoctor 3.1.2 (C#) on the updated build
- Builds with the project's own .NET Framework `csc` build script.
- Its own test suite: **18/18** pass after adapting three checks that still expected the old 29-qubit limit
  (refusal of a 30-qubit circuit became refusal of a 299-qubit circuit; legacy dense-reference gate comparison
  restricted to gates with at most 3 targets). Russell approved publishing on that basis.
- Fresh references: all 241 presets in one session (240 completed; qc-198 fails with "Preset unavailable" because
  `q.compile synthesize` is unavailable), the chug series, a 298-qubit command replay
  (`reference/wide_ref_3.1.2-298.json`) and the 11-file 298-qubit example folder
  (`reference/wide298_example_ref.json`, files in `reference/examples/298-native-run/`).

## Engine 1.1.0 (Python) against those references
| Check | Result |
|---|---|
| 241 presets, same seeds as the reference session | 241/241 same outcome, phase and step count; 0 result differences (floating-point values compared within tolerance) |
| qc-198 | fails the same way as 3.1.2 |
| 298-qubit command replay (`tests/wide_parity.py`) | 0 differences (volatile timestamps excluded) |
| 298-qubit example folder (`tests/wide298_example_parity.py`) | PASS: same histogram, sampling mode and factor count |
| Function-table examples (`tests/functions_test.py`) | 168/168 run, 0 failures |
| Theory testing (`tests/theory_test.py`) | 43/43, and 43/43 with `--no-pypdf` |
| Validation suite (`tests/validate.py`) | 22/22 without NumPy, 32/32 with NumPy (statistics vs an independent statevector, determinism, 298/299 guardrails, basis z above 29, 59-qubit factor merge refused, reports) |
| MCP end-to-end over stdio (`tests/e2e_mcp.py`) | 12/12 |
| Chug (folder-ingest) series | 40/41; see below |

## Chug series (folder ingestion), engine 1.1.0
`08_cancel_long_running` is marked FAIL by the generic runner because the job completes instead of being cancelled.
The Python `q.folder` runs synchronously, so there is nothing running to cancel; this is a documented difference,
not a defect. Every other case matches the 3.1.2 expected outcome and message.

| Case | Result | Time |
|---|---|---|
| 01_smoke | PASS | [0.1s] |
| 02_functional | PASS | [0.9s] |
| 03_presets | PASS | [0.5s] |
| 04a_1_file | PASS | [0.0s] |
| 04b_64_files | PASS | [1.0s] |
| 04c_127_files | PASS | [1.6s] |
| 04d_128_files | PASS | [1.7s] |
| 04e_129_files_REJECT | PASS | [0.0s] |
| 04f_128_files_x_120_cmds_HEAVY | PASS | [39.2s] |
| 05a_size_4MiB_exact | PASS | [0.1s] |
| 05b_size_4MiB_plus1_REJECT | PASS | [0.0s] |
| 05c_120_commands | PASS | [0.4s] |
| 05c2_128_commands_REPORT_CAP | PASS | [0.3s] |
| 05d_129_commands_REJECT | PASS | [0.0s] |
| 05e_command_4096_chars | PASS | [0.0s] |
| 05f_command_4097_chars_REJECT | PASS | [0.0s] |
| 05g_angle_1e12 | PASS | [0.0s] |
| 05h_angle_over_REJECT | PASS | [0.0s] |
| 06a_bom_crlf | PASS | [0.0s] |
| 06b_unicode_and_space_names | PASS | [0.0s] |
| 06c_ordinal_sort | PASS | [0.1s] |
| 06d_comments_headings_blanks | PASS | [0.0s] |
| 06e_decoys_skipped | PASS | [0.1s] |
| 06f_same_stem_mixed | PASS | [0.1s] |
| 07a_prose_line | PASS | [0.0s] |
| 07b_code_fence | PASS | [0.0s] |
| 07c_unknown_command | PASS | [0.0s] |
| 07d_unquoted_semicolon | PASS | [0.0s] |
| 07e_qc198_unavailable | PASS | [0.0s] |
| 07f_nested_folder | PASS | [0.0s] |
| 07g_nested_input | PASS | [0.0s] |
| 07h_delete_refused | PASS | [0.0s] |
| 07i_invalid_utf8 | PASS | [0.0s] |
| 07j_empty_file | PASS | [0.0s] |
| 07k_json_bad_field | PASS | [0.0s] |
| 07l_qasm_no_header | PASS | [0.0s] |
| 07m_pdf_untagged | PASS | [0.0s] |
| 07n_csv_parameter_table | PASS | [0.0s] |
| 07o_no_supported_files | PASS | [0.0s] |
| 07p_good_good_BAD_good | PASS | [0.0s] |
| 08_cancel_long_running | FAIL | job completed != cancelled (after q.folder cancel) () [115.2s] |
