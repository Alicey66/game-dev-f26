# Moving Walls: rule and source map

Scope: this student's browser minigame only. The shared Garden Door map and
reference minigame are outside the variation's scope.

The student chose moving blocks, one wall step per player action, then more
obstacles and multiple directions. Detailed hold/rail/input limits are local
implementation choices, not claims about the book or human play evidence.
Every `code` label below is backed by implementation and acceptance tests;
none establishes human enjoyment or comprehension.

| Rule | Implemented evidence |
| --- | --- |
| Slide until a fixed wall, a wall's current position, or the border; crossing the exit wins immediately. | `code`: `engine.js:67` (`step`); static compatibility and multi-wall brake tests. |
| After a successful non-winning slide or Wait, all moving walls advance one cell simultaneously using their own phase and the player's final cell. | `code`: `engine.js:67`; opposite-direction movement and independent-hold tests in `tests/multiple-walls.test.cjs`. |
| Each wall bounces at its endpoints. It pauses if its next target contains the player; other walls continue. No wall pushes or crushes the player. | `code`: `engine.js:57` (`advanceWall`); endpoint, occupied-target and independent-hold tests. |
| A board has at most three separate straight contiguous rails, 2-20 cells each. Rail cells are floor/start terrain, cannot cross or overlap, and initial walls cannot cover the player. Walls never collide with each other because their rails are disjoint. | `code`: `engine.js:6` (`create`); malformed rails, crossing rails, maximum count and reachable-phase separation tests. |
| Wait keeps the player still and spends a turn. Blocked directions spend nothing and move no walls. Static boards do not offer Wait. | `code`: `engine.js:67` and `engine.js:87` (`legalActions`); refused action and static compatibility tests. |
| Undo/reset restore every wall's position and direction with the player. Winning freezes all actors. | `code`: `app.js:133` and `app.js:134`; `engine.js:67`; terminal-freeze test and browser lifecycle checks in `experiment.md`. |
| Observations detach all visible rail/phase/target data. Solving includes Wait and keys every wall's position/direction as well as the player. | `code`: `engine.js:93` (`observe`) and `engine.js:106` (`solve`); detached observation, different-phase and three-board route tests. No model player is added. |
| The exact search admission bound is rows * columns * product(2 * rail.length) <= 120000. Unsupported combinations are rejected before solving, not called unsolvable. | `code`: `engine.js:53`; oversized-phase validation test. |
| A/B/C and colors identify walls; arrows and dashed letters show next targets. A target is entered only if the player's final cell does not occupy it. Winning walls show completion checkmarks. | `code`: `app.js:64` (`updateActors`) and `app.js:72` (`renderBoard`); occupied-target observation test and browser preview/completion checks. |
| Board exchange preserves all initial phases; trace v2 records all walls before/after moves and restored phases on Undo. | `code`: `puzzle-code.js:5`, `puzzle-code.js:8`, `app.js:109` and `app.js:159`; multi-wall roundtrip and browser trace checks. |

Tests: `tests/engine.test.cjs`, `tests/moving-walls.test.cjs`, and
`tests/multiple-walls.test.cjs`. Nine original new rule tests failed before the
single-wall engine change. Seven additional multi-wall tests failed before
revision 2 support was implemented. Current total: 31 passing tests, including a dynamic dead-end regression prompted by the author's self-play feedback.

The three boards have 8/15/16 fixed obstacles and 2/3/3 moving walls. Their
acceptance routes take 10/9/12 turns, respectively; the final route uses every
moving wall as a brake. All three have no route if the moving walls are removed.
These are mechanical facts checked in tests, not human difficulty assessments.

## Optimal-turn challenge

`code`: `app.js:29` computes the exact initial route length using the existing
phase-aware solver. `app.js:113` compares a finished attempt with that fixed
target. Wait costs one turn and blocked directions cost none, as the engine
already specifies. Undo keeps the target, reset recomputes the same initial
target, and custom imports get their own target. The original 10/9/12 route
length tests and final browser lifecycle checks establish the displayed value;
the motivational benefit remains a design prediction.

Some final-maze positions have no forward solution, even after Wait.
`tests/multiple-walls.test.cjs` supplies a concrete reachable sequence; the
solver returns null there and the hint recommends Undo/reset. This is a known
level-design limitation, not a claim that every position is solvable.
