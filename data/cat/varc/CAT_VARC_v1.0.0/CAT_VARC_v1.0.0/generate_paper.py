# -*- coding: utf-8 -*-
"""CAT VARC paper generator (Python standard library only).

Example:
  python generate_paper.py --bank cat_varc_v1.0.0.json --seed 7 --output practice7
Options:
  --rc-sets N      number of RC passages (default 4); whole passages only
  --rc-size K      questions per passage to use: 4 (default, CAT) uses only 4-question passages;
                   5 uses only 5-question passages; 0 allows both
  --pj --ps --ooo --sp   counts of para jumbles, para summaries, odd sentence out, sentence placement
                   (defaults 2, 3, 2, 1: 8 VA questions, so the default paper is 24 questions as in CAT)
  --exam NAME      only items tagged for an exam (CAT, XAT, NMAT, SNAP, CMAT, MAH-CET)
  --chapter K      restrict RC passages to one RC chapter (1 to 8)
  --minutes M      time printed on the paper (default 40)
Rules (Generator_Contract.md): whole passages; RC passages from different chapters where possible;
no two units (passages or VA items) share any entry of family_dependencies; difficulty as close as
possible to 30/45/25 of the section.
"""
import argparse, json, random
from collections import Counter

DIFFS = ("Easy", "Medium", "Difficult")
VA_TYPES = (("pj", "Para jumble"), ("ps", "Para summary"), ("ooo", "Odd sentence out"), ("sp", "Sentence placement"))


def quotas(n):
    e = int(n * 0.30 + 0.5); m = int(n * 0.45 + 0.5)
    return {"Easy": e, "Medium": m, "Difficult": n - e - m}


def build(bank, a, seed, tries=3000):
    qs = {q["id"]: q for q in bank["questions"] if q.get("generator_eligible", True)}
    sets = [s for s in bank["sets"] if s.get("generator_eligible", True)
            and (a.rc_size == 0 or s["question_count"] == a.rc_size)
            and (a.chapter is None or s["chapter_number"] == a.chapter)
            and (a.exam is None or a.exam in s["exam_tags"])
            and all((a.exam is None or a.exam in qs[i]["exam_tags"]) and i in qs for i in s["question_ids"])]
    va = {t: [q for q in qs.values() if q["question_type"] == name and (a.exam is None or a.exam in q["exam_tags"])]
          for t, name in VA_TYPES}
    need_va = {t: getattr(a, t) for t, _ in VA_TYPES}
    rnd = random.Random(seed)
    best = None
    for _ in range(tries):
        used, chosen_sets, chs = set(), [], Counter()
        pool = list(sets); rnd.shuffle(pool)
        pool.sort(key=lambda s: chs[s["chapter_number"]])
        for s in pool:
            if len(chosen_sets) == a.rc_sets:
                break
            if used & set(s["family_dependencies"]):
                continue
            if chs[s["chapter_number"]] and len({x["chapter_number"] for x in sets}) >= a.rc_sets:
                continue
            chosen_sets.append(s); used |= set(s["family_dependencies"]); chs[s["chapter_number"]] += 1
        if len(chosen_sets) < a.rc_sets:
            continue
        rcq = [qs[i] for s in chosen_sets for i in s["question_ids"]]
        n = len(rcq) + sum(need_va.values())
        target = quotas(n)
        have = Counter(q["difficulty"] for q in rcq)
        chosen_va, ok = [], True
        for t, _ in VA_TYPES:
            cand = list(va[t]); rnd.shuffle(cand)
            k = 0
            for q in sorted(cand, key=lambda q: -(target[q["difficulty"]] - have[q["difficulty"]])):
                if k == need_va[t]:
                    break
                if used & set(q["family_dependencies"]):
                    continue
                chosen_va.append(q); used |= set(q["family_dependencies"]); have[q["difficulty"]] += 1; k += 1
            if k < need_va[t]:
                ok = False; break
        if not ok:
            continue
        dev = sum(abs(have[d] - target[d]) for d in DIFFS)
        if best is None or dev < best[0]:
            best = (dev, chosen_sets, chosen_va)
        if dev == 0:
            break
    if best is None:
        raise SystemExit("Could not build a paper with these constraints; relax the options.")
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bank", required=True)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--output", default="paper")
    ap.add_argument("--rc-sets", type=int, default=4)
    ap.add_argument("--rc-size", type=int, default=4, choices=(0, 4, 5))
    for t, _ in VA_TYPES:
        ap.add_argument("--" + t, type=int, default={"pj": 2, "ps": 3, "ooo": 2, "sp": 1}[t])
    ap.add_argument("--exam")
    ap.add_argument("--chapter", type=int)
    ap.add_argument("--minutes", type=int, default=40)
    a = ap.parse_args()
    bank = json.load(open(a.bank, encoding="utf-8"))
    dev, sets, va = build(bank, a, a.seed)
    qs = {q["id"]: q for q in bank["questions"]}
    order = [i for s in sets for i in s["question_ids"]] + [q["id"] for q in va]
    n = len(order)
    paper = dict(seed=a.seed, description=f"CAT-style VARC section of {n} questions: {len(sets)} reading passages and {len(va)} verbal ability items.",
                 time_minutes=a.minutes, max_marks=3 * n,
                 marking={"MCQ": {"correct": 3, "incorrect": -1, "unattempted": 0},
                          "TITA": {"correct": 3, "incorrect": 0, "unattempted": 0}},
                 passages=[s["set_id"] for s in sets], questions=order,
                 difficulty=dict(Counter(qs[i]["difficulty"] for i in order)), difficulty_deviation=dev)
    key = [dict(number=k + 1, id=i, set_id=qs[i]["set_id"], format=qs[i]["answer_format"],
                answer=qs[i]["correct_option"] if qs[i]["answer_format"] == "MCQ" else qs[i]["tita_answer"])
           for k, i in enumerate(order)]
    json.dump(paper, open(a.output + "_paper.json", "w"), indent=1)
    json.dump(key, open(a.output + "_answer_key.json", "w"), indent=1)
    print("questions", n, paper["difficulty"], dict(Counter(qs[i]["answer_format"] for i in order)))


if __name__ == "__main__":
    main()
