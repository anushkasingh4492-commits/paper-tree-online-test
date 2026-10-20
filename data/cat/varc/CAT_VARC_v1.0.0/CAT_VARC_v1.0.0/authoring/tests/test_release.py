# -*- coding: utf-8 -*-
"""Automated tests for the CAT VARC release. Run from the authoring folder: python3 tests/test_release.py"""
import glob, json, os, re, subprocess, sys
AUTH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REL = os.path.dirname(AUTH) if os.path.basename(AUTH) == "authoring" else os.path.join(AUTH, "release", "CAT_VARC_v1.0.0")
sys.path.insert(0, AUTH)
BANK = json.load(open(sorted(glob.glob(os.path.join(REL, "cat_varc_v*.json")))[0]))
R = []


def test(fn):
    try:
        fn(); R.append((fn.__name__, "PASS", ""))
    except AssertionError as e:
        R.append((fn.__name__, "FAIL", str(e)[:300]))
    except Exception as e:
        R.append((fn.__name__, "ERROR", f"{type(e).__name__}: {e}"[:300]))


@test
def schema_valid():
    import jsonschema
    jsonschema.validate(BANK, json.load(open(os.path.join(REL, "question_bank_schema.json"))))


@test
def harness_all_files():
    plan = json.load(open(os.path.join(AUTH, "plan.json")))
    bad = []
    for p in plan:
        cmd = p["cmd"].split("&& ")[1].split()
        r = subprocess.run(cmd, cwd=AUTH, capture_output=True, text=True)
        if r.returncode:
            bad.append(p["tag"])
    assert not bad, bad


@test
def rebuild_identical():
    r = subprocess.run([sys.executable, "build.py"], cwd=AUTH, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-300:]
    b = json.load(open(os.path.join(AUTH, "build", "bank.json")))
    assert b["questions"] == BANK["questions"] and b["sets"] == BANK["sets"]


@test
def no_edits_after_last_blind_round():
    snap = os.path.join(AUTH, "verify", "drafts_a1")
    if not os.path.exists(snap):
        snap = os.path.join(AUTH, "verify", "snapshot_after_audit")
    r = subprocess.run([sys.executable, "changed.py", snap, "drafts", "/tmp/_ch.json"], cwd=AUTH, capture_output=True, text=True)
    assert r.returncode == 0 and r.stdout.startswith("0 changed"), r.stdout[:200] + r.stderr[-200:]


@test
def every_item_agreed_in_latest_round():
    s1 = json.load(open(os.path.join(AUTH, "verify", "blind", "b1_score.json")))
    s2 = json.load(open(os.path.join(AUTH, "verify", "blind", "b2_score.json")))
    ch = set(json.load(open(os.path.join(AUTH, "verify", "changed_r2.json"))))
    adjudicated = {"V01-A-006"}  # solver typing slip; its own working matched the key (see evidence/blind_resolve_results.json)
    bad1 = {d["id"] for d in s1["disagreements"]} - ch - adjudicated
    assert not bad1, bad1
    assert not s2["disagreements"] and not s2["missing"] and s2["items"] == len(ch)


@test
def verify_release_passes():
    r = subprocess.run([sys.executable, "verify_release.py"], cwd=REL, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout[-400:]


@test
def books_contain_every_item():
    for c in range(1, 13):
        for kind in ("Student", "Teacher"):
            h = open(os.path.join(REL, "books", f"Chapter_{c:02d}_{kind}.html"), encoding="utf-8").read()
            ids = [q["id"] for q in BANK["questions"] if q["chapter_number"] == c]
            missing = [i for i in ids if i not in h]
            assert not missing, (c, kind, missing[:3])
            if kind == "Student":
                assert "Answer and explanation" not in h and "Why not" not in h, (c, "student book leaks answers")


@test
def no_reviewer_words_student_facing():
    pat = re.compile(r"\b(distractors?|reviewer|erratum|errata|blind solver|this item)\b|\bthe key\b(?! (distinction|point|term|word|idea|claim|step|question|sentence))", re.I)
    for q in BANK["questions"]:
        txt = " ".join([q["explanation"], q["common_misconception"]] + list(q["option_rationales"].values()) +
                       [w["reason"] for w in q["tita_common_wrong_entries"]])
        m = pat.search(txt)
        assert not m, (q["id"], m.group(0))


@test
def sample_paper_matches_generator():
    p = json.load(open(os.path.join(REL, "sample_paper.json")))
    assert p["seed"] == 42 and len(p["questions"]) == 24
    h = open(os.path.join(REL, "Sample_Paper.html"), encoding="utf-8").read()
    assert "Question 24" in h and "Answer and explanation" not in h


for n, r, m in R:
    print(f"{r:5} {n}" + (f" :: {m}" if m else ""))
out = os.path.join(REL, "evidence", "test_results.json")
json.dump(R, open(out, "w"), indent=1)
sys.exit(0 if all(r == "PASS" for _, r, _ in R) else 1)
