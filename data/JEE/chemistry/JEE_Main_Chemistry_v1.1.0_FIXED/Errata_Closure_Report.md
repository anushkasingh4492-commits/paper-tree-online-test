# Corrected Chemistry bank | v1.1.0

All ten reported finding families are closed against the revised bank. This is the complete 2,160-question replacement release, not an errata-only supplement.

Prepared 7 September 2026. The question IDs, 20-unit allocation, XI/XII split and difficulty totals remain stable. Previous releases and the Physics, NEET and MHT-CET banks are preserved.

| Delivery parameter | Verified total |
| --- | --- |
| Four-option single-correct MCQs | 2,160 |
| Easy / Medium / Difficult | 648 / 972 / 540 |
| Class XI / Class XII | 1,080 / 1,080 |
| Correct keys A / B / C / D | 540 each |
| Numerical alternative presentations | 270: 12 Easy, 108 Medium, 150 Difficult |
| Practical requirement entries | 39 with surviving evidence IDs |
| Finding/question rows closed | 1,195 across 1,065 original records |

## What changed

The 732 old independent-case pairs and 180 former Medium numerical questions were rebuilt as 912 linked applications. This includes two new conformation-diagram tasks. The 540 retained Difficult numerical questions received new distractors. Specific chemistry, wording, topic and numerical-alternative defects were corrected and propagated to the exports.

The revision contains 1,450 calculation-backed MCQs across 141 disclosed models, plus the retained conceptual and foundational items. The 270 numerical alternatives are alternate presentations of existing questions, not additional questions.

Read START_HERE.html after extracting the ZIP. Complete student and teacher banks, searchable/printable views, machine-readable exports, sample papers, generator, source maps and validation evidence are included.

# Assessment corrections | F01-F03

## F01 - Deterministic numerical-option rule

Numerical options replaced with distinct error candidates and domain filters; affected Medium questions rebuilt. Original rank attack now succeeds on 200/720 (27.78%) rather than 720/720. Every revised numerical key agrees with separate recalculation.

The former uniform percentage-offset routine was removed. Options now come from alternative counts, stoichiometric or unit mistakes, competing chemical assignments, or recalculated model-error candidates. Duplicate numeric values and invalid percentage/count domains are filtered. Correct numerical rank varies independently of its answer letter.

The 27.78% result is a measured attack score, not a claim that every possible test-taking heuristic is defeated. The original deterministic shortcut is no longer valid. The full per-question distractor register is supplied.

## F02 - Difficulty assigned to recall/substitution

All 422 flagged IDs replaced with linked applications. The revision also replaces the full 732 independent-case pairs and all 180 former Medium numerical items: 912 replacements in total, including two new conformation diagrams. Quotas preserved without merely relabelling the flagged questions.

Examples now require purity plus aliquot conservation; a structure-derived hydrogen demand; a reaction sequence followed by product accounting; ionic configuration followed by magnetic moment; or a projection followed by rotation and energy comparison. The 60 retained Medium coverage/geometry questions remain in the bank.

A separate arithmetic checker found a sigma-bond-count error in one new template during development. Its four generated records and associated numerical alternatives were corrected before the successful final run. This intermediate failure is not concealed as a first-pass success.

## F03 - Integer-domain giveaways

Retained integral-answer models now have only integral alternatives within their relevant count domain. Recalculation and four-option uniqueness pass.

The relevant initial-rate and hydrogenation options are integral. The final key is supported by the rate equations or molecular formula rather than being the only integer on the page.

# Source and wording corrections | F04-F06

## F04 - Cross-unit molarity family

The two cross-unit molarity-definition families merged into CHEM-molarity-definition. Superseded paired records replaced; semantic dependencies retained and further model equivalences linked.

Additional explicit dependency links cover shared hydrogen-level, first-order progress, solvent-extraction, peptide-composition, Werner-sphere, CFT and precipitation models. The generator rejects overlaps across both Section A and Section B.

## F05 - Aniline-yellow preparation

Direct preparation item rewritten around diazoaminobenzene rearrangement in aniline with aniline hydrochloride under weakly acidic conditions; related old pairs replaced. Practical evidence re-established. NCERT also permits a weakly acidic direct-coupling alternative; the old aniline key was not itself false.

