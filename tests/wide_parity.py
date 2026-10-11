# SpinDoctor Qwerty 1.1.0 - upgrade handoff kit: wide_parity.py
# Copyright (C) 2026 RUSSELL PHILIP SMITHSON <russellsmithson77@outlook.com>
# SPDX-License-Identifier: GPL-3.0-or-later
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version. It is distributed WITHOUT ANY WARRANTY; see the LICENSE file for details.
"""Replay the C# 3.1.2-298 wide-register reference (wide_ref.json) and compare histograms/results/errors."""
import json, os, sys
sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
from spindoctor import Session
ref = json.load(open(sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reference", "wide_ref_3.1.2-298.json"), encoding="utf-8-sig"))
seed = [r for r in ref if r["command"] == "q.circuit export"][0]["result"]["measurementSeed"]
s = Session(None, write_reports=False); s.circuit.seed = seed  # C# export shows the derived circuit seed
fails = 0
for r in ref:
    p = s.run_command(r["command"]); ok = p["ok"]
    res = p["response"].get("result") if ok else p["response"].get("error")
    if ok != r["ok"]:
        fails += 1; print("OK-MISMATCH", r["command"], r.get("error"), "|", res); continue
    if not ok:
        if res != r["error"]: fails += 1; print("ERR-DIFF", r["command"], "\n  C#:", r["error"], "\n  py:", res)
        continue
    c = r["command"]
    if c == "q.circuit result":
        a = {h["bitstring"]: h["count"] for h in r["result"]["histogram"]}; b = {h["bitstring"]: h["count"] for h in res["histogram"]}
        same = a == b
        for k in ("samplingMode", "samplingFactorCount", "completedShots", "measuredQubits", "counterEnd"):
            if str(r["result"].get(k)) != str(res.get(k)): same = False; print("  field", k, r["result"].get(k), res.get(k))
        ck = {k: (r["result"]["counts"][k], res["counts"][k]) for k in r["result"]["counts"] if str(r["result"]["counts"][k]) != str(res["counts"].get(k))}
        print("RESULT", "match" if same else "DIFF", len(a), "outcomes; count diffs:", ck)
        if not same: fails += 1
    elif c.startswith("q.query") or c.startswith("q.circuit state") or c.startswith("q.circuit spin"):
        def norm(o):
            if isinstance(o, dict): return {k: norm(v) for k, v in o.items() if k not in ("elapsedMs", "capturedUtc")}
            if isinstance(o, list): return [norm(v) for v in o]
            if isinstance(o, (int, float)) and not isinstance(o, bool): return float(o) + 0.0  # -0.0 serialises as 0 in .NET JSON too
            return o
        ja = json.dumps(norm(r["result"]), sort_keys=True); jb = json.dumps(norm(res), sort_keys=True)
        print(c, "match" if ja == jb else "DIFF"); 
        if ja != jb:
            i = next(i for i in range(min(len(ja), len(jb))) if ja[i] != jb[i]); fails += 1; print("  C#:", ja[i-150:i+150], "\n  py:", jb[i-150:i+150])
print("FAILS", fails)
sys.exit(1 if fails else 0)
