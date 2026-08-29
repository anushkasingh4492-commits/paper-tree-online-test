# NEET 2027 Physics Errata Report

Status: PASS  
Audit date: 2026-08-21  
Errors found: 10  
Unresolved errors: 0

## 1. Syllabus coverage — Resolved

- Question ID: MULTIPLE
- Severity: Major
- Original: Zero or thin coverage in explicitly listed subtopics
- Problem: Frames and motion graphs, elasticity, Gauss-law applications, bar magnets, galvanometer conversion, transformers, optical instruments, logic gates and Zener regulation were absent or thin.
- Correction: Added 76 targeted questions and replaced surplus coverage while retaining the 2,160-record total.
- Verification: NMC/NTA NEET-UG 2026 Physics syllabus for academic session 2026-27

## 2. Syllabus scope — Removed

- Question ID: MULTIPLE
- Severity: Major
- Original: Seven hysteresis/retentivity/coercivity questions in Unit 13
- Problem: The block exceeded the strict wording of the current official syllabus.
- Correction: Excluded all hysteresis, retentivity and coercivity candidates and replaced them with explicitly listed Unit 13 content.
- Verification: NMC/NTA NEET-UG 2026 Physics syllabus for academic session 2026-27

## 3. Figure dependency — Resolved

- Question ID: MULTIPLE
- Severity: Major
- Original: 111 figure-required stems disclosed the highlighted position or apparatus cue
- Problem: The questions could be answered without the linked image.
- Correction: Removed textual position/apparatus cues; all 111 required-image questions now depend on information carried by the linked figure.
- Verification: Corrected dataset and figure-dependency audit

## 4. Experimental skills — Resolved

- Question ID: MULTIPLE
- Severity: Major
- Original: Cue-driven Unit 20 questions with remote distractors
- Problem: Several items tested lexical recognition more than experimental reasoning.
- Correction: Rewrote stems and supplied same-experiment misconceptions for principles, observations, precautions and purpose-principle matches.
- Verification: Corrected Unit 20 question block

## 5. Figure rendering — Resolved

- Question ID: MULTIPLE
- Severity: Major
- Original: N m□¹ in four spring figures
- Problem: The font lacked the superscript-minus glyph.
- Correction: Regenerated the figures using N/m and visually verified the rendered unit.
- Verification: u04-work-005.png through u04-work-008.png

## 6. Asset accounting — Resolved

- Question ID: MULTIPLE
- Severity: Moderate
- Original: 117 distinct_original_figures
- Problem: The label overstated educational visual diversity and counted cosmetic A/B variants.
- Correction: Use 99 byte-distinct asset files, one asset per Unit 20 experiment, and report distinct_asset_files.
- Verification: Figure manifest, byte hashes and image decode audit

## 7. Repetition — Resolved

- Question ID: MULTIPLE
- Severity: Moderate
- Original: Repeated cue-driven spectrum, experimental formats and number-substitution drill families
- Problem: Template repetition reduced discrimination.
- Correction: Made spectrum identification depend on diagrams, diversified experimental misconceptions, limited each non-figure numeric template to at most two records and replaced pruned variants with different concepts.
- Verification: Question-plus-figure and numeric-template diversity audits

## 8. Explanation accuracy — Resolved

- Question ID: NEET27-PHY-1544 (pre-rebuild ID)
- Severity: Minor
- Original: 475.6 and 525.6 described as rounding to 475 and 525
- Problem: Nearest-whole-number rounding was incorrect.
- Correction: Explanation now identifies 475 and 525 as the symmetric narrow-band approximation.
- Verification: Series-LCR half-power relation

## 9. Provenance — Resolved

- Question ID: MULTIPLE
- Severity: Moderate
- Original: All source_page values null
- Problem: Record-level syllabus provenance was incomplete.
- Correction: All records now include the applicable official-syllabus PDF page and an official-syllabus/NCERT source description.
- Verification: NMC/NTA NEET-UG 2026 Physics syllabus for academic session 2026-27

## 10. Difficulty — Resolved

- Question ID: MULTIPLE
- Severity: Moderate
- Original: Difficulty labels treated as definitive
- Problem: Difficulty is editorial until calibrated with response data.
- Correction: Retained the intended 30/45/25 deployment mix and explicitly labelled it editorial provisional in the blueprint, manifest and README.
- Verification: Coverage blueprint and release policy