JEE-CHEM-2108 now names the specific rearrangement conditions. Five new practical application variants use this route with an explicit 1:1 rearrangement and product formula C12H11N3. The source register records NCERT XII Laboratory Manual Unit 10, Experiment 10.5, printed pages 111-113.

This is a correction to procedural specificity and coverage. It should not be misread as rejecting NCERT's alternative direct diazotisation/coupling route under weakly acidic conditions.

## F06 - Separating-funnel sequence

Direct funnel item now asks what must occur before draining the lower layer. Explanation includes contacting/mixing, settling and draining; related old pairs replaced.

JEE-CHEM-1384 now asks about the stage immediately before draining. Its answer is to allow two distinct liquid layers to form. The explanation distinguishes contacting the solvents, settling and draining, avoiding the previous claim that the apparatus is used only after separation.

# Numerical and editorial corrections | F07-F10

## F07 - Stored unrounded value

JEE-CHEM-0510 unrounded scaled value corrected to 1000/(0.0821×300)=40.60089321965083. Integer answer remains 41. Option-dependent wording removed from all numerical alternatives.

All 270 alternatives were checked for stored value, scaling, integer rounding and option-independent wording. For calculation-backed alternatives, the rounded-givens sensitivity check also preserves the final integer.

## F08 - Floating-point display tails

Ten initial-rate stems formatted to readable significant figures; full stored precision retained for calculation. No long floating-point tails remain in printed stems.

## F09 - Chemical case

Whole-word lower-case hi corrected to HI wherever retained; old affected pairs replaced. Additional C-H, H-X, N-H, B/F and ln K notation corrected where found.

Formula-aware correction was targeted. Ordinary English text was not globally uppercased. In particular, the electrochemical relation is written ln K = nFE°/(RT).

## F10 - Misleading topic tag

All ten carbonate-bicarbonate questions now use the accurate topic Carbonate-bicarbonate mixture: acid consumption; science and key independently recomputed.

## Additional observations addressed

The two retained constant-result solution models were regenerated: molar mass in the evaporation model and composition in the density/molality model now vary. The former constant-result colligative-M cohort was replaced. A Fajans polarising-power application and actual Newman and sawhorse projection tasks were added. Parameter variants remain explicitly grouped and are not represented as independent topics.

# Final verification evidence

| Check | Result |
| --- | --- |
| Canonical record, ID and four-option integrity | PASS - 2,160 records |
| Per-record unit, class and difficulty preservation | PASS |
| Separate numerical recalculation | PASS - 1,450 MCQs / 141 models |
| Rounded-givens key and numerical sensitivity | PASS within stated precision scope |
| Numerical alternatives | PASS - all 270 |
| Full-field JSONL / CSV agreement | PASS |
| Student / teacher export agreement | PASS |
| Complete HTML question counts | PASS - 2,160 each |
| Published schema constructs | PASS |
| Required figure links and practical evidence | PASS |
| Constrained generator suite | PASS - 1,005 seeds; all 2,160 IDs selected |
| Individual errata closure tests | PASS - F01 through F10 |

The generator suite verifies 25 unique questions; 20 MCQ plus 5 numerical; 8/11/6 difficulty balance; 1/2/2 difficulty balance in Section B; five MCQ keys per letter; maximum three questions per unit; alternating 12/13 class split; family exclusions; and exact stem, key and figure projection.

Detailed evidence is provided in independent_numeric_results.json, independent_validation.json, generator_validation.json, generator_seed_evidence.json and errata_closure_tests.json. Errata_Closure_Register.csv contains all 1,195 finding/question associations, including replacement versus repair and final answers.

The final archive is checked separately after packaging. Its SHA-256 and archive-verification sidecar accompany the ZIP. This avoids attempting to embed an archive hash inside the archive being hashed.

# Coverage and retained blueprint

