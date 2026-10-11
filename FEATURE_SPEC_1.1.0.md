# FEATURE SPEC: SpinDoctor Qwerty plugins v1.1.0

> **Status: DONE.** Implemented in engine 1.1.0 (`engine/spindoctor/functions.py`, `engine/spindoctor/theory.py`,
> `engine/spindoctor/api.py`, `engine/spindoctor/mcp_server.py`, `engine/scripts/spindoctor_cli.py`,
> `engine/examples/theory/`) on the updated SpinDoctor 3.1.2 base, and shipped in every published plugin repo
> (see `STATE.md`). This file is kept as the reference spec for the remaining repos and for audits.
> Limits follow the updated 3.1.2: up to 298 logical qubits, at most 59 per entangled factor, basis z above 29 qubits.

There are two capabilities. Both live in the shared Python engine and are exposed by every plugin repo, with the
same engine and the same presets in each.

---------------------------------------------------------------------
## A. In-chat function table — tool `spindoctor_functions`

**Purpose:** return a Markdown table of EVERY function or command the plugin implements, so the AI can show it in chat.

- Columns, exactly: `Function | What it does | Command to type`.
- Rows are grouped by command family, one `###` heading and one table per family: Circuits (q.circuit), Queries (q.query), Tranche (q.tranche), Procedural grid (q.prepare/q.migrate/q.gate/q.state/q.measure/q.verify/q.export/q.reset/q.status/q.help), Presets and sequences (q.preset/q.sequence), Resource (q.resource), Math (q.math), Models (q.model), Lessons (q.lesson), Noise (q.noise), QEC (q.qec), Compile (q.compile), Algorithm (q.algorithm), Cartridge (q.cartridge), a gate-set table, and a "Not available in this plugin" table (3.1.2 features that are not ported, each with the reason or alternative). Plus a first table covering the plugin tools themselves, including the three theory modes.
- Every "Command to type" is a **real, runnable example**. A test must run every example, top to bottom per family in a fresh workspace, with **0 failures**. Engine 1.1.0: 168 examples, 0 failures (`tests/functions_test.py`).
- Presets are a separate list (`section='presets'`): one row per preset (id, label and category, `q.preset run qc-NNN`), **all 241** (qc-198 is marked unavailable, as in 3.1.2).
- Parameters: `section` ∈ {commands (default: tools + every family + gates), gates, tools, presets, all}; `filter` is an optional case-insensitive text filter.
- Output: hosts that can carry plain text (MCP `content[0].text`, CLI stdout, JS/TS tools, SK, the companion exe) must return the **raw Markdown**, not JSON-escaped text. Object-returning hosts (for example Cline, Dify JSON) carry it in a `markdown` field.
- Every SKILL.md, agent, rules, or instructions file must tell the AI: *show this table verbatim when the user asks what the plugin can do, asks for help or functions, or on first use.*
- Footer line: classical FP64 simulation, up to 298 logical qubits with at most 59 in one entangled factor (plus this port's dense memory guard), not a quantum computer, no quantum-advantage claims.

Example (start of the rendered output):

```
## SpinDoctor Qwerty - plugin tools

| Function | What it does | Command to type |
|---|---|---|
| Function table (spindoctor_functions) | Show this table in chat | Ask: "show the SpinDoctor functions" (CLI: `spindoctor_cli.py functions`) |
| Test the theory we discussed (spindoctor_test_theory source=chat) | The AI summarises the theory from the conversation (claims, assumptions, variables, prediction), you confirm, then it is tested; quoted excerpts go in the report under 'Source: chat history'. An exported chat transcript (.txt/.md/.json/.html) also works | Ask: "test the theory we discussed" |

### Circuits (q.circuit) - build, run and inspect named circuits (1..298 logical qubits; one entangled factor <=59)

| Function | What it does | Command to type |
|---|---|---|
| q.circuit new | Create a named circuit with N logical qubits (1..298) and select it | `q.circuit new bell 2` |
| q.circuit add | Append a gate: name, then angles, then qubit(s); `all` = every qubit | `q.circuit add h 0` |
```

---------------------------------------------------------------------
## B. Theory testing — tool `spindoctor_test_theory`

### B1. Sources (`source`)
| source | Input | Notes |
|---|---|---|
| `file` | `path` to a local file: `.txt .md .markdown .pdf .py .json .csv .q .qs .text` | The size limit is 5 MiB. Extracted text is truncated at 60,000 chars and the truncation is recorded. PDF: use `pypdf` if it is importable. Otherwise use a **pure-Python fallback** that handles FlateDecode streams, Tj/TJ text operators, and **ToUnicode CMaps** (needed for LibreOffice/Word subset-font PDFs). |
| `text` | `text` = pasted theory | |
| `chat` | `text` = a theory summary the AI wrote from the conversation and the user confirmed. Optional `excerpts` = verbatim quotes ("User: …", "Assistant: …"). Optional `path` = an exported chat transcript | Transcript formats: plain `.txt`/`.md` ("User:/Assistant:" or "## User" style), ChatGPT `conversations.json` (mapping tree), Claude export JSON (`chat_messages`), generic `[{role, content}]` JSON, and `.html` chat exports. At least one of summary, excerpts, or transcript is required. |

Any `q.*` lines found in the source become the default script.

### B2. Actions
- `action='extract'`: read and parse the source only. Return the extracted text, the q.* lines, and the excerpts/transcript turns (capped), plus a "next" hint.
- `action='run'` (default): requires `hypothesis` and `prediction` (refuse without them) and a `script` (refuse if none was supplied or found). Optional: `checks`, `assumptions`, `variables`, `title`, `workspace`, and `isolate` (default **true**: run in a fresh sub-workspace `<workspace>/theory-runs/<run-id>` so circuit names never collide and runs are reproducible).

### B3. Machine checks (`checks`, list)
- `{kind:'probability', outcome:'00', expected:0.5, tolerance:0.05, command?:N}`: uses the last histogram (or command N). Bitstrings: qubit 0 is the RIGHTMOST bit. Also accepts zero/one counts from `q.measure`/`q.tranche measure`. Report the observed value, shots, and standard error.
- `{kind:'value', command:N, path:'result.fidelity', op:'approx|eq|ne|lt|le|gt|ge|contains|true|false', value:X, tolerance?:T}`
- `{kind:'ok', command:N, expected:true}`

### B4. Verdict rules
- No checks → **inconclusive** ("no machine-checkable prediction").
- Any check that cannot be evaluated (missing data or a failed command) → **inconclusive**.
- All checks pass → **supported** ("in the simulated model").
- Otherwise → **not supported**.

### B5. Theory test report (TXT + JSON + PDF, written under `<workspace>/reports/theory/theory-<run-id>.*`)
Sections, in order:
1. Title, created time (UTC, labelled), engine version and SpinDoctor base version, run workspace.
2. Source:
   - chat → **"Source: chat history"**: the confirmed summary, the transcript path, kind, and turn count, and **every excerpt quoted** with its role (`[1] User: "…"`), plus the note that the plugin cannot read chat itself and long chats may be truncated by the host's context window.
   - file → path, type, bytes, extractor (pypdf / pure-python), truncation, and an excerpt.
   - text → the pasted text.
3. Hypothesis; assumptions; variables.
4. Measurable prediction.
5. Script (numbered q.* lines).
6. Raw results (one line per command: ok/ERROR plus compact JSON).
7. Prediction vs result (PASS/FAIL/INCONCLUSIVE per check, with detail).
8. **VERDICT: SUPPORTED / NOT SUPPORTED / INCONCLUSIVE** plus the reason, and the failed command numbers.
9. Limits (verbatim list below) and the guardrail line.
JSON schema id: `SPINDOCTOR-QWERTY/THEORY-TEST/1`. The PDF uses the engine's built-in minimal PDF writer (no dependencies).

Limits text (must appear in every report):
- Classical FP64 simulation of an ideal circuit model (noise-free unless q.noise is used); not a quantum computer and no quantum-advantage claim.
- Registers up to 298 logical qubits, at most 59 qubits per entangled factor; dense factors are limited by the memory guard (22 qubits stdlib / 26 with NumPy) and the configured budget. Registers wider than 29 qubits sample in basis z only.
- Sampled histograms carry shot noise (standard error ~ sqrt(p(1-p)/shots)); seeded sampling is reproducible in one workspace.
- The verdict only covers what the q.* script encodes and what the checks state; it is not evidence about physical hardware or about claims outside the model.
- The plugin cannot read chat history or host attachments directly; it tests the summary, excerpts, or file content the AI passed in.

### B6. Skill/agent instructions (every format that has an instructions surface)
1. **Restate** the hypothesis → state a **measurable prediction** with checks → write a **q.* script** → (show the user) → **run** → **compare** → present the verdict and the report paths.
2. **Chat-history flow** ("test the theory we discussed"): gather the theory from the conversation the AI can see. Write a short summary (claims, assumptions, variables, measurable prediction). **Show it to the user and ask them to confirm or correct it before calling the tool.** Then call with `source='chat'`, the confirmed summary, and short verbatim excerpts. Say honestly that the plugin cannot read chat history (only the AI sees it) and that very long chats may be truncated by the host's context window. An exported transcript file is an alternative.
3. **Attachments:** a plugin cannot read chat attachments by itself; the host or AI must pass a file path or the content. Document how for each host in its README. Each published repo's README documents this for its host. **Verify each against current host docs** (`DOCS_LINKS.md`).
4. Never claim a theory is "proven"; the verdict is about the simulated model only.

### B7. Tests required
- A sample theory file per type (`.txt .md .pdf .py .json .csv .q`), at least 2 PDFs (one simple, one from LibreOffice/Word with subset fonts), run both with and without `pypdf`.
- A sample **multi-turn chat transcript** in each supported export format (txt, md, ChatGPT JSON, Claude JSON, html), plus a **summarized-theory call with excerpts** that checks the "Source: chat history" section and the quoted excerpts in the TXT and PDF.
- Verdict coverage: supported, not supported, inconclusive (no checks, and a failed command), refusals (no hypothesis, no script, chat with no content), and repeat runs isolated.
- A test that runs every function-table example (0 failures), and confirms the presets list has 241 rows and the table mentions `source=chat`.
- Both tools exercised through EVERY wrapper's real entry point (all MCP server copies, CLI bridges, JS/TS modules, Nous/QwenPaw/Open WebUI/Dify classes, the SK class, the companion exe, and the Zed context server command).

Results with engine 1.1.0 on the updated 3.1.2 base: theory tests 43/43 (with and without pypdf), function-table
examples 168/168, MCP end-to-end 12/12, and each published repo's clean-room gate through its real entry point (see
each repo's `E2E_RESULTS.md`). The earlier 1.1.0 work-in-progress results on the 3.0.3 base are in
`history/v110_wip_tests_on_303/`.
