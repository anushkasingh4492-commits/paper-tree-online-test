# MHT-CET Biology Full Question Bank v2.1.0 (Repaired)

This deployment package contains 2,120 four-option Biology MCQs aligned to the MHT-CET 2026 scope: 436 Standard XI questions and 1,684 Standard XII questions across 19 chapters.

## Upload file

Use `MHT-CET_Biology_question_bank_v2.1.0.json`. Keep the `figures` directory beside it so all relative asset paths resolve.

## Quality controls

- Every question has one of four difficulty tags: Easy, Medium, Hard or Challenging.
- Correct answers are exactly balanced: 530 each in A, B, C and D.
- The release includes 44 original 1800 x 1100 PNG assets linked to 82 questions. Standard XII has 60 genuine graph/diagram questions, with 15 at each difficulty.
- The schemas strictly validate A-D options, three distractor rationales, enums, IDs and figure paths.
- `assemble_test.py` builds a 100-question paper with a 20/80 XI/XII split, 25/40/25/10 difficulty mix and exactly 25 answers in each letter position. It prevents repeated concept families and repeated option sets and caps one subtopic at two questions.
- Source locators and explicit review fields are present on all 2,120 records.

## Review

Content, structure, assets and generated-paper functionality have been reviewed and validated for this release.
