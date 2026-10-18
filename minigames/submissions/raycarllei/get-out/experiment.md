# Get Out! Route notebook

Principle: progress (visible progress), following the course exercise card's
application of Schell Chapter 14 and Lens 58: The Puzzle.

Status: playable draft; human playtest observations and interpretation pending.

## Design and playtesting

- Decisions: Mark previously reached stopping positions with dots and list
  their coordinates. A checkbox hides the notebook. Undo retains explored
  stops; Reset or a new board clears them. The notebook records exploration,
  rather than distance to the exit.
- Possible outcomes: A player might use marked stops to avoid unproductive
  repeats. Dots might also distract them or suggest progress toward victory.
  Ask what a dot means and record whether it informs a route choice.
- Playtest: TODO: Play the reference, design and exchange a board with a
  classmate, and record actual observations. Compare notebook visibility
  using anonymous player labels. Record board, order, revisits, hints,
  resets, completion, and one revealing remark. Consider prior familiarity
  and practice effects when comparing runs.
- Next decision: Keep the notebook if it supports an explained route choice;
  simplify it if it adds clutter; revise its explanation if dots suggest
  distance to victory. TODO: Review these conditions after playing and
  supply the interpretation and chosen revision.

## Prediction

TODO: Supply a prediction before the next iteration and peer playtest.
No student prediction was recorded before this prototype.

## Changes after feedback

Undo now displays a reminder that explored stops remain recorded. When the
notebook is hidden, the reminder omits the stop count.

## Checks

The manifest check, 10 Node tests, desktop and phone browser checks, and
independent review passed. Movement rules, boards, the solver, and one-step
hints are unchanged. Human observations remain pending.
