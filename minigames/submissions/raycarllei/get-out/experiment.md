# Get Out! Gradual challenge

Principle: sequence, with optional progressive hints, following the course
exercise card's application of Schell Chapter 14 and Lens 58: The Puzzle.

## Design and playtesting

- Decisions: Keep the four original boards and insert three bridge boards.
  Each bridge changes one or two walls from the following board, giving a
  related idea another try. The shortest routes now increase from 3 through
  9 moves. Each board names its learning goal. Players can step back or skip
  ahead. Switching starts a fresh attempt.
- Possible outcomes: Smaller structural steps may make the sequence easier
  to follow. Optional hints begin with a question, then outline a useful
  stopping point, then reveal one move. Repeated blocked moves or revisits
  offer help. Hints never move the player. The notebook remains optional.
- Playtest: My experience was that the game easily fell into two extremes:
  too easy and boring, or too difficult and completely stuck. It was hard
  to find a satisfying middle ground. TODO: Add the original board context
  and exchange the revised version with a peer. Record where a route became
  clear, hint tiers requested, skips, and one revealing remark.
- Next decision: The revision focuses on a smoother sequence and a choice
  of how much help to reveal. TODO: After peer play, decide which bridge
  boards and hint levels to keep or change. More moves alone do not prove
  greater difficulty; the revised experience still needs testing.

## Prediction

Proposed expectation: bridge boards will reduce abrupt transitions, while
players who find them easy can skip ahead. A contrary result would be that
players still abandon a board or cannot explain a move after a hint.
TODO: Supply the student's prediction before the next peer playtest.

## Checks

All 16 Node tests and the manifest check passed. Tests cover every reachable
teaching-board position, hint agreement with the solver, and optional-help
triggers. The movement engine is unchanged. Desktop, phone, and narrow-screen
browser checks passed; independent code review found no actionable issues.
