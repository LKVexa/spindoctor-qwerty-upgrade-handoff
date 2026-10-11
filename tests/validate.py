# SpinDoctor Qwerty 1.1.0 - upgrade handoff kit: validate.py
# Copyright (C) 2026 RUSSELL PHILIP SMITHSON <russellsmithson77@outlook.com>
# SPDX-License-Identifier: GPL-3.0-or-later
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version. It is distributed WITHOUT ANY WARRANTY; see the LICENSE file for details.
"""SpinDoctor Qwerty cartridge validation suite (stdlib + optional numpy).
Usage: python validate.py <cartridge_root> <out.json>
Runs: statistical histogram checks vs an independent statevector, backend/seed determinism,
dense-cap guardrail, workspace persistence, report (TXT/JSON/PDF) integrity, small scaling benchmark."""
import json, math, os, random, subprocess, sys, tempfile, time, cmath
from shutil import which as shutil_which

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine")); OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(tempfile.gettempdir(), "spindoctor_validate.json")
sys.path.insert(0, ROOT)
results = {"checks": [], "benchmarks": []}

def check(name, ok, detail=""):
    results["checks"].append({"name": name, "ok": bool(ok), "detail": detail})
    print(("PASS " if ok else "FAIL ") + name + ("  -- " + detail if detail else ""), flush=True)

# ---------- independent reference statevector (pure python, little-endian: qubit 0 = rightmost bit) ----------
def ref_probs(n, gates):
    st = [0j] * (1 << n); st[0] = 1
    s2 = 1 / math.sqrt(2)
    def one(q, m):
        b = 1 << q
        for i in range(1 << n):
            if not i & b:
                a, c = st[i], st[i | b]
                st[i] = m[0][0] * a + m[0][1] * c; st[i | b] = m[1][0] * a + m[1][1] * c
    for g in gates:
        k = g[0]
        if k == "h": one(g[1], [[s2, s2], [s2, -s2]])
        elif k == "x": one(g[1], [[0, 1], [1, 0]])
        elif k == "t": one(g[1], [[1, 0], [0, cmath.exp(1j * math.pi / 4)]])
        elif k == "s": one(g[1], [[1, 0], [0, 1j]])
        elif k == "ry":
            th = g[2]; one(g[1], [[math.cos(th / 2), -math.sin(th / 2)], [math.sin(th / 2), math.cos(th / 2)]])
        elif k == "rz":
            th = g[2]; one(g[1], [[cmath.exp(-0.5j * th), 0], [0, cmath.exp(0.5j * th)]])
        elif k == "cx":
            c, t = 1 << g[1], 1 << g[2]
            for i in range(1 << n):
                if i & c and not i & t: st[i], st[i | t] = st[i | t], st[i]
        elif k == "cz":
            c, t = 1 << g[1], 1 << g[2]
            for i in range(1 << n):
                if i & c and i & t: st[i] = -st[i]
    return [abs(a) ** 2 for a in st]

def to_cmd(g):
    if g[0] in ("ry", "rz"): return "q.circuit add %s %r %d" % (g[0], g[2], g[1])
    return "q.circuit add " + g[0] + " " + " ".join(str(x) for x in g[1:])

def rand_circuit(n, depth, seed):
    r = random.Random(seed); gates = []
    for _ in range(depth):
        for q in range(n):
            k = r.choice(["h", "t", "s", "ry", "rz", "x"])
            gates.append((k, q, round(r.uniform(-3, 3), 6)) if k in ("ry", "rz") else (k, q))
        for q in range(n - 1):
            if r.random() < 0.6: gates.append((r.choice(["cx", "cz"]), q, q + 1) if r.random() < .5 else (r.choice(["cx", "cz"]), q + 1, q))
    return gates

def gammaincc(a, x):  # regularized upper incomplete gamma Q(a,x)
    if x <= 0: return 1.0
    if x < a + 1:
        s = t = 1.0 / a; ap = a
        for _ in range(10000):
            ap += 1; t *= x / ap; s += t
            if abs(t) < abs(s) * 1e-15: break
        return max(0.0, 1 - s * math.exp(-x + a * math.log(x) - math.lgamma(a)))
    b = x + 1 - a; c = 1e300; d = 1 / b; h = d
    for i in range(1, 10000):
        an = -i * (i - a); b += 2; d = an * d + b; d = 1e-300 if abs(d) < 1e-300 else d
        c = b + an / c; c = 1e-300 if abs(c) < 1e-300 else c; d = 1 / d; de = d * c; h *= de
        if abs(de - 1) < 1e-15: break
    return math.exp(-x + a * math.log(x) - math.lgamma(a)) * h

