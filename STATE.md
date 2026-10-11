# STATE (as of 2026-10-10, PT)

## 1. Base and engine
- **Base:** SpinDoctor 3.1.2, updated build `3.1.2-298-20261010` (ProductVersion still 3.1.2). What the update changed:
  `results_3.1.2/DIFF_312_updated.md`. Summary: 298 logical qubits; 59 per entangled factor; `mcx7`
  (7 controls + target); circuits above 29 qubits use prepared-factor Born-Z sampling (basis z only); `BigInteger`
  basis indices; reworded operand errors; PDFs skip the wire diagram above 29 qubits. Folder and sequence limits are
  unchanged.
- **SpinDoctor 3.1.2's own tests:** 18/18 pass on the updated build with the three 29-qubit checks adapted to the
  298 limit (they tested refusal of a 30-qubit circuit; now 299). Russell approved publishing on that basis.
- **Engine 1.1.0** (`engine/`, `CARTRIDGE_VERSION = "1.1.0"`): pure Python 3.8+ standard library, NumPy optional.
  Six tools: `spindoctor_run_script`, `spindoctor_run_preset`, `spindoctor_list_presets`, `spindoctor_report`,
  `spindoctor_functions`, `spindoctor_test_theory`. Entry points: `engine/scripts/spindoctor_mcp.py` (MCP over
  stdio, JSON-RPC 2.0) and `engine/scripts/spindoctor_cli.py` (CLI and one-shot `tool` bridge, JSON in/out).
  Environment: `SPINDOCTOR_WORKSPACE` (default `~/spindoctor-workspace`), and for reproducible new workspaces
  `SPINDOCTOR_MEASUREMENT_SEED` and `SPINDOCTOR_FIELD_SEED`.

## 2. Phase A results (engine vs the updated 3.1.2)
Full numbers: `results_3.1.2/PHASE_A_RESULTS.md`.
- 241/241 presets: same outcome, phase and step count as fresh updated-3.1.2 references (240 completed; qc-198
  fails the same way in both: `q.compile synthesize` is unavailable in 3.1.2).
- Chug (folder-ingest) series: 40/41. `08_cancel_long_running` doesn't apply (the Python `q.folder` is synchronous).
- Kit tests: functions 168/168 examples, theory 43/43 (with and without pypdf), validate 22/22 (32/32 with NumPy), 298-qubit reference
  replay 0 differences, 298-qubit example folder PASS, MCP end-to-end 12/12.

## 3. Documented engine differences (accepted, not bugs)
- No GPU/OpenCL: the C# OpenCL timing and device fields aren't produced (CPU-only reference instead).
- C# work-accounting counters (internal operation counts and lifetimes) can differ; `tests/e2e_mcp.py` excludes
  them from strict comparison. Results, histograms, phases and step counts match.
- Tranche checkpoint wording and the session state file name differ slightly.
- `q.folder` runs synchronously, so `q.folder cancel` has nothing to cancel and `q.folder status` reports the
  finished job.

## 4. Published repos
| Folder | Repo | Commit |
|---|---|---|
| zed | https://github.com/LKVexa/spindoctor-qwerty-zed | 9ad7ae663ab12945507ecd11d009b97a4cd6c05b |
| amp | https://github.com/LKVexa/spindoctor-qwerty-amp | 4803b2e906ad88fb22f4dd06b3f7e50d6c31ba0f |
| antigravity | https://github.com/LKVexa/spindoctor-qwerty-antigravity | ab2e7519c9bd95ed79c530653d3a1002f7ca67da |
| anythingllm | https://github.com/LKVexa/spindoctor-qwerty-anythingllm | c5db7915554d75720a9973a7b528e1226ae2f49e |
| augment-auggie | https://github.com/LKVexa/spindoctor-qwerty-augment-auggie | bfd19b2ffbb36f26e399d7ae38708dbeebe80331 |
| CHATGPT_HANDOFF | https://github.com/LKVexa/spindoctor-qwerty-upgrade-handoff (this kit) | see the repo |

The log with E2E details: `results_3.1.2/PUBLISH_LOG.csv`.

## 5. Queue (Russell's order; next first)
chatgpt-codex, claude, claude-code, claude-desktop, cline, codebuddy, continue, copilot, cursor, deepseek-harness,
devin-cli, dify, factory-droid, flowise, gemini-cli, goose, grok_bot_skill, grok-build, hermes, kilo-code, kiro,
letta-code, midjourney, mistral-vibe, nous, openclaw, opencode, openhands, open-webui, pi, qoder-cli, qoderwork,
qwen-code, qwenpaw, roo-code, semantic-kernel.

The v1.0.0 source folders live in Russell's "Qwerty Plugin" delivery folder (not in this repo). Read them; don't
change them.

## 6. Schema drift found while preparing this kit
- Agent Plugins now publishes **1.1.0** schemas next to 1.0.0 (`schemas/agent-plugins/`). v1.0 validated against
  1.0.0. Check which version each host (Hermes portable, Copilot, Kiro, Qwen Code, Mistral Vibe, Codex) expects.
