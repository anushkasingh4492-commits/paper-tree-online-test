#!/usr/bin/env python3
"""Reproduce the structural release checks (standard library only). Run from the extracted folder."""
import glob, hashlib, json, os, re, sys
from collections import Counter

os.chdir(os.path.dirname(os.path.abspath(__file__)))
fails = []
bank_path = glob.glob("jee_main_maths_v*.json")[0]
recs = json.load(open(bank_path, encoding="utf-8"))
ids = [r["id"] for r in recs]
if len(set(ids)) != len(ids):
    fails.append("duplicate ids")
for r in recs:
    if r["correct_answer"] != r["options"][r["correct_option"]]:
        fails.append(f"{r['id']} key text mismatch")
    if len(set(r["options"].values())) != 4:
        fails.append(f"{r['id']} options not distinct")
    for f in ("question", "explanation", "correct_answer", "common_misconception", "difficulty_reason") + tuple("ABCD"):
        t = r["options"][f] if f in "ABCD" else r[f]
        if re.search("[\u2013\u2014]", t):
            fails.append(f"{r['id']} dash in {f}")
        if t.count("$") % 2:
            fails.append(f"{r['id']} unbalanced $ in {f}")
    if re.search(r"option\s*\(?[ABCD]\)?\b|\([ABCD]\)", r["explanation"]):
        fails.append(f"{r['id']} explanation names a letter")
    nv = r["numerical_variant"]
    if nv and (not isinstance(nv["answer_integer"], int) or nv["parent_id"] != r["id"]):
        fails.append(f"{r['id']} numerical variant malformed")
stems = Counter(re.sub(r"\s+", " ", r["question"].lower()) for r in recs)
fails += [f"duplicate stem: {s[:50]}" for s, c in stems.items() if c > 1]
for u in sorted({r["unit_number"] for r in recs}):
    ur = [r for r in recs if r["unit_number"] == u]
    k = Counter(r["correct_option"] for r in ur)
    if max(k.values()) - min(k.values()) > 1:
        fails.append(f"unit {u} key imbalance {dict(k)}")
    seq = "".join(r["correct_option"] for r in ur)
    if re.search(r"(.)\1\1\1", seq):
        fails.append(f"unit {u} key run > 3")
# family rule on sample paper
sp = json.load(open("sample_paper.json"))
byid = {r["id"]: r for r in recs}
deps = [d for i in sp["section_a"] + sp["section_b"] for d in byid[i]["family_dependencies"]]
if len(deps) != len(set(deps)):
    fails.append("sample paper repeats a family dependency")
if Counter(byid[i]["correct_option"] for i in sp["section_a"]) != Counter({L: 5 for L in "ABCD"}):
    fails.append("sample section A keys not 5 each")
if Counter(byid[i]["difficulty"] for i in sp["section_a"] + sp["section_b"]) != Counter({"Easy": 8, "Medium": 11, "Difficult": 6}):
    fails.append("sample difficulty blueprint")
# checksums
for line in open("checksums.sha256"):
    h, p = line.strip().split("  ", 1)
    if p in ("verify_release.py",):
        pass
    if not os.path.exists(p) or hashlib.sha256(open(p, "rb").read()).hexdigest() != h:
        fails.append(f"checksum mismatch {p}")
print(f"records={len(recs)} difficulty={dict(Counter(r['difficulty'] for r in recs))} keys={dict(Counter(r['correct_option'] for r in recs))} "
      f"numerical={sum(1 for r in recs if r['numerical_variant'])} machine_match={sum(1 for r in recs if r['machine_check']['status']=='match')}")
print("FAILURES:", len(fails))
for f in fails:
    print("  ", f)
sys.exit(1 if fails else 0)