def chi2(hist, probs, n, shots):
    bins = []; exp_other = 0; obs_other = 0
    for i, p in enumerate(probs):
        key = format(i, "0%db" % n); e = p * shots; o = hist.get(key, 0)
        if e >= 5: bins.append((o, e))
        else: exp_other += e; obs_other += o
    if exp_other > 0: bins.append((obs_other, exp_other))
    stat = sum((o - e) ** 2 / e for o, e in bins); dof = max(1, len(bins) - 1)
    return stat, dof, gammaincc(dof / 2, stat / 2)

CHILD = r'''
import json, sys
sys.path.insert(0, sys.argv[1])
from spindoctor import Session, backend
spec = json.loads(sys.argv[2])
s = Session(None, measurement_seed=spec["seed"], write_reports=False)
for c in spec["cmds"]: s.native(c)
j = s.circuit.job
print(json.dumps({"backend": backend.NAME if hasattr(backend, "NAME") else str(backend.np is not None), "phase": j.phase, "error": j.error, "hist": dict(j.histogram)}))
'''

def run_child(cmds, seed, stdlib):
    env = dict(os.environ)
    if stdlib: env["SPINDOCTOR_NO_NUMPY"] = "1"
    else: env.pop("SPINDOCTOR_NO_NUMPY", None)
    p = subprocess.run([sys.executable, "-c", CHILD, ROOT, json.dumps({"cmds": cmds, "seed": seed})], capture_output=True, text=True, env=env, timeout=3000)
    if p.returncode: raise RuntimeError(p.stderr[-2000:])
    return json.loads(p.stdout.strip().splitlines()[-1])

try:
    import numpy  # noqa: F401
    HAVE_NP = True
except ImportError:
    HAVE_NP = False

# ---------- 1. statistical checks ----------
pvals = []
for idx, (n, depth, shots) in enumerate([(3, 4, 20000), (5, 5, 20000), (8, 6, 20000), (10, 6, 20000), (12, 5, 30000)]):
    gates = rand_circuit(n, depth, 1000 + idx)
    probs = ref_probs(n, gates)
    cmds = ["q.circuit new st%d %d" % (idx, n)] + [to_cmd(g) for g in gates] + ["q.circuit run shots %d basis z" % shots]
    seed = format(idx + 7, "x") * 64
    seed = seed[:64]
    outs = {}
    for stdlib in ([False, True] if HAVE_NP else [True]):
        o = run_child(cmds, seed, stdlib); outs[stdlib] = o
        if o["phase"] != "completed":
            check("stats n=%d %s" % (n, "stdlib" if stdlib else "numpy"), False, o["error"]); continue
        stat, dof, p = chi2(o["hist"], probs, n, shots); pvals.append(p)
        tvd = 0.5 * sum(abs(o["hist"].get(format(i, "0%db" % n), 0) / shots - probs[i]) for i in range(1 << n))
        check("chi-square n=%d gates=%d shots=%d backend=%s" % (n, len(gates), shots, "stdlib" if stdlib else "numpy"), p > 0.001,
              "chi2=%.1f dof=%d p=%.4f TVD=%.4f" % (stat, dof, p, tvd))
    if len(outs) == 2:
        check("numpy/stdlib identical histogram n=%d (same seed)" % n, outs[False]["hist"] == outs[True]["hist"])
# Fisher combination of p-values (should look uniform)
if pvals:
    X = -2 * sum(math.log(max(p, 1e-300)) for p in pvals); pc = gammaincc(len(pvals), X / 2)
    check("Fisher combined p-value over %d chi-square tests" % len(pvals), pc > 0.001, "p=%.4f" % pc)

# ---------- 2. determinism / seed sensitivity ----------
cmds = ["q.circuit new dz 6", "q.circuit add h all", "q.circuit add cx 0 1", "q.circuit add ry 0.4 3", "q.circuit run shots 4000 basis z"]
a = run_child(cmds, "a" * 64, not HAVE_NP); b = run_child(cmds, "a" * 64, not HAVE_NP); c = run_child(cmds, "b" * 64, not HAVE_NP)
check("same seed -> byte-identical histogram", a["hist"] == b["hist"])
check("different seed -> different sample", a["hist"] != c["hist"])

# ---------- 3. guardrails ----------
from spindoctor import Session
s = Session(None, measurement_seed="c" * 64, write_reports=False)
r = s.native("q.circuit new big 299"); check("299-qubit circuit refused (1..298 range)", not r["ok"], (r.get("error") or "")[:120])
r = s.native("q.circuit new wide 298"); check("298-qubit circuit accepted (3.1.2-298)", r["ok"], (r.get("error") or "")[:120])
r = s.native("q.circuit run shots 4 basis x"); check("wide circuit refuses basis x", (not r["ok"]) and "basis z" in (r.get("error") or ""), (r.get("error") or "")[:120])
s.native("q.circuit new f61 61")
for q in range(1, 61): s.native("q.circuit add cx 0 %d" % q)
s.native("q.circuit run shots 2 basis z"); j = s.native("q.circuit status")["result"]["job"]
check("merge beyond the 59-qubit joint factor fails the run", j["phase"] == "failed" and "59-qubit" in j["error"], j["error"][:120])
for cmd in ["q.circuit new ghz29 29", "q.circuit add h 0"] + ["q.circuit add cx %d %d" % (i, i + 1) for i in range(28)] + ["q.circuit run shots 200 basis z"]:
    s.native(cmd)
