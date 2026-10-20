# -*- coding: utf-8 -*-
"""Comprehensive automated test suite for a JEE Main Mathematics release folder.

usage: python3 tests/test_release.py <release_dir> [--prev <previous_release_dir>] [--zip <zip>] [--out results.json] [--quick]

Every test is independent of the build scripts' own assertions: it re-derives what it checks from the
released files. Results are written as JSON (one entry per test: name, passed, details).
"""
import argparse, csv, difflib, glob, hashlib, html, importlib.util, io, json, os, re, shutil, subprocess, sys, tempfile, time, zipfile
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RESULTS = []


def test(name):
    def deco(fn):
        def run(*a):
            t0 = time.time()
            try:
                passed, details = fn(*a)
            except Exception as e:  # a crashing test is a failing test
                import traceback
                passed, details = False, dict(exception=repr(e), trace=traceback.format_exc()[-1500:])
            RESULTS.append(dict(test=name, passed=bool(passed), seconds=round(time.time() - t0, 1), details=details))
            print(("PASS " if passed else "FAIL ") + name, flush=True)
        run.__name__ = fn.__name__
        return run
    return deco


TEXT_FIELDS = ("question", "correct_answer", "explanation", "common_misconception", "difficulty_reason")


def all_texts(r):
    for f in TEXT_FIELDS:
        yield f, r[f]
    for L in "ABCD":
        yield "option " + L, r["options"][L]
    for a in r["assumptions"]:
        yield "assumption", a
    if r["numerical_variant"]:
        yield "numerical question", r["numerical_variant"]["question"]


# ---------------------------------------------------------------- data and schema
@test("T01 schema: every record validates against question_bank_schema.json")
def t01(R, recs):
    import jsonschema
    schema = json.load(open(os.path.join(R, "question_bank_schema.json")))
    v = jsonschema.Draft202012Validator(schema) if "2020" in schema.get("$schema", "") else jsonschema.Draft7Validator(schema)
    errs = [dict(path=list(e.path)[:3], msg=e.message[:200]) for e in v.iter_errors(recs)]
    return not errs, dict(records=len(recs), errors=errs[:20], error_count=len(errs))


@test("T02 identity: 2,700 unique IDs, sequential per unit, unit counts as planned, local IDs unique")
def t02(R, recs):
    plan = {1: 140, 2: 220, 3: 220, 4: 160, 5: 140, 6: 180, 7: 280, 8: 280, 9: 140, 10: 300, 11: 140, 12: 160, 13: 180, 14: 160}
    bad = []
    ids = [r["id"] for r in recs]
    if len(ids) != 2700 or len(set(ids)) != 2700:
        bad.append("count or uniqueness")
    for u, n in plan.items():
        got = [r["id"] for r in recs if r["unit_number"] == u]
        if got != [f"JEE-MATH-U{u:02d}-{k:03d}" for k in range(1, n + 1)]:
            bad.append(f"unit {u} ids not sequential or count != {n}")
    loc = [r["provenance"]["local_id"] for r in recs]
    if len(set(loc)) != len(loc):
        bad.append("local ids not unique")
    if {r["release_version"] for r in recs} != {re.search(r"v([\d.]+)\.json$", glob.glob(os.path.join(R, "jee_main_maths_v*.json"))[0]).group(1)}:
        bad.append("release_version does not match file name")
    return not bad, dict(problems=bad)


@test("T03 options: 4 distinct options, key letter valid, key text equals keyed option, distinct after whitespace normalisation")
def t03(R, recs):
    bad = []
    for r in recs:
        o = r["options"]
        if sorted(o) != list("ABCD") or r["correct_option"] not in o:
            bad.append((r["id"], "letters"))
        if r["correct_answer"] != o[r["correct_option"]]:
            bad.append((r["id"], "key text"))
        if len({re.sub(r"\s+", "", v) for v in o.values()}) != 4:
            bad.append((r["id"], "options equal after whitespace removal"))
        if any(not v.strip() for v in o.values()):
            bad.append((r["id"], "empty option"))
    return not bad, dict(problems=bad[:30], count=len(bad))


