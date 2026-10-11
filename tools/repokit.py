# SpinDoctor Qwerty 1.1.0 - upgrade handoff kit: repokit.py
# Copyright (C) 2026 RUSSELL PHILIP SMITHSON <russellsmithson77@outlook.com>
# SPDX-License-Identifier: GPL-3.0-or-later
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version. It is distributed WITHOUT ANY WARRANTY; see the LICENSE file for details.
"""Helpers for the spindoctor-qwerty-* repos: bundle the engine, write license files, add SPDX headers,
and run the strict pre-push scan (secrets, tokens, machine paths, emails).

Usage (from the kit root):
  python3 tools/repokit.py scan <repo> [--allow-binary REL ...] [--deny PATTERNS.txt]
  python3 tools/repokit.py bundle <dst-engine-dir> [--engine DIR]
  python3 tools/repokit.py license <repo> "<title>"
  python3 tools/repokit.py header <file> "<component>"

--deny takes a text file with one extra regular expression per line (for example your own user name or
private folder names). Keep that file OUTSIDE the repo you scan, so the patterns are never published.
"""
import os, re, shutil, sys

AUTHOR = "RUSSELL PHILIP SMITHSON"; EMAIL = "russellsmithson77@outlook.com"
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(KIT, "engine")

HDR = ["SpinDoctor Qwerty %s - %s", "Copyright (C) 2026 " + AUTHOR + " <" + EMAIL + ">", "SPDX-License-Identifier: GPL-3.0-or-later",
       "This program is free software: you can redistribute it and/or modify it under the terms of the GNU General",
       "Public License as published by the Free Software Foundation, either version 3 of the License, or (at your",
       "option) any later version. It is distributed WITHOUT ANY WARRANTY; see the LICENSE file for details."]
PREFIX = {".py": "#", ".sh": "#", ".ps1": "#", ".toml": "#", ".rs": "//", ".js": "//", ".mjs": "//", ".ts": "//", ".cs": "//", ".yaml": "#", ".yml": "#"}


def header(prefix, component, version="1.1.0"):
    lines = list(HDR); lines[0] = lines[0] % (version, component)
    return "\n".join((prefix + " " + l) for l in lines) + "\n"


def add_header(path, component):
    pre = PREFIX.get(os.path.splitext(path)[1].lower())
    if not pre: return False
    s = open(path, encoding="utf-8").read()
    if "SPDX-License-Identifier" in s[:2000]: return False
    lines = s.split("\n"); keep = []
    while lines and (lines[0].startswith("#!") or re.match(r"#.*coding[:=]", lines[0])): keep.append(lines.pop(0))
    if path.endswith(".rs"):
        while lines and lines[0].startswith("//!"): keep.append(lines.pop(0))
    open(path, "w", encoding="utf-8", newline="\n").write("\n".join(keep + [header(pre, component).rstrip("\n")] + lines)); return True


