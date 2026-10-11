# Qwerty Plugin — VALIDATION

Generated 2026-10-10 (PT). All formats share one engine: SpinDoctor Scripter Cartridge 1.0.0 (SpinDoctor 3.0.3 semantics, stdlib-only Python, NumPy optional) and one stdio MCP server (`spindoctor_mcp.py`, JSON-RPC 2.0, protocol 2025-11-25 .. 2024-11-05).

**Guardrail:** classical FP64 simulation, not a quantum computer, no quantum advantage claimed. No hooks run anything; no format touches the network.

## Engine validation

- 241-preset parity replay vs 3.0.3 final run (stdlib and NumPy backends identical): 240 completed + qc-198 refused exactly like 3.0.3 (q.compile synthesize not implemented); 1292/1292 steps same ok/error outcome; 40 exact diffs in 5 presets are expected (ledger timestamps qc-009, wording of scope strings qc-006/qc-016, extra 3.0.3 status fields qc-008, state file name qc-019); 29 FP last-digit diffs; work counters differ by design.
- validate.py: 29/29 PASS with NumPy (chi-square/TVD vs independent statevector, Fisher combined p, seed determinism, 1..29 qubit range, GHZ-29 sparse, dense 28-qubit refused with memory-budget message, persistence, TXT/JSON/PDF integrity, pdfinfo/pdftotext) and 19/19 stdlib-only.
- Official MCP Python SDK client (mcp 2.3.0): PASS against the shipped Claude Desktop and Hermes server copies.
- Offline format suite (tests/formats_test.py): 291/291 checks PASS (every JSON/YAML/TOML parses; Agent Plugins 1.0, MCPB v0.3 and AnythingLLM JSON Schemas; documented required fields; SKILL/agent/command/rule frontmatter; hooks empty; stdio MCP initialize/tools/list/tools/call through every shipped launcher; CLI bridge through every copy; Nous/QwenPaw/Open WebUI/Dify stubs).
- JS/TS host-stub suite (jstest/test_js.mjs, Node 20): 11/11 PASS.
- Windows (Russell's PC, Python 3.14.8): companion exe MCP test PASS; Python MCP servers for claude-code, claude-desktop, goose PASS.

## Toolchains (box only, none installed on the PC)

- Rust: rustc 1.99.0 / cargo 1.99.0, target wasm32-wasip2 (rustup)
- .NET SDK 8.0.425 + NuGet (Microsoft.SemanticKernel 1.81.0)
- dify plugin CLI v0.6.11 (langgenius/dify-plugin-daemon release binary)
- Node 20.19.2, TypeScript 7.0.2, @opencode-ai/plugin, @kilocode/plugin, zod, @langchain/core (test-only, in the JS test harness)
- PC: only the in-box .NET Framework csc.exe (v4.0.30319) was used to compile the companion exe.

## Format table

| # | Format | Path (under Qwerty Plugin\) | Docs cited | Validation | Checks | Caveats |
|---|---|---|---|---|---|---|
| 1 | Claude (.plugin) | `claude\spindoctor-qwerty.plugin` | https://code.claude.com/docs/en/plugins-reference ; https://code.claude.com/docs/en/plugins | zip of the claude-code tree | 1/1 PASS | Same tree as #8; MCP server only used by hosts that launch local servers. |
| 2 | ChatGPT / Codex | `chatgpt-codex\spindoctor-qwerty\ (+ .zip)` | https://developers.openai.com/codex/plugins/build ; https://agent-plugins.org/ | Agent Plugins 1.0 schema | 8/8 PASS | Some codex-cli builds don't expand ${PLUGIN_ROOT} (openai/codex#22842) - absolute-path fallback in README. |
| 3 | Grok Bot skill folder | `grok_bot_skill\` | https://agentskills.io/specification | SKILL.md frontmatter, CLI bridge | 3/3 PASS | Downloadable bot packaging left to Russell (scope change). |
| 4 | Nous Research Hermes Agent | `nous\spindoctor-qwerty\` | https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins ; https://hermes-agent.nousresearch.com/docs/guides/build-a-hermes-plugin | stub ctx register(ctx) test | 3/3 PASS | Tested with stub ctx, not a live Hermes install. |
| 5 | Hermes portable (Agent Plugins v1) | `hermes\spindoctor-qwerty\` | https://agent-plugins.org/ (spec 1.0.0 schemas) | Agent Plugins 1.0 schemas | 7/7 PASS | - |
| 6 | GitHub Copilot | `copilot\spindoctor-qwerty\` | https://docs.github.com/en/copilot/concepts/agents/about-plugins ; https://code.visualstudio.com/docs/copilot/customization/agent-plugins | Agent Plugins schemas, agent frontmatter, hooks v1 empty | 10/10 PASS | - |
| 7 | Midjourney-companion style | `midjourney\spindoctor-qwerty-companion\` | (no public Midjourney plugin spec) Agent Plugins 1.0 conventions | exe built with csc on PC; offline initialize/tools/list/tools/call/ping/unknown-tool test PASS | 7/7 PASS | Python REQUIRED (exe launches bundled engine). Exe SHA256 cf6d1cd9d6661226f6f51c36ed70cad6903cb3e953c1b7c25c0c1f4f1308e781 |
| 8 | Claude Code | `claude-code\spindoctor-qwerty\` | https://code.claude.com/docs/en/plugins-reference | manifest fields, frontmatter, MCP | 10/10 PASS | Windows: edit python3 -> python in .mcp.json if needed. |
| 9 | Claude Desktop (MCPB) | `claude-desktop\spindoctor-qwerty\ + spindoctor-qwerty.mcpb` | https://github.com/modelcontextprotocol/mcpb/blob/main/MANIFEST.md | MCPB v0.3 JSON schema; official MCP SDK client test | 5/5 PASS | Folder AND .mcpb: spec defines the bundle as a ZIP; folder for review. |
| 10 | Cursor | `cursor\spindoctor-qwerty\` | https://prod.cursor.com/docs/reference/plugins | manifest, .mdc rule frontmatter | 10/10 PASS | Uses ${CURSOR_PLUGIN_ROOT} (Cursor doesn't expand ${PLUGIN_ROOT}). |
| 11 | Gemini CLI | `gemini-cli\spindoctor-qwerty\` | https://geminicli.com/docs/extensions/reference/ | JSON + TOML commands parse | 7/7 PASS | - |
| 12 | Kiro | `kiro\spindoctor-qwerty\` | https://kiro.dev/docs/powers/create/ | Agent Plugins schemas | 7/7 PASS | - |
| 13 | OpenCode | `opencode\spindoctor-qwerty\` | https://docs.opencode.ai/docs/plugins/ ; https://opencode.ai/docs/config/ | real @opencode-ai/plugin tool() helper, run_script | 5/5 PASS | Tools need @opencode-ai/plugin resolvable; opencode.json path placeholder. |
| 14 | OpenClaw | `openclaw\spindoctor-qwerty\` | https://docs.openclaw.ai/plugins/manifest ; https://docs.openclaw.ai/plugins/sdk-entrypoints/define-plugin-entry | stub api.registerTool | 8/8 PASS | Not tested in a live OpenClaw. |
| 15 | Grok Build | `grok-build\spindoctor-qwerty\` | https://github.com/xai-org/plugin-marketplace | manifest, hooks empty | 12/12 PASS | Root variable undocumented; ${CLAUDE_PLUGIN_ROOT} used. |
| 16 | Letta Code | `letta-code\` | https://docs.letta.com/configuration/mods | stub letta.tools.register | 3/3 PASS | - |
| 17 | Qwen Code | `qwen-code\spindoctor-qwerty\` | https://qwenlm.github.io/qwen-code-docs/en/users/extension/introduction/ | native + Agent Plugins schemas | 11/11 PASS | - |
| 18 | Qoder CLI | `qoder-cli\spindoctor-qwerty\` | https://docs.qoder.com/cli/plugins | manifest, hooks empty | 12/12 PASS | ${QODER_PLUGIN_ROOT} documented for hooks; used in .mcp.json. |
| 19 | QoderWork Expert Kit | `qoderwork\spindoctor-qwerty\ + spindoctor-qwerty-kit.zip` | https://docs.qoder.com/qoderwork/expert-kits | manifest, hooks empty | 13/13 PASS | Folder AND zip: upload path only accepts the ZIP. |
| 20 | Pi | `pi\spindoctor-qwerty\` | https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/packages.md ; .../docs/extensions.md | stub pi.registerTool | 6/6 PASS | - |
| 21 | Amp | `amp\spindoctor-qwerty\` | https://ampcode.com/docs/customize/plugins | stub amp.registerTool | 3/3 PASS | - |
| 22 | Antigravity | `antigravity\spindoctor-qwerty\` | https://www.antigravity.google/docs/plugins?tab=ide | manifest, hooks empty | 10/10 PASS | Schema URL 404s; validated against schema text in docs. Plugin-relative MCP path. |
| 23 | Cline | `cline\spindoctor-qwerty\` | https://github.com/cline/cline/blob/main/docs/customization/plugins.mdx ; docs/sdk/plugins.mdx | stub setup(api) | 5/5 PASS | Cline SDK/CLI only. |
| 24 | Mistral Vibe | `mistral-vibe\spindoctor-qwerty\` | https://github.com/mistralai/mistral-vibe/blob/main/vibe/plugins/builtins/vibe/skills/vibe/SKILL.md | Agent Plugins schemas | 9/9 PASS | No agents (TOML schema undocumented). |
| 25 | goose | `goose\spindoctor-qwerty\` | https://goose-docs.ai/docs/guides/config-files/ | YAML parse; Windows MCP check | 3/3 PASS | Path pre-filled for Russell's PC. |
| 26 | Continue | `continue\spindoctor-qwerty\` | https://docs.continue.dev/reference | YAML parse | 4/4 PASS | Path pre-filled for Russell's PC. |
| 27 | Roo Code | `roo-code\spindoctor-qwerty\` | https://roocodeinc.github.io/Roo-Code/features/mcp/using-mcp-in-roo/ | JSON + SKILL frontmatter | 4/4 PASS | Relative script path assumes workspace-root cwd. |
| 28 | Zed | `zed\spindoctor-qwerty\` | https://zed.dev/docs/extensions/developing-extensions ; https://zed.dev/docs/extensions/mcp-extensions | compiled to wasm32-wasip2 on box (rustc 1.99.0, zed_extension_api 0.7.0) | 7/7 PASS | User must set settings.engine path (WASM sandbox). extension.wasm SHA256 9bad895421078d572ed201de861b47ce2612fdac5aa49a8ab071abc8a1b74340. repository URL in extension.toml is a placeholder (only matters for publishing). |
| 29 | Factory Droid | `factory-droid\spindoctor-qwerty\` | https://docs.factory.com/harness/plugins | manifest, hooks empty | 12/12 PASS | Needs local marketplace wrapper to install; ${DROID_PLUGIN_ROOT} documented for hooks, used in mcp.json. |
| 30 | Augment Auggie | `augment-auggie\spindoctor-qwerty\` | https://docs.augmentcode.com/cli/plugins | manifest, hooks empty | 12/12 PASS | - |
| 31 | Devin CLI | `devin-cli\spindoctor-qwerty\` | https://docs.devin.ai/cli/extensibility/plugins/overview | manifest, rules frontmatter, hooks empty | 11/11 PASS | Native-layout root variable not explicit; ${CLAUDE_PLUGIN_ROOT} used. |
| 32 | Kilo Code | `kilo-code\spindoctor-qwerty\` | https://github.com/kilo-org/kilocode/blob/main/packages/kilo-docs/pages/automate/extending/plugins.md | real @kilocode/plugin/tool helper, list_presets | 5/5 PASS | - |
| 33 | CodeBuddy / WorkBuddy | `codebuddy\spindoctor-qwerty\` | https://www.workbuddy.ai/docs/zh/cli/plugins-reference | both manifests, hooks empty | 15/15 PASS | .lsp.json omitted (no language server for q.*). |
| 34 | OpenHands | `openhands\spindoctor-qwerty\` | https://docs.openhands.dev/overview/plugins | manifest, hooks empty | 12/12 PASS | No documented root variable; ${CLAUDE_PLUGIN_ROOT} used; Python needed in sandbox. |
| 35 | QwenPaw | `qwenpaw\spindoctor-qwerty\` | https://github.com/agentscope-ai/QwenPaw/blob/main/website/public/docs/plugins.en.md | stub api.register_tool | 3/3 PASS | Tools disabled by default (QwenPaw default); enable per agent. |
| 36 | DeepSeek Harness | `deepseek-harness\spindoctor-qwerty\` | https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/develop/basic/publish.md ; .../basic/tool.md | stub ctx.tools.register | 7/7 PASS | Not published (private). |
| 37 | AnythingLLM | `anythingllm\spindoctor-qwerty\` | https://docs.anythingllm.com/agent/custom/developer-guide ; /plugin-json ; /handler-js | official imported-manifest JSON schema; handler run | 6/6 PASS | One entrypoint -> `action` param multiplexes 4 tools. |
| 38 | Open WebUI | `open-webui\spindoctor-qwerty\` | https://docs.openwebui.com/features/extensibility/plugin/tools/development/ | Tools class import + run with pydantic | 3/3 PASS | engine_dir valve must point to engine on the server; no Function shipped. |
| 39 | Dify | `dify\spindoctor_qwerty\ + spindoctor_qwerty.difypkg` | https://docs.dify.ai/en/develop-plugin/features-and-specs/plugin-types/plugin-info-by-manifest | packaged by official dify CLI v0.6.11; tools import with dify_plugin SDK | 15/15 PASS | .difypkg is unsigned (self-hosted needs signature verification off). SHA256 69531364a5b61664d7bb6ce01c6cec061bc3d250868c37bcb7ea52d0a3bf918a |
| 40 | Semantic Kernel (C#) | `semantic-kernel\SpinDoctorQwerty.SemanticKernel\` | https://learn.microsoft.com/en-us/semantic-kernel/concepts/plugins/ | compiled on box (.NET SDK 8.0.425, Microsoft.SemanticKernel 1.81.0, 0 warnings); sample ran OK | 2/2 PASS | Built/tested on Linux box only (no SDK on PC). |
| 41 | Flowise | `flowise\spindoctor-qwerty\` | https://docs.flowiseai.com/integrations/langchain/tools/custom-tool ; https://docs.flowiseai.com/contributing/building-node | custom-tool function run; INode compiled with tsc 7.0.2 against stubs and invoked | 6/6 PASS | Export JSON shape from Flowise's Load/Export, not shown on the doc page; INode needs a Flowise source build. |

## Binary hashes

- SpinDoctor.Qwerty.Companion.exe: `cf6d1cd9d6661226f6f51c36ed70cad6903cb3e953c1b7c25c0c1f4f1308e781`
- zed extension.wasm: `9bad895421078d572ed201de861b47ce2612fdac5aa49a8ab071abc8a1b74340`
- spindoctor_qwerty.difypkg: `69531364a5b61664d7bb6ce01c6cec061bc3d250868c37bcb7ea52d0a3bf918a`
- spindoctor-qwerty.plugin: `1ef3640b5702ed2a56dd14f65cb181e002a818e3e7843bbe48853d8075d0a6ae`
- spindoctor-qwerty.mcpb: `9fd5cf19b06c0380372c8105dac61bbe3406ebfdd735e85540cc98e3fbfba5df`

Full per-file list: SHA256SUMS.txt.