j = s.circuit.job; check("GHZ-29 (sparse) runs within budget", j.phase == "completed" and set(j.histogram) <= {"0" * 29, "1" * 29}, "hist=%s" % dict(j.histogram))
s2 = Session(None, measurement_seed="c" * 64, write_reports=False)
for cmd in ["q.circuit new dense28 28", "q.circuit add h all"] + ["q.circuit add cx %d %d" % (i, i + 1) for i in range(27)] + ["q.circuit add ry 0.3 all", "q.circuit run shots 10 basis z"]:
    s2.native(cmd)
j = s2.circuit.job
check("dense 28-qubit factor refused with a clear memory-cap message (no crash)", j.phase == "failed" and ("cap" in (j.error or "").lower() or "budget" in (j.error or "").lower()), (j.error or "")[:160])
r = s.native("q.compile synthesize u3 0.1 0.2 0.3 tol 1e-3"); check("q.compile synthesize returns the documented not-implemented error", not r["ok"], (r.get("error") or "")[:100])

# ---------- 4. persistence + reports ----------
ws = tempfile.mkdtemp(prefix="sd_val_")
s = Session(ws)
rr = s.run_command("q.circuit new keep 2"); s.run_command("q.circuit add h 0"); s.run_command("q.circuit add cx 0 1")
rr = s.run_command("q.circuit run shots 500 basis z")
s.save(); s3 = Session(ws)
check("workspace persistence: circuit survives a new session", "keep" in s3.circuit.programs, str(list(s3.circuit.programs.keys())))
reps = rr.get("reports", [])
txt = [p for p in reps if p.endswith(".txt")]; pdf = [p for p in reps if p.endswith(".pdf")]; js = [p for p in reps if p.endswith(".json")]
check("TXT+JSON+PDF report triple written", bool(txt and pdf and js), ", ".join(os.path.basename(p) for p in reps))
if txt:
    t = open(txt[0], encoding="utf-8").read(); check("TXT report carries guardrail text", "Not a quantum computer" in t)
if js:
    json.load(open(js[0], encoding="utf-8")); check("JSON report parses", True)
if pdf:
    b = open(pdf[0], "rb").read()
    ok = b.startswith(b"%PDF-1.") and b.rstrip().endswith(b"%%EOF")
    sx = int(b[b.rindex(b"startxref") + 9:].split()[0]); ok = ok and b[sx:sx + 4] == b"xref"
    info = subprocess.run(["pdfinfo", pdf[0]], capture_output=True, text=True) if shutil_which("pdfinfo") else None
    text = subprocess.run(["pdftotext", pdf[0], "-"], capture_output=True, text=True).stdout if shutil_which("pdftotext") else ""
    check("PDF structure (header, startxref->xref, EOF)", ok)
    if info is not None:
        check("pdfinfo parses PDF", info.returncode == 0 and "Pages:" in info.stdout, " ".join(l for l in info.stdout.splitlines() if l.startswith(("Pages", "PDF version"))))
        check("pdftotext extracts command text", "q.circuit run shots 500" in text)

# ---------- 5. small scaling benchmark (dense random entangling circuit, 1000 shots) ----------
for n in [int(x) for x in os.environ.get("SD_BENCH", "10,14,18").split(",") if x]:
    cmds = ["q.circuit new b%d %d" % (n, n), "q.circuit add h all"]
    for k in range(3):
        cmds += ["q.circuit add cx %d %d" % (q, q + 1) for q in range(n - 1)] + ["q.circuit add rz 0.37 all", "q.circuit add ry 0.21 all"]
    cmds.append("q.circuit run shots 1000 basis z")
    for stdlib in ([False, True] if HAVE_NP else [True]):
        t0 = time.time(); o = run_child(cmds, "d" * 64, stdlib); dt = time.time() - t0
        results["benchmarks"].append({"qubits": n, "backend": "stdlib" if stdlib else "numpy", "gates": len(cmds) - 2, "shots": 1000, "phase": o["phase"], "seconds": round(dt, 2)})
        print("BENCH n=%d %s %s %.2fs" % (n, "stdlib" if stdlib else "numpy", o["phase"], dt), flush=True)

results["summary"] = {"passed": sum(c["ok"] for c in results["checks"]), "total": len(results["checks"]), "numpy": HAVE_NP, "python": sys.version.split()[0]}
json.dump(results, open(OUT, "w"), indent=1)
print("SUMMARY", results["summary"])
sys.exit(0 if results["summary"]["passed"] == results["summary"]["total"] else 1)
