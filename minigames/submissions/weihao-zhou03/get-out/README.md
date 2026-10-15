# Get Out! Moving Walls: Cross Traffic

An individual variation by `weihao-zhou03`. Open `index.html` directly in a
browser; no installation, build, server, or model connection is required.

## Play this variation

- Arrows, WASD, on-screen direction buttons, or swipe: slide until a fixed
  wall, moving wall, or border stops you. Crossing the exit wins immediately.
- After a successful non-winning slide, **all moving walls** advance one rail
  cell simultaneously. Each reverses direction at its own rail endpoints.
- Space, **.**, or **Wait** keeps the player in place and spends one turn while
  the walls advance. A blocked direction spends no turn and moves no walls.
- Occupying a wall's next target holds that wall; other walls continue moving.
  Walls never push or crush the player. Rails are separate and cannot cross,
  so moving walls cannot collide or overlap with one another.
- A/B/C labels, distinct colors, and arrows identify every wall and its next
  direction. A dashed square with the same letter marks its next target.
  The target is entered only if it is free after the player's action.
- **OPTIMAL** shows the shortest escape from the initial board, counting Wait.
  Completion compares your turn count with this goal; matching it is optional.
- Undo restores the player and **every** wall's position/direction together.
  Reset restores all initial phases. Hints account for every wall and Wait.

## Challenge boards

| Board | Size | Fixed walls | Moving walls | Shortest turns |
| --- | --- | --- | --- | --- |
| Cross traffic | 7 x 7 | 8 | 2, horizontal + vertical | 10 |
| Three-way timing | 7 x 7 | 15 | 3, both movement axes | 9 |
| Clockwork maze | 8 x 8 | 16 | 3, both movement axes | 12 |

All three boards are unsolvable if the moving walls are removed. The first
acceptance route borrows brakes from both walls; the last borrows a brake from
all three. Route length establishes a mechanical property, not human difficulty.

## Design and exchange

The editor changes walls/start/exit around the existing rails. Rail cells
must stay open, and initial moving walls cannot overlap the start. **Clear
board** starts a static 7 x 7 board. There is no graphical rail-authoring tool;
new rails can be authored in exchange code or `levels.js`.

**Get current code** exports the complete initial puzzle, not a mid-game phase.
The code retains format `get-out-moving-walls-v1`, a `board` of S / E / # / .
strings, and `movers: [{path: [[row,column], ...], index, direction}, ...]`.
Coordinates are zero-based and direction is 1 or -1. Use up to three separate
straight adjacent rails, 2-20 cells each. One-wall and plain static codes still
work. Loading validates the full puzzle and dynamic route before replacing it.

For responsive exact hints, the conservative bound
`rows * columns * product(2 * rail.length)` must be at most 120000. Larger custom
combinations are refused before search, with a message to shorten rails or the
board; they are not falsely reported as unsolvable.

Trace format `get-out-moving-walls-trace-v2` records all initial/final phases,
all walls before/after each move, the optimal-turn goal, Wait, blocked inputs,
hints and Undo. Each
Undo event also records the restored player and walls. Traces record actions,
not intentions or feelings.

## Checks

From the full class repository root:

```sh
python scripts/minigames.py check --owner weihao-zhou03
python scripts/minigames.py test --owner weihao-zhou03
```

The browser/Node API is `create(board, {movers})`, `step`, `observe`,
`legalActions`, and `solve`. Static `create(board)` remains supported. The solver
keys the player position plus every wall's position and direction.
See `experiment.md` for self-play feedback, the peer-test plan and checks, and
`rule-source-map.md` for implemented rule evidence.

---

# Reference documentation (static game)

The notes below describe the source classroom workshop. The rules above govern
this moving-wall variation; the shared reference remains unchanged.

A classroom adaptation of Eric Zimmerman's **Get Out!**, exercise 11 in
*The Rules We Break* (printed pp. 90–97; game sheets pp. 185–189).
The interface and four teaching boards were created for this course.
The book's artwork, sample board, and prose are not bundled.

## Play

Open `minigames/get-out/index.html` directly in a browser. No installation,
build, account, API key, or runtime network connection is needed.

Alternatively, from the repository root:

```sh
python3 -m http.server 8000
```

Open <http://localhost:8000/minigames/get-out/>. For classroom phone access,
serve these static files through the course's approved hosting route.
A localhost URL belongs to the device running the server. Campus Wi-Fi may
prevent phones from reaching a laptop server. Hosting is not configured here.

