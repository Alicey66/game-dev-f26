---
name: minigame-variation
description: Use when a student creates, revises, tests, or prepares a Get Out puzzle variation for the class repository and needs the scaffold commands, experiment report, or submission workflow.
---

# Minigame variation

This is the command reference for the Get Out classroom lab. Read root
`AGENTS.md`, `minigames/STUDENT-GUIDE.md`, and `minigames/EXERCISES.md`.
Run commands from the repository root. Read `git status` before editing.

## Inputs and workspace

Identify the student's lowercase GitHub login, chosen principle ID, and their
prediction. Infer these from an existing manifest/report when available; ask
for missing inputs. Preserve unrelated changes. Use the existing student
branch, or create `<login>/get-out-<principle>` from the agreed clean base.

If the student's copy does not exist, run:

```sh
python3 scripts/minigames.py new <login> --principle <principle>
```

If it exists, resume it. All changes for this PR belong in
`minigames/submissions/<login>/get-out/`. Shared scripts, reference game,
workflows, skills, and other students' folders are instructor-owned.

## Build and evidence

1. Read the existing game and report. State one proposed change, its affected
   files, and the tests/browser checks that will demonstrate its behavior.
2. Implement the student's selected change. For rule changes, update relevant
   tests and check solver/hint consistency. Keep the game self-contained.
3. Run the commands below, then open the student's game and check the changed
   interaction plus reset, undo, completion, hints, and narrow-screen controls.
   If browser access is unavailable, say which checks remain for the student.
4. Record implementation facts and actual test results in `experiment.md`.
   The student supplies their prediction, interpretation, and AI disclosure.
   Human observations come from actual play. Missing evidence remains TODO.
5. Request a separate review task/conversation scoped to the student's folder.
   Review can inspect code and evidence; it cannot supply human experience.
6. Help the student resolve findings, inspect the diff, and prepare one draft
   PR following the guide. Stage only the student's folder. Preserve the
   instructor's merge decision and existing course deadlines.

```sh
python3 scripts/minigames.py check --owner <login>
python3 scripts/minigames.py test --owner <login>
python3 scripts/minigames.py gallery
```

Before marking ready for human review, complete the report and run:

```sh
python3 scripts/minigames.py check --owner <login> --ready
```

Update `submission.json` title and principle as needed; author matches the
folder and entry stays `index.html`. The gallery discovers this manifest.
There is no shared index to edit. Generated `build/` stays uncommitted.

## Example task

“My login is alice. I chose hints. My prediction is that a question before a
move reveal will help a player explain their next decision. Create my copy,
propose the smallest change, and run checks. I will supply playtest evidence.”

Use `new alice --principle hints` once, work only in Alice's folder, and leave
human observations unfinished until supplied. A draft PR can record progress.
The October 18 Motivation Atlas contribution follows its own repository's
contract; this skill does not treat Get Out as automatic Atlas completion.
