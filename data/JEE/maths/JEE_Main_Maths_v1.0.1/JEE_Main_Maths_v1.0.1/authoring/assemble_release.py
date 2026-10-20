# -*- coding: utf-8 -*-
"""Assemble the pilot release folder for Unit 2 (extendable to all units)."""
import csv, hashlib, json, os, shutil, subprocess, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = "/tmp/claude-0/-home-claude/6e18757b-ac0a-52e3-bf2e-85587c7b2e26/scratchpad"
VERSION = "1.0.0-pilot"
NAME = f"JEE_Main_Maths_v{VERSION}"
REL = os.path.join(HERE, "release", NAME)
UNITS = ["U02"]
SYLLABUS_URL = "https://cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2025/10/202510311323551056.pdf"
BULLETIN_URL = "https://cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2025/11/202511021649722475.pdf"

PLAN = [  # unit, name, total, XI, XII, branch
    (1, "Sets, Relations and Functions", 140, 60, 80, "Algebra"),
    (2, "Complex Numbers and Quadratic Equations", 220, 220, 0, "Algebra"),
    (3, "Matrices and Determinants", 220, 0, 220, "Algebra"),
    (4, "Permutations and Combinations", 160, 160, 0, "Algebra"),
    (5, "Binomial Theorem and its Simple Applications", 140, 140, 0, "Algebra"),
    (6, "Sequence and Series", 180, 180, 0, "Algebra"),
    (7, "Limit, Continuity and Differentiability", 280, 80, 200, "Calculus"),
    (8, "Integral Calculus", 280, 0, 280, "Calculus"),
    (9, "Differential Equations", 140, 0, 140, "Calculus"),
    (10, "Co-ordinate Geometry", 300, 300, 0, "Coordinate Geometry"),
    (11, "Three Dimensional Geometry", 140, 0, 140, "Vectors and 3D Geometry"),
    (12, "Vector Algebra", 160, 0, 160, "Vectors and 3D Geometry"),
    (13, "Statistics and Probability", 180, 100, 80, "Statistics and Probability"),
    (14, "Trigonometry", 160, 110, 50, "Trigonometry"),
]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main():
    if os.path.exists(REL):
        shutil.rmtree(REL)
    os.makedirs(os.path.join(REL, "evidence"))
    recs = []
    for u in UNITS:
        recs += json.load(open(os.path.join(HERE, "build", u, "records.json")))
    base = os.path.join(REL, f"jee_main_maths_v{VERSION}")
    json.dump(recs, open(base + ".json", "w"), indent=1, ensure_ascii=False)
    with open(base + ".jsonl", "w") as f:
        for r in recs:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    cols = list(recs[0].keys())
    with open(base + ".csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for r in recs:
            w.writerow([json.dumps(r[c], ensure_ascii=False) if isinstance(r[c], (dict, list)) or r[c] is None else r[c] for c in cols])

    qonly = [dict(id=r["id"], unit_number=r["unit_number"], unit=r["unit"], topic=r["topic"], subtopic=r["subtopic"],
                  difficulty=r["difficulty"], source_class=r["source_class"], question=r["question"], options=r["options"],
                  figures=r["figures"], assumptions=r["assumptions"], notation=r["notation"],
                  numerical_question=r["numerical_variant"]["question"] if r["numerical_variant"] else None) for r in recs]
    json.dump(qonly, open(os.path.join(REL, "questions_only.json"), "w"), indent=1, ensure_ascii=False)
    ans = [dict(id=r["id"], correct_option=r["correct_option"], correct_answer=r["correct_answer"], explanation=r["explanation"],
                numerical_answer=r["numerical_variant"]["answer_integer"] if r["numerical_variant"] else None) for r in recs]
    json.dump(ans, open(os.path.join(REL, "answers_and_explanations.json"), "w"), indent=1, ensure_ascii=False)

    # index csv
    with open(os.path.join(REL, "question_index.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "unit_number", "topic", "subtopic", "difficulty", "source_class", "question_type", "correct_option", "concept_family", "has_numerical_variant"])
        for r in recs:
            w.writerow([r["id"], r["unit_number"], r["topic"], r["subtopic"], r["difficulty"], r["source_class"], r["question_type"], r["correct_option"], r["concept_family"], bool(r["numerical_variant"])])

    # families
    fam = defaultdict(list)
    for r in recs:
        for d in r["family_dependencies"]:
            fam[d].append(r["id"])
    json.dump([dict(dependency=k, members=v, maximum_per_paper=1) for k, v in sorted(fam.items())],
              open(os.path.join(REL, "family_register.json"), "w"), indent=1)

    # coverage map
    units = []
    for u in sorted({r["unit_number"] for r in recs}):
        ur = [r for r in recs if r["unit_number"] == u]
        units.append(dict(unit=u, name=ur[0]["chapter"], count=len(ur), difficulty=dict(Counter(r["difficulty"] for r in ur)),
                          classes=dict(Counter(r["source_class"] for r in ur)), keys=dict(Counter(r["correct_option"] for r in ur)),
                          numerical_variants=sum(1 for r in ur if r["numerical_variant"]),
                          question_types=dict(Counter(r["question_type"] for r in ur)),
                          topics=dict(Counter(r["topic"] for r in ur)), question_ids=[r["id"] for r in ur]))
    scope = json.load(open(os.path.join(HERE, "config", "scope_notes.json")))
    json.dump(dict(total=len(recs), planned_full_bank=dict(total=sum(p[2] for p in PLAN), units=[dict(unit=p[0], name=p[1], planned=p[2], XI=p[3], XII=p[4], branch=p[5]) for p in PLAN]),
                   units=units, scope_interpretation=scope),
              open(os.path.join(REL, "coverage_map.json"), "w"), indent=1, ensure_ascii=False)

    json.dump(dict(syllabus_url=SYLLABUS_URL, bulletin_url=BULLETIN_URL, checked_date="2026-10-07", basis_year=2026,
                   status_2027="Separate official 2027 syllabus not located at build time",
                   attribution="Scope references only. All questions are originally authored; none is attributed to a past NTA paper."),
              open(os.path.join(REL, "source_references.json"), "w"), indent=1)

    # evidence
    for u in UNITS:
        for f in os.listdir(os.path.join(HERE, "build", u, "evidence")):
            shutil.copy(os.path.join(HERE, "build", u, "evidence", f), os.path.join(REL, "evidence", f"{u}_{f}"))
    # blind re-solve evidence
    id_map = {r["provenance"]["local_id"]: r["id"] for r in recs}
    k1 = json.load(open(os.path.join(SCRATCH, "blind_key_u02.json")))
    k2 = json.load(open(os.path.join(SCRATCH, "blind_key_u02_r2.json")))
    rows = []
    for i in range(1, 5):
        for a in json.load(open(os.path.join(HERE, "blind", f"answers{i}.json"))):
            rows.append(dict(round=1, id=id_map[a["id"]], local_id=a["id"], solver_choice=a["choice"], author_key_in_shuffled_pack=k1[a["id"]],
                             agree=a["choice"] == k1[a["id"]], solver_working=a["working"], confidence=a["confidence"], issue=a["issue"]))
    for a in json.load(open(os.path.join(HERE, "blind", "answers5.json"))):
        rows.append(dict(round=2, id=id_map[a["id"]], local_id=a["id"], solver_choice=a["choice"], author_key_in_shuffled_pack=k2[a["id"]],
                         agree=a["choice"] == k2[a["id"]], solver_working=a["working"], confidence=a["confidence"], issue=a["issue"]))
    json.dump(dict(method="Options shuffled into fresh packs; separate solver agents with no access to drafts or keys solved every item; round 2 re-solved every item whose stem or options changed after the editorial audit.",
                   note="Option letters here refer to the shuffled review packs, not to the released option order.",
                   round1_items=sum(1 for r in rows if r["round"] == 1), round1_agree=sum(1 for r in rows if r["round"] == 1 and r["agree"]),
                   round2_items=sum(1 for r in rows if r["round"] == 2), round2_agree=sum(1 for r in rows if r["round"] == 2 and r["agree"]),
                   results=rows), open(os.path.join(REL, "evidence", "U02_blind_resolve_results.json"), "w"), indent=1, ensure_ascii=False)
    closure = json.load(open(os.path.join(HERE, "verify", "audit_closure_u02.json")))
    json.dump(closure, open(os.path.join(REL, "evidence", "U02_editorial_audit_closure.json"), "w"), indent=1, ensure_ascii=False)

    # schema
    shutil.copy(os.path.join(HERE, "question_bank_schema.json"), REL)

    # generator + sample
    shutil.copy(os.path.join(HERE, "generate_paper.py"), REL)
    shutil.copy(os.path.join(HERE, "Generator_Contract.md"), REL)
    shutil.copy(os.path.join(HERE, "verify_release.py"), REL)
    gen_ok, gen_fail = 0, []
    sys.path.insert(0, REL)
    import importlib
    gp = importlib.import_module("generate_paper")
    for s in range(1005):
        try:
            a_, b_, _ = gp.build(recs, s, unit=2)
            gen_ok += 1
        except Exception as e:
            gen_fail.append((s, str(e)))
    json.dump(dict(mode="unit-practice, unit 2", seeds_tested="0-1004", passed=gen_ok, failed=gen_fail),
              open(os.path.join(REL, "evidence", "generator_validation.json"), "w"), indent=1)
    shutil.rmtree(os.path.join(REL, "__pycache__"), ignore_errors=True)
    subprocess.run([sys.executable, os.path.join(REL, "generate_paper.py"), "--bank", base + ".json", "--seed", "42", "--unit", "2", "--output", os.path.join(REL, "sample")], check=True)
    for f in ("paper.json", "questions.json", "answer_key.json"):
        shutil.move(os.path.join(REL, "sample", f), os.path.join(REL, "sample_" + f))
    os.rmdir(os.path.join(REL, "sample"))

    subprocess.run(["node", os.path.join(HERE, "render_html.js"), base + ".json", REL, "JEE Main Mathematics", os.path.join(REL, "sample_paper.json")], check=True)

    summary = dict(version=VERSION, date="2026-10-07", scope="Pilot: Unit 2 only. Remaining 13 units to follow in the same pipeline.",
                   questions=len(recs), difficulty=dict(Counter(r["difficulty"] for r in recs)),
                   classes=dict(Counter(r["source_class"] for r in recs)), keys=dict(Counter(r["correct_option"] for r in recs)),
                   numerical_variants=sum(1 for r in recs if r["numerical_variant"]),
                   machine_recomputed=sum(1 for r in recs if r["machine_check"]["status"] == "match"),
                   blind_resolved=len(recs), families=len({r["concept_family"] for r in recs}),
                   selection_dependencies=len(fam), figures=0,
                   generator_seeds_passed=gen_ok, planned_full_bank_total=sum(p[2] for p in PLAN),
                   review_note="Machine recomputation, independent blind re-solving and an editorial audit by separate model agents. No external human subject-expert review is claimed. Difficulty is editorial.")
    json.dump(summary, open(os.path.join(REL, "release_summary.json"), "w"), indent=1)
    shutil.copy(os.path.join(HERE, "README_template.md"), os.path.join(REL, "README.md"))
    shutil.copy(os.path.join(HERE, "START_HERE.html"), REL)

    # authoring sources (pipeline used to build and continue the bank)
    A = os.path.join(REL, "authoring")
    os.makedirs(A)
    for f in ["qlib.py", "harness.py", "katex_check.js", "DRAFTING_SPEC.md", "build_unit.py", "render_html.js", "assemble_release.py"]:
        shutil.copy(os.path.join(HERE, f), A)
    for d in ["briefs", "config"]:
        shutil.copytree(os.path.join(HERE, d), os.path.join(A, d))
    os.makedirs(os.path.join(A, "drafts"))
    for f in os.listdir(os.path.join(HERE, "drafts")):
        if f.endswith(".py") and not f.startswith("_sample"):
            shutil.copy(os.path.join(HERE, "drafts", f), os.path.join(A, "drafts", f))
    shutil.copy(os.path.join(HERE, "drafts", "_sample.py"), os.path.join(A, "drafts", "_sample.py"))

    # checksums
    lines = []
    for root, _, files in os.walk(REL):
        for f in sorted(files):
            p = os.path.join(root, f)
            rel = os.path.relpath(p, REL)
            if rel == "checksums.sha256" or rel.startswith("katex/"):
                continue
            lines.append(f"{sha(p)}  {rel}")
    open(os.path.join(REL, "checksums.sha256"), "w").write("\n".join(sorted(lines, key=lambda l: l[66:])) + "\n")
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
