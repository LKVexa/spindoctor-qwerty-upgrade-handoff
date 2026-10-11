# SpinDoctor Qwerty 1.1.0 - upgrade handoff kit: functions_test.py
# Copyright (C) 2026 RUSSELL PHILIP SMITHSON <russellsmithson77@outlook.com>
# SPDX-License-Identifier: GPL-3.0-or-later
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version. It is distributed WITHOUT ANY WARRANTY; see the LICENSE file for details.
"""Every 'Command to type' in the v1.1.0 function table must run OK in the engine."""
import sys, tempfile, os
sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine")); sys.dont_write_bytecode = True
from spindoctor import functions
from spindoctor.terminal import Session
fails = []; n = 0
PRE = {"Queries": "q.circuit new bell 2\nq.circuit add h 0\nq.circuit add cx 0 1\nq.circuit run shots 1000 basis z"}
for fam, rows in functions.FAMILIES:
    s = Session(tempfile.mkdtemp(prefix="fn-"), write_reports=False)
    for k, v in PRE.items():
        if fam.startswith(k):
            for c in v.split("\n"): assert s.run_command(c)["ok"], c
    for a, _, cmd in rows:
        for c in cmd.split("\n"):
            r = s.run_command(c); n += 1
            if not r["ok"]: fails.append((fam[:20], c, r.get("response", {}).get("error")))
s = Session(tempfile.mkdtemp(prefix="fn-"), write_reports=False); s.run_command("q.circuit new g 3")
for g, c in functions.GATES:
    r = s.run_command(c); n += 1
    if not r["ok"]: fails.append(("gates", c, r.get("response", {}).get("error")))
md = functions.table("all")
assert md.count("q.preset run qc-") >= 241 and "source=chat" in md
print("examples run:", n, "failed:", len(fails)); [print(" ", f) for f in fails]
print("table chars: commands=%d presets=%d all=%d" % (len(functions.table()), len(functions.table("presets")), len(md)))
sys.exit(1 if fails else 0)
