# Get Out experiment: bgarakani

Principle: sequence — gradual difficulty

## Student's design decision

“make the size of the board increase for every 3 levels played until a maximum
of 42 by 42. also, make the number of moves capped at double the expected on
easy levels (7x7 grid) tapering down to exactly the number of minimum moves at
42x42. if the player does not complete the level by the given number of moves,
they fail.”

## Implementation choices

108 fixed levels, increasing side length by one every three numbered levels.
Replays/resets retain the current size. Budget uses the solver's shortest route:
M + floor(M × (42 − N) / 35). Final-move exit wins; other exhausted attempts
fail. Blocked moves are free; undo/reset remain available. Generated boards are
solvable; larger boards are not yet proven harder for humans. The first three
boards preserve the class reference. See rule-source-map.md and README.md.

## Planned human playtest — not observations

Proposed prediction for student confirmation: decreasing slack encourages
planning stopping points. Alternative outcome: larger grids and strict budgets
cause guessing or frustration. Have a neighbor try levels 1, 4 and 106, recording
hints, resets, completion and one anonymous explanation of their next move.
If planning increases, retain the taper; if readability or frustration dominates,
consider larger board display or a gentler taper. These are proposed interpretations,
not statements supplied by the student.

TODO: Student supplies their prediction, alternative outcome and interpretation
after an actual peer test. No human playtest was run during implementation.

## Actual technical observations

Four new regression tests failed against the reference before implementation.
All 12 game tests passed after review, including solutions for all 108 campaign boards,
size progression, taper endpoints, terminal loss and final-move win.
Submission metadata validation passed. The default Python lacked anthropic;
rerunning in the existing repository virtual environment passed all 43 Python
tests. Offline/headless diagnostics passed in that environment (partial Setup
Verification only; no live model call). Browser control reported “No browser is
available”; visual layout, narrow-screen buttons, undo/reset/hint interaction,
editor and completion UI checks remain manual checks, not verified observations.

## Independent review

Independent rules reviewer found no blocking correctness issues. Addressed
their suggestions by adding an over-budget hint rejection test, requiring
exactly 108 levels in the campaign test, and adding source line references
to the rule map. Game tests and metadata checks were repeated after these
changes. Browser interactions remain unverified. No gate approval or merge
is implied.
