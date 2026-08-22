"""Assemble a balanced 100-question MHT-CET Biology paper from v2.1.0."""

import argparse
import json
import random
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BANK_PATH = ROOT / "MHT-CET_Biology_question_bank_v2.1.0.json"

BLUEPRINT = {
    11: {
        "Easy": {"A": 2, "B": 1, "C": 1, "D": 1},
        "Medium": {"A": 2, "B": 2, "C": 2, "D": 2},
        "Hard": {"A": 1, "B": 2, "C": 1, "D": 1},
        "Challenging": {"A": 0, "B": 0, "C": 1, "D": 1},
    },
    12: {
        "Easy": {"A": 5, "B": 5, "C": 5, "D": 5},
        "Medium": {"A": 8, "B": 8, "C": 8, "D": 8},
        "Hard": {"A": 5, "B": 5, "C": 5, "D": 5},
        "Challenging": {"A": 2, "B": 2, "C": 2, "D": 2},
    },
}


def option_signature(q):
    return tuple(sorted(" ".join(value.lower().split()) for value in q["options"].values()))


def choose(candidates, count, rng, state):
    chosen = []
    pool = list(candidates)
    rng.shuffle(pool)
    for _ in range(count):
        valid = []
        for q in pool:
            chapter = (q["standard"], q["chapter_number"])
            subtopic = (q["standard"], q["chapter_number"], q["subtopic"])
            signature = option_signature(q)
            challenge_signature = q["correct_answer_text"] if q["difficulty"] == "Challenging" else None
            if q["concept_family_id"] in state["families"]:
                continue
            if signature in state["option_sets"]:
                continue
            if state["subtopics"][subtopic] >= 2:
                continue
            if challenge_signature and state["challenge_answers"][challenge_signature] >= 2:
                continue
            valid.append(q)
        if not valid:
            raise RuntimeError("Insufficient diverse questions for a blueprint cell")
        minimum_chapter = min(state["chapters"][(q["standard"], q["chapter_number"])] for q in valid)
        valid = [q for q in valid if state["chapters"][(q["standard"], q["chapter_number"])] == minimum_chapter]
        minimum_subtopic = min(state["subtopics"][(q["standard"], q["chapter_number"], q["subtopic"])] for q in valid)
        valid = [q for q in valid if state["subtopics"][(q["standard"], q["chapter_number"], q["subtopic"])] == minimum_subtopic]
        q = rng.choice(valid)
        pool.remove(q)
        chosen.append(q)
        state["families"].add(q["concept_family_id"])
        state["option_sets"].add(option_signature(q))
        state["chapters"][(q["standard"], q["chapter_number"])] += 1
        state["subtopics"][(q["standard"], q["chapter_number"], q["subtopic"])] += 1
        if q["difficulty"] == "Challenging":
            state["challenge_answers"][q["correct_answer_text"]] += 1
    return chosen


def assemble(seed):
    bank = json.loads(BANK_PATH.read_text(encoding="utf-8"))
    cells = defaultdict(list)
    for q in bank:
        if q["generator_eligible_strict_cet"]:
            cells[(q["standard"], q["difficulty"], q["correct_option"])].append(q)
    state = {
        "families": set(), "option_sets": set(), "chapters": Counter(),
        "subtopics": Counter(), "challenge_answers": Counter(),
    }
    rng = random.Random(seed)
    selected = []
    # Scarcer cells first makes the constrained selection stable across seeds.
    for standard in (11, 12):
        for difficulty in ("Challenging", "Hard", "Easy", "Medium"):
            for letter in "ABCD":
                selected.extend(choose(cells[(standard, difficulty, letter)], BLUEPRINT[standard][difficulty][letter], rng, state))
    rng.shuffle(selected)
    return {
        "paper_metadata": {
            "exam": "MHT-CET Biology", "release": "2.1.0", "syllabus": "MHT-CET 2026",
            "seed": seed, "questions": 100, "marks": 100, "duration_minutes": 90,
            "negative_marking": False,
            "standard_split": dict(Counter(str(q["standard"]) for q in selected)),
            "difficulty": dict(Counter(q["difficulty"] for q in selected)),
            "answer_key": dict(Counter(q["correct_option"] for q in selected)),
            "chapter_distribution": {f"Std {s} Ch {c:02d}": n for (s, c), n in sorted(state["chapters"].items())},
            "diversity_guards": {"unique_concept_family": True, "unique_option_set": True, "maximum_same_subtopic": 2, "maximum_same_challenge_answer": 2},
        },
        "questions": selected,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--output", default="examples/sample_test.json")
    args = parser.parse_args()
    paper = assemble(args.seed)
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(paper, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(paper["paper_metadata"], indent=2))


if __name__ == "__main__":
    main()
