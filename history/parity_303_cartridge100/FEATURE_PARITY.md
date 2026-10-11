# FEATURE_PARITY — SpinDoctor 3.0.3 vs SpinDoctor Qwerty cartridge 1.0.0 (41 plugin formats)

Audit date 2026-10-10 (PT). Verify-only: no delivered plugin was changed by this audit.

Sources of truth: 3.0.3 C# sources in <3.0.3 build>/carrier_root/mvp (quantum\*.cs, byte-identical to the box copies; harness/kernel identical to the Desktop 3.0.3 package). Inventory derived from the dispatcher (QuantumTerminal.Execute), each module's Execute/Help, capability tables (AddCapabilities), TrancheRegister.SupportedGates and the LoopbackServer routes.

## Method

1. 241-preset replay (existing, stdlib + NumPy): every step compared with the 3.0.3 final run.
2. NEW direct probe: 163 commands (every subcommand, all 32 gates + aliases, flags, refusals, attachments/history/folder) run in the REAL 3.0.3 TerminalSession (compiled from source with Add-Type on Russell's PC) and in the cartridge with the SAME field/measurement seeds; results normalised (volatile timing/memory/ids excluded, FP <= 1e-9) and compared.
3. NEW wrapper sweep: a 31-command script touching every command family (circuit, query, math, resource, model, lesson, noise, qec, compile, algorithm, procedural grid, verify, tranche, preset/sequence, help/status, cartridge) run through every real entry point: 37 MCP server copies, 37 CLI bridges, 11 JS/TS modules (stand-in hosts), Nous/QwenPaw/Open WebUI/Dify Python classes, the Semantic Kernel class (.NET 8) and the companion exe (Windows). Each run checked 31/31 ok plus 31 TXT + 31 PDF report files.

## Headline verdict

The core simulator is at parity: every gate, circuit/tranche/procedural-grid command, all 77 calculator/analysis actions and all 241 presets give the same results as 3.0.3 when seeded identically. It is NOT a full feature clone: the attachment (q.input), command-history (q.history) and folder-batch (q.folder) families, sequence export/cancel, 'memory auto', the OpenCL GPU path and the desktop app's visual PDF/printout/equation features are missing, and jobs run synchronously. All 41 wrappers expose the full cartridge engine (every q.* command reachable); two (AnythingLLM, Flowise) squeeze it into one multiplexed tool, and the text wrappers cap a single reply at 60,000 characters.

## Counts (feature x engine)

| Status | Count |
|---|---|
| identical | 162 |
| different | 26 |
| missing | 22 |
| n/a | 7 |
| extra | 1 |
| **total** | 218 |

## Missing or different features

| Area | Feature | Status | Note |
|---|---|---|---|
| Circuit (q.circuit) | `q.circuit run` | different | 3.0.3 queues an asynchronous job (queued/job, poll q.circuit status); cartridge runs synchronously and returns the completed job inline. Final histogram and q.circuit result identical with the same seeds. |
| Circuit (q.circuit) | `q.circuit status` | different | Lifetime work-accounting counters differ by design (per-shot replay vs state clone); phase/histogram identical. |
| Circuit (q.circuit) | `q.circuit memory` | different | 'q.circuit memory MiB' identical; 'q.circuit memory auto' (measured-RAM auto budget) missing in cartridge ('Expected an unsigned decimal integer'). |
| Tranche register (q.tranche) | `q.tranche gate` | different | Gate results identical; 3.0.3 runs gates as cancellable background jobs (note text differs); cartridge is synchronous. |
| Tranche register (q.tranche) | `q.tranche status` | different | Default memory limit differs (3.0.3 sizes to measured RAM, cartridge 512 MiB); status omits checkpointStateRestored, allocated*Bytes, lifetimeActualWork; scope wording differs. |
| Tranche register (q.tranche) | `q.tranche cancel` | different | Accepted, but nothing to cancel (cartridge tranche work is synchronous). |
| Tranche register (q.tranche) | `q.tranche memory` | different | 'q.tranche memory MiB' identical; 'q.tranche memory auto' missing in cartridge. |
| Tranche register (q.tranche) | `q.tranche save` | different | Dense checkpoint written as JSON (spindoctor-tranche.json) instead of binary spindoctor-tranche-state.bin; not interchangeable with 3.0.3 checkpoints. |
| Procedural grid | `q.verify samples` | different | Same samples/outcome; scope text says CPU/reference instead of CPU/GPU (no OpenCL GPU backend). |
| Procedural grid | `q.verify status` | different | As q.verify samples (scope text). |
| Procedural grid | `q.status` | different | Cartridge status block omits runtimeSourceHashes, memoryPolicy, tranche.lifetimeActualWork/scope/checkpointStateRestored; adds cartridge fields. Lifetime work counters differ (cartridge clones the premeasured state per shot instead of replaying the circuit per shot). |
| Procedural grid | `q.export descriptor` | different | Omits runtimeSourceHashes (C# source hashes); verification scope text differs. |
| Procedural grid | `q.help` | different | Cartridge returns its own namespace/command summary + capability lists; 3.0.3 returns the procedural command list, verificationLimit, batch/shot limits. |
| Sequences & presets | `q.preset list` | different | All 241 presets returned with commands; registry metadata (schema, manifestSha256, available/conditional/needsBackend totals, backend per preset) absent; availability field named runtimeAvailability. |
| Sequences & presets | `q.preset show` | different | Card lacks nativeCapabilities, parameterSchema, selectionExecutes, scope; 'Unknown preset id.' vs 'Unknown preset ID.'. |
| Sequences & presets | `q.preset run` | different | 3.0.3 queues a background sequence job; cartridge runs it synchronously (same steps/results per 241-preset replay). |
| Sequences & presets | `q.sequence status` | different | Omits manifestSha256, totalJobs, recentJobIds, maximumCommands, scope. |
| Sequences & presets | `q.sequence help` | different | Lists 5 commands (no sequence cancel/export); jobBarriers absent; describes .q scripts instead of POSTed command arrays. |
| Sequences & presets | `q.sequence export` | missing | Re-reading a finished sequence job record by id is not implemented. |
| Sequences & presets | `q.sequence cancel` | missing | Not implemented (sequences are synchronous in the cartridge). |
| Attachments / history / folders | `q.input list` | missing | Attachment ingestion (JSON circuit specs, OpenQASM2 subset, TXT, CSV parameter sweeps, PDF-embedded programs): list/show/evaluate/import/run/delete/export/help. Not ported. |
| Attachments / history / folders | `q.input show` | missing | Attachment ingestion (JSON circuit specs, OpenQASM2 subset, TXT, CSV parameter sweeps, PDF-embedded programs): list/show/evaluate/import/run/delete/export/help. Not ported. |
| Attachments / history / folders | `q.input evaluate` | missing | Attachment ingestion (JSON circuit specs, OpenQASM2 subset, TXT, CSV parameter sweeps, PDF-embedded programs): list/show/evaluate/import/run/delete/export/help. Not ported. |
| Attachments / history / folders | `q.input import` | missing | Attachment ingestion (JSON circuit specs, OpenQASM2 subset, TXT, CSV parameter sweeps, PDF-embedded programs): list/show/evaluate/import/run/delete/export/help. Not ported. |
| Attachments / history / folders | `q.input run` | missing | Attachment ingestion (JSON circuit specs, OpenQASM2 subset, TXT, CSV parameter sweeps, PDF-embedded programs): list/show/evaluate/import/run/delete/export/help. Not ported. |
| Attachments / history / folders | `q.input delete` | missing | Attachment ingestion (JSON circuit specs, OpenQASM2 subset, TXT, CSV parameter sweeps, PDF-embedded programs): list/show/evaluate/import/run/delete/export/help. Not ported. |
| Attachments / history / folders | `q.input export` | missing | Attachment ingestion (JSON circuit specs, OpenQASM2 subset, TXT, CSV parameter sweeps, PDF-embedded programs): list/show/evaluate/import/run/delete/export/help. Not ported. |
| Attachments / history / folders | `q.input help` | missing | Attachment ingestion (JSON circuit specs, OpenQASM2 subset, TXT, CSV parameter sweeps, PDF-embedded programs): list/show/evaluate/import/run/delete/export/help. Not ported. |
| Attachments / history / folders | `q.history list` | missing | Per-command TXT/JSON archive index (list/show ID/export ID/help). Cartridge writes per-command TXT/JSON/PDF files but has no q.history command. |
| Attachments / history / folders | `q.history show` | missing | Per-command TXT/JSON archive index (list/show ID/export ID/help). Cartridge writes per-command TXT/JSON/PDF files but has no q.history command. |
| Attachments / history / folders | `q.history export` | missing | Per-command TXT/JSON archive index (list/show ID/export ID/help). Cartridge writes per-command TXT/JSON/PDF files but has no q.history command. |
| Attachments / history / folders | `q.history help` | missing | Per-command TXT/JSON archive index (list/show ID/export ID/help). Cartridge writes per-command TXT/JSON/PDF files but has no q.history command. |
| Attachments / history / folders | `q.folder run` | missing | Batch-run a folder of structured inputs (run path= downloads= purge=, status, cancel, help). Not ported. |
| Attachments / history / folders | `q.folder status` | missing | Batch-run a folder of structured inputs (run path= downloads= purge=, status, cancel, help). Not ported. |
| Attachments / history / folders | `q.folder cancel` | missing | Batch-run a folder of structured inputs (run path= downloads= purge=, status, cancel, help). Not ported. |
| Attachments / history / folders | `q.folder help` | missing | Batch-run a folder of structured inputs (run path= downloads= purge=, status, cancel, help). Not ported. |
| Errors & refusals | `Refusal: unknown namespace text` | different | 3.0.3 'Unknown quantum command. Use q.help.' vs cartridge 'Unknown command namespace. Use q.help.' |
| Errors & refusals | `Refusal: non q.* input` | different | 3.0.3 'Unknown quantum command.' vs cartridge 'Only native q.* commands are accepted.' |
| Errors & refusals | `Refusal: unquoted ';' in a command` | different | 3.0.3 'Invalid circuit name.' (context-specific) vs cartridge generic macro-separator refusal |
| Errors & refusals | `Refusal: .NET ArgumentException suffix` | different | 3.0.3 appends '\r\nParameter name: X' to some messages; cartridge omits it |
| Workspace, state & reports | `Asynchronous jobs + polling (circuit/tranche/verify/sequence)` | different | Cartridge executes synchronously; status/cancel commands exist but jobs are already complete. |
| Workspace, state & reports | `OpenCL GPU verification backend` | missing | Cartridge has CPU/reference only (NumPy optional). |
| Workspace, state & reports | `Per-command TXT report` | different | Cartridge TXT has its own layout (command, ok, result, guardrail); 3.0.3 'SPINDOCTOR — COMMAND RESULT' printout layout differs. |
| Workspace, state & reports | `Per-command JSON report` | different | Cartridge JSON is .NET-serializer-exact for the result; envelope fields differ from 3.0.3 history JSON. |
| Workspace, state & reports | `PDF reports` | different | 3.0.3 builds selected/session/circuit PDFs with histogram visuals on request (/api/reports); cartridge writes a text-only PDF per command (no visuals, no session/circuit kinds). |
| Workspace, state & reports | `Circuit printout (/api/circuit/printout)` | missing | Full-circuit printout endpoint not ported (q.circuit show/export give the data). |
| Workspace, state & reports | `Sequence printout / sequence JSON export` | missing | Not ported (see q.sequence export). |
| Workspace, state & reports | `Equation catalogue (/api/equations, EquationCatalogue.json)` | missing | Not shipped in the cartridge. |

## Full feature x engine matrix

| Area | Feature | Status | Evidence |
|---|---|---|---|
| Circuit (q.circuit) | `q.circuit new` | identical | preset replay 127 step(s) identical; probe 4 cmd(s): identical=3, different=1 |
| Circuit (q.circuit) | `q.circuit select` | identical | probe 1 cmd(s): identical=1 |
| Circuit (q.circuit) | `q.circuit list` | identical | preset replay 1 step(s) identical; probe 1 cmd(s): identical=1 |
| Circuit (q.circuit) | `q.circuit show` | identical | preset replay 116 step(s) identical; probe 1 cmd(s): identical=1 |
| Circuit (q.circuit) | `q.circuit add` | identical | preset replay 415 step(s) identical; probe 40 cmd(s): identical=40 |
| Circuit (q.circuit) | `q.circuit input` | identical | preset replay 128 step(s) identical; probe 1 cmd(s): identical=1 |
| Circuit (q.circuit) | `q.circuit clear` | identical | probe 1 cmd(s): identical=1 |
| Circuit (q.circuit) | `q.circuit delete` | identical | probe 2 cmd(s): identical=2 |
| Circuit (q.circuit) | `q.circuit preset` | identical | preset replay 3 step(s) identical; probe 4 cmd(s): identical=4 |
| Circuit (q.circuit) | `q.circuit run` | different | preset replay 128 step(s) identical; probe 5 cmd(s): different=3, identical=2 |
| Circuit (q.circuit) | `q.circuit status` | different | preset replay 129 step(s) identical; probe 1 cmd(s): different=1 |
| Circuit (q.circuit) | `q.circuit result` | identical | preset replay 115 step(s) identical; probe 1 cmd(s): identical=1 |
| Circuit (q.circuit) | `q.circuit state` | identical | preset replay 3 step(s) identical; probe 1 cmd(s): identical=1 |
| Circuit (q.circuit) | `q.circuit spin` | identical | preset replay 6 step(s) identical; probe 1 cmd(s): identical=1 |
| Circuit (q.circuit) | `q.circuit cancel` | identical | preset replay 1 step(s) identical; probe 1 cmd(s): identical=1 |
| Circuit (q.circuit) | `q.circuit export` | identical | preset replay 1 step(s) identical; probe 1 cmd(s): identical=1 |
| Circuit (q.circuit) | `q.circuit memory` | different | preset replay 1 step(s) identical; probe 2 cmd(s): identical=1, different=1 |
| Circuit (q.circuit) | `q.circuit capacity` | identical | probe 4 cmd(s): identical=4 |
| Circuit (q.circuit) | `q.circuit prune` | identical | probe 2 cmd(s): identical=2 |
| Circuit (q.circuit) | `q.circuit help` | identical | preset replay 1 step(s) identical; probe 1 cmd(s): identical=1 |
| Tranche register (q.tranche) | `q.tranche prepare` | identical | preset replay 1 step(s) identical; probe 1 cmd(s): identical=1 |
| Tranche register (q.tranche) | `q.tranche from` | identical | preset replay 1 step(s) identical; probe 1 cmd(s): identical=1 |
| Tranche register (q.tranche) | `q.tranche gate` | different | probe 5 cmd(s): different=4, identical=1 |
| Tranche register (q.tranche) | `q.tranche state` | identical | preset replay 1 step(s) identical; probe 1 cmd(s): identical=1 |
| Tranche register (q.tranche) | `q.tranche spin` | identical | preset replay 1 step(s) identical; probe 1 cmd(s): identical=1 |
| Tranche register (q.tranche) | `q.tranche measure` | identical | preset replay 2 step(s) identical; probe 2 cmd(s): identical=2 |
| Tranche register (q.tranche) | `q.tranche status` | different | preset replay 1 step(s), 1 with diffs; probe 1 cmd(s): different=1 |
| Tranche register (q.tranche) | `q.tranche cancel` | different | preset replay 1 step(s) identical; probe 1 cmd(s): identical=1 |
| Tranche register (q.tranche) | `q.tranche memory` | different | preset replay 1 step(s) identical; probe 2 cmd(s): identical=1, different=1 |
| Tranche register (q.tranche) | `q.tranche export` | identical | preset replay 1 step(s) identical; probe 1 cmd(s): identical=1 |
| Tranche register (q.tranche) | `q.tranche save` | different | preset replay 1 step(s), 1 with diffs; probe 1 cmd(s): different=1 |
| Tranche register (q.tranche) | `q.tranche resume` | identical | probe 1 cmd(s): identical=1 |
| Tranche register (q.tranche) | `q.tranche reset` | identical | probe 1 cmd(s): identical=1 |
| Tranche register (q.tranche) | `q.tranche release` | identical | probe 1 cmd(s): identical=1 |
| Tranche register (q.tranche) | `q.tranche help` | identical | preset replay 1 step(s) identical; probe 1 cmd(s): identical=1 |
| Procedural grid | `q.prepare` | identical | probe 1 cmd(s): identical=1 |
| Procedural grid | `q.migrate` | identical | probe 1 cmd(s): identical=1 |
| Procedural grid | `q.state` | identical | preset replay 1 step(s) identical; probe 1 cmd(s): identical=1 |
| Procedural grid | `q.gate` | identical | probe 13 cmd(s): identical=13 |
| Procedural grid | `q.verify rule` | identical | preset replay 1 step(s) identical; probe 1 cmd(s): identical=1 |
| Procedural grid | `q.verify samples` | different | preset replay 1 step(s), 1 with diffs; probe 1 cmd(s): different=1 |
| Procedural grid | `q.verify status` | different | probe 1 cmd(s): different=1 |
| Procedural grid | `q.verify cancel` | identical | probe 1 cmd(s): identical=1 |
| Procedural grid | `q.measure` | identical | preset replay 1 step(s) identical; probe 2 cmd(s): identical=2 |
| Procedural grid | `q.status` | different | preset replay 1 step(s), 1 with diffs; probe 1 cmd(s): different=1 |
| Procedural grid | `q.export descriptor` | different | preset replay 1 step(s), 1 with diffs; probe 1 cmd(s): different=1 |
| Procedural grid | `q.reset` | identical | probe 1 cmd(s): identical=1 |
| Procedural grid | `q.help` | different | probe 1 cmd(s): different=1 |
| Sequences & presets | `q.preset list` | different | probe 1 cmd(s): different=1 |
| Sequences & presets | `q.preset show` | different | probe 2 cmd(s): different=2 |
| Sequences & presets | `q.preset run` | different | probe 3 cmd(s): different=2, identical=1 |
| Sequences & presets | `q.sequence status` | different | probe 1 cmd(s): different=1 |
| Sequences & presets | `q.sequence help` | different | probe 1 cmd(s): different=1 |
| Sequences & presets | `q.sequence export` | missing | probe 1 cmd(s): missing=1 |
| Sequences & presets | `q.sequence cancel` | missing | probe 1 cmd(s): missing=1 |
| Calculators / analysis (q.math) | `q.math normalize` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.math) | `q.math norm` | identical | preset replay 1 step(s) identical; probe 1 cmd(s): identical=1 |
| Calculators / analysis (q.math) | `q.math probabilities` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.math) | `q.math bloch` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.math) | `q.math from-bloch` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.math) | `q.math validate-bloch` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.math) | `q.math density` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.math) | `q.math validate-density` | identical | preset replay 2 step(s) identical |
| Calculators / analysis (q.math) | `q.math purity` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.math) | `q.math entropy` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.math) | `q.math overlap` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.math) | `q.math fidelity` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.math) | `q.math trace-distance` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.math) | `q.math gate-matrix` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.math) | `q.math compare-gates` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.math) | `q.math unitary` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.math) | `q.math tensor` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.math) | `q.math commutator` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.math) | `q.math eigen` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.math) | `q.math expectation` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.math) | `q.math canonical-phase` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.query) | `q.query amplitudes` | identical | preset replay 1 step(s) identical; probe 1 cmd(s): identical=1 |
| Calculators / analysis (q.query) | `q.query probabilities` | identical | preset replay 1 step(s) identical; probe 1 cmd(s): identical=1 |
| Calculators / analysis (q.query) | `q.query marginal` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.query) | `q.query reduced-density` | identical | preset replay 2 step(s) identical |
| Calculators / analysis (q.query) | `q.query purity` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.query) | `q.query entropy` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.query) | `q.query expectation` | identical | preset replay 4 step(s) identical |
| Calculators / analysis (q.query) | `q.query concurrence` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.query) | `q.query negativity` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.query) | `q.query stabilizers` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.query) | `q.query fidelity` | identical | probe 1 cmd(s): identical=1 |
| Calculators / analysis (q.resource) | `q.resource memory` | identical | preset replay 3 step(s) identical |
| Calculators / analysis (q.resource) | `q.resource max-n` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.resource) | `q.resource factor-memory` | identical | preset replay 3 step(s) identical |
| Calculators / analysis (q.resource) | `q.resource tranche-plan` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.resource) | `q.resource sampling` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.resource) | `q.resource shots` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.resource) | `q.resource grover` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.resource) | `q.resource qec` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.resource) | `q.resource headroom` | identical | probe 1 cmd(s): identical=1 |
| Calculators / analysis (q.resource) | `q.resource auto` | identical | probe 1 cmd(s): identical=1 |
| Calculators / analysis (q.model) | `q.model spectrum` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.model) | `q.model ising` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.model) | `q.model qubo-to-ising` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.model) | `q.model evolve` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.model) | `q.model mbqc` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.model) | `q.model compare` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.model) | `q.model compare-codes` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.model) | `q.model topology` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.lesson) | `q.lesson amplitude-vs-probability` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.lesson) | `q.lesson entanglement` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.lesson) | `q.lesson complexity` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.lesson) | `q.lesson parallelism` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.lesson) | `q.lesson stabilizer` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.lesson) | `q.lesson magic` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.lesson) | `q.lesson algorithms` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.lesson) | `q.lesson pqc` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.noise) | `q.noise apply` | identical | preset replay 6 step(s) identical |
| Calculators / analysis (q.noise) | `q.noise circuit` | identical | preset replay 2 step(s) identical |
| Calculators / analysis (q.noise) | `q.noise t1` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.noise) | `q.noise t2` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.noise) | `q.noise readout` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.noise) | `q.noise zne` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.qec) | `q.qec repetition3` | identical | preset replay 4 step(s) identical |
| Calculators / analysis (q.qec) | `q.qec phase-repetition3` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.qec) | `q.qec validate` | identical | preset replay 2 step(s) identical |
| Calculators / analysis (q.qec) | `q.qec parameters` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.qec) | `q.qec correction-budget` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.qec) | `q.qec compare` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.compile) | `q.compile identity` | identical | preset replay 3 step(s) identical |
| Calculators / analysis (q.compile) | `q.compile simplify` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.compile) | `q.compile count` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.compile) | `q.compile depth` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.compile) | `q.compile classify` | identical | preset replay 2 step(s) identical |
| Calculators / analysis (q.compile) | `q.compile universality` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.algorithm) | `q.algorithm phase-estimation` | identical | preset replay 1 step(s) identical |
| Calculators / analysis (q.compile) | `q.compile synthesize` | identical | probe 1 cmd(s): different=1 |
| Attachments / history / folders | `q.input list` | missing | probe 1 cmd(s): missing=1 |
| Attachments / history / folders | `q.input show` | missing | probe 1 cmd(s): missing=1 |
| Attachments / history / folders | `q.input evaluate` | missing | probe 1 cmd(s): missing=1 |
| Attachments / history / folders | `q.input import` | missing | probe 1 cmd(s): missing=1 |
| Attachments / history / folders | `q.input run` | missing | probe 1 cmd(s): missing=1 |
| Attachments / history / folders | `q.input delete` | missing | probe 1 cmd(s): missing=1 |
| Attachments / history / folders | `q.input export` | missing | probe 1 cmd(s): missing=1 |
| Attachments / history / folders | `q.input help` | missing | probe 1 cmd(s): missing=1 |
| Attachments / history / folders | `q.history list` | missing | probe 1 cmd(s): missing=1 |
| Attachments / history / folders | `q.history show` | missing | probe 1 cmd(s): missing=1 |
| Attachments / history / folders | `q.history export` | missing | probe 1 cmd(s): missing=1 |
| Attachments / history / folders | `q.history help` | missing | probe 1 cmd(s): missing=1 |
| Attachments / history / folders | `q.folder run` | missing | probe 1 cmd(s): missing=1 |
| Attachments / history / folders | `q.folder status` | missing | probe 1 cmd(s): missing=1 |
| Attachments / history / folders | `q.folder cancel` | missing | probe 1 cmd(s): missing=1 |
| Attachments / history / folders | `q.folder help` | missing | probe 1 cmd(s): missing=1 |
| Gate set (q.circuit add / q.tranche gate) | `gate h` | identical | probe: q.circuit add h identical (descriptor hash and program equal) |
| Gate set (q.circuit add / q.tranche gate) | `gate x` | identical | probe: q.circuit add x identical (descriptor hash and program equal) |
| Gate set (q.circuit add / q.tranche gate) | `gate y` | identical | probe: q.circuit add y identical (descriptor hash and program equal) |
| Gate set (q.circuit add / q.tranche gate) | `gate z` | identical | probe: q.circuit add z identical (descriptor hash and program equal) |
| Gate set (q.circuit add / q.tranche gate) | `gate s` | identical | probe: q.circuit add s identical (descriptor hash and program equal) |
| Gate set (q.circuit add / q.tranche gate) | `gate sdg` | identical | probe: q.circuit add sdg identical (descriptor hash and program equal) |
| Gate set (q.circuit add / q.tranche gate) | `gate t` | identical | probe: q.circuit add t identical (descriptor hash and program equal) |
| Gate set (q.circuit add / q.tranche gate) | `gate tdg` | identical | probe: q.circuit add tdg identical (descriptor hash and program equal) |
| Gate set (q.circuit add / q.tranche gate) | `gate i` | identical | probe: q.circuit add i identical (descriptor hash and program equal) |
| Gate set (q.circuit add / q.tranche gate) | `gate sx` | identical | probe: q.circuit add sx identical (descriptor hash and program equal) |
| Gate set (q.circuit add / q.tranche gate) | `gate sxdg` | identical | probe: q.circuit add sxdg identical (descriptor hash and program equal) |
| Gate set (q.circuit add / q.tranche gate) | `gate rx` | identical | probe: q.circuit add rx identical (descriptor hash and program equal) |
| Gate set (q.circuit add / q.tranche gate) | `gate ry` | identical | probe: q.circuit add ry identical (descriptor hash and program equal) |
| Gate set (q.circuit add / q.tranche gate) | `gate rz` | identical | probe: q.circuit add rz identical (descriptor hash and program equal) |
| Gate set (q.circuit add / q.tranche gate) | `gate p` | identical | probe: q.circuit add p identical (descriptor hash and program equal) |
| Gate set (q.circuit add / q.tranche gate) | `gate u` | identical | probe: q.circuit add u identical (descriptor hash and program equal) |
| Gate set (q.circuit add / q.tranche gate) | `gate cx` | identical | probe: q.circuit add cx identical (descriptor hash and program equal) |
| Gate set (q.circuit add / q.tranche gate) | `gate cy` | identical | probe: q.circuit add cy identical (descriptor hash and program equal) |
| Gate set (q.circuit add / q.tranche gate) | `gate cz` | identical | probe: q.circuit add cz identical (descriptor hash and program equal) |
| Gate set (q.circuit add / q.tranche gate) | `gate ch` | identical | probe: q.circuit add ch identical (descriptor hash and program equal) |
| Gate set (q.circuit add / q.tranche gate) | `gate swap` | identical | probe: q.circuit add swap identical (descriptor hash and program equal) |
| Gate set (q.circuit add / q.tranche gate) | `gate cp` | identical | probe: q.circuit add cp identical (descriptor hash and program equal) |
| Gate set (q.circuit add / q.tranche gate) | `gate crx` | identical | probe: q.circuit add crx identical (descriptor hash and program equal) |
| Gate set (q.circuit add / q.tranche gate) | `gate cry` | identical | probe: q.circuit add cry identical (descriptor hash and program equal) |
| Gate set (q.circuit add / q.tranche gate) | `gate crz` | identical | probe: q.circuit add crz identical (descriptor hash and program equal) |
| Gate set (q.circuit add / q.tranche gate) | `gate rxx` | identical | probe: q.circuit add rxx identical (descriptor hash and program equal) |
| Gate set (q.circuit add / q.tranche gate) | `gate ryy` | identical | probe: q.circuit add ryy identical (descriptor hash and program equal) |
| Gate set (q.circuit add / q.tranche gate) | `gate rzz` | identical | probe: q.circuit add rzz identical (descriptor hash and program equal) |
| Gate set (q.circuit add / q.tranche gate) | `gate rzx` | identical | probe: q.circuit add rzx identical (descriptor hash and program equal) |
| Gate set (q.circuit add / q.tranche gate) | `gate cu` | identical | probe: q.circuit add cu identical (descriptor hash and program equal) |
| Gate set (q.circuit add / q.tranche gate) | `gate ccx` | identical | probe: q.circuit add ccx identical (descriptor hash and program equal) |
| Gate set (q.circuit add / q.tranche gate) | `gate cswap` | identical | probe: q.circuit add cswap identical (descriptor hash and program equal) |
| Gate set (q.circuit add / q.tranche gate) | `alias/operand cnot→cx` | identical | probe |
| Gate set (q.circuit add / q.tranche gate) | `alias/operand toffoli→ccx` | identical | probe |
| Gate set (q.circuit add / q.tranche gate) | `alias/operand fredkin→cswap` | identical | probe |
| Gate set (q.circuit add / q.tranche gate) | `alias/operand id/identity→i` | identical | probe |
| Gate set (q.circuit add / q.tranche gate) | `alias/operand u3→u` | identical | probe |
| Gate set (q.circuit add / q.tranche gate) | `alias/operand all` | identical | probe |
| Errors & refusals | `Refusal: unknown gate / bad operands / qubit out of range` | identical | probe q.circuit add bogus|cx 0 0|h 7: identical messages |
| Errors & refusals | `Refusal: 30-qubit circuit (1..29 range)` | identical | probe q.circuit new big 30 identical; validate.py |
| Errors & refusals | `Refusal: shots 0 / bad basis` | identical | probe identical |
| Errors & refusals | `Refusal: capacity 0/abc, prune users` | identical | probe identical (3.0.3 appends .NET 'Parameter name:' suffix) |
| Errors & refusals | `Refusal: dense memory budget exceeded (28-qubit dense)` | identical | validate.py PASS (same message family) |
| Errors & refusals | `Refusal: query before run / query on stale circuit` | identical | probe identical |
| Errors & refusals | `Refusal: unknown namespace text` | different | probe |
| Errors & refusals | `Refusal: non q.* input` | different | probe |
| Errors & refusals | `Refusal: unquoted ';' in a command` | different | probe |
| Errors & refusals | `Refusal: .NET ArgumentException suffix` | different | probe |
| Workspace, state & reports | `Workspace persistence of circuits/capacity/seeds/counters` | identical | validate.py persistence; test303 equivalents |
| Workspace, state & reports | `Capacity 1..1024 + preset-owned auto-prune` | identical | probe + preset replay (capacity/prune steps) |
| Workspace, state & reports | `Seeded SHA-256 Born sampling (same seeds -> same histogram)` | identical | probe with 3.0.3 seeds: all measurement results identical |
| Workspace, state & reports | `Asynchronous jobs + polling (circuit/tranche/verify/sequence)` | different | probe |
| Workspace, state & reports | `Measured-RAM memory planning (q.resource auto / headroom)` | identical | probe |
| Workspace, state & reports | `OpenCL GPU verification backend` | missing | code: QuantumCore OpenCL path vs backend.py |
| Workspace, state & reports | `Per-command TXT report` | different | file inspection |
| Workspace, state & reports | `Per-command JSON report` | different | file inspection |
| Workspace, state & reports | `PDF reports` | different | code: SpinDoctorReportPdf.Build vs reports.py |
| Workspace, state & reports | `Circuit printout (/api/circuit/printout)` | missing | code |
| Workspace, state & reports | `Sequence printout / sequence JSON export` | missing | code |
| Workspace, state & reports | `Equation catalogue (/api/equations, EquationCatalogue.json)` | missing | code |
| Workspace, state & reports | `q.cartridge info|limit|backend` | extra | code |
| UI / host only | `WinForms SimulationForm desktop window` | n/a | code: TIFFGifHoloHarness.cs, QuantumTerminal.cs LoopbackServer |
| UI / host only | `Loopback HTTP server + QUANTUM_TERMINAL.html browser terminal` | n/a | code: TIFFGifHoloHarness.cs, QuantumTerminal.cs LoopbackServer |
| UI / host only | `/api/command, /api/status, /api/presets, /api/history, /api/sequences endpoints` | n/a | code: TIFFGifHoloHarness.cs, QuantumTerminal.cs LoopbackServer |
| UI / host only | `Attachment upload UI (/api/attachments, AttachInput/AttachBinary)` | n/a | code: TIFFGifHoloHarness.cs, QuantumTerminal.cs LoopbackServer |
| UI / host only | `Report download controls` | n/a | code: TIFFGifHoloHarness.cs, QuantumTerminal.cs LoopbackServer |
| UI / host only | `TIFF/GIF holographic carrier packaging, carrier mount & VM` | n/a | code: TIFFGifHoloHarness.cs, QuantumTerminal.cs LoopbackServer |
| UI / host only | `Console colours / interactive prompt` | n/a | code: TIFFGifHoloHarness.cs, QuantumTerminal.cs LoopbackServer |
| Presets | `241 presets qc-001..qc-241` | identical | 241-preset replay (stdlib + NumPy) |

