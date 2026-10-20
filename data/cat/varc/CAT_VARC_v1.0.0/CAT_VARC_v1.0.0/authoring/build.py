# -*- coding: utf-8 -*-
"""Build canonical VARC records from the drafting files.

python3 build.py   ->  build/bank.json  {"sets": [...], "questions": [...]}
Assigns final ids, option letters (balanced per chapter, no run longer than 3, no letter more than
twice inside one RC passage), standard VA instructions, family_dependencies (subject alias groups)
and cleans reviewer vocabulary out of student-facing text.
"""
import glob, json, math, os, random, re, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from harness import load, words, fk_grade  # noqa: E402

CHAPTERS = [
    ("R01", 1, "Reading Comprehension", "Philosophy and Ethics"),
    ("R02", 2, "Reading Comprehension", "Psychology and Cognitive Science"),
    ("R03", 3, "Reading Comprehension", "Society, Anthropology and Culture"),
    ("R04", 4, "Reading Comprehension", "History and Politics"),
    ("R05", 5, "Reading Comprehension", "Economics, Business and Development"),
    ("R06", 6, "Reading Comprehension", "Science, Environment and Technology"),
    ("R07", 7, "Reading Comprehension", "Arts, Literature and Aesthetics"),
    ("R08", 8, "Reading Comprehension", "Language, Media and Communication"),
    ("V01", 9, "Verbal Ability", "Para Jumbles"),
    ("V02", 10, "Verbal Ability", "Para Summary"),
    ("V03", 11, "Verbal Ability", "Odd Sentence Out"),
    ("V04", 12, "Verbal Ability", "Sentence Placement"),
]
CH = {c[0]: c for c in CHAPTERS}
SECTION = "Verbal Ability and Reading Comprehension"

PJ_STEM = ("The {n} sentences (labelled {labs}) given below, when properly sequenced, form a coherent paragraph. "
           "Decide on the proper order of the sentences and key in the sequence of {n} numbers as your answer.")
OOO_STEM = ("Five jumbled sentences (labelled 1, 2, 3, 4 and 5), related to a topic, are given below. Four of them "
            "can be put together to form a coherent paragraph. Identify the odd sentence and key in its number as your answer.")
PS_STEM = ("The passage given below is followed by four summaries. Choose the option that best captures the essence of the passage.")
SP_STEM = ("There is a sentence that is missing in the paragraph below. Look at the paragraph and decide in which blank "
           "(1, 2, 3 or 4) the missing sentence can best fit.")

KEEP_AFTER = ("point|points|term|terms|word|words|phrase|idea|ideas|distinction|claim|step|difference|question|sentence|issue|"
              "test|feature|move|contrast|reason|evidence|role|clue|condition|assumption|premise|factor|insight|link|lock|signal|"
              "cue|marker|concept|fact|finding|lesson|figure|player|variable|mechanism|example|detail|task|skill|theme|word's")


def clean(t):
    """Remove reviewer vocabulary from student-facing text."""
    if not t:
        return t
    t = re.sub(r"\b([Tt])he key's\b", lambda m: m.group(1) + "he correct answer's", t)
    t = re.sub(r"\b([Tt])he key\b(?!\s+(?:%s)\b)(?!-)" % KEEP_AFTER, lambda m: m.group(1) + "he correct answer", t)
    t = re.sub(r"\b([Dd])istractors\b", lambda m: ("W" if m.group(1) == "D" else "w") + "rong options", t)
    t = re.sub(r"\b([Dd])istractor\b", lambda m: ("W" if m.group(1) == "D" else "w") + "rong option", t)
    t = re.sub(r"\bthe trap\b", "the tempting error", t)
    return t


def corpus():
    sets, qs = {}, []
    for f in sorted(glob.glob(os.path.join(HERE, "drafts", "[rv]*.py"))):
        S, Q = load(f)
        for s in S:
            sets[s["set_id"]] = s
        qs += Q
    return sets, qs


# ------------------------------------------------------------------ subject alias groups
def tfidf_groups(units, thresh=0.32):
    """units: list of (unit_id, chapter_group, text). Returns {unit_id: group_id or None}."""
    stop = set("the a an of and or to in is are was were be been it that this as for on with by from at which its their his her not but they them these those than more most can may also such into what who whom whose has have had do does did would could should will about between because so if then there here when where while one two all any some each other only very".split())
    docs = {}
    for uid, g, text in units:
        toks = [w.lower() for w in words(text) if len(w) > 3 and w.lower() not in stop]
        docs[uid] = Counter(toks)
    df = Counter()
    for c in docs.values():
        df.update(set(c))
    N = len(docs)
    vec = {}
    for uid, c in docs.items():
        v = {w: (1 + math.log(n)) * math.log(N / df[w]) for w, n in c.items() if df[w] > 1}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1
        vec[uid] = {w: x / norm for w, x in v.items()}
    ids = [u[0] for u in units]
    parent = {u: u for u in ids}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    inv = defaultdict(list)
    for uid, v in vec.items():
        for w, x in sorted(v.items(), key=lambda kv: -kv[1])[:25]:
            inv[w].append(uid)
    pairs = []
    seen = set()
    for w, lst in inv.items():
        if len(lst) > 60:
            continue
        for i in range(len(lst)):
            for j in range(i + 1, len(lst)):
                a, b = lst[i], lst[j]
                if (a, b) in seen:
                    continue
                seen.add((a, b))
                va, vb = vec[a], vec[b]
                if len(va) > len(vb):
                    va, vb = vb, va
                s = sum(x * vb.get(w2, 0) for w2, x in va.items())
                if s >= thresh:
                    pairs.append((a, b, round(s, 3)))
                    parent[find(a)] = find(b)
    groups = defaultdict(list)
    for u in ids:
        groups[find(u)].append(u)
    out = {}
    n = 0
    for root, mem in sorted(groups.items()):
        if len(mem) > 1:
            n += 1
            for m in mem:
                out[m] = f"SUBJ-{n:04d}"
    return out, pairs


