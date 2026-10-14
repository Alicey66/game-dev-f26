# Get Out experiment: liangl5

Principle: perception

## Prediction (student writes before building)

TODO: Describe one design change, the player behavior you predict, and what
observation would make you question that prediction.

## Implementation

Changed files (all in `minigames/submissions/liangl5/get-out/`):

- `engine.js`: state tracks a `visited` set (the start square counts from the
  first move). Sliding onto a visited square ends the run with `died: true`;
  dead states cannot move. `observe()` exposes `died` and `visited`. The solver
  searches position + visited set, so hints and the editor's solvability check
  respect the ice rule.
- `app.js`: paints used squares as ice, adds "cracked ice" to cell labels,
  records `died` in the trace, and restarts the board 1.2 s after a fall.
- `style.css`: `.cell.visited` ice styling.
- `levels.js`: boards 3 and 4 were unsolvable under the ice rule, so each
  gained one wall. "Change direction" adds a wall at row 5, column 3 (shortest
  route 8 moves, vs. 7 in the reference). "A useful detour" adds a wall at
  row 5, column 4 (7 moves).
- `tests/engine.test.cjs`: every teaching board must be solvable without
  falling; new tests cover falling through ice (including the start square)
  and the solver rejecting a board that only the reference rules can solve.

Rule change: re-entering any square you have already slid across ends the
attempt. Everything else (slide to wall/border, mid-slide exit, undo, reset,
hints) is unchanged.

Checks: `node --test minigames/submissions/liangl5/get-out/tests/engine.test.cjs`
→ 9 passed, 0 failed. `python scripts/minigames.py check --owner liangl5` → passed.

## Playtest observations

Player A played the thin-ice variation's teaching boards.

Observed:

- Time to first move rose sharply. Before touching a key, Player A stopped to
  map out the whole route as efficiently as possible.
- On some levels Player A showed frustration at first, and described solving
  them as very rewarding.

Not recorded: exact boards and order, hint requests, number of falls/restarts,
and timings. Player A's familiarity with the reference game was not noted.

Interpretation (designer's, not observed): the reward after solving came from
the difficulty increase.

## Interpretation and revision (student writes)

TODO: Compare the evidence with the prediction. Mention prior familiarity,
practice effects, sample size, or other limits. Describe the revision made or
one next test. A single player's response supports a question, not a general claim.

## AI assistance and human decisions (student writes)

TODO: State what Codex generated, what you checked, and one design decision you
retained or changed. Include any remaining known issues.

## Independent review

TODO: Record reviewer role, issues found, tests or browser checks repeated,
and your resolution. A fresh Codex review can check code; human play supplies
experience evidence. The student and instructor retain approval decisions.
