# -*- coding: utf-8 -*-
"""Self-check harness for a VARC drafting file.

RC:  python3 harness.py drafts/r01_a.py --sets 8 --q5 2 --easy 10 --medium 15 --difficult 9
VA:  python3 harness.py drafts/v01_a.py --items 25 --easy 7 --medium 11 --difficult 7 [--five 8]

Checks structure, counts, word counts, readability, option-length giveaways, house style,
meta commentary and n-gram overlap with every other drafting file. Exit 0 only if no BLOCKING.
"""
import argparse, glob, importlib.util, json, os, re, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def load(path):
    import vlib
    vlib.SETS.clear(); vlib.QUESTIONS.clear()
    spec = importlib.util.spec_from_file_location("vdraft_" + re.sub(r"\W", "_", os.path.basename(path)), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return list(vlib.SETS), list(vlib.QUESTIONS)


WORD = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")


def words(t):
    return WORD.findall(t)


def syllables(w):
    w = w.lower()
    if len(w) <= 3:
        return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w)
    w = re.sub(r"^y", "", w)
    return max(1, len(re.findall(r"[aeiouy]{1,2}", w)))


def fk_grade(text):
    sents = max(1, len(re.findall(r"[.!?]+(?:\s|$)", text)))
    ws = words(text)
    if not ws:
        return 0.0
    syl = sum(syllables(w) for w in ws)
    return 0.39 * len(ws) / sents + 11.8 * syl / len(ws) - 15.59


def shingles(text, n=8):
    ws = [w.lower() for w in words(text)]
    return set(tuple(ws[i:i + n]) for i in range(len(ws) - n + 1))


DASHES = ['—', '–', '‒', '―']
META = re.compile(r"\b(reviewer|errata|erratum|this item|question bank|this bank|note to (the )?(editor|reviewer)|as revised|was corrected|blind solver|audit(or)? (found|note))\b", re.I)
LETTER_REF = re.compile(r"(\boption\s*\(?[ABCD]\)?(?![a-z])|\([ABCD]\)|\b[ABCD]\s+is\s+(correct|wrong|incorrect)|\bchoice\s+[ABCD]\b)")
BANNED = re.compile(r"(none of (these|the above)|all of (these|the above)|both \(?[abcd1-4]\)? and \(?[abcd1-4]\)?|cannot be determined)", re.I)


def item_texts(x):
    """(field, text, is_student_facing) for every text field of a question."""
    out = [("explanation", x["explanation"], True), ("misconception", x["common_misconception"], False),
           ("difficulty_reason", x["difficulty_reason"], False)]
    k = x["kind"]
    if k in ("RC", "PS"):
        out.append(("question" if k == "RC" else "paragraph", x["question"] if k == "RC" else x["paragraph"], True))
        out.append(("correct", x["correct"], True))
        for i, d in enumerate(x["distractors"]):
            out += [(f"d{i+1}", d["text"], True), (f"why{i+1}", d["rationale"], True)]
    if k in ("PJ", "OOO"):
        for i, s in enumerate(x["sentences_original"]):
            out.append((f"s{i+1}", s, True))
        for i, t in enumerate(x["tita_traps"]):
            out.append((f"trap{i+1}", t["rationale"], True))
    if k == "SP":
        for i, s in enumerate(x["sentences"]):
            out.append((f"s{i+1}", s, True))
        out.append(("missing", x["missing"], True))
        for g, r in x["gap_reasons"].items():
            out.append((f"gap{g}", r, True))
    return out


def style(qid, field, t, blocking, advisory, student=True):
    if any((ord(c) < 32 and c != "\n") or ord(c) == 127 for c in t):
        blocking.append((qid, f"control character in {field}"))
    if any(d in t for d in DASHES):
        blocking.append((qid, f"dash character in {field}"))
    bad = [c for c in t if ord(c) > 126]
    if bad:
        blocking.append((qid, f"non-ASCII in {field}: {bad[:5]}"))
    if re.search(r"(?<![A-Za-z])--(?![A-Za-z])|\s-\s", t):
        blocking.append((qid, f"hyphen or double hyphen used as a dash in {field}"))
    if "[[" in t or "]]" in t:
        blocking.append((qid, f"unresolved placeholder in {field}"))
    if META.search(t):
        blocking.append((qid, f"meta commentary in {field}: {META.search(t).group(0)!r}"))
    if field in ("explanation",) or field.startswith("why") or field.startswith("trap") or field.startswith("gap"):
        if LETTER_REF.search(t):
            blocking.append((qid, f"{field} names an option letter: {LETTER_REF.search(t).group(0)!r}"))
    if re.search(r"\s{2,}", t.strip()):
        advisory.append((qid, f"double space in {field}"))