- MCPB now has **v0.4** and `latest` manifest schemas (`schemas/mcpb/`). v1.0's `.mcpb` used v0.3; re-check the
  Claude Desktop manifest against the current MCPB MANIFEST.md.

## 7. Toolchains used so far
- Python 3.8+ (tests ran on 3.13), Node 20+ for JS/TS hosts, Rust with `wasm32-wasip2` and `wasm-tools` for Zed,
  .NET SDK 8 for Semantic Kernel (v1.0 built it on Linux only), the official Dify CLI for `.difypkg`, `csc` (.NET
  Framework) for the midjourney companion exe. Install host CLIs in an isolated HOME; never sign in.

## 8. Per-host caveats and status
Docs links are as cited in v1.0; re-check each one (`DOCS_LINKS.md`). Order 6 is this kit.

| Order | Format | v1.0 folder | Docs (as cited in v1.0; re-check) | v1.0 caveats | Status |
|---|---|---|---|---|---|
| 1 | Zed | `zed` | https://zed.dev/docs/extensions/developing-extensions ; https://zed.dev/docs/extensions/mcp-extensions | User must set settings.engine path (WASM sandbox). repository URL in extension.toml is a placeholder (only matters for publishing). | **published** https://github.com/LKVexa/spindoctor-qwerty-zed (9ad7ae6). No GPU/Vulkan on the test box, so Zed itself ran host-simulated; wasm built from source (wasm-tools validated); the wasm is not committed (text-only push). |
| 2 | Amp | `amp` | https://ampcode.com/docs/customize/plugins | - | **published** https://github.com/LKVexa/spindoctor-qwerty-amp (4803b2e). Real Amp CLI loads and activates the plugin; `amp plugins list` needs a sign-in, so tool listing is host-partial. index.js exposes executeTool so results aren't re-run. |
| 3 | Antigravity | `antigravity` | https://www.antigravity.google/docs/plugins?tab=ide | Schema URL 404s; validated against schema text in docs. Plugin-relative MCP path. | **published** https://github.com/LKVexa/spindoctor-qwerty-antigravity (ab2e751). Real `agy` CLI validates, installs and lists the plugin; MCP tool listing host-simulated. |
| 4 | AnythingLLM | `anythingllm` | https://docs.anythingllm.com/agent/custom/developer-guide ; /plugin-json ; /handler-js | One entrypoint -> `action` param multiplexes 4 tools. | **published** https://github.com/LKVexa/spindoctor-qwerty-anythingllm (c5db791). Host-simulated with AnythingLLM's own unchanged loader (imported.js, MIT); setup_args PYTHON/WORKSPACE; handler hardened (timeouts, output caps, UTF-8). |
| 5 | Augment Auggie | `augment-auggie` | https://docs.augmentcode.com/cli/plugins | - | **published** https://github.com/LKVexa/spindoctor-qwerty-augment-auggie (bfd19b2). Published as an Auggie marketplace. Auggie expands ${AUGMENT_PLUGIN_ROOT} only in .mcp.json and hooks, not in commands/agents, so those now name the MCP tools and a skill-relative CLI fallback. |
| 7 | ChatGPT / Codex | `chatgpt-codex` | https://developers.openai.com/codex/plugins/build ; https://agent-plugins.org/ | Some codex-cli builds don't expand ${PLUGIN_ROOT} (openai/codex#22842) - absolute-path fallback in README. | queued #7 |
| 8 | Claude (.plugin) | `claude` | https://code.claude.com/docs/en/plugins-reference ; https://code.claude.com/docs/en/plugins | Same tree as #8; MCP server only used by hosts that launch local servers. | queued #8 |
| 9 | Claude Code | `claude-code` | https://code.claude.com/docs/en/plugins-reference | Windows: edit python3 -> python in .mcp.json if needed. | queued #9 |
| 10 | Claude Desktop (MCPB) | `claude-desktop` | https://github.com/modelcontextprotocol/mcpb/blob/main/MANIFEST.md | Folder AND .mcpb: spec defines the bundle as a ZIP; folder for review. | queued #10 |
| 11 | Cline | `cline` | https://github.com/cline/cline/blob/main/docs/customization/plugins.mdx ; docs/sdk/plugins.mdx | Cline SDK/CLI only. | queued #11 |
| 12 | CodeBuddy / WorkBuddy | `codebuddy` | https://www.workbuddy.ai/docs/zh/cli/plugins-reference | .lsp.json omitted (no language server for q.*). | queued #12 |
| 13 | Continue | `continue` | https://docs.continue.dev/reference | v1.0 shipped a machine-specific path; use a placeholder. | queued #13 |
| 14 | GitHub Copilot | `copilot` | https://docs.github.com/en/copilot/concepts/agents/about-plugins ; https://code.visualstudio.com/docs/copilot/customization/agent-plugins | - | queued #14 |
| 15 | Cursor | `cursor` | https://prod.cursor.com/docs/reference/plugins | Uses ${CURSOR_PLUGIN_ROOT} (Cursor doesn't expand ${PLUGIN_ROOT}). | queued #15 |
| 16 | DeepSeek Harness | `deepseek-harness` | https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/develop/basic/publish.md ; .../basic/tool.md | Not published (private). | queued #16 |
| 17 | Devin CLI | `devin-cli` | https://docs.devin.ai/cli/extensibility/plugins/overview | Native-layout root variable not explicit; ${CLAUDE_PLUGIN_ROOT} used. | queued #17 |
| 18 | Dify | `dify` | https://docs.dify.ai/en/develop-plugin/features-and-specs/plugin-types/plugin-info-by-manifest | .difypkg is unsigned (self-hosted needs signature verification off). | queued #18 |
| 19 | Factory Droid | `factory-droid` | https://docs.factory.com/harness/plugins | Needs local marketplace wrapper to install; ${DROID_PLUGIN_ROOT} documented for hooks, used in mcp.json. | queued #19 |
| 20 | Flowise | `flowise` | https://docs.flowiseai.com/integrations/langchain/tools/custom-tool ; https://docs.flowiseai.com/contributing/building-node | Export JSON shape from Flowise's Load/Export, not shown on the doc page; INode needs a Flowise source build. | queued #20 |
| 21 | Gemini CLI | `gemini-cli` | https://geminicli.com/docs/extensions/reference/ | - | queued #21 |
| 22 | goose | `goose` | https://goose-docs.ai/docs/guides/config-files/ | v1.0 shipped a machine-specific path; use a placeholder. | queued #22 |
| 23 | Grok Bot skill folder | `grok_bot_skill` | https://agentskills.io/specification | Downloadable bot packaging was out of scope in v1.0. | queued #23 |
| 24 | Grok Build | `grok-build` | https://github.com/xai-org/plugin-marketplace | Root variable undocumented; ${CLAUDE_PLUGIN_ROOT} used. | queued #24 |
| 25 | Hermes portable (Agent Plugins v1) | `hermes` | https://agent-plugins.org/ (spec 1.0.0 schemas) | - | queued #25 |
| 26 | Kilo Code | `kilo-code` | https://github.com/kilo-org/kilocode/blob/main/packages/kilo-docs/pages/automate/extending/plugins.md | - | queued #26 |
| 27 | Kiro | `kiro` | https://kiro.dev/docs/powers/create/ | - | queued #27 |
| 28 | Letta Code | `letta-code` | https://docs.letta.com/configuration/mods | - | queued #28 |
| 29 | Midjourney-companion style | `midjourney` | (no public Midjourney plugin spec) Agent Plugins 1.0 conventions | Python REQUIRED (exe launches bundled engine). | queued #29 |
| 30 | Mistral Vibe | `mistral-vibe` | https://github.com/mistralai/mistral-vibe/blob/main/vibe/plugins/builtins/vibe/skills/vibe/SKILL.md | No agents (TOML schema undocumented). | queued #30 |
| 31 | Nous Research Hermes Agent | `nous` | https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins ; https://hermes-agent.nousresearch.com/docs/guides/build-a-hermes-plugin | Tested with stub ctx, not a live Hermes install. | queued #31 |
| 32 | OpenClaw | `openclaw` | https://docs.openclaw.ai/plugins/manifest ; https://docs.openclaw.ai/plugins/sdk-entrypoints/define-plugin-entry | Not tested in a live OpenClaw. | queued #32 |
| 33 | OpenCode | `opencode` | https://docs.opencode.ai/docs/plugins/ ; https://opencode.ai/docs/config/ | Tools need @opencode-ai/plugin resolvable; opencode.json path placeholder. | queued #33 |
| 34 | OpenHands | `openhands` | https://docs.openhands.dev/overview/plugins | No documented root variable; ${CLAUDE_PLUGIN_ROOT} used; Python needed in sandbox. | queued #34 |
| 35 | Open WebUI | `open-webui` | https://docs.openwebui.com/features/extensibility/plugin/tools/development/ | engine_dir valve must point to engine on the server; no Function shipped. | queued #35 |
| 36 | Pi | `pi` | https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/packages.md ; .../docs/extensions.md | - | queued #36 |
| 37 | Qoder CLI | `qoder-cli` | https://docs.qoder.com/cli/plugins | ${QODER_PLUGIN_ROOT} documented for hooks; used in .mcp.json. | queued #37 |
| 38 | QoderWork Expert Kit | `qoderwork` | https://docs.qoder.com/qoderwork/expert-kits | Folder AND zip: upload path only accepts the ZIP. | queued #38 |
| 39 | Qwen Code | `qwen-code` | https://qwenlm.github.io/qwen-code-docs/en/users/extension/introduction/ | - | queued #39 |
| 40 | QwenPaw | `qwenpaw` | https://github.com/agentscope-ai/QwenPaw/blob/main/website/public/docs/plugins.en.md | Tools disabled by default (QwenPaw default); enable per agent. | queued #40 |
| 41 | Roo Code | `roo-code` | https://roocodeinc.github.io/Roo-Code/features/mcp/using-mcp-in-roo/ | Relative script path assumes workspace-root cwd. | queued #41 |
| 42 | Semantic Kernel (C#) | `semantic-kernel` | https://learn.microsoft.com/en-us/semantic-kernel/concepts/plugins/ | Built/tested on Linux box only (no SDK on PC). | queued #42 |
