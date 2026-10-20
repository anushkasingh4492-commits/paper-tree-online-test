# -*- coding: utf-8 -*-
"""Authoring helper for the JEE Main Mathematics bank.

Every drafting file does:   from qlib import *
and then calls q(...) once per question. Nothing else is required.
"""
from sympy import *  # noqa: F401,F403  (authors use sympy freely inside checks)

QUESTIONS = []

DIFFICULTIES = ("Easy", "Medium", "Difficult")
QTYPES = (
    "Direct concept MCQ",
    "Single-step computation MCQ",
    "Multi-step computation MCQ",
    "Inverse/parameter MCQ",
    "Conceptual/application MCQ",
    "Statement-based MCQ",
    "Graph/diagram MCQ",
)
COGNITIVE = ("Recall", "Understanding", "Application", "Analysis")


def q(local_id, topic, subtopic, difficulty, qtype, question, correct, distractors,
      explanation, misconception, family, difficulty_reason,
      check=None, values=None, numerical=None, cognitive="Application",
      assumptions=(), source_class="XI", figure=None, flags=""):
    """Register one question.

    local_id      e.g. "U02-A-001"
    question      stem, LaTeX inline with $...$
    correct       LaTeX text of the correct option (what the student sees)
    distractors   list of exactly 3 tuples (option_latex, rationale_for_reviewer)
    explanation   worked solution, never mentions option letters
    check         zero-argument function that RECOMPUTES the answer from the givens in the
                  stem (sympy object, number, sympy Set, tuple, or bool). None only for
                  purely conceptual items.
    values        list of 4 sympy objects: [value_of_correct, value_d1, value_d2, value_d3]
                  in the same order as correct + distractors. Required whenever check is given.
    numerical     None, or dict(question=<stem rewritten for integer entry, no options>,
                  answer=<int>) for items that make a clean JEE Section B integer question.
    flags         anything you are unsure about. Leave "" if nothing.
    """
    assert difficulty in DIFFICULTIES, (local_id, difficulty)
    assert qtype in QTYPES, (local_id, qtype)
    assert cognitive in COGNITIVE, (local_id, cognitive)
    assert len(distractors) == 3, (local_id, "need 3 distractors")
    for d in distractors:
        assert isinstance(d, tuple) and len(d) == 2 and d[1].strip(), (local_id, "distractor needs (text, rationale)")
    texts = [correct] + [d[0] for d in distractors]
    assert len(set(t.strip() for t in texts)) == 4, (local_id, "options not distinct")
    if check is not None:
        assert values is not None and len(values) == 4, (local_id, "values required with check")
    if numerical is not None:
        assert set(numerical) == {"question", "answer"}, local_id
        assert isinstance(numerical["answer"], int), local_id
    QUESTIONS.append(dict(
        local_id=local_id, topic=topic, subtopic=subtopic, difficulty=difficulty,
        question_type=qtype, question=question, correct=correct,
        distractors=[dict(text=t, rationale=r) for t, r in distractors],
        explanation=explanation, common_misconception=misconception,
        concept_family=family, difficulty_reason=difficulty_reason,
        check=check, values=values, numerical=numerical, cognitive_level=cognitive,
        assumptions=list(assumptions), source_class=source_class, figure=figure,
        flags=flags,
    ))
