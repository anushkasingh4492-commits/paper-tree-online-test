# Authoring records

The canonical current bank is the root jee_main_physics_v1.4.0.json file.
original_model_candidates.json contains 511 retained active candidates;
challenge_calculations.json contains 260 retained active model records.
revised_tasks.json, revised_tasks_v1_3.json and revised_tasks_v1_4.json contain
14, 24 and 6 active replacement tasks respectively. Together these account
for the 815 active model-derived questions checked by verify_release.py.

The numbered Python replacement modules document their corresponding authoring
stages. Apply later-stage overrides after earlier ones; a historical stage is
not a standalone rebuild of the current bank. In particular, the current 2129
record is in figure_tasks_v1_4.json and supersedes its v1.3 figure-task entry.
The original v1.3 entry is retained to make the correction traceable.

The current original-model candidate snapshots and the shared coil/ordinal
templates have been synchronized. Separate independent_* routines check the
printed current tasks; they do not import replacement answer expressions.