def corpus_except(path):
    """Shingles of every other drafting file (passages, paragraphs, sentence sets)."""
    out = {}
    for f in sorted(glob.glob(os.path.join(HERE, "drafts", "*.py"))):
        if os.path.abspath(f) == os.path.abspath(path) or os.path.basename(f).startswith("_"):
            continue
        cache = f + ".shingles.json"
        try:
            if os.path.exists(cache) and os.path.getmtime(cache) >= os.path.getmtime(f):
                d = json.load(open(cache))
            else:
                S, Q = load(f)
                d = {}
                for s in S:
                    d[s["set_id"]] = " ".join(s["paragraphs"])
                for x in Q:
                    if x["kind"] == "PS":
                        d[x["local_id"]] = x["paragraph"]
                    elif x["kind"] in ("PJ", "OOO"):
                        d[x["local_id"]] = " ".join(x["sentences_original"])
                    elif x["kind"] == "SP":
                        d[x["local_id"]] = " ".join(x["sentences"] + [x["missing"]])
                json.dump(d, open(cache, "w"))
        except Exception:
            continue
        for k, t in d.items():
            out[k] = shingles(t)
    return out


def run(path, a, json_out=None):
    S, Q = load(path)
    blocking, advisory = [], []
    kinds = Counter(x["kind"] for x in Q)
    ids = [x["local_id"] for x in Q]
    for k, v in Counter(ids).items():
        if v > 1:
            blocking.append((k, "duplicate local_id"))
    texts_for_overlap = {}
    # ---------------- passages
    by_set = defaultdict(list)
    for x in Q:
        if x["kind"] == "RC":
            by_set[x["set_id"]].append(x)
    fk_list = []
    for s in S:
        sid = s["set_id"]
        body = " ".join(s["paragraphs"])
        texts_for_overlap[sid] = body
        for i, p in enumerate(s["paragraphs"]):
            style(sid, f"paragraph{i+1}", p, blocking, advisory)
        style(sid, "subtopic", s["subtopic"], blocking, advisory)
        wc = len(words(body))
        nq = len(by_set[sid])
        fk = fk_grade(body); fk_list.append(fk)
        lo, hi, blo, bhi = (380, 600, 350, 650) if nq == 4 else (550, 750, 520, 800)
        if not (blo <= wc <= bhi):
            blocking.append((sid, f"passage has {wc} words; a {nq}-question passage needs {lo} to {hi}"))
        elif not (lo <= wc <= hi):
            advisory.append((sid, f"passage has {wc} words (target {lo} to {hi})"))
        if fk < 10.5:
            advisory.append((sid, f"readability grade {fk:.1f} is low for CAT (aim 12 to 17)"))
        if fk > 19:
            advisory.append((sid, f"readability grade {fk:.1f} is very high; check sentence length"))
        if nq not in (4, 5):
            blocking.append((sid, f"passage has {nq} questions (need 4 or 5)"))
        nums = sorted(int(x["local_id"].rsplit("-", 1)[1]) for x in by_set[sid])
        if nums != list(range(1, nq + 1)):
            blocking.append((sid, f"question numbers {nums} are not 1..{nq}"))
        qt = Counter(x["question_type"] for x in by_set[sid])
        if qt and max(qt.values()) > 2:
            blocking.append((sid, f"question type used more than twice in one passage: {dict(qt)}"))
        if len(qt) < min(3, nq):
            advisory.append((sid, f"only {len(qt)} distinct question types"))
        if re.search(r'"[^"]{12,}"\s*(,|\.)?\s*(said|wrote|argued|observed)\s+[A-Z][a-z]+', body):
            advisory.append((sid, "passage seems to quote a named person; never invent quotations for real people"))
        if s["flags"]:
            advisory.append((sid, "AUTHOR FLAG: " + s["flags"]))
    fam = Counter(s["family"] for s in S)
    for k, v in fam.items():
        if v > 1:
            blocking.append((k, "two passages share a family (each passage needs its own subject)"))
    # ---------------- questions
    key_longest = key_shortest = n_mcq = 0
    sp_keys = Counter()
    for x in Q:
        qid = x["local_id"]
        for f, t, stu in item_texts(x):
            style(qid, f, t, blocking, advisory, stu)
        if len(x["explanation"]) < 80:
            blocking.append((qid, "explanation too short (needs a real justification)"))
        k = x["kind"]
        if k in ("RC", "PS"):
            opts = [x["correct"]] + [d["text"] for d in x["distractors"]]
            if len(set(o.lower() for o in opts)) < 4:
                blocking.append((qid, "options not distinct"))
            for o in opts:
                if BANNED.search(o):
                    blocking.append((qid, f"banned option phrasing: {o[:40]!r}"))
            lens = [len(words(o)) for o in opts]
            n_mcq += 1
            if lens[0] > max(lens[1:]):
                key_longest += 1
            if lens[0] < min(lens[1:]):
                key_shortest += 1
            if lens[0] > 1.5 * max(lens[1:]) and lens[0] >= 12:
                advisory.append((qid, f"key ({lens[0]} words) much longer than every distractor {lens[1:]}"))
            if min(lens) * 2.5 < max(lens) and max(lens) > 15:
                advisory.append((qid, f"option lengths very uneven {lens}"))
        if k == "RC":
            if x["question_type"] == "Except / not supported" and not re.search(r"\b(EXCEPT|NOT|LEAST)\b", x["question"]):
                blocking.append((qid, "EXCEPT/NOT question must capitalise EXCEPT, NOT or LEAST in the stem"))
            for o in [x["correct"]] + [d["text"] for d in x["distractors"]]:
                if not (2 <= len(words(o)) <= 55):
                    advisory.append((qid, f"RC option length {len(words(o))} words"))
        if k == "PS":
            wc = len(words(x["paragraph"]))
            texts_for_overlap[qid] = x["paragraph"]
            if not (70 <= wc <= 230):
                blocking.append((qid, f"para-summary paragraph has {wc} words (need 90 to 200)"))
            elif not (90 <= wc <= 200):
                advisory.append((qid, f"para-summary paragraph has {wc} words (target 90 to 200)"))
            for o in [x["correct"]] + [d["text"] for d in x["distractors"]]:
                if not (10 <= len(words(o)) <= 60):
                    blocking.append((qid, f"summary option has {len(words(o))} words (need 12 to 55)"))
        if k in ("PJ", "OOO"):
            texts_for_overlap[qid] = " ".join(x["sentences_original"])
            for i, s in enumerate(x["sentences_original"]):
                if not (7 <= len(words(s)) <= 60):
                    blocking.append((qid, f"sentence {i+1} has {len(words(s))} words (need 8 to 55)"))
                if not re.search(r"[.?!]['\"]?$", s):
                    blocking.append((qid, f"sentence {i+1} does not end with terminal punctuation"))
            for t in x["tita_traps"]:
                if t["value"] == x["tita_answer"]:
                    blocking.append((qid, "trap equals the key"))
            if k == "PJ" and not x["tita_traps"]:
                advisory.append((qid, "no traps given (give the most tempting wrong order)"))
            if re.search(r"[Ss]entences \[\[\d\]\] to \[\[\d\]\]", x.get("raw_explanation", "")):
                blocking.append((qid, "sentence range like [[1]] to [[4]] breaks after shuffling; list the sentences"))
            if re.search(r"\bsentence\s+[1-5]\b", x.get("raw_explanation", ""), re.I):
                blocking.append((qid, "explanation uses a raw sentence number; use [[n]] placeholders"))
        if k == "SP":
            texts_for_overlap[qid] = " ".join(x["sentences"] + [x["missing"]])
            sp_keys[x["key_number"]] += 1
            wc = len(words(" ".join(x["sentences"])))
            if not (100 <= wc <= 320):
                blocking.append((qid, f"sentence-placement paragraph has {wc} words (need 110 to 300)"))
            if not (8 <= len(words(x["missing"])) <= 50):
                blocking.append((qid, "missing sentence length out of range"))
            if not re.search(r"gap \([1-4]\)", x["explanation"]):
                advisory.append((qid, "explanation should name the true gap as gap (n)"))
        if x.get("flags"):
            advisory.append((qid, "AUTHOR FLAG: " + x["flags"]))
    if n_mcq >= 8:
        if key_longest > 0.4 * n_mcq:
            blocking.append(("options", f"the key is the longest option in {key_longest}/{n_mcq} MCQs (max 40%)"))
        if key_shortest > 0.35 * n_mcq:
            blocking.append(("options", f"the key is the shortest option in {key_shortest}/{n_mcq} MCQs (max 35%)"))
    if sp_keys:
        n = sum(sp_keys.values())
        for g in (1, 2, 3, 4):
            if abs(sp_keys.get(g, 0) - n / 4) > 2:
                blocking.append(("keys", f"sentence-placement true gap is ({g}) in {sp_keys.get(g,0)}/{n} items; balance to about n/4"))
    vfam = Counter(x["family"] for x in Q if x["kind"] != "RC")
    for k2, v in vfam.items():
        if v > 3:
            blocking.append((k2, f"family has {v} members (max 3)"))
    # ---------------- counts
    dc = Counter(x["difficulty"] for x in Q)
    if a.easy is not None:
        for lab, v in (("Easy", a.easy), ("Medium", a.medium), ("Difficult", a.difficult)):
            if dc.get(lab, 0) != v:
                blocking.append(("counts", f"{lab}: have {dc.get(lab,0)} need {v}"))
    if a.sets is not None:
        if len(S) != a.sets:
            blocking.append(("counts", f"passages: have {len(S)} need {a.sets}"))
        n5 = sum(1 for s in S if len(by_set[s["set_id"]]) == 5)
        if a.q5 is not None and n5 != a.q5:
            blocking.append(("counts", f"5-question passages: have {n5} need {a.q5}"))
        sd = Counter(s["difficulty"] for s in S)
        if a.sets >= 6 and (sd.get("Easy", 0) < 1 or sd.get("Difficult", 0) < 1):
            blocking.append(("counts", f"passage difficulty spread {dict(sd)}: need at least one Easy and one Difficult passage"))
    if a.items is not None and len(Q) != a.items:
        blocking.append(("counts", f"items: have {len(Q)} need {a.items}"))
    if a.five is not None:
        n5 = sum(1 for x in Q if x["kind"] == "PJ" and len(x["sentences_original"]) == 5)
        if n5 != a.five:
            blocking.append(("counts", f"5-sentence jumbles: have {n5} need {a.five}"))
    # ---------------- overlap
    corpus = corpus_except(path)
    mine = {k: shingles(t) for k, t in texts_for_overlap.items()}
    keys = list(mine)
    for i, k1 in enumerate(keys):
        others = [(k2, mine[k2]) for k2 in keys[i + 1:]] + list(corpus.items())
        for k2, sh2 in others:
            common = mine[k1] & sh2
            if not common:
                continue
            frac = len(common) / max(1, min(len(mine[k1]), len(sh2)))
            if frac > 0.04 or len(common) >= 6:
                blocking.append((k1, f"text overlaps {k2}: {len(common)} shared 8-word runs (rewrite)"))
            elif len(common) >= 2:
                advisory.append((k1, f"shares {len(common)} 8-word runs with {k2}: {' '.join(next(iter(common)))!r}"))
    print(f"FILE {path}")
    print(f"kinds={dict(kinds)} passages={len(S)} questions={len(Q)} difficulty={dict(dc)}")
    if S:
        print(f"passage words={[len(words(' '.join(s['paragraphs']))) for s in S]} grade={[round(f,1) for f in fk_list]}")
        print(f"passage difficulty={dict(Counter(s['difficulty'] for s in S))} rc qtypes={dict(Counter(x['question_type'] for x in Q))}")
    if n_mcq:
        print(f"key longest {key_longest}/{n_mcq}, key shortest {key_shortest}/{n_mcq}")
    if sp_keys:
        print(f"sentence-placement true gaps {dict(sorted(sp_keys.items()))}")
    print(f"BLOCKING ({len(blocking)}):")
    for b in blocking:
        print("  ", b)
    print(f"ADVISORY ({len(advisory)}):")
    for x in advisory:
        print("  ", x)
    if json_out:
        json.dump({"blocking": blocking, "advisory": advisory}, open(json_out, "w"), indent=1)
    return not blocking


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    for o in ("easy", "medium", "difficult", "sets", "q5", "items", "five"):
        ap.add_argument("--" + o, type=int)
    ap.add_argument("--json")
    a = ap.parse_args()
    sys.exit(0 if run(a.path, a, a.json) else 1)
