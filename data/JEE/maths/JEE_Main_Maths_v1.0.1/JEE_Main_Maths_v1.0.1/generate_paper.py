#!/usr/bin/env python3
"""JEE Main Mathematics practice-section generator (standard library only).

Full-bank mode (all 14 units present):
    python generate_paper.py --bank jee_main_maths.json --seed 42 --output practice42
Unit-practice mode (one unit, e.g. the Unit 2 pilot):
    python generate_paper.py --bank <bank.json> --seed 42 --unit 2 --output practice42

Blueprint (see Generator_Contract.md): 20 single-correct MCQs (Section A) + 5 integer-answer
questions (Section B); +4/-1/0; 8 Easy / 11 Medium / 6 Difficult overall, Section B 1/2/2;
Section A keys exactly five per letter; every selected record has family_dependencies disjoint
from every other selected record. Full-bank mode adds: at most 3 questions per unit and a
12/13 XI/XII split that alternates with seed parity. The generator returns a complete valid
paper or raises; it never silently relaxes a constraint.
"""
import argparse, json, os, random, sys

TOTAL = {"Easy": 8, "Medium": 11, "Difficult": 6}
SEC_B = {"Easy": 1, "Medium": 2, "Difficult": 2}
SEC_A = {k: TOTAL[k] - SEC_B[k] for k in TOTAL}
RESTARTS = 3000


def build(bank, seed, unit=None):
    rnd = random.Random(seed)
    pool = [r for r in bank if r.get("generator_eligible")]
    if unit is not None:
        pool = [r for r in pool if r["unit_number"] == unit]
        unit_cap, class_quota = None, None
    else:
        units = {r["unit_number"] for r in pool}
        if len(units) < 14:
            raise SystemExit(f"Full-bank mode needs all 14 units; bank has {sorted(units)}. Use --unit.")
        unit_cap = 3
        class_quota = {"XI": 12, "XII": 13} if seed % 2 == 0 else {"XI": 13, "XII": 12}
    for attempt in range(RESTARTS):
        used_fams, unit_count, class_count = set(), {}, {"XI": 0, "XII": 0}
        chosen_b, chosen_a = [], []
        keys = {L: 0 for L in "ABCD"}

        def fits(r):
            if used_fams & set(r["family_dependencies"]):
                return False
            if unit_cap and unit_count.get(r["unit_number"], 0) >= unit_cap:
                return False
            if class_quota and class_count[r["source_class"]] >= class_quota[r["source_class"]]:
                return False
            return True

        def take(r):
            used_fams.update(r["family_dependencies"])
            unit_count[r["unit_number"]] = unit_count.get(r["unit_number"], 0) + 1
            class_count[r["source_class"]] += 1

        ok = True
        for lvl, n in SEC_B.items():
            cands = [r for r in pool if r["difficulty"] == lvl and r.get("numerical_variant")]
            rnd.shuffle(cands)
            got = 0
            for r in cands:
                if got == n:
                    break
                if fits(r):
                    take(r); chosen_b.append(r); got += 1
            ok &= got == n
        if not ok:
            continue
        for lvl, n in SEC_A.items():
            cands = [r for r in pool if r["difficulty"] == lvl and r not in chosen_b]
            rnd.shuffle(cands)
            got = 0
            for r in cands:
                if got == n:
                    break
                if keys[r["correct_option"]] >= 5:
                    continue
                if fits(r):
                    take(r); chosen_a.append(r); keys[r["correct_option"]] += 1; got += 1
            ok &= got == n
        if ok and all(v == 5 for v in keys.values()):
            if class_quota and class_count != class_quota:
                continue
            rnd.shuffle(chosen_a)
            order = {"Easy": 0, "Medium": 1, "Difficult": 2}
            chosen_b.sort(key=lambda r: order[r["difficulty"]])
            return chosen_a, chosen_b, attempt
    raise RuntimeError(f"No valid paper for seed {seed} within {RESTARTS} restarts")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bank", required=True)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--unit", type=int)
    ap.add_argument("--output", required=True)
    a = ap.parse_args()
    bank = json.load(open(a.bank, encoding="utf-8"))
    sec_a, sec_b, attempt = build(bank, a.seed, a.unit)
    os.makedirs(a.output, exist_ok=True)
    mode = f"Unit {a.unit} practice section" if a.unit else "Mathematics subject section"
    paper = dict(seed=a.seed, mode=mode, restarts_used=attempt,
                 description=f"{mode}: Section A 20 MCQs, Section B 5 integer-answer questions.",
                 section_a=[r["id"] for r in sec_a], section_b=[r["id"] for r in sec_b],
                 marking=dict(correct=4, incorrect=-1, unattempted=0), max_marks=100)
    questions = dict(paper, items_a=[dict(id=r["id"], question=r["question"], options=r["options"]) for r in sec_a],
                     items_b=[dict(id=r["id"], question=r["numerical_variant"]["question"]) for r in sec_b])
    answers = dict(seed=a.seed, section_a={r["id"]: r["correct_option"] for r in sec_a},
                   section_b={r["id"]: r["numerical_variant"]["answer_integer"] for r in sec_b})
    json.dump(paper, open(os.path.join(a.output, "paper.json"), "w"), indent=1)
    json.dump(questions, open(os.path.join(a.output, "questions.json"), "w"), indent=1, ensure_ascii=False)
    json.dump(answers, open(os.path.join(a.output, "answer_key.json"), "w"), indent=1)
    print(f"seed {a.seed}: {len(sec_a)} MCQ + {len(sec_b)} numerical; restarts used {attempt}")


if __name__ == "__main__":
    main()
