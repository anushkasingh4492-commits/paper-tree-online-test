# -*- coding: utf-8 -*-
"""Assemble the full JEE Main Mathematics release (all 14 units). v1.0.1 adds the errata round."""
import csv, glob, hashlib, importlib, json, os, shutil, subprocess, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = "/tmp/claude-0/-home-claude/6e18757b-ac0a-52e3-bf2e-85587c7b2e26/scratchpad"
VERSION = "1.0.1"
NAME = f"JEE_Main_Maths_v{VERSION}"
REL = os.path.join(HERE, "release", NAME)
UNITS = [f"U{u:02d}" for u in range(1, 15)]
SYLLABUS_URL = "https://cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2025/10/202510311323551056.pdf"
BULLETIN_URL = "https://cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2025/11/202511021649722475.pdf"
sys.path.insert(0, HERE)
from assemble_release import PLAN  # noqa: E402


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main():
    if os.path.exists(REL):
        shutil.rmtree(REL)
    os.makedirs(os.path.join(REL, "evidence"))
    os.makedirs(os.path.join(REL, "books"))
    recs = []
    for u in UNITS:
        recs += json.load(open(os.path.join(HERE, "build", u, "records.json")))
    for r in recs:
        r["release_version"] = VERSION
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
    with open(os.path.join(REL, "question_index.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "unit_number", "topic", "subtopic", "difficulty", "source_class", "question_type", "correct_option", "concept_family", "has_numerical_variant"])
        for r in recs:
            w.writerow([r["id"], r["unit_number"], r["topic"], r["subtopic"], r["difficulty"], r["source_class"], r["question_type"], r["correct_option"], r["concept_family"], bool(r["numerical_variant"])])

    fam = defaultdict(list)
    for r in recs:
        for d in r["family_dependencies"]:
            fam[d].append(r["id"])
    json.dump([dict(dependency=k, members=v, maximum_per_paper=1) for k, v in sorted(fam.items())],
              open(os.path.join(REL, "family_register.json"), "w"), indent=1)

    plan = json.load(open(os.path.join(HERE, "config", "batch_plan.json")))
    units = []
    for u in sorted({r["unit_number"] for r in recs}):
        ur = [r for r in recs if r["unit_number"] == u]
        units.append(dict(unit=u, name=ur[0]["chapter"], count=len(ur), difficulty=dict(Counter(r["difficulty"] for r in ur)),
                          classes=dict(Counter(r["source_class"] for r in ur)), keys=dict(Counter(r["correct_option"] for r in ur)),
                          numerical_variants=sum(1 for r in ur if r["numerical_variant"]),
                          question_types=dict(Counter(r["question_type"] for r in ur)),
                          topics=dict(Counter(r["topic"] for r in ur)), question_ids=[r["id"] for r in ur]))
    scope = json.load(open(os.path.join(HERE, "config", "scope_notes.json")))
    scope_units = {}
    for f in sorted(glob.glob(os.path.join(HERE, "briefs", "U*_scope.md"))):
        scope_units[os.path.basename(f)[:3]] = open(f).read()
    json.dump(dict(total=len(recs), planned_full_bank=dict(total=sum(p[2] for p in PLAN), units=[dict(unit=p[0], name=p[1], planned=p[2], XI=p[3], XII=p[4], branch=p[5]) for p in PLAN]),
                   units=units, scope_interpretation=scope, unit_scope_briefs=scope_units),
              open(os.path.join(REL, "coverage_map.json"), "w"), indent=1, ensure_ascii=False)
    json.dump(dict(syllabus_url=SYLLABUS_URL, bulletin_url=BULLETIN_URL, checked_date="2026-10-07", basis_year=2026,
                   status_2027="Separate official 2027 syllabus not located at build time",
                   attribution="Scope references only. All questions are originally authored; none is attributed to a past NTA paper."),
              open(os.path.join(REL, "source_references.json"), "w"), indent=1)

    # ---------------- evidence
    ev = os.path.join(REL, "evidence")
    mc, dr, nc, kb = [], [], [], []
    for u in UNITS:
        e = os.path.join(HERE, "build", u, "evidence")
        mc += json.load(open(os.path.join(e, "machine_checks.json")))
        dr += json.load(open(os.path.join(e, "distractor_review.json")))
        nc += json.load(open(os.path.join(e, "numerical_checks.json")))
        kb.append(json.load(open(os.path.join(e, "key_balance.json"))))
    json.dump(mc, open(os.path.join(ev, "machine_checks.json"), "w"), indent=1, ensure_ascii=False)
    json.dump(dr, open(os.path.join(REL, "distractor_review.json"), "w"), indent=1, ensure_ascii=False)
    json.dump(nc, open(os.path.join(ev, "numerical_checks.json"), "w"), indent=1, ensure_ascii=False)
    json.dump(kb, open(os.path.join(ev, "key_balance.json"), "w"), indent=1)

    id_map = {r["provenance"]["local_id"]: r["id"] for r in recs}
    rows = []
    k1 = json.load(open(os.path.join(SCRATCH, "blind_key_u02.json")))
    k2 = json.load(open(os.path.join(SCRATCH, "blind_key_u02_r2.json")))
    kf = json.load(open("/root/.blind_key_full.json"))
    kr = json.load(open("/root/.blind_key_r2.json"))
    def add(rnd, a, key):
        rows.append(dict(round=rnd, id=id_map[a["id"]], local_id=a["id"], solver_choice=a["choice"], key_in_review_pack=key[a["id"]],
                         agree=a["choice"] == key[a["id"]], solver_working=a["working"], confidence=a["confidence"], issue=a["issue"]))
    for i in range(1, 5):
        for a in json.load(open(os.path.join(HERE, "blind", f"answers{i}.json"))):
            add("U02 round 1", a, k1)
    for a in json.load(open(os.path.join(HERE, "blind", "answers5.json"))):
        add("U02 round 2", a, k2)
    for f in sorted(glob.glob(os.path.join(HERE, "blind", "full", "answers*.json"))):
        for a in json.load(open(f)):
            add("Units 1,3-14 round 1", a, kf)
    for f in sorted(glob.glob(os.path.join(HERE, "blind", "r2", "answers*.json"))):
        for a in json.load(open(f)):
            add("Units 1,3-14 round 2 (changed items)", a, kr)
    adjud = json.load(open(os.path.join(HERE, "verify", "adjudication.json")))
    summ = defaultdict(lambda: [0, 0])
    for r in rows:
        summ[r["round"]][0] += 1
        summ[r["round"]][1] += r["agree"]
    json.dump(dict(method="Options shuffled into fresh packs; separate solver agents with no access to drafts or keys solved every item. Round 2 re-solved every item whose stem or options changed after the editorial audit.",
                   note="Option letters here refer to the shuffled review packs, not to the released option order.",
                   rounds={k: dict(items=v[0], agree=v[1]) for k, v in summ.items()}, adjudication=adjud, results=rows),
              open(os.path.join(ev, "blind_resolve_results.json"), "w"), indent=1, ensure_ascii=False)

    findings = []
    for x in json.load(open(os.path.join(HERE, "verify", "audit_closure_u02.json")))["findings"]:
        findings.append(dict(x, unit="U02"))
    for f in sorted(glob.glob(os.path.join(HERE, "verify", "audit", "*.json"))):
        for x in json.load(open(f)):
            findings.append(dict(finding_id=x["id"], category=x.get("category"), severity=x.get("severity"), finding=x.get("finding"),
                                 suggested_fix=x.get("suggested_fix"), source="editorial audit"))
    closures = {}
    for f in sorted(glob.glob(os.path.join(HERE, "verify", "fix", "*_closure.json"))):
        c = json.load(open(f))
        closures[os.path.basename(f).replace("_closure.json", "")] = c
    json.dump(dict(audit="Hostile editorial audit by separate model agents (two batches per auditor) of every full record, plus issues raised by blind solvers; corrections by separate correcting agents; harness re-run and blind re-solve of all changed items.",
                   findings=findings, batch_closures=closures, editor_actions=json.load(open(os.path.join(HERE, "verify", "editor_actions.json")))),
              open(os.path.join(ev, "editorial_audit_closure.json"), "w"), indent=1, ensure_ascii=False)
    for f in ("mcq_audit_full.json",):
        shutil.copy(os.path.join(HERE, "build", f), os.path.join(ev, f))
    # errata round (v1.0.1)
    er = os.path.join(ev, "errata_v1.0.1")
    os.makedirs(er)
    for f in sorted(os.listdir(os.path.join(HERE, "errata", "out"))):
        if f.endswith(".json"):
            shutil.copy(os.path.join(HERE, "errata", "out", f), er)
    shutil.copy(os.path.join(HERE, "errata", "all_audit_findings.json"), os.path.join(er, "audit_findings.json"))
    json.dump({os.path.basename(f)[:-13]: json.load(open(f)) for f in sorted(glob.glob(os.path.join(HERE, "errata", "fix", "*_closure.json")))},
              open(os.path.join(er, "batch_closures.json"), "w"), indent=1, ensure_ascii=False)
    for f in ("config_changes.json", "v101_diff.json", "dupcheck_v101.json"):
        shutil.copy(os.path.join(HERE, "errata", f), er)
    shutil.copy(os.path.join(HERE, "errata", "out", "Errata_Closure_Register.csv"), REL)
    for f in ("Errata_Report.html", "Errata_Report.pdf"):
        if os.path.exists(os.path.join(HERE, "errata", "out", f)):
            shutil.copy(os.path.join(HERE, "errata", "out", f), REL)

    shutil.copy(os.path.join(HERE, "question_bank_schema.json"), REL)
    for f in ("generate_paper.py", "Generator_Contract.md", "verify_release.py"):
        shutil.copy(os.path.join(HERE, f), REL)
    sys.path.insert(0, REL)
    gp = importlib.import_module("generate_paper")
    ok, fails, restarts = 0, [], []
    for s in range(1005):
        try:
            a_, b_, att = gp.build(recs, s)
            ok += 1
            restarts.append(att)
        except Exception as e:
            fails.append((s, str(e)))
    ok_u = {}
    for u in range(1, 15):
        ok_u[u] = sum(1 for s in range(200) if _try(gp, recs, s, u))
    json.dump(dict(full_bank_mode=dict(seeds_tested="0-1004", passed=ok, failed=fails, max_restarts_used=max(restarts) if restarts else None),
                   unit_practice_mode=dict(seeds_tested="0-199 per unit", passed_by_unit=ok_u)),
              open(os.path.join(ev, "generator_validation.json"), "w"), indent=1)
    shutil.rmtree(os.path.join(REL, "__pycache__"), ignore_errors=True)
    subprocess.run([sys.executable, os.path.join(REL, "generate_paper.py"), "--bank", base + ".json", "--seed", "42", "--output", os.path.join(REL, "sample")], check=True)
    for f in ("paper.json", "questions.json", "answer_key.json"):
        shutil.move(os.path.join(REL, "sample", f), os.path.join(REL, "sample_" + f))
    os.rmdir(os.path.join(REL, "sample"))

    env = dict(os.environ)
    subprocess.run(["node", os.path.join(HERE, "render_html.js"), base + ".json", REL, "JEE Main Mathematics", os.path.join(REL, "sample_paper.json")],
                   check=True, env=dict(env, SKIP_BOOKS="1"))
    tmp = os.path.join(HERE, "build", "unit_tmp")
    os.makedirs(tmp, exist_ok=True)
    for u in range(1, 15):
        ur = [r for r in recs if r["unit_number"] == u]
        p = os.path.join(tmp, f"u{u}.json")
        json.dump(ur, open(p, "w"), ensure_ascii=False)
        subprocess.run(["node", os.path.join(HERE, "render_html.js"), p, os.path.join(REL, "books"), f"JEE Main Mathematics, Unit {u}: {ur[0]['chapter']}"],
                       check=True, env=dict(env, KATEX_PREFIX="../", KATEX_DIR=REL, STU_NAME=f"Unit_{u:02d}_Student.html", TEA_NAME=f"Unit_{u:02d}_Teacher.html"))

    errata = json.load(open(os.path.join(HERE, "errata", "out", "errata_summary.json")))
    summary = dict(version=VERSION, date="2026-10-08", questions=len(recs), units=14,
                   difficulty=dict(Counter(r["difficulty"] for r in recs)), classes=dict(Counter(r["source_class"] for r in recs)),
                   keys=dict(Counter(r["correct_option"] for r in recs)),
                   numerical_variants=sum(1 for r in recs if r["numerical_variant"]),
                   machine_recomputed=sum(1 for r in recs if r["machine_check"]["status"] == "match"),
                   blind_resolved=len(recs), concept_families=len({r["concept_family"] for r in recs}),
                   selection_dependencies=len(fam), figures=0, generator_full_bank_seeds_passed=ok,
                   supersedes="1.0.0 (same IDs, same key letters; option order of every unchanged item is identical; see Errata_Closure_Register.csv)",
                   errata=errata,
                   review_note="Machine recomputation, independent blind re-solving, an editorial audit and a full errata round (independent code recomputation of every item, hostile unit audit, fixes, re-verification) by separate AI model agents. No external human subject-expert review is claimed. Difficulty is editorial.")
    json.dump(summary, open(os.path.join(REL, "release_summary.json"), "w"), indent=1)
    shutil.copy(os.path.join(HERE, "README_full.md"), os.path.join(REL, "README.md"))
    shutil.copy(os.path.join(HERE, "START_HERE_full.html"), os.path.join(REL, "START_HERE.html"))

    A = os.path.join(REL, "authoring")
    os.makedirs(A)
    for f in ["qlib.py", "harness.py", "katex_check.js", "DRAFTING_SPEC.md", "build_unit.py", "render_html.js", "assemble_release.py", "assemble_full.py", "gen_configs.py", "make_briefs.py", "update_configs_errata.py", "make_errata_evidence.py", "dup_scan.py"]:
        shutil.copy(os.path.join(HERE, f), A)
    for d in ["briefs", "config"]:
        shutil.copytree(os.path.join(HERE, d), os.path.join(A, d))
    os.makedirs(os.path.join(A, "tests"))
    shutil.copy(os.path.join(HERE, "tests", "test_release.py"), os.path.join(A, "tests"))
    os.makedirs(os.path.join(A, "drafts"))
    for f in sorted(os.listdir(os.path.join(HERE, "drafts"))):
        if f.endswith(".py"):
            shutil.copy(os.path.join(HERE, "drafts", f), os.path.join(A, "drafts", f))

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


def _try(gp, recs, s, u):
    try:
        gp.build(recs, s, unit=u)
        return True
    except Exception:
        return False


if __name__ == "__main__":
    main()