@test("T04 export parity: JSON = JSONL = CSV; student and teacher exports and question index agree with the bank")
def t04(R, recs):
    base = glob.glob(os.path.join(R, "jee_main_maths_v*.json"))[0][:-5]
    bad = []
    jl = [json.loads(l) for l in open(base + ".jsonl", encoding="utf-8")]
    if jl != recs:
        bad.append("jsonl differs")
    rows = list(csv.DictReader(open(base + ".csv", encoding="utf-8", newline="")))
    if len(rows) != len(recs):
        bad.append("csv row count")
    for r, row in zip(recs, rows):
        for k, v in r.items():
            cv = row[k]
            if isinstance(v, (dict, list)) or v is None:
                if json.loads(cv) != v:
                    bad.append((r["id"], k)); break
            elif isinstance(v, bool):
                if cv != str(v):
                    bad.append((r["id"], k)); break
            elif str(v) != cv:
                bad.append((r["id"], k)); break
    q = json.load(open(os.path.join(R, "questions_only.json"), encoding="utf-8"))
    leak_keys = {"correct_option", "correct_answer", "explanation", "common_misconception", "numerical_variant", "answer_integer", "distractor", "provenance"}
    for r, x in zip(recs, q):
        if x["id"] != r["id"] or x["question"] != r["question"] or x["options"] != r["options"]:
            bad.append((r["id"], "questions_only mismatch"))
        if leak_keys & set(x):
            bad.append((r["id"], "questions_only leaks " + str(leak_keys & set(x))))
        if x["numerical_question"] != (r["numerical_variant"]["question"] if r["numerical_variant"] else None):
            bad.append((r["id"], "numerical question mismatch"))
    a = json.load(open(os.path.join(R, "answers_and_explanations.json"), encoding="utf-8"))
    for r, x in zip(recs, a):
        if (x["id"], x["correct_option"], x["correct_answer"], x["explanation"]) != (r["id"], r["correct_option"], r["correct_answer"], r["explanation"]):
            bad.append((r["id"], "answers mismatch"))
        if x["numerical_answer"] != (r["numerical_variant"]["answer_integer"] if r["numerical_variant"] else None):
            bad.append((r["id"], "numerical answer mismatch"))
    idx = list(csv.DictReader(open(os.path.join(R, "question_index.csv"), newline="")))
    for r, x in zip(recs, idx):
        if (x["id"], x["correct_option"], x["difficulty"], x["source_class"], x["concept_family"]) != (r["id"], r["correct_option"], r["difficulty"], r["source_class"], r["concept_family"]):
            bad.append((r["id"], "index mismatch"))
    return not bad, dict(problems=bad[:30], count=len(bad))


# ---------------------------------------------------------------- mathematics rendering and style
@test("T05 KaTeX: every $...$ segment in every text field renders with throwOnError (strict parser)")
def t05(R, recs):
    items = [dict(id=r["id"], field=f, text=t) for r in recs for f, t in all_texts(r)]
    items += [dict(id=d["id"], field="distractor rationale " + x["option"], text=x["reason"])
              for d in json.load(open(os.path.join(R, "distractor_review.json"), encoding="utf-8")) for x in d["distractors"]]
    p = subprocess.run(["node", os.path.join(ROOT, "katex_check.js")], input=json.dumps(items), capture_output=True, text=True, timeout=900)
    fails = json.loads(p.stdout)
    return not fails, dict(segments_source_strings=len(items), failures=fails[:20], failure_count=len(fails))


@test("T06 house style: no em/en dashes in any release text file; no control characters; one log convention; no letter references in solutions")
def t06(R, recs):
    bad = []
    for p in glob.glob(os.path.join(R, "**", "*"), recursive=True):
        if os.path.isdir(p) or "/katex/" in p or not p.endswith((".json", ".jsonl", ".csv", ".md", ".html", ".py", ".sha256")):
            continue
        s = open(p, encoding="utf-8").read()
        if re.search("[\u2013\u2014]", s):
            bad.append((os.path.relpath(p, R), "em/en dash"))
    for r in recs:
        for f, t in all_texts(r):
            if re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", t):
                bad.append((r["id"], f, "control char"))
            if re.search(r"\\log(?![_a-zA-Z])", t) or re.search(r"\\ln\b", t) or re.search(r"(?<![\\\w])ln\s*\(", t):
                bad.append((r["id"], f, "log notation"))
            if t.count("$") % 2:
                bad.append((r["id"], f, "unbalanced $"))
        if re.search(r"\boption\s*\(?[ABCD]\)?(?![a-z])|\([ABCD]\)|\b(?:choice|answer)\s+[ABCD]\b", r["explanation"]):
            bad.append((r["id"], "explanation names a letter"))
    return not bad, dict(problems=bad[:30], count=len(bad))


