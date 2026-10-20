# -*- coding: utf-8 -*-
"""Self-check harness for a drafting file.

usage: python3 harness.py drafts/u02_a.py --easy 17 --medium 25 --difficult 13 [--json out.json]

Runs every machine check, compares with the keyed value, confirms distractor values differ
from the key, scans style, renders all LaTeX with KaTeX, and prints a report.
Exit code 0 only when nothing blocking was found.
"""
import argparse, importlib.util, json, os, random, re, subprocess, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sympy as sp  # noqa: E402


def load(path):
    import qlib
    qlib.QUESTIONS.clear()
    spec = importlib.util.spec_from_file_location("draftmod_" + os.path.basename(path).replace('.', '_'), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return list(qlib.QUESTIONS)


def _num_equal(a, b):
    a = sp.sympify(a); b = sp.sympify(b)
    syms = sorted((a.free_symbols | b.free_symbols), key=str)
    if not syms:
        try:
            if sp.simplify(a - b) == 0:
                return True
        except Exception:
            pass
        try:
            va, vb = complex(sp.N(a, 30)), complex(sp.N(b, 30))
            return abs(va - vb) <= 1e-9 * max(1.0, abs(va), abs(vb))
        except Exception:
            return False
    try:
        if sp.simplify(a - b) == 0:
            return True
    except Exception:
        pass
    rnd = random.Random(7)
    for _ in range(6):
        sub = {s: sp.Rational(rnd.randint(11, 97), rnd.randint(7, 23)) for s in syms}
        try:
            va, vb = complex(sp.N(a.subs(sub), 30)), complex(sp.N(b.subs(sub), 30))
        except Exception:
            return False
        if abs(va - vb) > 1e-8 * max(1.0, abs(va), abs(vb)):
            return False
    return True


def equal(a, b):
    if isinstance(a, bool) or isinstance(b, bool):
        return bool(a) == bool(b) and type(a) == type(b)
    if isinstance(a, sp.MatrixBase) or isinstance(b, sp.MatrixBase):
        try:
            A, B = sp.Matrix(a), sp.Matrix(b)
        except Exception:
            return False
        return A.shape == B.shape and all(_num_equal(x, y) for x, y in zip(A, B))
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(equal(x, y) for x, y in zip(a, b))
    if isinstance(a, sp.Set) or isinstance(b, sp.Set):
        if not (isinstance(a, sp.Set) and isinstance(b, sp.Set)):
            return False
        if a == b:
            return True
        try:
            if sp.simplify(sp.Complement(a, b)) == sp.S.EmptySet and sp.simplify(sp.Complement(b, a)) == sp.S.EmptySet:
                return True
        except Exception:
            pass
        if isinstance(a, sp.FiniteSet) and isinstance(b, sp.FiniteSet) and len(a) == len(b):
            la, lb = list(a), list(b)
            return all(any(_num_equal(x, y) for y in lb) for x in la) and all(any(_num_equal(y, x) for x in la) for y in lb)
        return False
    try:
        return _num_equal(a, b)
    except Exception:
        return False


DASHES = ['\u2014', '\u2013', '\u2012', '\u2015']
LEAK = re.compile(r"\b(obtained by|comes from|incorrect(ly)?|wrong(ly)?|mistak|forgot|forgetting|error|instead of|confus)", re.I)
BANNED = re.compile(r"(none of (these|the above)|all of (these|the above)|both \(?[ab]\)? and|cannot be determined)", re.I)
LETTER_REF = re.compile(r"(option\s*\(?[ABCD]\)?\b|\([ABCD]\)|\b[ABCD]\s+is\s+correct)")


def run(path, quotas=None, json_out=None):
    qs = load(path)
    blocking, advisory = [], []
    ids = [x["local_id"] for x in qs]
    for k, v in Counter(ids).items():
        if v > 1:
            blocking.append((k, "duplicate local_id"))
    stems = Counter(re.sub(r"\s+", " ", x["question"].strip().lower()) for x in qs)
    for k, v in stems.items():
        if v > 1:
            blocking.append((k[:60], "duplicate stem"))
    machine = 0
    for x in qs:
        qid = x["local_id"]
        texts = {"question": x["question"], "correct": x["correct"], "explanation": x["explanation"]}
        for i, d in enumerate(x["distractors"]):
            texts[f"distractor{i+1}"] = d["text"]
        if x["numerical"]:
            texts["numerical"] = x["numerical"]["question"]
        aux = {"misconception": x["common_misconception"], "difficulty_reason": x["difficulty_reason"]}
        for i, d in enumerate(x["distractors"]):
            aux[f"rationale{i+1}"] = d["rationale"]
        for f, t in list(texts.items()) + list(aux.items()):
            if any((ord(c) < 32 and c != "\n") or ord(c) == 127 for c in t):
                blocking.append((qid, f"control character in {f} (use a raw string r'...')"))
            if "mathrm{does" in t:
                blocking.append((qid, f"words typeset in math mode in {f}"))
        for f, t in texts.items():
            if any(dch in t for dch in DASHES):
                blocking.append((qid, f"dash character in {f}"))
            if any(ord(c) > 126 for c in t):
                blocking.append((qid, f"non-ASCII in {f}: {[c for c in t if ord(c) > 126][:5]}"))
            if "$$" in t:
                blocking.append((qid, f"display math $$ in {f}"))
        for f in ["correct", "distractor1", "distractor2", "distractor3"]:
            if LEAK.search(texts[f]):
                blocking.append((qid, f"possible leakage wording in option text ({f})"))
            if BANNED.search(texts[f]):
                blocking.append((qid, f"banned option phrasing ({f})"))
        if LETTER_REF.search(x["explanation"]):
            blocking.append((qid, "explanation names an option letter"))
        if re.search(r"\b(?:point|matrix|set|statement|body)\s+[ABCD]\b", x["question"]):
            advisory.append((qid, "stem labels something A/B/C/D; prefer P,Q,R,S"))
        if x["check"] is not None:
            machine += 1
            import signal
            def _to(*a): raise TimeoutError("check exceeded 60 s")
            signal.signal(signal.SIGALRM, _to); signal.alarm(60)
            try:
                got = x["check"]()
                signal.alarm(0)
            except Exception as e:
                signal.alarm(0)
                blocking.append((qid, f"check() raised {type(e).__name__}: {e}"))
                continue
            vals = x["values"]
            if not equal(got, vals[0]):
                blocking.append((qid, f"MACHINE MISMATCH: check()={got!r} but keyed value={vals[0]!r}"))
            for j in (1, 2, 3):
                if equal(vals[j], vals[0]):
                    blocking.append((qid, f"distractor {j} has the same value as the key: {vals[j]!r}"))
            for j in range(1, 4):
                for k in range(j + 1, 4):
                    if equal(vals[j], vals[k]):
                        blocking.append((qid, f"distractors {j} and {k} have equal values"))
        elif x["question_type"] not in ("Direct concept MCQ", "Conceptual/application MCQ", "Statement-based MCQ", "Graph/diagram MCQ"):
            advisory.append((qid, "computational type without a machine check"))
        if x["numerical"]:
            if x["check"] is None:
                advisory.append((qid, "numerical alternate without a machine check"))
            else:
                try:
                    if not equal(sp.Integer(x["numerical"]["answer"]), x["values"][0]) and "Express" not in x["numerical"]["question"] and "multipl" not in x["numerical"]["question"]:
                        advisory.append((qid, "numerical answer differs from MCQ value; confirm the integer question asks for a scaled/related quantity"))
                except Exception:
                    pass
        if x["flags"]:
            advisory.append((qid, "AUTHOR FLAG: " + x["flags"]))
        lens = [len(x["correct"])] + [len(d["text"]) for d in x["distractors"]]
        if lens[0] > 1.6 * max(lens[1:]) and lens[0] > 25:
            advisory.append((qid, "correct option much longer than distractors"))
    # KaTeX
    items = []
    for x in qs:
        for f in ("question", "correct", "explanation"):
            items.append({"id": x["local_id"], "field": f, "text": x[f]})
        for i, d in enumerate(x["distractors"]):
            items.append({"id": x["local_id"], "field": f"d{i+1}", "text": d["text"]})
        if x["numerical"]:
            items.append({"id": x["local_id"], "field": "numerical", "text": x["numerical"]["question"]})
        for f in ("common_misconception", "difficulty_reason"):
            items.append({"id": x["local_id"], "field": f, "text": x[f]})
        for i, d in enumerate(x["distractors"]):
            items.append({"id": x["local_id"], "field": f"rationale{i+1}", "text": d["rationale"]})
    r = subprocess.run(["node", os.path.join(HERE, "katex_check.js")], input=json.dumps(items), capture_output=True, text=True)
    try:
        for f in json.loads(r.stdout):
            blocking.append((f["id"], f"KaTeX {f['field']}: {f['error']} :: {f.get('math','')}"))
    except Exception:
        blocking.append(("katex", "renderer failed: " + r.stderr[:300]))
    dc = Counter(x["difficulty"] for x in qs)
    if quotas:
        for k, v in quotas.items():
            if dc.get(k, 0) != v:
                blocking.append(("counts", f"{k}: have {dc.get(k,0)} need {v}"))
    fam = Counter(x["concept_family"] for x in qs)
    for k, v in fam.items():
        if v > 3:
            advisory.append((k, f"family has {v} members (max 3)"))
    print(f"FILE {path}")
    print(f"questions={len(qs)} difficulty={dict(dc)} machine_checked={machine} families={len(fam)} "
          f"numerical_alternates={sum(1 for x in qs if x['numerical'])}")
    print(f"qtypes={dict(Counter(x['question_type'] for x in qs))}")
    print(f"BLOCKING ({len(blocking)}):")
    for b in blocking:
        print("  ", b)
    print(f"ADVISORY ({len(advisory)}):")
    for a in advisory:
        print("  ", a)
    if json_out:
        json.dump({"blocking": blocking, "advisory": advisory, "count": len(qs)}, open(json_out, "w"), indent=1, default=str)
    return not blocking


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--easy", type=int)
    ap.add_argument("--medium", type=int)
    ap.add_argument("--difficult", type=int)
    ap.add_argument("--json")
    a = ap.parse_args()
    quotas = None
    if a.easy is not None:
        quotas = {"Easy": a.easy, "Medium": a.medium, "Difficult": a.difficult}
    ok = run(a.path, quotas, a.json)
    sys.exit(0 if ok else 1)
