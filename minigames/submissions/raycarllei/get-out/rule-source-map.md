# Route notebook evidence

| Behavior | Evidence | Implementation and check |
| --- | --- | --- |
| Movement, walls, border, exit crossing, hint solver | code: copied instructor reference | `engine.js`, unchanged; `tests/engine.test.cjs` |
| Record the start and the destinations of successful moves, once each | assumed: design choice based on the progress exercise in `minigames/EXERCISES.md`; human observation pending | `notebook.js`; `tests/notebook.test.cjs` |
| Blocked moves and passed-through tiles add no stopping position | code: `engine.js` returns the same state on a blocked move; trace records final destination | `notebook.js`; first notebook test |
| Undo keeps exploration history; Reset/new board clears it | assumed: history describes experienced stops | `app.js` loads a fresh trace on reset/board change; notebook tests and browser checks |
| Optional overlay does not change moves, legal actions, board, hints or outcomes | code: notebook only reads copied coordinates and trace | unchanged engine and levels; input-immutability and solver-completion test |
| Undo explains retained exploration history at the moment of use; a hidden notebook does not announce its count | assumed: contextual UI revision after feedback; human effect untested | `app.js` Undo handler and `index.html` notebook callout; desktop/phone browser regression |

The overlay presents already experienced destinations. It does not call the
solver or reveal a future stopping point. There is no model player or new
agent access in this variation.
