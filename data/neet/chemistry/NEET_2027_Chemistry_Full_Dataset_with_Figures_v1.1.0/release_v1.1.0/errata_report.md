# NEET 2027 Chemistry — Corrected Errata Report

Errata status: **PASS**  
Release: **v1.1.0**  
Finding groups resolved or removed: **24**  
Unresolved errors: **0**

The entries below describe corrections already applied to the delivered dataset.

## CHEM-001 — Question wording [Critical]

- Question ID/scope: 10 records in the superseded v1.0.0 bank
- Original: Order of the stated periodic property
- Problem: The property being ordered was omitted.
- Correction applied: Each retained order question now names atomic radius, ionic radius, ionisation enthalpy, electronegativity or electron-gain enthalpy explicitly.
- Verification source: NMC/NTA NEET-UG 2026 Chemistry syllabus, Notice dated 8 January 2026
- Resolution status: **Resolved**

## CHEM-002 — Single-correct integrity [Critical]

- Question ID/scope: 5 equilibrium records in v1.0.0
- Original: A species-specific direction and a synonymous product/reactant direction appeared together.
- Problem: Two options were defensibly correct.
- Correction applied: Synonymous directions were removed and replaced by chemically distinct distractors.
- Verification source: Le Chatelier principle; corrected final options
- Resolution status: **Resolved**

## CHEM-003 — Scientific notation [Major]

- Question ID/scope: 4 Avogadro-constant records in v1.0.0
- Original: Long binary-floating integers
- Problem: The display implied false precision and was unsuitable for an exam.
- Correction applied: Values are rendered with × 10 and Unicode superscript exponents.
- Verification source: Avogadro constant notation in the corrected dataset
- Resolution status: **Resolved**

## CHEM-004 — Difficulty distribution [Critical]

- Question ID/scope: Release-level
- Original: Easy 648; Medium 972; Difficult 540
- Problem: The governing equal-third distribution failed.
- Correction applied: Easy 720; Medium 720; Difficult 720.
- Verification source: Independent validation: equal_difficulty_distribution
- Resolution status: **Resolved**

## CHEM-005 — Answer-key pattern [Critical]

- Question ID/scope: Release-level
- Original: ABCD repeated across the complete key
- Problem: The answer sequence was predictable.
- Correction applied: Complete options were moved to produce 540 A/B/C/D globally, 180 each within every difficulty, and a maximum run of two.
- Verification source: Independent validation: answer_pattern_control
- Resolution status: **Resolved**

## CHEM-006 — Figures [Critical]

- Question ID/scope: 120 v1.0.0 SVG assets
- Original: Text panels repeating question wording
- Problem: The files were not scientific figures.
- Correction applied: Replaced by original vector molecular geometries, Newman projections, chromatograms and laboratory schematics; unused assets were removed.
- Verification source: Corrected figure_manifest.json and SVG inspection
- Resolution status: **Resolved**

## CHEM-007 — Schema [Critical]

- Question ID/scope: All 2160 records
- Original: Canonical fields absent
- Problem: Strict generator imports could fail.
- Correction applied: All required canonical fields, option keys, source mappings, tags and figure arrays are present.
- Verification source: schema_and_generator_contract.json; independent validation
- Resolution status: **Resolved**

## CHEM-008 — Package contract [Critical]

- Question ID/scope: Release-level
- Original: Missing question_index.csv and independent_validation.json; unhashed manifest
- Problem: The package did not meet the delivery contract.
- Correction applied: Required exports were created; the final manifest records path, byte size and SHA-256 for every payload file.
- Verification source: Final package manifest and archive integrity test
- Resolution status: **Resolved**

## CHEM-009 — Source traceability [Critical]

- Question ID/scope: All 2160 records
- Original: No canonical source-document or source-chapter fields
- Problem: Question-level source mapping was absent.
- Correction applied: Every record is mapped to its official syllabus unit and corresponding NCERT chapter; page is null where no stable edition-specific locator can be asserted.
- Verification source: NMC/NTA NEET-UG 2026 Chemistry syllabus, Notice dated 8 January 2026; NCERT XI/XII chapter mapping
- Resolution status: **Resolved**

## CHEM-010 — Question-type metadata [Major]

- Question ID/scope: 253 conservatively flagged v1.0.0 records
- Original: Format labels were quota-filled.
- Problem: Some labels did not describe the visible question.
- Correction applied: Types were recalculated from final stems, computations, reactions and figure use; no format quota was forced.
- Verification source: Corrected question_type fields
- Resolution status: **Resolved**

## CHEM-011 — Question diversity [Major]

- Question ID/scope: 70 repetitive variants selected by the corrected template screen
- Original: Number-only or parameter-only variations
- Problem: They did not provide distinct learning outcomes.
- Correction applied: All excess variants were replaced with different syllabus-based reasoning outcomes; exact and numeric-template near-duplicate groups are both zero.
- Verification source: Independent validation: duplicate screens
- Resolution status: **Resolved**

## CHEM-012 — Syllabus coverage [Major]

- Question ID/scope: Unit 13
- Original: Phosphorus detection and halogen/sulphur/phosphorus quantitative principles were incomplete.
- Problem: The unit did not demonstrate every prescribed characterisation outcome.
- Correction applied: Added phosphorus detection and gravimetric/quantitative analysis items for halogens, sulphur and phosphorus.
- Verification source: NMC/NTA NEET-UG 2026 Chemistry syllabus, Notice dated 8 January 2026
- Resolution status: **Resolved**

## CHEM-013 — Practical Chemistry coverage [Critical]

