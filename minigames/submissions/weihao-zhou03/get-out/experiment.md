# Get Out! Moving Walls: Cross Traffic

Playable files: `minigames/submissions/weihao-zhou03/get-out/index.html`.
Open the HTML file in a browser; no build, installation, model or API key is
required. The Minigame lab workflow also packages this folder in its
`minigame-gallery` artifact.

## Design and playtesting

### Decisions

I changed the static puzzle into a timing puzzle with two or three moving
walls, more fixed obstacles, and both horizontal and vertical movement. After
one successful slide or Wait, every wall moves one rail cell. Letters, colors,
arrows and dashed targets show where each wall wants to move next. Wait lets
me advance the wall pattern without changing my position. The intended
experience is to plan my route ahead, including when a moving obstacle becomes
a useful stopping point.

This connects to Schell Chapter 14, Principle 10 (perceptual shifts), and Lens
58: a wall can be a tool as well as an obstacle. The sequence from two to three
walls also applies Principle 5 (gradual difficulty). I wanted a minimum-turn
goal to make planning more challenging. The interface now shows the solver's
OPTIMAL turn count from the starting board and compares it with a completed
attempt. Wait counts as one turn. The three goals are 10, 9 and 12 turns.

### Possible outcomes

- Expected: a player predicts a future stopping point, deliberately waits or
  holds one wall while others move, and uses that plan to approach the optimal
  turn count. That would support keeping predictable wall motion and targets.
- Alternative: a player repeatedly moves or waits without a stated plan, or
  copies hints without understanding the next stop. That would suggest the
  multi-wall sequence or its preview needs a simpler introductory example.
- Alternative: a player understands the pattern but finds waiting, corner
  traps, or the optimal goal frustrating. I would adjust rail phases or maze
  geometry and observe a fresh board before adding more complexity.

### Playtest: actual self-play and planned peer test

**My self-play feedback:** the variation felt harder than the reference. Moving
walls sometimes left me feeling stuck in a corner. Wait was useful for advancing
the obstacles, and I found the movement and previews generally easy to
understand. I wanted the design to encourage planning a route in advance and
wanted a minimum-turn challenge. Specific board/completion/hint counts were
not recorded, so these are qualitative observations from the author.

The OPTIMAL display was implemented after this feedback. Its effect on player
experience is still a prediction; its numerical correctness is checked
technically. No peer observations of this version are claimed.

**Peer-test plan:** ask an anonymous Player A to try the three boards without
coaching. Record version, order, completion, waits, hints, Undo/reset, and one
revealing action or remark. Watch whether waits have a clear purpose and whether
the player uses a moving wall as a brake on a new board. Ask "What were you
trying to do?" and "Which wall helped you find the route?" Compare the trace
with their explanation; actions alone do not establish intention or enjoyment.
A small classroom test and prior familiarity limit any conclusions.

### Next decision

I would keep the moving walls, Wait, and readable previews, and test whether the
optimal-turn target encourages planning. The next observation should focus on
whether getting stuck feels like a useful planning consequence or a reason to
stop playing. If traps cause abandonment, I would revise the relevant wall
phase or corner geometry; if the previews are confusing, I would simplify the
first board. If the goal makes players guess, I would give clearer preparation
for planning efficient routes. Escaping remains possible without matching the
optimal count.

**Known limit:** some reachable positions in the final maze have no forward
route to the exit. Wait cannot repair every such choice; the existing hint
reports no route and suggests Undo/reset. A regression test covers a concrete
case and verifies the previous state is recoverable. This is separate from the
initial boards, all of which are solver-verified as solvable. Rails are separate
and support up to three walls; large custom phase combinations are refused
before expensive searches. The graphical editor can edit around existing rails,
but does not paint new rails. Physical phone swipe gestures are not verified.

## Checks and review

- Owner metadata validation and ready-report validation: passed for
  `weihao-zhou03`.
- Game rules: 31 passing Node tests. Static and single-wall compatibility,
  simultaneous movement, independent holds, malformed/crossing rails, complete
  observation/exchange, terminal freeze, dynamic no-route detection and all
  three acceptance routes are covered. Reachable-phase traversal checks actor
  separation and Wait previews.
- Browser checks already cover all three routes, blocked input, Wait,
  full-phase Undo/reset, target arrows, hints, exchange, invalid-import safety,
  editor protection and both guides. Revision-2 checks showed no horizontal
  overflow at 351px/1280px CSS widths and no console errors.
- Final browser checks: all three optimal routes display 10/9/12 and the
  matching completion result. The target stays fixed through Wait/Undo,
  hides while editing, and recomputes on level changes and custom import/reset.
  A static two-turn puzzle completed in four turns correctly reports two fewer.
  The final maze's no-route hint and Undo recovery work. The new counter fits
  the narrow viewport; no console errors were recorded.
- Independent code review: no findings; the reviewer reproduced 31 passing
  tests and reviewed all student files, including the target calculation,
  evidence distinctions, and documented dead-end regression.
- Earlier shared Python checks: 32 passed, three environment errors (Windows
  symlink privilege and missing `anthropic`); the separate Pyxel starter also
  lacks `pyxel`. These do not affect this standalone JavaScript game. No shared
  code or machine permissions were changed to work around them.

All changes are confined to this author's game folder. Technical checks and
code review are distinct from my self-play feedback and the planned peer test.
