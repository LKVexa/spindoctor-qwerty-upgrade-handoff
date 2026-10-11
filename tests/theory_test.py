# SpinDoctor Qwerty 1.1.0 - upgrade handoff kit: theory_test.py
# Copyright (C) 2026 RUSSELL PHILIP SMITHSON <russellsmithson77@outlook.com>
# SPDX-License-Identifier: GPL-3.0-or-later
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version. It is distributed WITHOUT ANY WARRANTY; see the LICENSE file for details.
"""v1.1.0 tests: spindoctor_test_theory for every attachment type, pasted text, chat summary + excerpts, chat transcripts
(.txt/.md/ChatGPT json/Claude json/html), verdict logic, TXT+JSON+PDF report integrity (incl. pypdf-free PDF extraction)."""
import json, os, sys, tempfile
ENGINE = next((a for a in sys.argv[1:] if not a.startswith("--")), os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine")); sys.path.insert(0, ENGINE); sys.dont_write_bytecode = True
if "--no-pypdf" in sys.argv: sys.modules["pypdf"] = None
from spindoctor import api, theory
from spindoctor.reports import check_pdf
EX = os.path.join(ENGINE, "examples", "theory"); WS = tempfile.mkdtemp(prefix="theory-"); R = []
def T(name, cond, detail=""):
    R.append((name, bool(cond), detail)); print(("PASS " if cond else "FAIL ") + name + ("  -- " + str(detail)[:160] if detail and not cond else ""))
def call(**a): a.setdefault("workspace", WS); return api.call("spindoctor_test_theory", a)
def report_ok(r, *needles):
    if not r.get("ok"): return False, r.get("error")
    rp = r["reports"]; txt = [x for x in rp if x.endswith(".txt")][0]; pdf = [x for x in rp if x.endswith(".pdf")][0]; js = [x for x in rp if x.endswith(".json")][0]; t = open(txt, encoding="utf-8").read(); ok, why = check_pdf(open(pdf, "rb").read())
    ptxt, _ = theory.pdf_text(open(pdf, "rb").read()); miss = [n for n in needles if n not in t]
    return ok and not miss and "VERDICT" in ptxt and json.load(open(js))["verdict"] == r["verdict"], (why, miss)
P1 = lambda out, exp, tol=0.05: {"kind": "probability", "outcome": out, "expected": exp, "tolerance": tol}
# ---- file types: extract then run
cases = [("hadamard_theory.txt", [P1("1", 0.5, 0.04)], "supported"), ("hadamard_theory.pdf", [P1("1", 0.5, 0.04)], "supported"),
         ("bell_theory.md", [P1("00", 0.5), P1("11", 0.5), P1("01", 0.0, 0.0), {"kind": "value", "command": 5, "path": "result.fidelity", "op": "approx", "value": 1, "tolerance": 1e-9}], "supported"),
         ("bell_theory.pdf", [P1("00", 0.5), P1("11", 0.5)], "supported"), ("ghz_theory.py", [P1("000", 0.5), P1("111", 0.5)], "supported"),
         ("rotation_theory.json", [P1("1", 0.25, 0.03)], "supported"), ("xbasis.q", [P1("0", 1.0, 0.0)], "supported")]
for f, checks, want in cases:
    p = os.path.join(EX, f); e = call(action="extract", source="file", path=p)
    T("extract %s" % f, e.get("ok") and e["extracted"]["qLines"], e.get("error") or e["extracted"].get("extractor"))
    r = call(source="file", path=p, hypothesis="From " + f, prediction="See checks", checks=checks)
    T("run %s -> %s" % (f, want), r.get("ok") and r["verdict"] == want, r.get("error") or r.get("checks"))
    ok, why = report_ok(r, "Source: attachment file", "Hypothesis", "Raw results", "Limits", "VERDICT: " + want.upper()); T("report %s (TXT+JSON+PDF)" % f, ok, why)
e = call(action="extract", source="file", path=os.path.join(EX, "angle_sweep.csv")); T("extract csv (rows)", e.get("ok") and e["extracted"]["csvRows"] == 3, e)
r = call(source="file", path=os.path.join(EX, "angle_sweep.csv"), hypothesis="RY(pi/2) gives P(1)=0.5 (row 2 of the sweep)", prediction="P(1)=0.5 +/- 0.05",
         script="q.circuit new sweep2 1\nq.circuit add ry 1.5707963267948966 0\nq.circuit run shots 2000 basis z", checks=[P1("1", 0.5)])
T("run csv sweep row -> supported", r.get("verdict") == "supported", r)
# ---- verdict logic
r = call(source="text", text="H on |0> always gives 1", hypothesis="H|0> always measures 1", prediction="P(1)=1",
         script="q.circuit new wrong 1\nq.circuit add h 0\nq.circuit run shots 1000 basis z", checks=[P1("1", 1.0, 0.01)])
T("pasted text, wrong prediction -> not supported", r.get("verdict") == "not supported", r); ok, why = report_ok(r, "Source: pasted text", "VERDICT: NOT SUPPORTED"); T("report pasted text", ok, why)
r = call(source="text", text="X flips", hypothesis="X flips |0>", prediction="always 1", script="q.circuit new nock 1\nq.circuit add x 0\nq.circuit run shots 10 basis z")
T("no checks -> inconclusive", r.get("verdict") == "inconclusive", r)
r = call(source="text", text="t", hypothesis="h", prediction="p", script="q.circuit new bad 299", checks=[{"kind": "value", "command": 1, "path": "result.qubits", "op": "eq", "value": 299}])
T("failed command (299 qubits > cap) -> inconclusive", r.get("verdict") == "inconclusive", r)
r = call(source="text", text="t", hypothesis="299 qubits are refused", prediction="command fails", script="q.circuit new bad2 299", checks=[{"kind": "ok", "command": 1, "expected": False}])
T("ok-check on refusal -> supported", r.get("verdict") == "supported", r)
r = call(source="text", text="t", hypothesis="h", prediction="p", script="q.circuit new tight 1\nq.circuit add h 0\nq.circuit run shots 100 basis z", checks=[P1("1", 0.5, 0.01)])
T("tolerance tighter than shot noise is flagged", "increase shots" in json.dumps(r.get("checks")), r.get("checks"))
# ---- chat history: summary + excerpts
summary = ("Theory (graph-to-Bell): H on both qubits, then CZ, then H on qubit 1 yields a Bell state. Assumptions: ideal gates, no noise. "
           "Variables: shots=4000. Measurable prediction: only 00 and 11 appear, each ~0.5 (+/-0.05); concurrence = 1.")
ex = ["User: if I put a Hadamard on both qubits and then a CZ, do I get an entangled state?",
      "Assistant: Yes. H on both gives |++>, and CZ turns it into a graph state.", "User: Then my theory is: measuring that circuit in Z gives only 00 and 11, about half each."]
script = "q.circuit new g2b 2\nq.circuit add h 0\nq.circuit add h 1\nq.circuit add cz 0 1\nq.circuit add h 1\nq.circuit run shots 4000 basis z\nq.query concurrence qubits=[0,1]"
chk = [P1("00", 0.5), P1("11", 0.5), {"kind": "value", "command": 7, "path": "result.concurrence", "op": "approx", "value": 1, "tolerance": 1e-9}]
r = call(source="chat", text=summary, excerpts=ex, hypothesis="H-H-CZ-H(1) prepares a Bell state", prediction="Only 00/11, ~0.5 each; concurrence 1",
         assumptions=["ideal gates", "no noise"], variables=["shots=4000"], script=script, checks=chk, title="graph-to-Bell (chat)")
T("chat summary + excerpts -> supported", r.get("verdict") == "supported" and r.get("excerptsRecorded") == 3, r.get("error") or r.get("checks"))
ok, why = report_ok(r, "Source: chat history", '[1] user: "if I put a Hadamard', '[2] assistant: "Yes. H on both', "Assumptions:", "Variables:", "cannot read chat history"); T("chat report quotes excerpts under 'Source: chat history'", ok, why)
# ---- exported transcripts
for f, n in [("chat_transcript.txt", 7), ("chat_transcript.md", 3), ("chatgpt_conversations.json", 5), ("claude_conversations.json", 4), ("chat_export.html", 4)]:
    e = call(action="extract", source="chat", path=os.path.join(EX, f)); x = e.get("extracted", {})
    roles = [t["role"] for t in x.get("transcript", [])]
    T("parse transcript %s (%d turns, roles user/assistant)" % (f, n), e.get("ok") and x.get("transcriptTurns") == n and roles[0] == "user" and "assistant" in roles, e.get("error") or (x.get("transcriptTurns"), roles))
r = call(source="chat", path=os.path.join(EX, "chatgpt_conversations.json"), text=summary, hypothesis="H-H-CZ-H(1) prepares a Bell state",
         prediction="Only 00/11", script=script.replace("g2b", "g2b2"), checks=chk[:2])
ok, why = report_ok(r, "Source: chat history", "Exported transcript:", "json chat export", '"If I put H on both qubits'); T("chat transcript file run + report", ok and r["verdict"] == "supported", why)
# ---- refusals
T("missing file refused", "not found" in call(source="file", path="/nonexistent/x.md", hypothesis="h", prediction="p").get("error", ""))
bad = os.path.join(WS, "theory.xyz"); open(bad, "w").write("q.help")
T("unsupported type refused", "Supported theory files" in call(source="file", path=bad, hypothesis="h", prediction="p").get("error", ""))
r1 = call(source="text", text="t", hypothesis="h", prediction="p", script="q.circuit new same 1\nq.circuit run shots 10 basis z", checks=[P1("0", 1.0, 0.0)])
r2 = call(source="text", text="t", hypothesis="h", prediction="p", script="q.circuit new same 1\nq.circuit run shots 10 basis z", checks=[P1("0", 1.0, 0.0)])
T("repeat runs isolated (no name collision)", r1.get("verdict") == r2.get("verdict") == "supported" and r1["runWorkspace"] != r2["runWorkspace"], (r1.get("error"), r2.get("error")))
T("run without hypothesis refused", "hypothesis" in call(source="text", text="x", script="q.help").get("error", ""))
T("chat without content refused", "needs" in call(source="chat", hypothesis="h", prediction="p").get("error", ""))
# ---- function table mentions chat option
md = api.call("spindoctor_functions", {})["markdown"]; T("function table lists theory tool incl. source=chat", "source=chat" in md and "spindoctor_test_theory" in md)
print("\n%d/%d passed" % (sum(x[1] for x in R), len(R))); json.dump(R, open(os.path.join(tempfile.gettempdir(), "theory_test_results%s.json" % ("_nopypdf" if "--no-pypdf" in sys.argv else "")), "w"), indent=1)
sys.exit(0 if all(x[1] for x in R) else 1)
