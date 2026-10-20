# -*- coding: utf-8 -*-
"""Collect the v1.0.1 errata round into evidence files, a closure register (CSV) and summary numbers.

Writes errata/out/*.json, errata/out/Errata_Closure_Register.csv and errata/out/errata_summary.json.
"""
import csv, glob, json, os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = "/tmp/claude-0/-home-claude/6e18757b-ac0a-52e3-bf2e-85587c7b2e26/scratchpad"
OUT = os.path.join(HERE, "errata", "out")
os.makedirs(OUT, exist_ok=True)
j = lambda p: json.load(open(os.path.join(HERE, p)))

old = {r["id"]: r for u in range(1, 15) for r in json.load(open(f"{SCRATCH}/build_v100/U{u:02d}/records.json"))}
new = {r["id"]: r for u in range(1, 15) for r in j(f"build/U{u:02d}/records.json")}
loc2id = {r["provenance"]["local_id"]: i for i, r in new.items()}

# ---------- 1. independent recomputation of all 2,700 v1.0.0 items
rc_rows = []
for f in sorted(glob.glob(os.path.join(HERE, "errata", "recompute", "U*.json"))):
    if f.endswith("_raw.json"):
        continue
    for x in json.load(open(f)):
        o = old[x["id"]]
        nv = o["numerical_variant"]
        rc_rows.append(dict(id=x["id"], local_id=o["provenance"]["local_id"], key_v100=o["correct_option"], verifier_choice=x["choice"],
                            matching_options=x["matching_options"], agree=x["choice"] == o["correct_option"] and x["matching_options"] == [o["correct_option"]],
                            numerical_answer_v100=nv["answer_integer"] if nv else None, verifier_numerical=x.get("numerical_answer"),
                            numerical_agree=(nv is None) or x.get("numerical_answer") == nv["answer_integer"],
                            method=x.get("method"), computed=x.get("computed"), issue=x.get("issue", "")))
assert len(rc_rows) == 2700 and len({r["id"] for r in rc_rows}) == 2700
RC_ADJ = {
    "JEE-MATH-U10-140": "Verifier error. Key confirmed by the editor with sympy: c in (-25,-15) U (15,25).",
    "JEE-MATH-U03-201": "Issue noted (transpose shortcut makes the item quicker than intended). Deliberate design; retained.",
}
rc_dis = [r for r in rc_rows if not r["agree"] or not r["numerical_agree"] or r["issue"]]
for r in rc_dis:
    r["adjudication"] = RC_ADJ.get(r["id"], "see audit findings")
json.dump(dict(method="Fresh verifier agents saw only the stem and options of each released v1.0.0 item (no keys, drafts or checks) and wrote and ran their own sympy/brute-force code per item.",
               items=len(rc_rows), by_code=sum(r["method"] == "code" for r in rc_rows),
               key_agree=sum(r["agree"] for r in rc_rows),
               numerical_items=sum(r["numerical_answer_v100"] is not None for r in rc_rows),
               numerical_agree=sum(r["numerical_answer_v100"] is not None and r["numerical_agree"] for r in rc_rows),
               disagreements_or_issues=rc_dis, results=rc_rows),
          open(os.path.join(OUT, "recompute_v100_all_items.json"), "w"), indent=1, ensure_ascii=False)

# ---------- 2. audit findings + closures -> register
findings = j("errata/all_audit_findings.json")
UPGRADED = {("JEE-MATH-U03-154", "E2"): "critical", ("JEE-MATH-U05-077", "E2"): "critical"}
closure_for = {}
for pf in sorted(glob.glob(os.path.join(HERE, "errata", "fix", "*.json"))):
    if pf.endswith("_closure.json"):
        continue
    batch = os.path.basename(pf)[:-5]
    P = json.load(open(pf))
    C = json.load(open(pf.replace(".json", "_closure.json")))
    pool = list(C["closures"])
    ch = set(C.get("changed_stem_or_options", []))
    covered = set()
    pairs = []
    for x in P:
        m = [c for c in pool if c["finding_id"] == x["id"] and c.get("category") == x["category"]] or [c for c in pool if c["finding_id"] == x["id"]]
        pool.remove(m[0])
        items = [i for i in [x["owner_local_id"]] + x.get("related_local_ids", []) if i in ch]
        covered |= set(items)
        pairs.append([x, m[0], items])
    for u in sorted(ch - covered):  # sibling items a fixer changed while closing a finding (named in its note)
        tgt = next((pr for pr in pairs if u in pr[1]["note"] or u[-3:] in pr[1]["note"]), pairs[0])
        tgt[2].append(u)
    for x, c, items in pairs:
        closure_for[(x["id"], x["category"], x["finding"])] = (batch, x, c, C, items)

