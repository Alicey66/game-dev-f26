# Variation rule and display map

All movement rules remain identical to the course reference in `minigames/get-out/engine.js`.

| Display rule | Implementation | Evidence | Check |
| --- | --- | --- | --- |
| Record start and each distinct successful arrival, not crossed floor cells. | `exploration.js`: `start`, `record`; `app.js`: `move` | assumed: new designer-selected variation; course EXERCISES.md `progress` suggests visited stopping positions | `tests/exploration.test.cjs` distinct stops and blocked moves |
| Undo preserves discoveries in this attempt; reset, next board, and valid board import start a new record. | `app.js`: `load`, Undo handler, `refreshExploration` | assumed: explicit on-screen design convention | notebook tests and browser smoke checks |
| Dots indicate explored locations, not distance or percentage toward solving. | `index.html`: Exploration notebook; `style.css` | code: course EXERCISES.md warns straight-line distance is not reliable progress | visible wording and narrow-screen browser checks |

No new legal actions, movement rules, success conditions, or solver answers are introduced. Notebook data is display-only; it is added as optional metadata to the downloadable trace. The solver does not receive or depend on it.
