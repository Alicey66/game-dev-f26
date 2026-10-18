## Get Out: Exploration notebook

Adds one visible-progress variation in `minigames/submissions/alicey66/get-out/`. Movement, collision, exit detection, and the shortest-path solver remain unchanged. The shared reference and other students' folders are untouched.

## Design and playtesting

- **Decisions:** Add dots at reached stopping positions and a small coordinate notebook. The idea follows the class guide's application of Schell Chapter 14 and Lens 58: make progress visible. Here progress means remembering explored states, not being physically closer to the exit. Undo retains discoveries; Reset or a different board clears them. The intended benefit is less repeated guessing without revealing a solution.
- **Possible outcomes:** A player may notice a repeated stop and choose another direction, suggesting that the notebook supports route planning. Alternatively, they may ignore the dots, find them distracting, or avoid a necessary revisit because it looks "finished." Those outcomes would suggest poor visibility, clutter, or misleading framing. Completing a board faster alone would not establish understanding.
- **Playtest:** No classmate or human playtest is claimed. Automated simulation ran 100 seeds per policy on each of four boards. A random legal-action baseline was compared with a policy that prefers unvisited stopping positions using one-step lookahead. On the first board, mean moves were 8.35 versus 4.04, and mean revisits 4.61 versus 0.27. This tests different agent policies, not the causal effect of dots on people. Planned human test: observe Player A on an unfamiliar board without coaching; record revisits, hints, resets, completion, and whether the notebook informs a stated decision. Ask "What changed your understanding?" Counterbalance reference/variation order across players and boards if available.
- **Next decision:** Keep the notebook if players use it to plan while recognizing that revisiting can be useful. If they treat dots as solved cells, revise the legend or replace dots with an optional coordinate record. If they ignore it, investigate visibility before adding features. No conclusion about human confidence, fun, or understanding follows from the simulation. Checks and any remaining limitations are recorded below.

## Checks

- Submission validation passes.
- All 11 deterministic game/notebook tests pass.
- Reproducible automated simulation included (`simulate.cjs`, `simulation-results.json`).
- Browser checks at 320/390/1280px: movement, completion, hints, Undo/Reset, notebook updates, both guides, editor Cancel, imports, and trace payload pass with no overflow or page errors.
- Independent read-only review found no concrete issues and reproduced the simulation.
- Full Python suite: 43 tests pass using the locked environment. Gallery generation passes.
- Remote CI has not run; the PR is not yet created from this environment.

Reference manual play and peer board exchange have not been evidenced. This is a draft experiment with a concrete future human-test plan, not a report of a simulated person.
