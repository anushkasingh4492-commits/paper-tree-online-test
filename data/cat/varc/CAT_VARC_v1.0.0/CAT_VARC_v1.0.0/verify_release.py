# -*- coding: utf-8 -*-
"""Verify the CAT VARC release (Python standard library only).

python verify_release.py          run from the release folder
Checks structure, ids, set membership, answer formats, key balance, checksums and the paper
generator's guarantees for seeds 1 to 200. Prints PASS/FAIL per check; exit code 0 if all pass.
"""
import glob, hashlib, json, os, re, subprocess, sys, tempfile
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
BANK_PATH = sorted(glob.glob(os.path.join(HERE, "cat_varc_v*.json")))[0]
B = json.load(open(BANK_PATH, encoding="utf-8"))
Q, S = B["questions"], B["sets"]
QI = {q["id"]: q for q in Q}
results = []


def check(name):
    def deco(fn):
        try:
            fn(); results.append((name, "PASS", ""))
        except AssertionError as e:
            results.append((name, "FAIL", str(e)[:300]))
        return fn
    return deco


@check("counts")
def _():
    assert len(S) == 400 and len(Q) == 2800, (len(S), len(Q))
    c = Counter(q["question_type"] for q in Q if not q["set_id"])
    assert c == {"Para jumble": 350, "Para summary": 350, "Odd sentence out": 250, "Sentence placement": 150}, c
    assert Counter(q["difficulty"] for q in Q) == {"Easy": 840, "Medium": 1260, "Difficult": 700}


@check("unique ids")
def _():
    assert len(QI) == len(Q) and len({s["set_id"] for s in S}) == len(S)


@check("set membership")
def _():
    for s in S:
        assert s["question_count"] == len(s["question_ids"]) in (4, 5), s["set_id"]
        for i in s["question_ids"]:
            assert QI[i]["set_id"] == s["set_id"], i
    assert sum(len(s["question_ids"]) for s in S) == sum(1 for q in Q if q["set_id"])


@check("answer formats")
def _():
    for q in Q:
        if q["answer_format"] == "MCQ":
            assert set(q["options"]) == set("ABCD") and q["correct_option"] in "ABCD" and q["tita_answer"] is None, q["id"]
            assert len(set(v.strip().lower() for v in q["options"].values())) == 4, q["id"]
            if q["question_type"] != "Sentence placement":
                assert set(q["option_rationales"]) == set("ABCD") - {q["correct_option"]}, q["id"]
        else:
            assert q["options"] is None and q["correct_option"] is None, q["id"]
            n = len(q["sentences"])
            if q["question_type"] == "Para jumble":
                assert n in (4, 5) and sorted(q["tita_answer"]) == [str(i) for i in range(1, n + 1)], q["id"]
                assert q["tita_answer"] != "".join(str(i) for i in range(1, n + 1)), q["id"]
            else:
                assert n == 5 and re.fullmatch("[1-5]", q["tita_answer"]), q["id"]


@check("house style")
def _():
    bad = re.compile("[‒-―]|(?<![A-Za-z])--(?![A-Za-z])")
    for q in Q:
        for f in ("question", "explanation"):
            assert not bad.search(q[f]) and all(ord(c) < 127 or c == "\n" for c in q[f]), (q["id"], f)
    for s in S:
        for p in s["paragraphs"]:
            assert not bad.search(p) and all(ord(c) < 127 for c in p), s["set_id"]


@check("key balance")
def _():
    for ch in range(1, 13):
        items = [q for q in Q if q["chapter_number"] == ch and q["correct_option"]]
        if not items:
            continue
        c = Counter(q["correct_option"] for q in items)
        assert max(c.values()) - min(c.values()) <= (1 if ch <= 10 else 6), (ch, c)
        if ch <= 10:
            seq = [q["correct_option"] for q in items]
            assert not any(seq[i] == seq[i + 1] == seq[i + 2] == seq[i + 3] for i in range(len(seq) - 3)), ch
    for s in S:
        c = Counter(QI[i]["correct_option"] for i in s["question_ids"])
        assert max(c.values()) <= 2, s["set_id"]


@check("generator seeds 1 to 200")
def _():
    gen = os.path.join(HERE, "generate_paper.py")
    with tempfile.TemporaryDirectory() as d:
        for seed in range(1, 201):
            out = os.path.join(d, "p")
            subprocess.run([sys.executable, gen, "--bank", BANK_PATH, "--seed", str(seed), "--output", out], check=True, capture_output=True)
            p = json.load(open(out + "_paper.json")); k = json.load(open(out + "_answer_key.json"))
            ids = p["questions"]
            assert len(ids) == 24 == len(set(ids)) == len(k), seed
            assert len(p["passages"]) == 4 and len({QI[i]["set_id"] for i in ids if QI[i]["set_id"]}) == 4, seed
            for sid in p["passages"]:
                s = next(x for x in S if x["set_id"] == sid)
                assert all(i in ids for i in s["question_ids"]), (seed, sid)
            assert len({next(x for x in S if x["set_id"] == sid)["chapter_number"] for sid in p["passages"]}) == 4, seed
            vt = Counter(QI[i]["question_type"] for i in ids if not QI[i]["set_id"])
            assert vt == {"Para jumble": 2, "Para summary": 3, "Odd sentence out": 2, "Sentence placement": 1}, (seed, vt)
            assert Counter(QI[i]["difficulty"] for i in ids) == {"Easy": 7, "Medium": 11, "Difficult": 6}, seed
            units = [next(x for x in S if x["set_id"] == sid) for sid in p["passages"]] + [QI[i] for i in ids if not QI[i]["set_id"]]
            fams = [f for u in units for f in u["family_dependencies"]]
            assert len(fams) == len(set(fams)), seed
            for row in k:
                q = QI[row["id"]]
                assert row["answer"] == (q["correct_option"] if q["answer_format"] == "MCQ" else q["tita_answer"])


@check("checksums")
def _():
    p = os.path.join(HERE, "checksums.sha256")
    assert os.path.exists(p), "checksums.sha256 missing"
    for line in open(p):
        h, f = line.rstrip("\n").split("  ", 1)
        assert hashlib.sha256(open(os.path.join(HERE, f), "rb").read()).hexdigest() == h, f


for n, r, m in results:
    print(f"{r:4}  {n}" + (f"  :: {m}" if m else ""))
sys.exit(0 if all(r == "PASS" for _, r, _ in results) else 1)
