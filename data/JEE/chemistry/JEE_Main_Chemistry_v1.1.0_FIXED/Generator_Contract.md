# Chemistry practice-paper generator contract

Every returned paper contains 25 questions: Section A has 20 single-correct MCQs and Section B has 5 numerical-answer questions. It is a Chemistry subject section, not a complete three-subject JEE paper. Maximum 100 marks; +4 correct, -1 incorrect, 0 unattempted.

The practice blueprint has 8 Easy, 11 Medium, 6 Difficult questions. Section B contributes 1 Easy, 2 Medium, 2 Difficult. Section A has five answer keys of each letter. A unit appears at most three times. XI/XII counts are 12/13 for an even seed and 13/12 for an odd seed. These quotas are the requested house practice format; NTA does not promise those chapter, key or difficulty proportions in an actual paper.

Every selected record must have family_dependencies disjoint from all previously selected records, including both sections and all paired constituents. A numerical alternative uses its parent question's family. Recognised semantic aliases unify selected related models across different authoring names. This recorded-family rule does not constitute a universal semantic similarity test.

Section B omits MCQ options and uses numerical_variant.question. The answer is answer_integer, after applying any factor explicitly requested in that question. Nearest-integer entry follows the 2026 bulletin. Exact halves away from zero is an explicit convention of this practice generator; it is not attributed to an NTA statement on tie-breaking. Near-half authored cases were excluded and displayed-input rounding was checked.

The generator uses deterministic seeded sampling with bounded restarts (3000). It returns a complete valid paper or raises an error; it never silently relaxes a constraint. Validation exercised seeds 0 through 1004. That test set does not prove success for every possible seed, and the random sampler does not promise equal item exposure.

Output: questions/answers JSON and student/teacher HTML. The JSON answer file records scaling details for numerical answers. The teacher HTML explicitly shows the scaling and rounding step. Figure paths are relative to the bank directory. Keep generated files there.
