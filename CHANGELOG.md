# Changelog

## 1.1.0 (2026-10-10)
- Rebased the kit on the **updated SpinDoctor 3.1.2** (`3.1.2-298-20261010`) and the finished **engine 1.1.0**.
- The 1.1.0 work (function table, theory testing from files, text and chat history) is marked DONE; the kit now
  tracks publishing of the per-host repos (5 published so far) and the queue.
- New: bundled `engine/`, runnable `tests/` with portable defaults and exit codes, `reference/` outputs from the
  updated 3.1.2, `tools/check_kit.py` (parse, tests, scan, links), a portable `tools/repokit.py` (no machine paths;
  private deny patterns come from a file outside the repo), `results_3.1.2/`, `DOCS_LINKS.md`.
- Schemas refreshed from upstream at pinned commits: Agent Plugins 1.0.0 and **1.1.0**, MCPB v0.3, **v0.4** and
  latest, AnythingLLM. Licenses added under `schemas/LICENSES/` and credited in NOTICE.
- Removed: third-party host documentation snapshots (replaced by links), the v1.0.0 41-format build scripts and
  format tests, the JS test harness, the Zed and companion sources (each published repo carries its own), raw
  3.0.3 to 3.0.4 C# diffs, and every machine path.
- Moved the 3.0.3 parity audit, the partial 3.0.3 to 3.0.4 diff, the 1.1.0 work-in-progress results and the v1.0.0
  validation snapshot to `history/`.
- Licensed GPL-3.0-or-later. Author: RUSSELL PHILIP SMITHSON <russellsmithson77@outlook.com>.

## 1.0.0 (2026-10-10)
- First handoff kit (local only): 3.0.4 rebase plan and the 1.1.0 spec for ChatGPT/Codex.