reverify = {}
for f in sorted(glob.glob(os.path.join(HERE, "errata", "recompute", "V101-*.json"))):
    if f.endswith("_raw.json"):
        continue
    for x in json.load(open(f)):
        reverify[x["id"]] = x  # later packs override earlier ones (V101-7 re-checks the reworded U02-C items)

register = []
for n, x in enumerate(findings, start=1):
    batch, pkt, c, C, items = closure_for[(x["id"], x["category"], x["finding"])]
    owner = pkt["owner_local_id"]
    oid = loc2id[owner]
    changed = bool(items)
    rvs = [reverify.get(loc2id[i]) for i in items]
    ok = all(v and v["choice"] == new[loc2id[i]]["correct_option"] and v["matching_options"] == [new[loc2id[i]]["correct_option"]] for i, v in zip(items, rvs))
    register.append(dict(
        errata_no=f"ERR-{n:03d}", item_id=x["id"], owner_local_id=owner, owner_item_id=oid,
        related_local_ids="; ".join(pkt.get("related_local_ids", [])), category=x["category"],
        severity_raised=x["severity"], severity_final=UPGRADED.get((x["id"], x["category"]), x["severity"]),
        finding=x["finding"], suggested_fix=x["suggested_fix"], fix_batch=batch, action=c["action"], closure_note=c["note"],
        stem_or_options_changed=changed, items_changed="; ".join(items),
        reverified=("yes: independent recompute agrees for every changed item" if changed and ok else
                    ("CHECK" if changed else "not required (stem and options unchanged)"))))

# post-fix findings raised by the re-verification and the editor
POST = [
    dict(item="U02-C-042", category="E2", severity="critical", action="fixed",
         finding="Re-verification: 'real and less than 5 (possibly equal)' can be read as 'less than or equal to 5'; under that reading k = 5 also qualifies and no option is correct.",
         note="Stem now reads '(not necessarily distinct) are real and strictly less than 5'. Key unchanged. Re-verified independently (V101-7)."),
    dict(item="U02-C-050", category="E2", severity="minor", action="fixed",
         finding="Re-verification: 'lie in the open interval (1, 5) (possibly equal)' is ambiguous about what may be equal.",
         note="Stem now reads 'both roots ... (not necessarily distinct) are real and lie in the open interval (1, 5)'. Key unchanged. Re-verified (V101-7)."),
    dict(item="U02-C-031", category="E2", severity="minor", action="fixed",
         finding="Editor sweep: the same '(possibly equal)' phrase appears in this stem.",
         note="Reworded to '(not necessarily distinct)'. Key unchanged. Re-verified (V101-7)."),
    dict(item="U02-D-051", category="E6", severity="minor", action="aliased",
         finding="Post-fix duplicate scan: the rewritten item uses the same recurrence on x^2 - 5x + c as U02-D-025 and has the same answer 5.",
         note="Alias group ALIAS-ERR-DUPSCAN-01 links U02-D-025 and U02-D-051."),
    dict(item="U14-B-041", category="E8", severity="minor", action="retained",
         finding="Fixer query: items counting solutions of a trigonometric curve against a non-trigonometric curve (U14-B-040, 041, 043, 045, 046) and range-attainment counts (U14-B-044, 054) might fall under the ruling that trigonometric equations are out of scope.",
         note="Editor ruling: solving trigonometric equations by general solution is out of scope and was removed (U14-B-014, U14-B-042). Counting intersections from graphs of trigonometric functions, and deciding whether a value lies in the range, test the graphs and ranges of trigonometric functions, which are in the syllabus. These items are retained."),
]
for k, p in enumerate(POST, start=len(findings) + 1):
    oid = loc2id[p["item"]]
    rv = reverify.get(oid)
    register.append(dict(errata_no=f"ERR-{k:03d}", item_id=oid, owner_local_id=p["item"], owner_item_id=oid, related_local_ids="",
                         category=p["category"], severity_raised=p["severity"], severity_final=p["severity"], finding=p["finding"],
                         suggested_fix="", fix_batch="editor (post-fix)", action=p["action"], closure_note=p["note"],
                         stem_or_options_changed=p["action"] == "fixed", items_changed=p["item"] if p["action"] == "fixed" else "",
                         reverified=("yes: independent recompute agrees" if rv and rv["choice"] == new[oid]["correct_option"] else
                                     "not required (stem and options unchanged)")))