| Unit | Topic | Easy | Medium | Difficult | Total |
| --- | --- | --- | --- | --- | --- |
| 1 | Some Basic Concepts in Chemistry | 18 | 26 | 40 | 84 |
| 2 | Atomic Structure | 18 | 19 | 30 | 67 |
| 3 | Chemical Bonding and Molecular Structure | 18 | 24 | 10 | 52 |
| 4 | Chemical Thermodynamics | 18 | 29 | 40 | 87 |
| 5 | Solutions | 29 | 44 | 70 | 143 |
| 6 | Equilibrium | 18 | 37 | 50 | 105 |
| 7 | Redox Reactions and Electrochemistry | 32 | 46 | 60 | 138 |
| 8 | Chemical Kinetics | 29 | 45 | 60 | 134 |
| 9 | Classification of Elements and Periodicity in Properties | 37 | 71 | 0 | 108 |
| 10 | p-Block Elements | 53 | 79 | 0 | 132 |
| 11 | d- and f-Block Elements | 45 | 75 | 0 | 120 |
| 12 | Coordination Compounds | 45 | 75 | 60 | 180 |
| 13 | Purification and Characterisation of Organic Compounds | 26 | 48 | 30 | 104 |
| 14 | Some Basic Principles of Organic Chemistry | 48 | 72 | 10 | 130 |
| 15 | Hydrocarbons | 42 | 63 | 20 | 125 |
| 16 | Organic Compounds Containing Halogens | 31 | 36 | 20 | 87 |
| 17 | Organic Compounds Containing Oxygen | 33 | 37 | 20 | 90 |
| 18 | Organic Compounds Containing Nitrogen | 30 | 36 | 10 | 76 |
| 19 | Biomolecules | 32 | 36 | 10 | 78 |
| 20 | Principles Related to Practical Chemistry | 46 | 74 | 0 | 120 |
|  | TOTAL | 648 | 972 | 540 | 2,160 |

All 39 named practical entries retain at least one valid evidence ID after the replacements. The crosswalk was rebuilt from surviving questions; obsolete paired IDs were removed. The new conformation questions are JEE-CHEM-1457 and JEE-CHEM-1458.

Unit presence is not a promise of equal depth in every subtopic. The coverage map and explicit family register allow a teacher to judge that balance. The syllabus baseline remains NTA 2026; this release does not certify a later syllabus.

# Review scope, sources and use

## What the checks establish

The final files are mutually consistent; every retained or newly authored numerical model was evaluated separately from the authoring routine; option uniqueness and relevant domains were checked; all reported errata have traceable closure actions; and the constrained generator passed the documented seed suite.

Chemical review addressed the new template reactions, formulae, conditions, stoichiometry, explanations and answer alternatives, together with the explicitly affected retained records. Unchanged foundational content inherits the earlier review. This is not an independent human-panel certification or an empirical estimate of candidate difficulty.

Rounded-givens checks round recorded numerical inputs to the displayed authoring precision (seven significant figures for retained models, eight for new models). They are sensitivity checks, not a claim of manually re-transcribing every graph label. Retained diagrams are unchanged assets; the two new projection images were visually inspected.

Difficulty remains an editorial judgement based on the shortest intended solution. Passing numerical and structural tests does not prove every question is immune to every alternative interpretation. Closely related numerical variants are disclosed and mutually excluded; question count is not independent conceptual breadth.

## Primary correction sources

[NTA JEE Main 2026 syllabus](https://jeemain.nta.nic.in/document/syllabus-2026/)

[NTA JEE Main 2026 information bulletin](https://jeemain.nta.nic.in/document/ib-2026/)

[NCERT XII Laboratory Manual, organic preparations: Experiment 10.5](https://www.ncert.nic.in/pdf/publication/sciencelaboratorymanuals/classXII/chemistry/lelm110.pdf)

[NCERT XI Organic Chemistry: section 8.8.4, differential extraction](https://ncert.nic.in/textbook/pdf/kech202.pdf)

## Use the full bank

Extract the ZIP while keeping its folder structure. Open START_HERE.html, then choose the complete student or teacher bank. Search by ID, topic or keyword; filter by unit/difficulty; print the selection. Keep the figures folder beside the HTML files. Machine-readable files and the optional Python generator are included for integration.
