# Get Out! Route notebook

Principle: progress (visible progress), using the course exercise card's
application of Schell Chapter 14 and Lens 58: The Puzzle.

Status: working Codex proposal. Ray's design selection and human experience
evidence are pending. This draft does not report a completed peer playtest.

## Design and playtesting

- Decisions: The proposed change marks previously reached stopping positions
  with a dot and records their coordinates. A checkbox hides the notebook.
  The record includes the start and retains explored stops after Undo; Reset
  or a new board clears it. The visible-progress question is whether a
  truthful record of exploration helps someone choose a different route.
  Ray has not yet confirmed this proposal as his own design decision.
- Possible outcomes: Codex's proposed hypothesis is that a player will use a
  marked stop to avoid an unproductive repeat. Another possible result is
  that the dots distract the player or suggest misleading progress toward
  the exit. Ask what a dot means before interpreting faster completion as
  improved understanding. These are predictions, with no human results yet.
- Playtest: TODO: Ray should play the reference, design and exchange a board
  with a classmate, and supply his actual observation and chosen change.
  For a later comparison, give anonymous Player A a fresh board and observe
  whether a marked stop informs their next action. Record board, order,
  revisits, hints, resets, completion, and one revealing remark. Use a
  different player or alternate order for an on/off comparison to limit
  practice effects. Actual observations remain unfilled.
- Next decision: The proposed response is to keep the notebook if a player
  can explain a route choice using it, simplify it if it adds clutter, and
  revise its explanation if dots are read as distance to victory. TODO:
  Ray should accept or revise these conditions after playing. Deterministic
  checks cover history, reset inputs, input immutability and solver agreement.

## Prediction (student writes before building)

TODO: No student prediction was supplied before this prototype was built.
Record the timing honestly. Ray can review or change this proposed question
and make his prediction before the next design iteration and peer playtest.

## Implementation

The personal game copy contains `notebook.js`, a pure function that derives
unique stopping positions from successful moves. `app.js` renders those
positions, announces their count, records visibility changes in the trace,
and includes the notebook in downloaded traces. `index.html` adds the
checkbox, explanation, and coordinate list. `style.css` adds dots and
outlines. `engine.js` and `levels.js` are unchanged from the reference.

Checks run: `python3 scripts/minigames.py check --owner raycarllei` and
`python3 scripts/minigames.py test --owner raycarllei`. The manifest check
passed; all 10 Node tests passed (7 reference tests and 3 notebook tests).
Automated Chromium checks passed at desktop and phone widths: toggling,
blocked moves, Undo, Reset, hints, guides, editor cancel, custom-board import,
invalid-import preservation, trace download, keyboard input, and page width.
No browser page errors were recorded. Code checks establish specified behavior; they do not
establish a player's understanding or feelings.

## Playtest observations

TODO: No human observations supplied. Record anonymous labels only. The
reference play, board exchange, and observation must be completed by people.

## Interpretation and revision (student writes)

TODO: Ray should supply his interpretation and next decision. Keep observed
actions separate from explanations, and mention order and prior familiarity.

## AI assistance and human decisions

Codex proposed and implemented the optional notebook, wrote tests and this
draft, and ran the checks listed above. Ray requested completion of the work
Codex could perform independently; no design selection or human-play
observations have yet been supplied. The assignment does not require an
additional AI-use disclosure.

## Independent review

A separate read-only Codex reviewer compared the student copy with the
reference and found no actionable code issues. It independently reran all
10 Node tests, which passed. The engine and levels match the reference,
and the changes stay inside this student folder. The implementation session
ran the desktop and phone browser checks listed above. Human play remains
pending. Ray and the instructor retain approval decisions.