- Move with arrow keys, WASD, swipe, or the on-screen direction buttons.
- Slide in one direction until a wall or the outside border stops you.
- Reach the exit to win, including when you encounter it during a slide.
- Blocked directions leave the board and move count unchanged.
- Undo reverses a successful move; reset starts a fresh attempt and trace.
- Optional hints reveal the next move on a shortest route from your position.
  Hint requests appear in the trace and completion message.

The border and mid-slide exit conventions are explicit classroom rules.
This version covers the basic wall puzzle, without the book's advanced pieces.

## In-game workshop guides

Open **Designer’s guide** or **Codex starter guide** from Workshop companions
beside the board (below it on phones). The guides expand within the game and
preserve the current puzzle. They are bundled with each scaffolded copy and
work offline, including inside the generated gallery. External installation
links need an internet connection. During a browser check, open both guides
after making a move and confirm the move count stays unchanged; arrow keys
used while focusing the guide should not move the player.

The designer's guide offers ten Schell-inspired questions with experiments
and observations, plus a human-playtest checklist. The Codex guide follows
play, exchange, and one plain-language request. The skill discovers the GitHub
login and creates the branch and copy; Codex handles checks and the later draft
PR. Building requires the full class repository, not just a downloaded gallery.

In the course's third edition, Schell's puzzle chapter is 14, with Lens 58;
chapter 13 covers balance. Guide text is original classroom interpretation.

## Design and exchange

Choose **Design a puzzle**, select a wall, clear, start, or exit tool, and
click/tap cells. A fresh board is 7 × 7. The editor preserves your current
game until you choose **Check & play**; Cancel returns to it.

Check & play verifies a single start and exit and at least one solution.
It does not reveal the solution. **Exchange a board** exports a plain-text
code that a partner can paste and load:

```text
S..#...
...#...
.......
..##E..
#......
.....##
#....#.
```

`S` is the start, `E` the exit, `#` a wall, and `.` an empty square. Boards
must be rectangular, between 2 and 20 rows and columns, with exactly one
start and exit. Invalid or unsolvable imports preserve the current game.
Boards and progress are kept in memory only. Copy the board code before
closing or reloading the page.

## Classroom sequence

1. Solve a sample in pairs. Predict each stopping point.
2. Design a board and record a solution privately.
3. Exchange board codes with a neighboring pair. Observe without coaching.
4. Discuss: When did a wall become useful? Did proximity to the door mean
   progress? What created a moment of discovery?
5. Inspect the trace. Distinguish legal moves, reaching the goal, efficiency,
   and the human experience.

Hints and traces support discussion; they are not a graded leaderboard.
The board uses symbols as well as color, visible focus, keyboard and touch
controls, status announcements, and reduced-motion preferences. The spatial
puzzle has not been validated as a complete screen-reader-only experience.

## Rules API and future agent scaffold

`engine.js` is dependency-free and shared by the browser and Node:

```js
const game = require('./engine.js');
let state = game.create(['S..', '...', '..E']);
const observation = game.observe(state);
const actions = game.legalActions(state);
state = game.step(state, 'right');
```

- `create(board)` validates and creates an initial state.
- `observe(state)` returns a detached, fully visible board, player position,
  move count, terminal flag, and legal actions.
- `step(state, direction)` returns the resulting state without mutating the
  input. It rejects unknown directions. Terminal states cannot move.
- `solve(state)` returns a shortest direction sequence, `[]` for a won
  state, or `null` if the exit is unreachable. It searches stopping positions.

`solve` is the instructor reference and hint provider. A future model player
should receive only observations and submit actions through a bounded runner;
keep solver answers and development tools outside that player's access.
There is no model player or live model connection in this minigame yet.

Trace downloads contain the starting board, attempted directions, outcomes,
undo and hint events, and final position. Coordinates in JSON are zero-based;
the visible trace uses one-based coordinates. Reset begins a new trace.

## Checks

From the repository root, with Node installed:

```sh
node --test minigames/get-out/tests/engine.test.cjs
```

The rules tests cover wall/border movement, blocked and invalid actions,
exit crossing, terminal behavior, shortest paths, unreachable exits, malformed
boards, detached observations, and the teaching boards' solvability.

Browser smoke check: finish the first board (down, right, down), undo, reset,
request a hint, edit a wall, play the custom board, export and reload its
code, reject an unsolvable code, and download a trace. Repeat movement with
phone controls and confirm the page fits the screen.

## Sources

- Eric Zimmerman, *The Rules We Break*, exercise 11, Get Out!, pp. 90–97.
- Author's printable game sheets: <https://theruleswebreak.com/gamesheets.html>.
- Course adaptation: original boards, browser interface, explicit border/exit
  rules, hints, undo, board exchange, and trace export.
