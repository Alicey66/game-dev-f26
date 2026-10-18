# Route notebook evidence

| Behavior | Evidence | Implementation and check |
| --- | --- | --- |
| Movement, walls, border, exit crossing, hint solver | code: copied instructor reference | `engine.js`, unchanged; `tests/engine.test.cjs` |
| Record the start and the destinations of successful moves, once each | assumed: Codex design proposal based on the progress exercise in `minigames/EXERCISES.md`; not a student observation | `notebook.js`; `tests/notebook.test.cjs` |
| Blocked moves and passed-through tiles add no stopping position | code: `engine.js` returns the same state on a blocked move; trace records final destination | `notebook.js`; first notebook test |
| Undo keeps exploration history; Reset/new board clears it | assumed: Codex proposal; history describes experienced stops | `app.js` loads a fresh trace on reset/board change; notebook tests and browser checks |
| Optional overlay does not change moves, legal actions, board, hints or outcomes | code: notebook only reads copied coordinates and trace | unchanged engine and levels; input-immutability and solver-completion test |

The overlay presents already experienced destinations. It does not call the
solver or reveal a future stopping point. There is no model player or new
agent access in this variation.
