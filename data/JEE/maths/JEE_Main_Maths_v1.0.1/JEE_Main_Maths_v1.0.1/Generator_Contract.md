# Mathematics practice-paper generator contract

Every returned paper has 25 questions. Section A has 20 single-correct MCQs and Section B has 5 integer-answer questions. It is a Mathematics subject section, not a complete three-subject JEE paper. Maximum 100 marks: +4 correct, -1 incorrect, 0 unattempted.

1. Keep each ID, stem, options, assumptions and figure links together. Mathematics is LaTeX inline between `$...$` and must be rendered with KaTeX or MathJax. Do not show raw LaTeX to students.
2. Student delivery must omit keys, explanations, misconceptions, rationales, provenance and numerical answers. If an importer shuffles options, it must remap `correct_option`. Explanations never name option letters, so they survive a shuffle.
3. For Section B, use only a non-null `numerical_variant`. Show its `question` (plus the parent assumptions and figures) without options. Grade against `answer_integer`. Every answer is an exact integer, so no rounding is involved.
4. Select at most one record per dependency. Every selected record must have `family_dependencies` disjoint from all other selected records, across both sections. A numerical alternate uses its parent's dependencies. Alias dependencies (prefixed `ALIAS-`) stop the generator from pairing items that would leak each other's answers. They are not a general semantic-similarity test.
5. Blueprint: 8 Easy / 11 Medium / 6 Difficult in total. Section B is 1 Easy / 2 Medium / 2 Difficult. Section A has exactly five keys of each letter.
6. Full-bank mode (all 14 units present) also requires at most 3 questions per unit and a XI/XII split of 12/13 for even seeds and 13/12 for odd seeds.
7. Unit-practice mode (`--unit N`) draws only from that unit and drops the unit and class quotas.
8. The difficulty, class and unit quotas are house practice choices, not NTA rules. Difficulty is editorial, not calibrated on students.
9. Sampling is deterministic for a seed, with up to 3000 restarts. The generator returns a complete valid paper or raises an error. It never relaxes a constraint silently. Seeds 0 to 1004 were exercised (see `evidence/generator_validation.json`). That does not prove every seed works, and the generator does not promise equal exposure of items.
