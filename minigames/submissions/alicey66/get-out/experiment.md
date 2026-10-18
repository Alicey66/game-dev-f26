# Get Out experiment: alicey66

Principle: progress (visible progress).

## Prediction and proposed decision

Proposed before implementation: mark distinct reached stopping positions so a player can recognize repeated routes and choose an alternative without being shown a solution. This is a Codex-proposed draft following the student's request to choose and build a variation. The student still owns the final design decision. Predicted human behavior: consult the marks after a repeated stop. An alternative is to ignore them or mistakenly avoid necessary revisits. The text explicitly labels exploration rather than closeness to victory.

## Implementation

`exploration.js` stores immutable lists of visited stop coordinates; `app.js`, `index.html`, and `style.css` display them. The start is included. Only successful arrivals count; crossed cells do not. Undo preserves knowledge, reset/new board clears it. Editor cancel preserves the attempt; successful imports reset it. Trace downloads include notebook metadata. `engine.js`, `levels.js`, and the solver are copied unchanged from the reference.

The new notebook tests were written first and initially failed because the module did not yet exist. After implementation, `python3 scripts/minigames.py check --owner alicey66` passes and `python3 scripts/minigames.py test --owner alicey66` passes all 11 tests (7 inherited engine checks and 4 notebook checks). The local display-rule map is `rule-source-map.md`.

## Actual automated observations

No human or classmate is simulated or impersonated. `simulate.cjs` runs four boards, 100 seeds per board and policy, with a budget of 200 legal moves per episode. Both policies use the same engine. The baseline chooses legal moves uniformly; the notebook policy prefers unvisited endpoints, requiring perfect-information one-step lookahead. The full reproducible results are `simulation-results.json`.

| Board | Baseline completion | Notebook-policy completion | Baseline mean moves, all episodes | Notebook-policy mean moves, all episodes |
| --- | --- | --- | --- | --- |
| Find your feet | 100/100 | 100/100 | 8.35 | 4.04 |
| Take the long way | 100/100 | 100/100 | 42.25 | 11.61 |
| Change direction | 92/100 | 100/100 | 67.80 | 10.78 |
| A useful detour | 72/100 | 100/100 | 116.13 | 13.90 |

Unfinished episodes contribute their attempted moves to the all-episode mean; success-only means are separately reported in JSON. These are agent-policy results, not human completion times.

## Planned human playtest

TODO: actual manual reference play and peer board exchange are not evidenced. No anonymous human label is used for a bot.

For a future Player A session, give an unfamiliar board and watch without coaching. Record board/version/order, repeat stops, hints, resets, completion, and any decision referencing the notebook. Ask "What were you trying to do?" and "What changed your understanding?" With more participants, counterbalance order and boards to reduce practice effects. Ask whether a visited mark means a place can never be useful again, to check for misleading progress cues.

## Interpretation and next decision

The simulation shows that a policy using explored-state memory can outperform this random baseline on these boards. It does not show that the UI teaches people to use that policy, nor establish confidence, satisfaction, or puzzle difficulty. Different policies are a confound; random seeds are not independent human participants. Keep marks if players use them without treating them as completed subgoals. If they avoid useful revisits, revise the legend or try a coordinate-only notebook. If the panel is ignored, first test its placement. No design revision based on invented human feelings has been made.

## Checks and independent review

- Submission check passes; 11 owner game tests pass. All repository game tests pass and the gallery builds.
- `uv run --frozen python -m unittest discover -s tests -v`: 43 tests pass. The first run without the locked environment failed on a missing `anthropic` dependency; installing the lockfile environment resolved it without changing project dependencies.
- Headless Chromium checks at widths 320, 390, and 1280 pass: arrows/Space/Enter-compatible native controls, touch direction buttons on phones, successful and blocked moves, Undo, Reset, unchanged hints, both workshop guides preserving state, editor Cancel, level changes, all four solver routes, valid board import, rejected unsolvable import preserving state, and generated trace JSON with explored coordinates. Zero horizontal overflow and no page errors. The trace payload was verified; an operating-system save dialog was not assessed.
- An independent read-only Codex review compared the variation to the reference, ran all 11 tests, and reproduced the simulation JSON. No concrete findings. It confirmed that movement and level files exactly match the reference, display conventions agree with the code, the diff stays within the owner folder, and synthetic evidence is labeled accurately. This is code review, not human experience evidence.
- The local environment has no authenticated GitHub CLI session; no push, PR, or remote CI result is claimed. The user's Windows session previously verified the GitHub login Alicey66; its lowercase spelling is used for this draft's ownership.

Code review does not substitute for a human playtest. The student and instructor retain approval and merge decisions.
