# Week 5: make one puzzle variation with Codex

You will change one aspect of Get Out, watch another person play, and prepare
one reviewable pull request. Work in your own folder and branch. Discuss ideas
and trade playtests with classmates; your design decisions and report are yours.

There is **no new submission due tonight**. A draft PR records progress.
The Motivation Atlas minigame remains due **October 18**, under its own
repository instructions. This exercise does not replace the midterm brief.

## 1. Open the repository and check your tools

Use the class repository `columbia-university-ai-games/game-dev-f26`.
If you already have it, open that checkout and run `git status` before pulling.
Save or commit your existing work on its own branch first. Avoid resetting a
dirty checkout to follow a class demo.

For a new checkout:

```sh
git clone https://github.com/columbia-university-ai-games/game-dev-f26.git
cd game-dev-f26
```

Run:

```sh
git status
git remote -v
python3 --version
node --version
codex --version
```

Use Python 3.11+ and Node 22+. On Windows, use `py` in place of `python3` if
that is your Python launcher. Python packages and cloud API keys are not
needed for this browser exercise. The native Codex app also works: open this
repository as the project and use its terminal for these commands.

Sign into Codex using the course's account instructions. Open it at the
repository root. Read `AGENTS.md`, then verify that the repository skill
`minigame-variation` appears in the skills list (`/skills` in the CLI).
Invoke it as `$minigame-variation`. If it does not appear, restart Codex after
updating the checkout. As a fallback, ask it to read
`.agents/skills/minigame-variation/SKILL.md` explicitly.

The skill is a small set of course instructions stored in the repo. It needs
no separate plugin installation. The baseline workflow needs no third-party
plugins or connectors. If the instructor demonstrates an optional plugin,
check its requested account access before connecting it. Coding-assistant
access and a model provider for your eventual playing agent are separate setups.

## 2. Play, choose, predict

Open `minigames/get-out/index.html` in your browser. On your computer it works
directly from the file. To serve locally instead:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Open `http://localhost:8000/minigames/get-out/`. Phone testing requires an
instructor-provided reachable URL or your approved local-network setup;
`localhost` on a phone points to that phone.

Play one board. Choose one question from [EXERCISES.md](EXERCISES.md). Write a
one-sentence prediction in your own words before implementation.

## 3. Make your own copy

In the commands below, replace `YOUR-LOGIN` with your lowercase GitHub login.
The example uses `hints`; choose your own principle ID from the exercise guide.
Start from an updated `main` with a clean working tree, then:

```sh
git switch -c YOUR-LOGIN/get-out-hints
python3 scripts/minigames.py new YOUR-LOGIN --principle hints
```

This creates:

```text
minigames/submissions/YOUR-LOGIN/get-out/
  index.html          # your playable entry point
  app.js, style.css   # interactions and appearance
  engine.js           # game rules, observations, and solver
  levels.js           # original boards you may replace
  tests/engine.test.cjs
  experiment.md       # prediction, evidence, and reflection
  submission.json     # gallery metadata
  README.md           # reference notes to adapt to your variant
```

The command refuses to overwrite an existing copy. Resume that folder and
branch if you already started. Keep a single evolving variation for this lab;
do not create a new folder for each revision. Only edit your own game folder.
The reference, gallery tooling, workflow files, and other students' games belong
to their owners. Report shared-tool issues to the instructor.

## 4. Build with a bounded Codex task

Start with this prompt, filled in with your own prediction:

> $minigame-variation My GitHub login is YOUR-LOGIN. My principle is hints.
> My prediction is: [your words]. Read my existing experiment.md and inspect my
> copy. Propose one small implementation and explain the affected files and
> checks before editing. Keep all changes inside my game folder. Implement the
> agreed change and run the relevant tests. Leave human playtest observations
> for me to supply.

Keep the task small enough to playtest today. Ask Codex to explain one changed
function. You should be able to trace how a player action changes game state.
For new rules, author or revise meaningful deterministic tests. For a visual or
wording change, check the actual browser behavior and layout.

Codex may record implementation facts, commands, and actual test results. You
write the prediction, interpretation, and AI disclosure. Keep unfinished
observations marked TODO; never substitute generated player reactions.