def bundle_engine(dst, engine=ENGINE):
    if os.path.abspath(dst) == os.path.abspath(engine): raise SystemExit("refusing to bundle the engine onto itself")
    if os.path.exists(dst): shutil.rmtree(dst)
    shutil.copytree(engine, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"))
    n = 0
    for root, _, files in os.walk(dst):
        for f in files:
            if f.endswith(".py") and add_header(os.path.join(root, f), "engine (SpinDoctor 3.1.2 parity)"): n += 1
    return n


def license_files(repo, title):
    shutil.copy(os.path.join(KIT, "LICENSE"), os.path.join(repo, "LICENSE"))
    open(os.path.join(repo, "COPYRIGHT"), "w", newline="\n").write(
        "%s\nCopyright (C) 2026 %s <%s>\n\nThis program is free software: you can redistribute it and/or modify it under the terms of\n"
        "the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or\n"
        "(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;\n"
        "without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public\n"
        "License for more details. You should have received a copy of the GNU General Public License along with this program\n"
        "(see LICENSE). If not, see <https://www.gnu.org/licenses/>.\n\nSPDX-License-Identifier: GPL-3.0-or-later\n" % (title, AUTHOR, EMAIL))
    open(os.path.join(repo, "NOTICE"), "w", newline="\n").write(
        "%s\nCopyright (C) 2026 %s <%s>\nLicensed under the GNU General Public License v3.0 or later (GPL-3.0-or-later); see LICENSE.\n\n"
        "Author: %s <%s>\n\nThis product bundles the SpinDoctor Qwerty engine 1.1.0, a pure-Python (standard library only) port of the\n"
        "SpinDoctor 3.1.2 quantum-circuit simulator semantics (update 3.1.2-298-20261010), by the same author.\n\n"
        "SpinDoctor is a CLASSICAL simulator: it runs FP64 arithmetic on an ordinary computer. It is not a quantum computer,\n"
        "does not connect to quantum hardware, and claims no quantum speed-up or quantum advantage.\n\n"
        "Third-party names (host applications, file formats, protocols) are trademarks of their respective owners and are used\n"
        "only to describe compatibility. No third-party code is vendored in this repository except where stated in README.md.\n"
        % (title, AUTHOR, EMAIL, AUTHOR, EMAIL))


TEXT_EXT = {".py", ".rs", ".toml", ".json", ".jsonc", ".md", ".txt", ".csv", ".q", ".qs", ".html", ".sh", ".ps1", ".lock", ".yaml", ".yml",
            ".js", ".ts", ".mjs", ".cs", ".csproj", ".gitignore", ".svg", ".diff", ""}
SECRETS = [r"ghp_[A-Za-z0-9]{20,}", r"github_pat_[A-Za-z0-9_]{20,}", r"gh[ousr]_[A-Za-z0-9]{20,}", r"\bsk-[A-Za-z0-9_-]{20,}", r"\bxox[abpors]-[A-Za-z0-9-]{10,}",
           r"AKIA[0-9A-Z]{16}", r"AIza[0-9A-Za-z_-]{35}", r"-----BEGIN [A-Z ]*PRIVATE KEY-----", r"(?i)(api[_-]?key|secret|password|passwd|token)\s*[:=]\s*['\"][^'\"\s]{8,}['\"]",
           r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}", r"(?i)bearer\s+[A-Za-z0-9._-]{20,}"]
# Generic machine-path patterns: Windows user folders, absolute drive paths, Unix home/box folders.
PATHS = [r"(?i)\b[A-Z]:[\\/]+Users[\\/]+[^\\/\s\"'<>]+", r"(?i)(?<![A-Za-z0-9])[A-Z]:\\[A-Za-z0-9_]", r"/(?:workspace)\b", r"/home/[a-z_][a-z0-9_-]*",
         r"/Users/[A-Za-z][A-Za-z0-9._-]*", r"(?i)OneDrive[\\/]", r"/tmp/[A-Za-z0-9_.-]+", r"(?i)AppData[\\/]"]
EMAIL_RE = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
ALLOWED_EMAILS = {EMAIL, "you@example.com", "user@example.com"}


def scan(repo, allow_binary=(), extra=()):
    findings = []; pats = PATHS + list(extra)
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in (".git", "target", "node_modules", "__pycache__")]
        for f in files:
            p = os.path.join(root, f); rel = os.path.relpath(p, repo).replace("\\", "/")
            ext = os.path.splitext(f)[1].lower(); data = open(p, "rb").read()
            if rel in allow_binary: continue
            if ext not in TEXT_EXT: findings.append((rel, "binary/unknown file type", ext)); continue
            if b"\x00" in data: findings.append((rel, "binary content", "")); continue
            t = data.decode("utf-8", "replace")
            for rx in SECRETS:
                for m in re.finditer(rx, t): findings.append((rel, "secret?", m.group(0)[:40]))
            for rx in pats:
                for m in re.finditer(rx, t): findings.append((rel, "path", t[max(0, m.start() - 30):m.end() + 30].replace("\n", " ")))
            for m in re.finditer(EMAIL_RE, t):
                if m.group(0) not in ALLOWED_EMAILS and not m.group(0).endswith((".png", ".pdf")): findings.append((rel, "email", m.group(0)))
    return findings


def _opt(args, name):
    vals = []
    while name in args:
        i = args.index(name); args.pop(i)
        while i < len(args) and not args[i].startswith("--"): vals.append(args.pop(i))
    return vals


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] not in ("scan", "bundle", "license", "header"): print(__doc__); sys.exit(2)
    cmd = a.pop(0)
    if cmd == "scan":
        allow = tuple(_opt(a, "--allow-binary")); extra = []
        for d in _opt(a, "--deny"): extra += [l.strip() for l in open(d, encoding="utf-8") if l.strip() and not l.startswith("#")]
        f = scan(a[0], allow, extra)
        for x in f: print("FINDING", *x)
        print("SCAN", "CLEAN" if not f else "%d findings" % len(f)); sys.exit(1 if f else 0)
    if cmd == "bundle":
        eng = (_opt(a, "--engine") or [ENGINE])[0]; print("headers added:", bundle_engine(a[0], eng))
    elif cmd == "license": license_files(a[0], a[1]); print("wrote LICENSE, COPYRIGHT, NOTICE")
    elif cmd == "header": print("added" if add_header(a[0], a[1]) else "unchanged")
