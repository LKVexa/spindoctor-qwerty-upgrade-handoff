# SpinDoctor Qwerty 1.1.0 - upgrade handoff kit: check_kit.py
# Copyright (C) 2026 RUSSELL PHILIP SMITHSON <russellsmithson77@outlook.com>
# SPDX-License-Identifier: GPL-3.0-or-later
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version. It is distributed WITHOUT ANY WARRANTY; see the LICENSE file for details.
"""Self-check for the upgrade handoff kit, run from a clean clone:
  python3 tools/check_kit.py            # everything (needs network only for the link check)
  python3 tools/check_kit.py --offline  # skip the link check
Steps: parse every JSON/YAML file, run every test script against the bundled engine, run the strict scan,
and check that every http(s) link in the Markdown files resolves. Exit code 0 only if all steps pass."""
import json, os, re, subprocess, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); PY = sys.executable
OFFLINE = "--offline" in sys.argv; R = []


def step(name, ok, detail=""):
    R.append((name, bool(ok), detail)); print(("PASS " if ok else "FAIL ") + name + ("  -- " + detail if detail else ""), flush=True)


def files(exts):
    for root, dirs, fs in os.walk(KIT):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__", "node_modules")]
        for f in fs:
            if f.lower().endswith(exts): yield os.path.join(root, f)


# 1. JSON / YAML parse
bad = []; nj = 0
for p in files((".json",)):
    nj += 1
    try: json.load(open(p, encoding="utf-8-sig"))
    except Exception as e: bad.append("%s: %s" % (os.path.relpath(p, KIT), e))
ys = list(files((".yaml", ".yml")))
if ys:
    try:
        import yaml
        for p in ys:
            try: yaml.safe_load(open(p, encoding="utf-8"))
            except Exception as e: bad.append("%s: %s" % (os.path.relpath(p, KIT), e))
    except ImportError: bad.append("PyYAML not installed but %d YAML files present" % len(ys))
step("JSON/YAML parse (%d JSON, %d YAML)" % (nj, len(ys)), not bad, "; ".join(bad[:5]))

# 2. scripts
T = os.path.join(KIT, "tests"); E = os.path.join(KIT, "engine")
RUNS = [("sample PDFs (make_sample_pdfs.py)", [PY, os.path.join(E, "examples", "theory", "make_sample_pdfs.py")]),
        ("function table examples (functions_test.py)", [PY, os.path.join(T, "functions_test.py")]),
        ("theory testing (theory_test.py)", [PY, os.path.join(T, "theory_test.py")]),
        ("theory testing without pypdf (theory_test.py --no-pypdf)", [PY, os.path.join(T, "theory_test.py"), "--no-pypdf"]),
        ("validation suite (validate.py)", [PY, os.path.join(T, "validate.py")]),
        ("298-qubit C# reference replay (wide_parity.py)", [PY, os.path.join(T, "wide_parity.py")]),
        ("298-qubit example folder parity (wide298_example_parity.py)", [PY, os.path.join(T, "wide298_example_parity.py")]),
        ("MCP end-to-end (e2e_mcp.py over stdio)", [PY, os.path.join(T, "e2e_mcp.py"), "--server", PY, os.path.join(E, "scripts", "spindoctor_mcp.py"),
                                                    "--examples", os.path.join(E, "examples", "theory"), "--out", os.path.join(__import__("tempfile").gettempdir(), "spindoctor_kit_e2e.json")]),
        ("strict pre-push scan (repokit.py scan)", [PY, os.path.join(KIT, "tools", "repokit.py"), "scan", KIT,
                                                    "--allow-binary", "engine/examples/theory/hadamard_theory.pdf", "engine/examples/theory/bell_theory.pdf"])]
env = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
for name, cmd in RUNS:
    t0 = time.time()
    try:
        p = subprocess.run(cmd, cwd=KIT, env=env, capture_output=True, text=True, timeout=1800)
        last = (p.stdout.strip().splitlines() or [""])[-1][:160]
        step(name, p.returncode == 0, "%.0fs, %s" % (time.time() - t0, last if p.returncode == 0 else (p.stdout + p.stderr)[-400:]))
    except subprocess.TimeoutExpired: step(name, False, "timeout")

# 3. links
if OFFLINE: print("SKIP link check (--offline)")
else:
    urls = set()
    for p in files((".md",)):
        for u in re.findall(r"https?://[^\s)\]>`'\"|]+", open(p, encoding="utf-8").read()):
            u = u.rstrip(".,;:*")
            if "<" in u or "example.com" in u or "localhost" in u: continue
            urls.add(u)

    def get(u):
        last = ""
        for method in ("HEAD", "GET"):
            try:
                rq = urllib.request.Request(u, method=method, headers={"User-Agent": "Mozilla/5.0 (spindoctor-kit link check)"})
                with urllib.request.urlopen(rq, timeout=25) as r: return u, r.status, ""
            except urllib.error.HTTPError as e: last = "HTTP %d" % e.code
            except Exception as e: last = type(e).__name__
        return u, 0, last
    with ThreadPoolExecutor(8) as ex: res = list(ex.map(get, sorted(urls)))
    dead = [(u, d) for u, s, d in res if not s]
    for u, d in dead: print("  DEAD", u, d)
    step("links resolve (%d unique URLs)" % len(urls), not dead, "%d dead" % len(dead) if dead else "")

print("\nKIT CHECK %d/%d passed" % (sum(r[1] for r in R), len(R)))
sys.exit(0 if all(r[1] for r in R) else 1)