## 5. Test, trade games, and review

```sh
python3 scripts/minigames.py check --owner YOUR-LOGIN
python3 scripts/minigames.py test --owner YOUR-LOGIN
```

Open **your** `index.html`, not the reference. Test keyboard controls, reset,
undo, a win, hints, and narrow-screen controls. If rules change, check the hint
solver, editor validation, and move trace for consistency with the new rules.

Trade games with a neighbor and follow the human-playtest protocol in the
exercise guide. Record evidence in `experiment.md`, revise once if useful, and
update `submission.json` with a short descriptive title. Keep `schema: 1`,
`author` matching your folder, and `entry: "index.html"`.

Ask a separate Codex conversation or review task:

> Review only minigames/submissions/YOUR-LOGIN/get-out/. Compare my prediction,
> implementation, tests, and experiment report. Find concrete rule bugs,
> regressions, misleading feedback, unsupported experience claims, and changes
> outside my folder. Report findings with file references; do not edit or
> invent evidence. Tell me which checks you actually ran.

A code review is not a human playtest. Resolve useful findings and record the
review in your report. Once the report is complete:

```sh
python3 scripts/minigames.py check --owner YOUR-LOGIN --ready
python3 scripts/minigames.py gallery
```

Open `build/minigames/index.html`. Your card appears automatically. Leave
`build/` uncommitted. Validation checks structure and unfinished placeholders;
it cannot judge the quality or honesty of an experiment.

The lab accepts self-contained games with regular files, no symlinks, up to
2 MiB per file and 5 MiB per game. Avoid network dependencies, tracking, API
keys, and personally identifiable playtest data. Ask about larger assets before
adding them. The repository and its PRs are public.

## 6. Make one draft PR

Review and stage only your folder:

```sh
git status --short
git add -- minigames/submissions/YOUR-LOGIN/get-out/
git diff --cached --stat
git diff --cached
git commit -m "Add YOUR-LOGIN Get Out hints experiment"
```

**If you have write access to the class repo:** confirm the remote pointing to
`columbia-university-ai-games/game-dev-f26`, then push your branch to it. In a
fresh clone above, that remote is `origin`:

```sh
git push -u origin YOUR-LOGIN/get-out-hints
```

**If you use a fork:** push your branch to your fork remote. Open a PR from
`YOUR-LOGIN:YOUR-LOGIN/get-out-hints` into the class repository's `main`.
Your fork's name does not change the required folder ownership.

On GitHub select **Create draft pull request**, target the **class repo's main**,
and use the `minigame` PR template if prompted. Link the experiment report and
any existing Asana task. Do not make a second GitHub planning backlog.

If you use the GitHub CLI, you can use your report as the PR body instead:

```sh
gh pr create --repo columbia-university-ai-games/game-dev-f26 --base main --draft --title "YOUR-LOGIN: Get Out hints experiment" --body-file minigames/submissions/YOUR-LOGIN/get-out/experiment.md
```

For a fork, add `--head YOUR-LOGIN:YOUR-LOGIN/get-out-hints` to that command.
Commit and push later revisions on the same branch; the same PR updates.
Leave it draft while evidence is incomplete. Request review when ready.
Instructor review controls merging. Automated checks do not award a grade.

## When something goes wrong

| Symptom | Next step |
| --- | --- |
| Skill is missing | Restart Codex in the repo; explicitly read the SKILL.md fallback above. |
| `Already exists` | Resume your existing copy. The scaffold protects your work. |
| Boundary check fails | Review the Files changed list. Keep only your own game folder in this PR. Ask for help before restoring files with other work in them. |
| Cannot push to the class repo | Use your fork or keep a local commit and show it to the instructor; access trouble is not a reason to share credentials. |
| Tests pass but play feels wrong | Observe a human player and review the design prediction. Tests cover specified behavior. |
| Hint becomes incorrect | Check whether you changed rules without updating the solver. |
| Other variants are missing | Update from the class repo after they are merged and regenerate the gallery. |
| PR artifact contains unfamiliar code | Inspect the diff before opening it. The gallery executes the games locally when played. |

Official reference: [Codex skills](https://learn.chatgpt.com/docs/build-skills).
