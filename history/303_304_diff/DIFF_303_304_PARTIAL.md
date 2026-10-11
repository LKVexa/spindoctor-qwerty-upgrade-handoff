# PARTIAL — SpinDoctor 3.0.3 -> 3.0.4 diff (file/text level only, NOT semantically mapped)

Status: **PARTIAL**. Work stopped 2026-10-10 ~03:00 PT on Russell's change of plan. Nothing below has been ported to the Python engine, and no 3.0.4 preset has been run.

Compared trees:
- 3.0.3: `<3.0.3 tree>/mvp` (the tree the released 3.0.3 GIF cartridge materialises; VERSION.txt = `3.0.3-hardened`)
- 3.0.4: `<SpinDoctor 3.0.4>/source/mvp` (read-only original; a scratch copy was made with robocopy, 3,867 files / 314 MB, untouched since). VERSION.txt = `3.0.4-hardened`.

## What the raw diff shows

- 54 entries differ (`file_level_diff.txt`): 48 changed files, 6 new files in 3.0.4 (`PACKAGE_TOOLS.md`, `PACKAGE_TOOLS.ps1`, `SpinDoctor-3.0.4-Release-Notes.txt`, `native/README.md`, `native/loopback_http.py`, `native/requirements.txt`), 0 removed.
- C# engine (`quantum/*.cs`), lines removed / added: QuantumTerminal 34/84, SpinDoctorTranches 38/95, SpinDoctorCommandReports 12/69, SpinDoctorTrancheTerminal 15/57, SpinDoctorPdfInputs 17/25, SpinDoctorInputs 10/22, SpinDoctorSequences 11/22, SpinDoctorCalculators 13/20, SpinDoctorCircuits 8/16, SpinDoctorReports 8/9, SpinDoctorSyntax 2/2, SpinDoctorAdvanced 1/1, QuantumCore 0/0. Full unified diff: `quantum_cs_303_to_304.diff`.
- Presets (`SPINDOCTOR_PRESETS.json`): still 241, the same ids, **no preset entry or command changed** (only top-level descriptive metadata changed). qc-198 is still deliberately unavailable.
- Command catalogue: only wording changed, plus a "CURRENT CIRCUIT STORAGE COMMANDS" section documenting `q.circuit capacity [N]` (1..1024, default 64) and `q.circuit prune presets [KEEP]`. The 1.0.0 cartridge already implements both.
- `ProductVersion` = `3.0.4-hardened`. The installed-namespace list in QuantumTerminal still contains `q.prepare q.migrate q.gate q.state q.verify q.measure q.status q.reset q.export q.tranche q.circuit q.input q.help q.history`.
- New or changed limits and messages I spotted (not exhaustive): PDF export at most 5,000 command records ("A PDF export contains at most5000 command records."), resolved PDF archives at most 64 MiB, input upload bounds (PDF 4 MiB, text 5 MiB, 32 preserved sources, 30 MiB total, folder 4 MiB / 128 files, non-recursive), checkpoint persistence failure appended to errors, verification `totalLimit` (at most 1024 digits), and `gpuBatchLimit` 16384.
- Per CHANGELOG.txt, the theme is hardening: bounded parsing, atomic publication, cancellation/RNG recovery, preset-capacity preflight and pruning, tranche indices, ownership, reset context, and numeric extremes.

## Not done (left for ChatGPT)
1. A semantic mapping of every C# hunk to user-visible behaviour (results, error text, limits, report fields).
2. Building and running all 241 presets from the scratch copy to get fresh 3.0.4 reference reports. 3.0.4 also ships its own run in `validation\presets` (3,311 files). Use it only for cross-checking, not as a substitute for your own run.
3. Porting the deltas into the Python engine and replaying the 241 presets for parity, with both the NumPy and the stdlib backends.