- Question ID/scope: Unit 20
- Original: Missing prescribed preparations, titrations, ions and iodide–H₂O₂ kinetics; non-prescribed practical variants present.
- Problem: Coverage was incomplete and contained scope mismatches.
- Correction applied: Added aniline yellow, oxalate and Mohr-salt titrations, iodide–H₂O₂ kinetics, CuSO₄ calorimetry and the specified ions; removed the non-prescribed practical variants.
- Verification source: NMC/NTA NEET-UG 2026 Chemistry syllabus, Notice dated 8 January 2026
- Resolution status: **Resolved**

## CHEM-014 — Validation independence [Critical]

- Question ID/scope: Release-level
- Original: The prior PASS report reused build assumptions and missed direct counterexamples.
- Problem: The validation evidence was unreliable.
- Correction applied: A separate validator now reads only corrected release files and independently checks every record and export.
- Verification source: independent_validation.json
- Resolution status: **Resolved**

## CHEM-015 — Exam-year labelling [Major]

- Question ID/scope: Release-level
- Original: The bank was described as if an official NEET-UG 2027 syllabus had been published.
- Problem: No official 2027 syllabus/bulletin was found on the official portal as of 21 August 2026.
- Correction applied: The release is explicitly for the 2025-2027 cohort and uses the official 2026 syllabus for academic session 2026-27; a 2027 notification delta check is stated as a release-time control.
- Verification source: NTA NEET documents portal; official 2026 syllabus notice
- Resolution status: **Resolved**

## CHEM-016 — Language and clarity [Critical]

- Question ID/scope: 179 inherited statement records plus one corrupted token
- Original: 'does not have the defining feature that ...' and 'alossst'
- Problem: Machine-negation phrasing was awkward; one pressure–volume item contained a corrupted word.
- Correction applied: False statements were rewritten as direct propositions, double negatives were removed, explanations were made grammatical, and the pressure–volume item was rewritten while preserving its solved key.
- Verification source: Corrected final stems and explanations
- Resolution status: **Resolved**

## CHEM-017 — Numerical explanation [Major]

- Question ID/scope: Small-value equilibrium records
- Original: Small factors could round to 0.000 or 0 in explanations.
- Problem: The displayed working could contradict the keyed option.
- Correction applied: Small values now use controlled scientific notation in both choices and explanations.
- Verification source: Corrected Kp/Kc records
- Resolution status: **Resolved**

## CHEM-018 — Grammar [Minor]

- Question ID/scope: Magnetic-property records
- Original: '1 unpaired electrons'
- Problem: Singular/plural grammar was incorrect.
- Correction applied: Options and explanations now use '1 unpaired electron' and plural forms for all other counts.
- Verification source: Corrected Unit 11 records
- Resolution status: **Resolved**

## CHEM-019 — NEET style [Major]

- Question ID/scope: 1,504 records in the prior candidate release
- Original: 'In the context of [chapter] ...'
- Problem: Synthetic chapter framing made otherwise standalone questions repetitive and unlike normal NEET presentation.
- Correction applied: The chapter preamble was removed and affected stems now open with the chemical task itself.
- Verification source: Final wording screen: zero chapter-framing matches
- Resolution status: **Resolved**

## CHEM-020 — Difficulty validity [Critical]

- Question ID/scope: 59 records conservatively flagged in the fresh audit
- Original: Difficult labels on direct definition, detail-recall and single-substitution items
- Problem: The displayed task did not support a Difficult tag.
- Correction applied: Difficulty was recalculated from visible multi-statement, integration, numerical and interpretation demand; no Difficult record matches the conservative recall screen, while the required 720/720/720 distribution is retained.
- Verification source: Independent validation: difficulty_validity_screen
- Resolution status: **Resolved**

## CHEM-021 — Question-type metadata [Major]

- Question ID/scope: NEET27-CHEM-1348
- Original: Reaction/reagent MCQ
- Problem: The visible oxidation-state statement did not require reaction or reagent reasoning.
- Correction applied: Reclassified as Statement-based MCQ from final visible content.
- Verification source: Independent validation: question_type_content_screen
- Resolution status: **Resolved**

## CHEM-022 — Option quality [Major]

- Question ID/scope: 60 records in the fresh audit plus one notation-triggered regression
- Original: Correct option conspicuously longer than every distractor
- Problem: Option length could cue the answer.
- Correction applied: Substantive, chemically plausible distractors of comparable specificity replaced terse distractors; the final screen reports zero length cues.
- Verification source: Independent validation: option_length_cue_screen
- Resolution status: **Resolved**

## CHEM-023 — Notation and language [Major]

- Question ID/scope: Inherited Chemistry notation across the bank
- Original: Examples included nabh4, lialh4, ph, delta g, d0 and sp3
- Problem: Lower-case or mechanically flattened notation reduced exam realism and could obscure meaning.
- Correction applied: Chemical formulae, symbols, oxidation-state notation, hybridisation labels and common abbreviations were normalised consistently in stems, options and explanations.
- Verification source: Independent validation: notation_regression_screen
- Resolution status: **Resolved**

## CHEM-024 — Scientific accuracy [Critical]

- Question ID/scope: NEET27-CHEM-1954
- Original: Vitamin E deficiency was associated with 'antioxidant protection'
- Problem: The wording confused the vitamin's function with its deficiency effects.
- Correction applied: Corrected to identify vitamin E as fat-soluble and antioxidant, with deficiency associated with red-blood-cell fragility and muscular weakness; distractors and explanation were updated.
- Verification source: NCERT biomolecules/vitamin table; corrected final record
- Resolution status: **Resolved**