assert not [r for r in register if r["reverified"] == "CHECK"], [r["errata_no"] for r in register if r["reverified"] == "CHECK"]
with open(os.path.join(OUT, "Errata_Closure_Register.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(register[0].keys()))
    w.writeheader()
    w.writerows(register)
json.dump(register, open(os.path.join(OUT, "errata_register.json"), "w"), indent=1, ensure_ascii=False)

# ---------- 3. re-verification of changed items
diff = j("errata/v101_diff.json")
changed_ids = sorted(set(diff["stem_or_options"]) | {loc2id["U02-C-031"]})
rv_rows = []
for i in sorted(set(changed_ids) | set(diff["numerical"])):
    x = reverify[i]
    r = new[i]
    nv = r["numerical_variant"]
    rv_rows.append(dict(id=i, local_id=r["provenance"]["local_id"], key=r["correct_option"], verifier_choice=x["choice"],
                        matching_options=x["matching_options"], agree=x["choice"] == r["correct_option"] and x["matching_options"] == [r["correct_option"]],
                        numerical_answer=nv["answer_integer"] if nv else None, verifier_numerical=x.get("numerical_answer"),
                        numerical_agree=(nv is None) or x.get("numerical_answer") == nv["answer_integer"], method=x.get("method"), issue=x.get("issue", "")))
assert all(r["agree"] and r["numerical_agree"] for r in rv_rows), [r for r in rv_rows if not (r["agree"] and r["numerical_agree"])]
first_round_issues = []
for f in sorted(glob.glob(os.path.join(HERE, "errata", "recompute", "V101-[1-6].json"))):
    for x in json.load(open(f)):
        if x.get("issue") or x["matching_options"] != [new[x["id"]]["correct_option"]]:
            first_round_issues.append(dict(id=x["id"], issue=x.get("issue"), choice=x["choice"]))
json.dump(dict(method="Every item whose stem, options or numerical alternate changed was rebuilt and sent, with options in released order but no key, to fresh verifier agents who recomputed it with their own code.",
               items=len(rv_rows), agree=sum(r["agree"] for r in rv_rows), numerical_checked=sum(r["numerical_answer"] is not None for r in rv_rows),
               first_pass_issues=first_round_issues,
               first_pass_resolution="Two U02-C stems were flagged as ambiguous ('possibly equal'). The editor reworded them and a third stem with the same phrase; all three were re-verified in pack V101-7 with no issue.",
               results=rv_rows),
          open(os.path.join(OUT, "reverification_changed_items.json"), "w"), indent=1, ensure_ascii=False)

# ---------- 4. summary
reg_f = register[:len(findings)]
summary = dict(
    recompute=dict(items=len(rc_rows), by_code=sum(r["method"] == "code" for r in rc_rows), key_agree=sum(r["agree"] for r in rc_rows),
                   numerical_items=sum(r["numerical_answer_v100"] is not None for r in rc_rows),
                   numerical_agree=sum(r["numerical_answer_v100"] is not None and r["numerical_agree"] for r in rc_rows)),
    audit=dict(findings=len(findings), by_category=dict(sorted(Counter(r["category"] for r in reg_f).items())),
               by_severity_final=dict(Counter(r["severity_final"] for r in reg_f)), by_action=dict(Counter(r["action"] for r in reg_f))),
    post_fix=dict(findings=len(POST), by_action=dict(Counter(p["action"] for p in POST))),
    all_closures=dict(total=len(register), by_action=dict(Counter(r["action"] for r in register))),
    changes=dict(stem_or_options_changed=len(changed_ids), numerical_alternates_changed=len(diff["numerical"]),
                 notation_only_log=len(diff["log_only"]), source_class_changed=len(diff["class"]), key_letters_changed=len(diff["key_letter"]),
                 alias_groups_added=len(j("errata/config_changes.json")["alias_groups_added"]),
                 numerical_selection_swaps=j("errata/config_changes.json")["numerical_added"]),
    reverification=dict(items=len(rv_rows), agree=sum(r["agree"] for r in rv_rows)),
)
json.dump(summary, open(os.path.join(OUT, "errata_summary.json"), "w"), indent=1)
print(json.dumps(summary, indent=1))
