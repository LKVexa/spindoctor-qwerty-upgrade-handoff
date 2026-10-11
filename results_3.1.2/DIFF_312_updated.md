# SpinDoctor 3.1.2: updated build vs. the build we shipped

Compared: the updated SpinDoctor 3.1.2 folder (updated by Russell, read-only) against
(a) the `SHA256SUMS.txt` we shipped (614 entries, 13:39 PT) and (b) our release copy of the shipped build. A full file-by-file hash list was kept with the build notes (not published).

Update identity: **3.1.2-298-20261010** ("298-qubit update"). ProductVersion is still `3.1.2`.

## Summary of counts (updated `SHA256SUMS.txt`, 641 entries)

| Kind | Count | Notes |
|---|---|---|
| Changed | 43 | 9 C# engine sources, 2 carriers (TIFF/GIF), BOOT.cmd x2, UI HTML, docs, catalogue, MODEL/ENTRYPOINT, integrity + validation JSON |
| Added | 27 | `UPDATE-298.txt` (x3), `Examples/298-native-run/01..11-full-record-298.txt`, `validation/298-update/*.json` (11), plus the zip + `.sha256` (they were next to the shipped tree, not listed in the old sums) |
| Removed | 0 | |
| Not in sums | 5,347 | `SpinDoctor\workspace\**` - Russell's live session data (reports, checkpoints, archives). Not product files; excluded from the build and from parity. |

Note: `SpinDoctor-3.1.2.zip` is unchanged (13:39 PT) and does **not** contain the 298 update.

## Engine source changes (13 compiled files, 9 changed)

| File | Lines (+/-) | What changed |
|---|---|---|
| SpinDoctorTranches.cs | 81 | `MaximumLogicalQubits=298`, `MaximumFactorQubits=59`; global indices use `BigInteger`; new gate `mcx7` (7 controls + target, no angle); gate refused if it would merge a factor wider than 59; new `SampleZ` (one joint Born-Z draw per factor, one uniform per factor, state unchanged); status adds `maximumLogicalQubits`/`maximumJointFactorQubits`; checkpoint factor width <=59 |
| SpinDoctorCircuits.cs | 154 | circuits 1..298 qubits; `initialBasis` any width; circuits >29 qubits use `samplingMode=prepared-factor-Born-Z` (prepare once, sample each factor jointly per shot; basis **z only**, else error); new job fields `samplingMode`, `samplingFactorCount`, `samplingScope`; new operand error text (names the circuit, valid range, every bad operand, remedy); preset QUBITS up to 298; help gains `limits`; checkpoint validation for wide jobs |
| SpinDoctorCalculators.cs | 18 | `q.query` addresses up to 298 qubits with `BigInteger` indices/`start`; explicit gate matrices refuse >4 operands (mcx7) |
| SpinDoctorSyntax.cs | 9 | `q.query` field preflight uses the 298 limit (other calculator namespaces keep 29) |
| SpinDoctorSequences.cs | 30 | sequence/folder preflight: circuit/tranche widths 1..298, spin/measure qubit 0..297, basis index `BigInteger`; parameter schema `qubits.maximum=298` |
| SpinDoctorInputs.cs | 34 | JSON/TXT/QASM2/CSV-gate inputs accept 1..298 qubits; `initialBasis` any width; `limits.qubits=298`; QASM message "one qreg of1..298 qubits" |
| SpinDoctorTrancheTerminal.cs | 15 | `q.tranche prepare` 1..298 (new message); `q.tranche state` wide index; status scope text |
| SpinDoctorReports.cs | 27 | mcx7 equation text; wide input kets; PDF wire diagram skipped above 29 qubits (operand table instead); long bar labels shortened (first/last 7 bits) with a note; wide-mode work paragraph |
| QuantumTerminal.cs | 1 | `q.status` gains `coherentRegisterCapabilities` (updateId, 298, 59, BigInteger, wide basis z, prepared-factor-Born-Z) |

## What it means

* **Commands:** new gate `mcx7`. `q.circuit new/preset`, `q.tranche prepare` accept up to 298. `q.circuit run ... basis x|y` is refused above 29 qubits. Operand errors are reworded. No commands removed.
* **Limits:** 298 logical qubits; 59 per entangled factor (plus the memory budget); full joint query analysis still 16 qubits; auxiliary q.compile/q.qec/q.noise/q.resource keep 29; `q.tranche from` keeps its 29-address partition. Folder/sequence limits unchanged (128 files, 4 MiB, 128 commands, 4096 chars).
* **Formats:** inputs accept wider registers and big basis indices; nothing else changed in the parsers.
* **Reports:** wide circuit reports add sampling fields; PDFs skip the wire diagram above 29 and shorten long bar labels; CSV mcx7 equation. Small (<=29) circuits are unchanged: same replay sampling, same histograms.
* **Presets:** definitions unchanged; all 241 run the same (see the preset results).

## Build and tests on the updated build (fresh scratch copy)

* Build (.NET Framework csc, 13 sources): exit 0, 0 errors, 0 warnings.
* Own test suite (the same 18 tests as the 3.1.2 release), **unmodified**: 15/18 pass. The 3 failures are tests written for the old 29-qubit limit:
  * `engine_regressions`: the dense 3-qubit reference loop indexes past its array when it reaches the new 8-operand `mcx7`. The update's own `validation/298-update/harness-adaptations.json` documents this same adaptation (restrict to targetCount<=3).
  * `direct_preset_regressions`: expects `q.circuit preset qft 30` to be refused (it is now valid).
  * `csv_gate_regressions`: expects a 30-qubit CSV circuit to be refused (it is now valid).
* With those three assertions adapted in a scratch copy (`tests_adapted`, 29 -> 298 bound): **18/18 pass**. The shipped tests in the updated folder were not changed (read-only).

## Fresh reference outputs from the updated build

* **241 presets** (one session, `run_presets.ps1`): 240 completed, qc-198 failed ("Preset unavailable", `q.compile synthesize`), identical per-preset outcome/phase/step count to the shipped 3.1.2 run (0 differences). Step reports with TXT+PDF per command were kept with the scratch build (not published).
* **Chug series** (40 folders, 04f_HEAVY excluded as before): same job phase, file count and message as the shipped 3.1.2 run for all 40. 04c_127_files was first cut off by the harness's 240 s timeout while the PC was busy; rerun with a 900 s timeout, it completed 127/127.
* **Wide-register references** (new): direct 298/35-qubit circuits with mcx7, a wide initial basis, errors and high-index queries (`wide_ref.json`), plus the 11-file `Examples/298-native-run` folder at 10,240 shots (`wide298_example_ref.json`, 532 s in C#).

## Cartridge engine 1.1.0 parity with the updated build

* 241-preset replay against the updated references: 236 identical. The same 5 documented differences as before (qc-006/008/009 CPU-only reference instead of OpenCL GPU fields, qc-016 tranche checkpoint/accounting text, qc-019 state file name). qc-198 fails the same way.
* Wide direct-command replay: histograms, sampling fields, counters, all 4 error messages, `q.query`, `q.circuit state/spin` are identical.
* 298-qubit 11-file example through cartridge `q.folder`: identical histogram (73 outcomes), identical work counters (53 s in Python).
* Chug series through cartridge `q.folder`: 40/41 pass. 08_cancel doesn't apply: cartridge tool calls run synchronously, so there's no live job to cancel. The folder still completes; the host's call timeout plays that role.
* Engine tests: validate.py 32/32 (NumPy) and 22/22 (stdlib-only); theory_test 43/43; functions_test 168 examples, 0 failed (table now lists 298-qubit circuits and mcx7).
