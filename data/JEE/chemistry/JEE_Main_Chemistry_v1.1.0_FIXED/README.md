# JEE Main Chemistry - corrected full bank v1.1.0

Extract the complete ZIP and open **START_HERE.html**. Keep the figures folder beside the HTML files.

This release contains 2,160 four-option single-correct questions: 648 Easy, 972 Medium and 540 Difficult, with 1,080 XI / 1,080 XII and 540 answer keys per letter. There are 270 numerical alternatives of existing questions. The complete student and teacher HTML banks are searchable, filterable and printable. They contain every question.

- Canonical bank: jee_main_chemistry_v1.1.0.json / .jsonl / .csv (CSV nested structures are JSON-encoded).
- Student and teacher machine exports: questions_only.json and answers_and_explanations.json.
- Sample_Paper.html and Sample_Solutions.html show a 25-question section.
- Errata_Closure_Report.pdf / .md explain the revision. Errata_Closure_Register.csv traces all 1,195 finding/question associations.
- coverage_map.json, practical_coverage_crosswalk.json, source_references.json and family_register.json document scope and exclusions.
- Validation files contain numerical, export, schema, generator and closure evidence.

The Python generator can create further practice sections: `python generate_paper.py --seed 42 --output practice42`.
It uses the standard library. The optional independent arithmetic audit requires Python and NumPy.

The syllabus basis is NTA 2026. Difficulty is editorial, not empirically calibrated. Parameter variants are explicitly grouped and are not independent conceptual breadth. Half-integers use the supplied practice convention of rounding away from zero.

The previous release is preserved outside this package. Use the v1.1.0 files as a complete replacement rather than mixing versions. The final ZIP is accompanied by a SHA-256 file and an archive-verification report.