## Format x capability matrix

All formats: PDF/JSON reports are written to disk and their paths returned, but spindoctor_report returns TXT only (no PDF bytes in chat).

| Format | Tools surfaced | Capability | Entry-point tests |
|---|---|---|---|
| claude | 4 MCP tools (Claude Code/desktop); skill-only in claude.ai/Cowork upload | Full via MCP; in claude.ai the skill runs the CLI through the code tool (needs code execution) |  |
| chatgpt-codex | 4 MCP tools + skill | Full | PASS MCP<br>PASS CLI |
| grok_bot_skill | skill only (CLI + MCP launcher scripts) | Skill-only: host must run Python (code execution) - no native tools | PASS MCP<br>PASS CLI |
| nous | 4 native tools | Full | PASS register(ctx) |
| hermes | 4 MCP tools + skill | Full | PASS MCP<br>PASS CLI |
| copilot | 4 MCP tools + skill + agent | Full | PASS MCP<br>PASS CLI |
| midjourney | 4 MCP tools (C# exe -> Python) | Full; Python required | PASS MCP<br>PASS CLI<br>PASS companion exe on PC (31/31, 31 TXT + 31 PDF) |
| claude-code | 4 MCP tools + skill + 2 commands + agent | Full | PASS MCP<br>PASS CLI |
| claude-desktop | 4 MCP tools (MCPB) | Full | PASS MCP<br>PASS CLI |
| cursor | 4 MCP tools + skill/rule/agent/command | Full | PASS MCP<br>PASS CLI |
| gemini-cli | 4 MCP tools + skill + 2 TOML commands | Full | PASS MCP<br>PASS CLI |
| kiro | 4 MCP tools + skill | Full | PASS MCP<br>PASS CLI |
| opencode | 4 native tools (+ MCP snippet) | Full; replies >60k chars truncated (reports keep full output) | PASS MCP<br>PASS CLI<br>PASS JS-module (reply truncated at 60k chars) |
| openclaw | 4 native tools | Full; 60k reply cap | PASS MCP<br>PASS CLI<br>PASS JS-module (reply truncated at 60k chars) |
| grok-build | 4 MCP tools + skill/commands/agent | Full | PASS MCP<br>PASS CLI |
| letta-code | 4 native tools | Full; 60k reply cap | PASS MCP<br>PASS CLI<br>PASS JS-module (reply truncated at 60k chars) |
| qwen-code | 4 MCP tools + skill/agent/command | Full | PASS MCP<br>PASS CLI |
| qoder-cli | 4 MCP tools + skill/commands/agent | Full | PASS MCP<br>PASS CLI |
| qoderwork | 4 MCP tools + skill/commands | Full | PASS MCP<br>PASS CLI |
| pi | 4 native tools | Full; 60k reply cap | PASS MCP<br>PASS CLI<br>PASS JS-module (reply truncated at 60k chars) |
| amp | 4 native tools | Full; 60k reply cap | PASS MCP<br>PASS CLI<br>PASS JS-module (reply truncated at 60k chars) |
| antigravity | 4 MCP tools + skill/agent/rule | Full | PASS MCP<br>PASS CLI |
| cline | 4 native tools | Full | PASS MCP<br>PASS CLI<br>PASS JS-module |
| mistral-vibe | 4 MCP tools + skill + knowledge | Full | PASS MCP<br>PASS CLI |
| goose | 4 MCP tools (config only) | Full; no skill text shipped to the model | PASS MCP<br>PASS CLI |
| continue | 4 MCP tools (config only) | Full; agent mode only; no skill text | PASS MCP<br>PASS CLI |
| roo-code | 4 MCP tools + skill | Full | PASS MCP<br>PASS CLI |
| zed | 4 MCP tools (context server) | Full once settings.engine is set | PASS MCP<br>PASS CLI |
| factory-droid | 4 MCP tools + skill/commands/agent | Full | PASS MCP<br>PASS CLI |
| augment-auggie | 4 MCP tools + skill/commands/agent | Full | PASS MCP<br>PASS CLI |
| devin-cli | 4 MCP tools + skill/rule/agent | Full | PASS MCP<br>PASS CLI |
| kilo-code | 4 native tools | Full; 60k reply cap | PASS MCP<br>PASS CLI<br>PASS JS-module (reply truncated at 60k chars) |
| codebuddy | 4 MCP tools + skill/commands/agent | Full | PASS MCP<br>PASS CLI |
| openhands | 4 MCP tools + skill/commands/agent | Full; Python needed in sandbox | PASS MCP<br>PASS CLI |
| qwenpaw | 4 native tools (disabled by default) | Full once enabled | PASS plugin.register(api) |
| deepseek-harness | 4 native tools | Full; 60k reply cap; preset overrides as string | PASS MCP<br>PASS CLI<br>PASS JS-module (reply truncated at 60k chars) |
| anythingllm | 1 skill with action=script|preset|list|report | REDUCED ergonomics: single entry point multiplexes the 4 tools; no workspace param; 60k reply cap. All q.* commands still reachable | PASS MCP<br>PASS CLI<br>PASS JS-module (reply truncated at 60k chars) |
| open-webui | 4 Tool methods | Full; workspace via valve; 60k reply cap | PASS MCP<br>PASS CLI<br>PASS Tools.spindoctor_run_script |
| dify | 4 Dify tools | Full; workspace fixed to plugin temp dir (no per-call workspace); report files live inside the plugin runtime | PASS RunScriptTool._invoke |
| semantic-kernel | 4 KernelFunctions | Full | PASS MCP<br>PASS CLI<br>PASS C# SK class (31/31, 31 TXT + 31 PDF) |
| flowise | custom tool: 1 function action=...; INode: 1 structured tool action=... | REDUCED ergonomics like AnythingLLM (single tool); 60k reply cap; all q.* reachable | PASS MCP<br>PASS CLI<br>PASS JS-module (reply truncated at 60k chars)<br>PASS JS-module (reply truncated at 60k chars) |

### Formats with reduced capability

- **anythingllm**, **flowise**: host gives one entry point, so the 4 tools become one tool with `action`; no per-call workspace; replies capped at 60k chars. Every q.* command is still reachable via action=script.
- **grok_bot_skill** and the **claude** `.plugin` when uploaded to claude.ai/Cowork: skill-only (no MCP tools); needs the host's code-execution sandbox to run the bundled CLI.
- **goose**, **continue**: MCP config only, so the model gets tool schemas but no skill/usage text (Continue: agent mode only).
- **dify**: workspace fixed inside the plugin runtime; report files are not directly downloadable by the user.
- **zed**: full, but only after the user sets the engine path (WASM sandbox).
- **qwenpaw**: tools disabled by default in QwenPaw until enabled per agent.
- Text-returning wrappers (opencode, openclaw, letta-code, pi, amp, kilo-code, deepseek-harness, anythingllm, open-webui, flowise): one reply capped at 60,000 characters (q.help/q.status in a long script hit it); full output stays in the report files.
- All formats: no tool returns PDF bytes; `spindoctor_report` reads TXT only.

## Proposed fixes (not applied)

| # | Fix | Closes | Effort |
|---|---|---|---|
| 1 | Port q.input (JSON spec, OpenQASM2 subset, TXT, CSV sweeps, PDF tagged blocks) incl. limits and refusal texts | q.input x8 | L (2-3 days; ~560 C# lines + PDF extractor) |
| 2 | Add q.history list/show/export/help over the existing per-command report index | q.history x4 | S (2-4 h) |
| 3 | Add q.folder run/status/cancel/help (non-recursive, reuses #1) | q.folder x4 | M (1 day, after #1) |
| 4 | Add q.sequence export/cancel + job registry fields (manifestSha256, totalJobs, recentJobIds) and full preset registry/card metadata | sequence/preset diffs | S-M (0.5 day) |
| 5 | 'q.circuit memory auto' / 'q.tranche memory auto' via existing q.resource auto plan; tranche default limit from measured RAM | memory auto, tranche status | S (2 h) |
| 6 | Align texts: q.help/q.status blocks, unknown-namespace/non-q.* refusals, preset ID casing, optional 'Parameter name' suffix, scope strings | refusal/text diffs | S (2-4 h) |
| 7 | Optional async job mode (background thread + polling/cancel) behind a flag; default stays synchronous for agents | async semantics | M (1-2 days) |
| 8 | Binary tranche checkpoint compatible with 3.0.3 (.bin) or a converter | q.tranche save | M (1 day) |
| 9 | Visual PDF reports (selected/session/circuit kinds with histograms) + circuit/sequence printouts + equation catalogue | PDF/printout/equations | M-L (2-3 days) |
| 10 | Wrappers: add `spindoctor_report` format=pdf|json returning base64 or path; raise/page the 60k reply cap (return summary + report paths); expose workspace in AnythingLLM/Flowise/Dify; ship skill text with goose/continue configs (README snippet / instructions field) | format-level gaps | S-M (0.5-1 day across all 41) |
| - | OpenCL GPU backend | GPU path | n/a for a stdlib plugin (keep documented) |

Raw evidence: probe_commands.txt, probe_303.json, probe_py.json, probe_compare.json, fam_py.json, fam_js.json (in this folder).
