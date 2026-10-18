# Get Out! Route notebook

Principle: progress (visible progress), following the course exercise card's
application of Schell Chapter 14 and Lens 58: The Puzzle.

Status: playable draft; student experience recorded, peer comparison pending.

## Design and playtesting

- Decisions: Mark previously reached stopping positions with dots and list
  their coordinates. A checkbox hides the notebook. Undo retains explored
  stops; Reset or a new board clears them. The notebook records exploration history.
- Possible outcomes: A player might use marked stops to avoid unproductive
  repeats. Dots might also distract them or suggest progress toward victory.
  Ask what a dot means and record whether it informs a route choice.
- Playtest: My experience was that the game easily fell into two extremes:
  too easy and boring, or too difficult and completely stuck. It was hard
  to find a satisfying middle ground. TODO: Add the board and play context,
  confirm the board exchange, and compare notebook visibility with a peer.
  Record route choices, revisits, hints, and prior familiarity.
- Next decision: The difficulty gap suggests checking whether the notebook
  helps a stuck player choose a new route while preserving the puzzle's
  challenge. TODO: Compare an easy board and a difficult board with a peer,
  then choose whether to keep, simplify, or revise the notebook.

## Prediction

TODO: Supply a prediction before the next iteration and peer playtest.
No student prediction was recorded before this prototype.

## Changes after feedback

Undo now displays a reminder that explored stops remain recorded. When the
notebook is hidden, the reminder omits the stop count.

## Checks

The manifest check, 10 Node tests, desktop and phone browser checks, and
independent review passed. Movement rules, boards, the solver, and one-step
hints are unchanged. A peer comparison remains pending.