@test("T07 books: student books contain every unit ID and no keys, solutions or integer answers; teacher books contain every ID and every key")
def t07(R, recs):
    bad = []
    for u in range(1, 15):
        ur = [r for r in recs if r["unit_number"] == u]
        stu = open(os.path.join(R, "books", f"Unit_{u:02d}_Student.html"), encoding="utf-8").read()
        tea = open(os.path.join(R, "books", f"Unit_{u:02d}_Teacher.html"), encoding="utf-8").read()
        for r in ur:
            if stu.count(r["id"] + " ") + stu.count(r["id"] + "<") < 1:
                bad.append((u, r["id"], "missing from student book"))
            if r["id"] not in tea:
                bad.append((u, r["id"], "missing from teacher book"))
        for marker in ("Answer:", 'class="key"', "Answer and solution", "Numerical-answer form", "<details", "Targets:"):
            if marker in stu:
                bad.append((u, "student book contains " + marker))
        if stu.count("<article") != len(ur) or tea.count("<article") != len(ur):
            bad.append((u, "article count"))
        if tea.count('class="key"') != len(ur):
            bad.append((u, "teacher key highlight count"))
        nv = sum(1 for r in ur if r["numerical_variant"])
        if tea.count("Numerical-answer form") != nv:
            bad.append((u, "teacher numerical count"))
        # structural: a student article holds only the meta line, the stem and the options
        for art in re.findall(r"<article[^>]*>(.*?)</article>", stu, flags=re.S):
            rest = re.sub(r'^<div class="meta">.*?</div><div class="q">.*?</div><ol>.*?</ol>$', "", art, flags=re.S)
            if rest:
                bad.append((u, "student article has extra content", rest[:80]))
                break
    sp = open(os.path.join(R, "Sample_Paper.html"), encoding="utf-8").read()
    for marker in ("Answer:", 'class="key"', "<details"):
        if marker in sp:
            bad.append(("Sample_Paper.html", marker))
    return not bad, dict(problems=bad[:30], count=len(bad))


@test("T08 rendered HTML: no raw LaTeX or stray $ in visible text of any book or sample page")
def t08(R, recs):
    bad = []
    for p in sorted(glob.glob(os.path.join(R, "books", "*.html")) + glob.glob(os.path.join(R, "Sample_*.html"))):
        s = open(p, encoding="utf-8").read()
        if s.count('class="katex"') == 0:
            bad.append((os.path.relpath(p, R), "no KaTeX output"))
        s = re.sub(r"<script.*?</script>|<style.*?</style>", "", s, flags=re.S)
        s = re.sub(r'<span class="katex">.*?<span class="katex-html" aria-hidden="true">', "", s, flags=re.S)
        vis = re.sub(r"<[^>]+>", " ", s)
        hits = re.findall(r"\\[a-zA-Z]{2,}|\$", vis)
        if hits:
            bad.append((os.path.relpath(p, R), Counter(hits).most_common(5)))
    return not bad, dict(problems=bad)


# ---------------------------------------------------------------- answers and evidence
@test("T09 integer alternates: 342 present, each an exact non-negative integer, parent link correct, every non-equal value reviewed")
def t09(R, recs):
    bad = []
    nvs = [r for r in recs if r["numerical_variant"]]
    for r in nvs:
        nv = r["numerical_variant"]
        if type(nv["answer_integer"]) is not int or nv["answer_integer"] < 0 or nv["parent_id"] != r["id"] or nv["unrounded_value"] != nv["answer_integer"]:
            bad.append((r["id"], "malformed"))
        if "$" not in nv["question"] and re.search(r"\d", nv["question"]):
            pass
    nc = {x["id"]: x for x in json.load(open(os.path.join(R, "evidence", "numerical_checks.json")))}
    if set(nc) != {r["id"] for r in nvs}:
        bad.append("numerical_checks.json id set differs")
    stems = Counter(r["numerical_variant"]["question"] for r in nvs)
    bad += [("duplicate numerical stem", s[:60]) for s, c in stems.items() if c > 1]
    per_unit = Counter(r["unit_number"] for r in nvs)
    return len(nvs) == 342 and not bad, dict(count=len(nvs), per_unit=dict(sorted(per_unit.items())), scaled=sum(not x["equals_mcq_value"] for x in nc.values()), problems=bad[:20])


