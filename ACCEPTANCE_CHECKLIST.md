# ACCEPTANCE CHECKLIST (checked for every repo, before and after the push)

## Content
- [ ] Version 1.1.0 in every manifest, README, CHANGELOG and the bundled engine (`CARTRIDGE_VERSION`).
- [ ] The bundled engine is this kit's `engine/` (only SPDX headers added).
- [ ] The README covers: what it is, which host, install steps for that host (Windows/macOS/Linux where they differ),
      the function table, theory testing (file, text, chat with user confirmation), a testing section, honest limits
      (classical FP64 simulation, 298 logical / 59 per factor, basis z above 29, Python 3.8+), and the author.
- [ ] Every SKILL/agent/rules/instructions file tells the AI to show the function table verbatim when asked for help,
      and to confirm a chat-derived theory summary with the user before testing it.
- [ ] LICENSE is the full GPL-3.0 text, verbatim. NOTICE and COPYRIGHT say "Copyright (C) 2026 RUSSELL PHILIP SMITHSON".
- [ ] SPDX `GPL-3.0-or-later` headers in source files; license and author fields in every manifest.
- [ ] Hooks (if any) never run engine commands and never touch the network.
- [ ] No machine paths; placeholders or plugin-relative paths only. Root-path variables are the ones the host documents.
- [ ] Third-party code only where its license allows, credited in NOTICE.

## Gate
- [ ] Strict scan: no secrets, tokens, machine paths, user names, or emails other than the author's.
- [ ] Manifests validate against the documented schema (offline).
- [ ] Clean-room install from the README only, through the host's real entry point.
- [ ] Function table, one script per command family, a preset, `q.folder` on a mixed folder, theory from a file and
      from a chat summary/transcript, TXT+PDF reports valid, results match `reference/`.
- [ ] Real host app loads the plugin and lists its tools, or the result is marked `host-simulated` with the reason.
- [ ] `E2E_RESULTS.md` committed, including the SpinDoctor 3.1.2 18/18 (3 checks adapted to 298) note.

## After the push
- [ ] Public, on `main`, description set.
- [ ] The tree read back from GitHub matches the staged files.
- [ ] A fresh clone passes the quick E2E.
- [ ] `PUBLISH_LOG.csv` row written; the per-push report sent.
