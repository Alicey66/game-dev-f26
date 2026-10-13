# Growing Challenge rules

This map stays inside the personal submission; the shared Garden Door map
belongs to a different game.

| Rule | Evidence | Test |
| --- | --- | --- |
| Levels 1–3 use 7 × 7; add one row/column every three levels, capped at 42; campaign ends after level 108 | code: generate-levels.cjs:10, levels.js:2 | campaign grows every three levels and stops at 42 |
| Budget is minimumMoves + floor(minimumMoves × (42 − max(7, rows, columns)) / 35) | code: engine.js:21 (create) | budget tapers from twice optimal to exactly optimal |
| A successful slide spends one move; blocked directions spend none | code: engine.js:35 (step) | blocked and unknown actions do not spend moves |
| Crossing exit wins, including on last allowed move; otherwise exhausting budget fails and freezes movement | code: engine.js:35 (step) | last allowed move wins; exhaustion fails and freezes movement |
| Hints and legal actions obey the move budget; observations expose public budget, minimum and failure | code: engine.js:40 (legalActions), engine.js:43 (observe), engine.js:47 (solve) | hints respect the remaining budget |
| Undo restores previous position/budget; reset starts the same level | code: app.js:80 (undo), app.js:81 (reset) | browser interaction checks pending |

Student request supplies growth, taper endpoints and failure. Implementation
choices are +1 per three numbered levels, linear taper rounded down, fixed
108-level campaign, using shortest route as expected moves, free blocked
inputs and retaining reversible undo. These are not human playtest findings.