@test("T10 machine-check evidence: every recomputed record has a matching evidence entry with distinct distractor values and check source")
def t10(R, recs):
    mc = {x["id"]: x for x in json.load(open(os.path.join(R, "evidence", "machine_checks.json"), encoding="utf-8"))}
    bad = []
    for r in recs:
        if r["machine_check"]["status"] == "match":
            x = mc.get(r["id"])
            if not x or not x["match"] or not x["distractors_differ_from_key"] or not x["check_source"].strip():
                bad.append(r["id"])
            elif x["computed"] != r["machine_check"]["computed_value"]:
                bad.append((r["id"], "computed value differs"))
        elif r["id"] in mc:
            bad.append((r["id"], "evidence for unchecked record"))
    return not bad, dict(machine_checked=sum(r["machine_check"]["status"] == "match" for r in recs), problems=bad[:20])


@test("T11 reproducibility: rebuilding every unit from the shipped authoring sources reproduces the released records exactly")
def t11(R, recs, quick=False):
    tmp = tempfile.mkdtemp()
    A = os.path.join(tmp, "authoring")
    shutil.copytree(os.path.join(R, "authoring"), A)
    nm = os.path.join(ROOT, "node_modules")
    if os.path.exists(nm):
        os.symlink(nm, os.path.join(A, "node_modules"))
    procs = [subprocess.Popen([sys.executable, "build_unit.py", f"config/U{u:02d}.json"], cwd=A, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for u in range(1, 15)]
    errs = []
    for u, p in enumerate(procs, start=1):
        o, e = p.communicate(timeout=1800)
        if p.returncode:
            errs.append((u, e[-400:]))
    rebuilt = [r for u in range(1, 15) for r in json.load(open(os.path.join(A, "build", f"U{u:02d}", "records.json")))] if not errs else []
    diff = [a["id"] for a, b in zip(recs, rebuilt) if a != b]
    shutil.rmtree(tmp, ignore_errors=True)
    return not errs and len(rebuilt) == len(recs) and not diff, dict(build_errors=errs, differing=diff[:20], differing_count=len(diff))


@test("T12 selection dependencies: family register matches records, every alias group links 2+ items, every errata alias request is enforced")
def t12(R, recs):
    bad = []
    for r in recs:
        if r["family_dependencies"][0] != r["concept_family"] or len(set(r["family_dependencies"])) != len(r["family_dependencies"]):
            bad.append((r["id"], "dependency list"))
    members = defaultdict(set)
    for r in recs:
        for d in r["family_dependencies"]:
            members[d].add(r["id"])
    reg = {x["dependency"]: set(x["members"]) for x in json.load(open(os.path.join(R, "family_register.json")))}
    if reg != members:
        bad.append("family_register.json differs from records")
    alias = {k: v for k, v in members.items() if k.startswith("ALIAS-")}
    bad += [(k, "alias with <2 members") for k, v in alias.items() if len(v) < 2]
    loc = {r["provenance"]["local_id"]: r for r in recs}
    cl = json.load(open(os.path.join(R, "evidence", "errata_v1.0.1", "batch_closures.json")))
    n_req = 0
    for b, c in cl.items():
        for grp in c.get("alias_requests", []):
            n_req += 1
            for x, y in [(x, y) for i, x in enumerate(grp) for y in grp[i + 1:]]:
                if not set(loc[x]["family_dependencies"]) & set(loc[y]["family_dependencies"]):
                    bad.append((b, x, y, "alias request not enforced"))
    return not bad, dict(dependencies=len(members), alias_groups=len(alias), alias_requests_checked=n_req, problems=bad[:20])


@test("T13 key balance: exact quotas per unit, no run longer than 3, no ABCD/DCBA run, no two units share a key sequence")
def t13(R, recs):
    bad, seqs = [], {}
    for u in range(1, 15):
        s = "".join(r["correct_option"] for r in recs if r["unit_number"] == u)
        c = Counter(s)
        if max(c.values()) - min(c.values()) > 1:
            bad.append((u, dict(c)))
        if re.search(r"(.)\1\1\1", s) or "ABCD" in s or "DCBA" in s:
            bad.append((u, "run or ladder"))
        seqs[u] = s
    for a in seqs:
        for b in seqs:
            if a < b and (seqs[a] in seqs[b] or seqs[b] in seqs[a]):
                bad.append((a, b, "shared sequence"))
    return not bad, dict(total=dict(Counter(r["correct_option"] for r in recs)), problems=bad)


@test("T14 errata stability vs previous release: same IDs and key letters; unchanged items keep stem and option order; every change is in the closure register")
def t14(R, recs, prev=None):
    if not prev:
        return True, dict(skipped="no previous release given")
    old = json.load(open(glob.glob(os.path.join(prev, "jee_main_maths_v*.json"))[0], encoding="utf-8"))
    norm = lambda s: s.replace("\\log_e", "\\log")
    bad, changed = [], set()
    for o, n in zip(old, recs):
        if o["id"] != n["id"] or o["provenance"]["local_id"] != n["provenance"]["local_id"]:
            bad.append((n["id"], "identity changed"))
        if o["correct_option"] != n["correct_option"]:
            bad.append((n["id"], "key letter changed"))
        if (o["question"], o["options"]) != (n["question"], n["options"]):
            if (norm(o["question"]), {k: norm(v) for k, v in o["options"].items()}) != (norm(n["question"]), {k: norm(v) for k, v in n["options"].items()}):
                changed.add(n["provenance"]["local_id"])
    reg = list(csv.DictReader(open(os.path.join(R, "Errata_Closure_Register.csv"), encoding="utf-8")))
    reg_changed = {i for x in reg for i in x["items_changed"].split("; ") if i}
    if changed - reg_changed:
        bad.append(("changed but not in register", sorted(changed - reg_changed)))
    if reg_changed - changed:
        bad.append(("register says changed but item identical", sorted(reg_changed - changed)))
    rv = json.load(open(os.path.join(R, "evidence", "errata_v1.0.1", "reverification_changed_items.json")))
    rv_ids = {x["local_id"] for x in rv["results"] if x["agree"] and x["numerical_agree"]}
    if changed - rv_ids:
        bad.append(("changed but not re-verified", sorted(changed - rv_ids)))
    return not bad, dict(previous=os.path.basename(prev), items_changed=len(changed), register_rows=len(reg), problems=bad)


# ---------------------------------------------------------------- generator
def _load_gen(R):
    spec = importlib.util.spec_from_file_location("gp_test", os.path.join(R, "generate_paper.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _ids(xs):
    return [x["id"] if isinstance(x, dict) else x for x in xs]


def _validate_paper(byid, a, b, unit=None, seed=0):
    a, b = _ids(a), _ids(b)
    p = []
    ids = a + b
    if len(a) != 20 or len(b) != 5 or len(set(ids)) != 25:
        p.append("size")
    deps = [d for i in ids for d in byid[i]["family_dependencies"]]
    if len(deps) != len(set(deps)):
        p.append("dependency repeated")
    if Counter(byid[i]["correct_option"] for i in a) != Counter({L: 5 for L in "ABCD"}):
        p.append("section A keys")
    if Counter(byid[i]["difficulty"] for i in ids) != Counter({"Easy": 8, "Medium": 11, "Difficult": 6}):
        p.append("difficulty blueprint")
    if Counter(byid[i]["difficulty"] for i in b) != Counter({"Easy": 1, "Medium": 2, "Difficult": 2}):
        p.append("section B blueprint")
    if any(not byid[i]["numerical_variant"] for i in b):
        p.append("section B without integer alternate")
    if unit is None:
        if max(Counter(byid[i]["unit_number"] for i in ids).values()) > 3:
            p.append("more than 3 per unit")
        xi = sum(byid[i]["source_class"] == "XI" for i in ids)
        if xi != (12 if seed % 2 == 0 else 13):
            p.append(f"class split {xi}")
    elif any(byid[i]["unit_number"] != unit for i in ids):
        p.append("unit mode drew from another unit")
    return p


@test("T15 generator, full-bank mode: seeds 0-1004 each produce a paper that passes an independent validator; output is deterministic")
def t15(R, recs, quick=False):
    gp = _load_gen(R)
    byid = {r["id"]: r for r in recs}
    bad, n = [], (101 if quick else 1005)
    for s in range(n):
        try:
            a, b, _ = gp.build(recs, s)
        except Exception as e:
            bad.append((s, "raised " + str(e)[:100])); continue
        p = _validate_paper(byid, a, b, seed=s)
        if p:
            bad.append((s, p))
        if s % 50 == 0 and tuple(map(_ids, gp.build(recs, s)[:2])) != (_ids(a), _ids(b)):
            bad.append((s, "not deterministic"))
    # CLI output equals the library call
    tmp = tempfile.mkdtemp()
    bank = glob.glob(os.path.join(R, "jee_main_maths_v*.json"))[0]
    subprocess.run([sys.executable, os.path.join(R, "generate_paper.py"), "--bank", bank, "--seed", "7", "--output", tmp], check=True, capture_output=True)
    pj = json.load(open(os.path.join(tmp, "paper.json")))
    a, b, _ = gp.build(recs, 7)
    if (_ids(pj["section_a"]), _ids(pj["section_b"])) != (_ids(a), _ids(b)):
        bad.append("CLI output differs from build()")
    qj = json.load(open(os.path.join(tmp, "questions.json")))
    if "correct_option" in json.dumps(qj) or "answer_integer" in json.dumps(qj) or "explanation" in json.dumps(qj):
        bad.append("CLI questions.json leaks answers")
    shutil.rmtree(tmp, ignore_errors=True)
    return not bad, dict(seeds=n, failures=bad[:20], failure_count=len(bad))


@test("T16 generator, unit-practice mode: seeds 0-199 for every unit pass the independent validator")
def t16(R, recs, quick=False):
    gp = _load_gen(R)
    byid = {r["id"]: r for r in recs}
    bad, per = [], {}
    n = 20 if quick else 200
    for u in range(1, 15):
        ok = 0
        for s in range(n):
            try:
                a, b, _ = gp.build(recs, s, unit=u)
            except Exception as e:
                bad.append((u, s, str(e)[:80])); continue
            p = _validate_paper(byid, a, b, unit=u, seed=s)
            if p:
                bad.append((u, s, p))
            else:
                ok += 1
        per[u] = ok
    return not bad, dict(seeds_per_unit=n, passed_by_unit=per, failures=bad[:20])


@test("T17 sample paper: sample files match seed 42 of the generator and the release summary")
def t17(R, recs):
    gp = _load_gen(R)
    sp = json.load(open(os.path.join(R, "sample_paper.json")))
    a, b, _ = gp.build(recs, 42)
    a, b = _ids(a), _ids(b)
    bad = []
    if (_ids(sp["section_a"]), _ids(sp["section_b"])) != (a, b) or sp["seed"] != 42:
        bad.append("sample_paper.json differs from seed 42")
    key = json.load(open(os.path.join(R, "sample_answer_key.json")))
    byid = {r["id"]: r for r in recs}
    blob = json.dumps(key)
    for i in a:
        if byid[i]["correct_option"] not in blob:
            bad.append((i, "key missing"))
    sol = open(os.path.join(R, "Sample_Solutions.html"), encoding="utf-8").read()
    for i in a + b:
        if i not in sol:
            bad.append((i, "missing from solutions"))
    return not bad, dict(problems=bad)


# ---------------------------------------------------------------- package integrity
@test("T18 checksums: every listed file matches; every non-KaTeX file is listed")
def t18(R, recs):
    listed, bad = {}, []
    for line in open(os.path.join(R, "checksums.sha256")):
        h, p = line.rstrip("\n").split("  ", 1)
        listed[p] = h
        fp = os.path.join(R, p)
        if not os.path.exists(fp) or hashlib.sha256(open(fp, "rb").read()).hexdigest() != h:
            bad.append((p, "mismatch"))
    for p in glob.glob(os.path.join(R, "**", "*"), recursive=True):
        rel = os.path.relpath(p, R)
        if os.path.isfile(p) and rel != "checksums.sha256" and not rel.startswith("katex/") and rel not in listed and "__pycache__" not in rel:
            bad.append((rel, "not listed"))
    return not bad, dict(files=len(listed), problems=bad[:20])


@test("T19 shipped verifier: verify_release.py (standard library only) exits 0")
def t19(R, recs):
    p = subprocess.run([sys.executable, "-I", os.path.join(R, "verify_release.py")], capture_output=True, text=True, timeout=600)
    shutil.rmtree(os.path.join(R, "__pycache__"), ignore_errors=True)
    return p.returncode == 0, dict(stdout=p.stdout[-800:])


@test("T20 links: every link in START_HERE.html and the README file list resolves inside the release")
def t20(R, recs):
    s = open(os.path.join(R, "START_HERE.html"), encoding="utf-8").read()
    bad = [h for h in re.findall(r'href="([^"#]+)"', s) if not h.startswith("http") and not os.path.exists(os.path.join(R, h))]
    md = open(os.path.join(R, "README.md"), encoding="utf-8").read()
    for f in re.findall(r"`([\w./-]+\.(?:json|jsonl|csv|html|py|md|pdf|sha256))`", md):
        if "NN" in f or "*" in f:
            continue
        if not os.path.exists(os.path.join(R, f)) and not glob.glob(os.path.join(R, "**", os.path.basename(f)), recursive=True):
            bad.append(f)
    ver = re.search(r"v([\d.]+)\.json$", glob.glob(os.path.join(R, "jee_main_maths_v*.json"))[0]).group(1)
    if f"v{ver}" not in md or f"Version {ver}" not in s:
        bad.append("version text out of date")
    return not bad, dict(problems=bad)


@test("T21 zip: archive opens, passes CRC, and every file in it matches the release folder byte for byte")
def t21(R, recs, zp=None):
    if not zp:
        return True, dict(skipped="no zip given")
    z = zipfile.ZipFile(zp)
    bad = z.testzip()
    probs = [bad] if bad else []
    names = [n for n in z.namelist() if not n.endswith("/")]
    top = os.path.commonprefix(names).split("/")[0]
    for n in names:
        fp = os.path.join(os.path.dirname(R), n) if n.startswith(os.path.basename(R) + "/") else None
        if not fp or not os.path.exists(fp) or open(fp, "rb").read() != z.read(n):
            probs.append(n)
    on_disk = [p for p in glob.glob(os.path.join(R, "**", "*"), recursive=True) if os.path.isfile(p)]
    if len(on_disk) != len(names):
        probs.append(f"file count {len(names)} in zip vs {len(on_disk)} on disk")
    return not probs, dict(zip=os.path.basename(zp), entries=len(names), top=top, problems=probs[:20])


# ---------------------------------------------------------------- content-level sweeps
@test("T22 duplicates: no two stems identical; near-identical stems (character 5-gram Jaccard >= 0.85, same unit) are dependency-linked or have different answers")
def t22(R, recs):
    norm = lambda s: re.sub(r"\s+", "", s)
    exact = [s for s, c in Counter(norm(r["question"]) for r in recs).items() if c > 1]
    sh = {}
    for r in recs:
        s = norm(r["question"])
        sh[r["id"]] = {s[i:i + 5] for i in range(max(1, len(s) - 4))}
    risky, linked, n = [], 0, 0
    for u in range(1, 15):
        ur = [r for r in recs if r["unit_number"] == u]
        for i, a in enumerate(ur):
            for b in ur[i + 1:]:
                A, B = sh[a["id"]], sh[b["id"]]
                jac = len(A & B) / len(A | B)
                if jac >= 0.85:
                    n += 1
                    if set(a["family_dependencies"]) & set(b["family_dependencies"]):
                        linked += 1
                    elif norm(a["correct_answer"]) == norm(b["correct_answer"]):
                        risky.append((a["id"], b["id"], round(jac, 3)))
    return not exact and not risky, dict(exact_duplicates=len(exact), near_pairs=n, near_pairs_linked=linked,
                                         near_pairs_unlinked_same_answer=risky)


@test("T23 option-length cue: the key is the strictly longest option in no more than chance (25%) of items")
def t23(R, recs):
    strict = sum(1 for r in recs if (lambda L: L[r["correct_option"]] == max(L.values()) and list(L.values()).count(max(L.values())) == 1)(
        {k: len(re.sub(r"\s", "", v)) for k, v in r["options"].items()}))
    rate = strict / len(recs)
    return rate <= 0.25, dict(key_strictly_longest=strict, rate=round(rate, 3))


@test("T24 scope sweep: no stem uses a topic excluded under the strict NTA 2026 reading")
def t24(R, recs):
    pats = {
        "equation of a plane": r"equation of (a|the) plane|\bplanes?\s+(passing|through|whose equation)|distance of .* from the plane|angle between .* plane",
        "scalar triple product": r"triple product|\[\s*\\vec\{?a\}?\s+\\vec\{?b\}?\s+\\vec\{?c\}?\s*\]",
        "binomial distribution by name": r"binomial distribution",
        "tangent or normal to a conic": r"(tangent|normal)s?\s+(line\s+)?(to|at)\s+(the\s+)?(parabola|ellipse|hyperbola)",
        "general solution of a trigonometric equation": r"general solution of (the equation )?\$\\(sin|cos|tan)",
        "heights and distances": r"angle of (elevation|depression)",
        "formation of differential equations": r"(differential equation|DE)\s+(of|representing)\s+(the\s+)?family",
        "parametric differentiation": r"x\s*=\s*[^$]*\\?(cos|sin|t)\b[^$]*,\s*y\s*=.*\\frac\{dy\}\{dx\}",
    }
    hits = []
    allowed = "Legitimate uses not flagged: lines or points in a plane, the Argand plane, coordinate planes (xy, yz, xz), a plane mirror, the plane containing three points in vector algebra (cross-product application), and general solutions of differential equations."
    for r in recs:
        q = r["question"] + " " + (r["numerical_variant"]["question"] if r["numerical_variant"] else "")
        for k, p in pats.items():
            if re.search(p, q, re.I):
                hits.append(dict(id=r["id"], local_id=r["provenance"]["local_id"], rule=k, stem=r["question"][:160]))
    return not hits, dict(hits=hits, note=allowed)


@test("T25 summary consistency: release_summary, coverage_map and question_index agree with the records")
def t25(R, recs):
    s = json.load(open(os.path.join(R, "release_summary.json")))
    cm = json.load(open(os.path.join(R, "coverage_map.json")))
    bad = []
    if s["questions"] != len(recs) or s["difficulty"] != dict(Counter(r["difficulty"] for r in recs)) or s["classes"] != dict(Counter(r["source_class"] for r in recs)):
        bad.append("release_summary counts")
    if s["numerical_variants"] != sum(1 for r in recs if r["numerical_variant"]):
        bad.append("release_summary numerical")
    for u in cm["units"]:
        ur = [r for r in recs if r["unit_number"] == u["unit"]]
        if u["count"] != len(ur) or u["question_ids"] != [r["id"] for r in ur] or u["classes"] != dict(Counter(r["source_class"] for r in ur)):
            bad.append(("coverage_map", u["unit"]))
    if Counter(r["difficulty"] for r in recs) != Counter({"Easy": 810, "Medium": 1215, "Difficult": 675}):
        bad.append("difficulty totals")
    return not bad, dict(problems=bad)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("release")
    ap.add_argument("--prev")
    ap.add_argument("--zip")
    ap.add_argument("--out")
    ap.add_argument("--quick", action="store_true")
    ar = ap.parse_args()
    R = os.path.abspath(ar.release)
    recs = json.load(open(glob.glob(os.path.join(R, "jee_main_maths_v*.json"))[0], encoding="utf-8"))
    for t in (t01, t02, t03, t04, t05, t06, t07, t08, t09, t10):
        t(R, recs)
    t11(R, recs, ar.quick)
    t12(R, recs); t13(R, recs)
    t14(R, recs, ar.prev)
    t15(R, recs, ar.quick); t16(R, recs, ar.quick)
    t17(R, recs); t18(R, recs); t19(R, recs); t20(R, recs)
    t21(R, recs, ar.zip)
    t22(R, recs); t23(R, recs); t24(R, recs); t25(R, recs)
    summary = dict(release=os.path.basename(R), run_at=time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()), tests=len(RESULTS),
                   passed=sum(r["passed"] for r in RESULTS), failed=[r["test"] for r in RESULTS if not r["passed"]], results=RESULTS)
    if ar.out:
        json.dump(summary, open(ar.out, "w"), indent=1, ensure_ascii=False)
    print(f"{summary['passed']}/{summary['tests']} passed")
    sys.exit(0 if not summary["failed"] else 1)


if __name__ == "__main__":
    main()