# ------------------------------------------------------------------ letters
def assign_letters(items, seed, passage_of=None):
    """items in chapter order. Returns {local_id: letter}. Balanced counts, no run > 3,
    at most 2 of one letter inside one passage."""
    rnd = random.Random(seed)
    for attempt in range(200):
        counts = Counter(); out = {}; run = []; per_p = defaultdict(Counter); ok = True
        n = len(items); target = n / 4
        for x in items:
            p = passage_of(x) if passage_of else None
            cand = []
            for L in "ABCD":
                if len(run) >= 3 and all(r == L for r in run[-3:]):
                    continue
                if p and per_p[p][L] >= 2:
                    continue
                cand.append(L)
            if not cand:
                ok = False; break
            m = min(counts[L] for L in cand)
            best = [L for L in cand if counts[L] == m]
            L = rnd.choice(best)
            out[x["local_id"]] = L; counts[L] += 1; run.append(L)
            if p:
                per_p[p][L] += 1
        if ok and max(counts.values()) - min(counts.values()) <= 1:
            return out
    raise SystemExit("letter assignment failed")


def main():
    sets, qs = corpus()
    # chapter order and final ids
    by_ch = defaultdict(list)
    for x in qs:
        by_ch[x["local_id"][:3]].append(x)
    set_ids, set_order = {}, defaultdict(list)
    for sid in sorted(sets):
        c = sid[:3]; set_order[c].append(sid)
    for c, lst in set_order.items():
        for i, sid in enumerate(lst, 1):
            set_ids[sid] = f"CAT-VARC-P{CH[c][1]:02d}-{i:03d}"
    qid = {}
    for c, lst in by_ch.items():
        lst.sort(key=lambda x: x["local_id"])
        if c.startswith("R"):
            for x in lst:
                n = x["local_id"].rsplit("-", 1)[1]
                qid[x["local_id"]] = f"{set_ids[x['set_id']]}-Q{n}"
        else:
            for i, x in enumerate(lst, 1):
                qid[x["local_id"]] = f"CAT-VARC-C{CH[c][1]:02d}-{i:03d}"
    # subject alias groups across all units (RC passages and VA items)
    units = [(sid, "RC", " ".join(s["paragraphs"]) + " " + s["subtopic"]) for sid, s in sets.items()]
    for x in qs:
        if x["kind"] == "PS":
            units.append((x["local_id"], "VA", x["paragraph"] + " " + x["subtopic"]))
        elif x["kind"] in ("PJ", "OOO"):
            units.append((x["local_id"], "VA", " ".join(x["sentences_original"]) + " " + x["subtopic"]))
        elif x["kind"] == "SP":
            units.append((x["local_id"], "VA", " ".join(x["sentences"] + [x["missing"]]) + " " + x["subtopic"]))
    grp, pairs = tfidf_groups(units)
    # letters
    letters = {}
    for c, lst in by_ch.items():
        mcq = [x for x in lst if x["kind"] in ("RC", "PS")]
        if mcq:
            letters.update(assign_letters(mcq, seed=c, passage_of=(lambda x: x.get("set_id")) if c.startswith("R") else None))
    recs, srecs = [], []
    for c, num, area, chname in CHAPTERS:
        for sid in set_order.get(c, []):
            s = sets[sid]
            qids = [qid[x["local_id"]] for x in sorted(by_ch[c], key=lambda y: y["local_id"]) if x["set_id"] == sid]
            body = " ".join(s["paragraphs"])
            fam = [s["family"]] + ([grp[sid]] if sid in grp else [])
            srecs.append(dict(
                set_id=set_ids[sid], set_type="RC passage", section=SECTION, area=area, chapter_number=num, chapter=chname,
                topic=s["topic"], subtopic=s["subtopic"], paragraphs=s["paragraphs"], word_count=len(words(body)),
                readability_fk_grade=round(fk_grade(body), 1), difficulty=s["difficulty"], difficulty_reason=clean(s["difficulty_reason"]),
                question_ids=qids, question_count=len(qids), exam_tags=s["exams"], concept_family=s["family"],
                family_dependencies=fam, generator_eligible=True,
                provenance=dict(local_id=sid, batch=sid[:5], original=True), human_subject_expert_reviewed=False))
        for x in sorted(by_ch[c], key=lambda y: y["local_id"]):
            k = x["kind"]
            r = dict(id=qid[x["local_id"]], section=SECTION, area=area, chapter_number=num, chapter=chname,
                     topic=x["topic"], subtopic=x.get("subtopic") or x["topic"], question_type=x["question_type"],
                     standard="CAT", exam_tags=x["exams"], set_id=set_ids.get(x.get("set_id")), answer_format=x["answer_format"])
            if k in ("RC", "PS"):
                L = letters[x["local_id"]]
                others = [d for d in x["distractors"]]
                random.Random(x["local_id"]).shuffle(others)
                opts, rat = {}, {}
                rest = [l for l in "ABCD" if l != L]
                opts[L] = x["correct"]
                for l, d in zip(rest, others):
                    opts[l] = d["text"]; rat[l] = clean(d["rationale"])
                opts = {l: opts[l] for l in "ABCD"}; rat = {l: rat[l] for l in sorted(rat)}
                if k == "RC":
                    r.update(question=x["question"], instructions=None)
                else:
                    r.update(instructions=PS_STEM, passage_text=x["paragraph"], question=PS_STEM + "\n\n" + x["paragraph"])
                r.update(options=opts, correct_option=L, tita_answer=None, correct_answer=f"({L}) {x['correct']}",
                         option_rationales=rat, tita_common_wrong_entries=[])
            elif k in ("PJ", "OOO"):
                n = len(x["printed"])
                stem = PJ_STEM.format(n="four" if n == 4 else "five", labs="1, 2, 3 and 4" if n == 4 else "1, 2, 3, 4 and 5") if k == "PJ" else OOO_STEM
                sents = [dict(label=str(i + 1), text=t) for i, t in enumerate(x["printed"])]
                r.update(instructions=stem, sentences=sents,
                         question=stem + "\n\n" + "\n".join(f"{s['label']}. {s['text']}" for s in sents),
                         options=None, correct_option=None, tita_answer=x["tita_answer"],
                         correct_answer=x["tita_answer"] if k == "PJ" else f"{x['tita_answer']} (the odd sentence)",
                         option_rationales={},
                         tita_common_wrong_entries=[dict(value=t["value"], reason=clean(t["rationale"])) for t in x["tita_traps"]])
            else:  # SP
                L = "ABCD"[x["key_number"] - 1]
                r.update(instructions=SP_STEM, missing_sentence=x["missing"], passage_text=x["printed_paragraph"],
                         question=SP_STEM + "\n\nSentence: " + x["missing"] + "\n\nParagraph: " + x["printed_paragraph"],
                         options={"A": "Blank (1)", "B": "Blank (2)", "C": "Blank (3)", "D": "Blank (4)"},
                         correct_option=L, tita_answer=None, correct_answer=f"({L}) Blank ({x['key_number']})",
                         option_rationales={"ABCD"[int(g) - 1]: clean(v) for g, v in x["gap_reasons"].items()},
                         tita_common_wrong_entries=[])
            unit = x.get("set_id") or x["local_id"]
            fam = [x["family"] or sets[x["set_id"]]["family"]]
            if unit in grp:
                fam.append(grp[unit])
            r.update(explanation=clean(x["explanation"]), common_misconception=clean(x["common_misconception"]),
                     difficulty=x["difficulty"], difficulty_reason=clean(x["difficulty_reason"]), cognitive_level=x["cognitive_level"],
                     concept_family=fam[0], family_dependencies=fam, generator_eligible=True,
                     provenance=dict(local_id=x["local_id"], batch=x["local_id"][:5], original=True),
                     human_subject_expert_reviewed=False)
            recs.append(r)
    os.makedirs(os.path.join(HERE, "build"), exist_ok=True)
    json.dump(dict(sets=srecs, questions=recs), open(os.path.join(HERE, "build", "bank.json"), "w"), indent=1)
    json.dump(dict(groups={g: [u for u, gg in grp.items() if gg == g] for g in sorted(set(grp.values()))},
                   pairs=pairs), open(os.path.join(HERE, "build", "subject_groups.json"), "w"), indent=1)
    left = sum(len(re.findall(r"\b(the key|distractor)", (q["explanation"] + " ".join(q["option_rationales"].values())), re.I)) for q in recs)
    print("sets", len(srecs), "questions", len(recs), "subject groups", len(set(grp.values())), "grouped units", len(grp),
          "pairs", len(pairs), "leftover key/distractor words", left)
    print("letters", {c: dict(Counter(r["correct_option"] for r in recs if r["chapter_number"] == CH[c][1] and r["correct_option"])) for c in CH})


if __name__ == "__main__":
    main()
