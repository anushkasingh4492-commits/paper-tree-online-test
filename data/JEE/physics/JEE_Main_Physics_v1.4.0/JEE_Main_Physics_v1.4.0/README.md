# JEE Main Physics - corrected release v1.4.0

Prepared 7 September 2026. This full bank supersedes v1.3.0.

Extract the ZIP before use. Open **Questions.html** for the student book or
**Review_and_Solutions.html** for the searchable teacher book. Keep the figures
folder beside the HTML files. The books work offline and can be printed.

All seven groups in the latest errata report have been addressed and pass the
documented closure checks. Twenty-two named questions are corrected, plus the
adjacent symbolic coil wording in 1540. The closure register contains 24 rows
for 23 distinct questions because 1427 belongs to two finding groups.

- 2160 four-option MCQs across all 20 units; stable IDs and answer letters.
- 648 Easy / 972 Medium / 540 Difficult.
- 1080 Class XI / 1080 Class XII; 540 keys each in A/B/C/D.
- 216 figure-linked questions; 101 figure-required records; 68 unchanged PNGs.
- 270 numerical alternates; one regenerated result and six wording updates.
- 1110 selection families after merging the Curie-law pair; previous guards retained.

## Files

- jee_main_physics_v1.4.0.json: complete canonical bank with solutions and metadata.
- Matching JSONL and CSV files: alternate import formats.
- questions_only.json and answers_explanations.json: separated delivery files.
- Questions.html and Review_and_Solutions.html: complete printable books.
- Sample_Paper.html and Sample_Solutions.html: generated 25-question section.
- sample_paper.json and sample_answer_key.json: sample data.
- coverage_map.json and question_index.csv: coverage and lookup.
- generate_paper.py and Generator_Contract.md: section generator and its rules.
- question_bank_schema.json: schema for the bank.
- Errata_Closure_Report.pdf and Errata_Closure_Register.csv: exact correction record.
- errata/: calculations, before/after changes and verification evidence.
- authoring/: model ledgers and separately implemented calculation routines.
- checksums.sha256: file integrity manifest.

Run verify_release.py from an extracted copy to reproduce the documented
checks. It requires Python and Pillow, writes verification evidence in errata/,
and regenerates the sample files. A rerun therefore changes the extracted
verification outputs; use the delivered checksum manifest before a rerun.

The official basis remains the NTA JEE Main 2026 syllabus and Paper 1 format.
The question IDs are project IDs, not official NTA question numbers. Numerical
alternates are alternate forms of existing questions, not additional items.

Verification combines six new printed-input calculations with retained model
regression, 54 experimental computations, export checks, all numerical
alternates and 1005 paper seeds. These checks close the named errata; they are
not a claim of an independent new solution of every question, external human
subject-expert review or student-performance difficulty calibration.
