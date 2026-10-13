# Get Out experiment: nicoh-yay

Principle: perception

## Prediction (student writes before building)

TODO: Describe one design change, the player behavior you predict, and what
observation would make you question that prediction.

## Implementation

Student request: “I want the walls to teleport you to another wall/direction (not randomly since it would be too hard) ... actively use like a portal gun ... then make the animations for moving smoother.”

Implemented selected blue/orange wall portals and chosen exit directions in engine.js/app.js/index.html/style.css. Hints share the engine rules; observe exposes detached portal state. Added tests/portals.test.cjs and rule-source-map.md. Rule interpretation remains assumed pending student play. New tests failed before implementation because placePortal was absent.

Checks: minigames.py check --owner nicoh-yay passed; minigames.py test --owner nicoh-yay passed all 11 tests. Browser: placed A on row 1 column 2 facing left and B on row 5 column 5 facing up on first board; right completed in one move; undo restored start and pair; hint suggested right. Reset cleared portals; Check & play returned the editor board to play; 390px viewport had no horizontal overflow and down button moved the player.

Board exchange preserves the original layout, not portal placement; custom boards retain baseline solvability requirement.

## Playtest observations

TODO: Record anonymous player labels, board, version and order played, hints
requested, restarts, completion, and one revealing action or remark. Separate
observations from interpretations. No names, emails, or other personal data.

## Interpretation and revision (student writes)

TODO: Compare the evidence with the prediction. Mention prior familiarity,
practice effects, sample size, or other limits. Describe the revision made or
one next test. A single player's response supports a question, not a general claim.

## AI assistance and human decisions (student writes)

TODO: State what Codex generated, what you checked, and one design decision you
retained or changed. Include any remaining known issues.

## Independent review

Independent rules_review agent reviewed engine, UI and tests. Corrected map wording (edge walls are allowed) and README paths; documented baseline custom-board validation and board-code limitation. No other engine/boundary findings. This is code review, not human play evidence.

## Revision 2 — straight shots and directional faces

Student request: “you can click anywhere and just put it near the exit ... directional ... a block limit ... limited function with the movement”. Student chose: “Only place portals on walls reachable by a straight shot from the player; emerge through the clicked face.”

Removed direction selector. Wall target must be in the player's row/column with no wall in between. The portal faces back toward the shooter; player must enter that face. Available targets highlighted in gold and announced as clear shots. No extra distance cap. Pair persists while moving so players can navigate to a second firing position.

Six revised portal tests failed before implementation; all 13 engine tests passed after. Browser rejected the exit-adjacent wall from the start, placed A facing left on row 1 column 2, moved down and placed B facing left on row 2 column 6, moved up then right to emerge and slide left to row 2 column 1.

Independent rules_review found no engine/boundary bugs. Fixed mixed evidence labels and stale function line references; updated README. Human observations and interpretation remain TODO above.

Revision 2 browser checks: undo restored start and pair; hint reported no movement-only route with this pair (wording updated to suggest changing portals); reset cleared pair; phone direction controls completed the baseline down/right/down route. 390px viewport had no horizontal overflow.

## Larger board revision

Student requested a bigger, more complex default and copyable puzzle codes. Added three original generated/solver-selected boards: Switchback Vault (12×12, 19 moves without portals), Crosscurrent (14×14, 21 moves), Deep Labyrinth (16×16, 30 moves). Switchback Vault is now the default; all original boards remain in the selector. Each is solvable under the baseline slide rules and is available in puzzle-codes.md. Path length is a rule/route metric, not evidence of human difficulty. All 13 tests passed including replay of every board solution. Human play observations remain TODO.

## Revision 3 — preserve incoming direction

Student feedback: “the portaling is inconsistent ... portals ONLY shoot you out in a single direction which is the direction you came with ... ONLY put a portal ON the current column or row that you stand ON (both input and output portals)”.

Both placement slots enforce current row/column and clear shot. Portal exits now preserve incoming direction (right in/right out, down in/down out). Existing input face restriction remains. If the adjacent output square in that direction is a wall or outside the board, the input stays solid. The larger 12×12 default and 14×14/16×16 puzzle codes remain. Two new direction/blocked-output tests failed before the change. Missing human prediction, observations, interpretation and disclosure remain TODO.

Revision 3 validation: all 14 engine tests passed; scaffold check passed. Browser imported S.#... / ...... / #..E.. / ......, placed A at row 1 column 3 and B at row 3 column 1 from the starting row/column. Right reached the exit in one move by emerging rightward despite the output entry face pointing up. Undo restored start/pair; hint suggested right; reset cleared portals. Default browser board remains Switchback Vault, 12×12. Narrow controls were checked in the prior revision; direction preservation is covered by engine tests and desktop browser.

Independent full-folder review found no engine or player-boundary bugs. Restored loop-refusal regression, corrected solver line reference, and clarified the seven-board count. No merge/approval is claimed.
