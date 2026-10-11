# SpinDoctor Qwerty 1.1.0 - upgrade handoff kit: wide298_example_parity.py
# Copyright (C) 2026 RUSSELL PHILIP SMITHSON <russellsmithson77@outlook.com>
# SPDX-License-Identifier: GPL-3.0-or-later
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version. It is distributed WITHOUT ANY WARRANTY; see the LICENSE file for details.
"""Run the 11-file 298-qubit example folder through the cartridge with the C# circuit seed and compare the histogram."""
import json, os, sys, tempfile
A = sys.argv[1:] + [None] * 3; H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, A[0] or os.path.join(H, "..", "engine")); from spindoctor import Session
ref = json.load(open(A[1] or os.path.join(H, "..", "reference", "wide298_example_ref.json"), encoding="utf-8-sig"))
folder = os.path.abspath(A[2] or os.path.join(H, "..", "reference", "examples", "298-native-run"))
s = Session(tempfile.mkdtemp(), write_reports=False); s.circuit.seed = ref["seed"]
r = s.run_command('q.folder run path="%s" downloads=false verify=false' % folder)
res = s.run_command("q.circuit result")["response"]["result"]
a = {h["bitstring"]: str(h["count"]) for h in ref["histogram"]}; b = {h["bitstring"]: str(h["count"]) for h in res["histogram"]}
ok = a == b and res["samplingMode"] == ref["samplingMode"] and int(res["samplingFactorCount"]) == int(ref["samplingFactorCount"])
cd = {k: (ref["counts"][k], res["counts"][k]) for k in ref["counts"] if str(ref["counts"][k]) != str(res["counts"].get(k))}
print("phase", ref["phase"], "C# distinct", ref["distinct"], "py distinct", res["distinctOutcomes"], "histogram preview match", a == b, "counts diffs", cd)
print("PASS" if ok and not cd else "FAIL"); sys.exit(0 if ok and not cd else 1)
