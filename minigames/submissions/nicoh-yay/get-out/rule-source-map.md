# Variation rule map

| Rule | Evidence | Implementation | Test |
| --- | --- | --- | --- |
| Shoot only the first wall in an unobstructed row or column from the current position. Face points toward the shooter. No distance cap. | observed: student's explicit choice of straight-shot placement | engine.js:18 portalTarget; engine.js:31 placePortal | tests/portals.test.cjs |
| Enter only through the marked face; preserve the incoming travel direction at the output wall and continue sliding. If the output cell in that direction is blocked or outside the board, stop at the input wall. Two distinct walls required. Lone portal stays solid. Loops refuse the entire move. | assumed: implementation of student-requested direction preservation and existing directional entry; pending human play | engine.js:39 step | tests/portals.test.cjs |
| Hints solve moves with the current fixed pair; placement remains a separate player decision. | code | engine.js:72 solve | tests/portals.test.cjs |
