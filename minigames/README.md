# Minigame lab

[Play Get Out](get-out/index.html), read the [student guide](STUDENT-GUIDE.md),
and choose an [exercise](EXERCISES.md). The reference has original boards and
runs in a browser with no build step, server, or model connection.

Each student makes an independent copy under
`submissions/<github-login>/get-out/`, then opens one draft pull request.
The instructor reference in `get-out/` stays available for comparison.

```sh
python3 scripts/minigames.py new YOUR-LOGIN --principle hints
python3 scripts/minigames.py check --owner YOUR-LOGIN
python3 scripts/minigames.py test --owner YOUR-LOGIN
python3 scripts/minigames.py gallery
```

Run these from the repository root, replacing `YOUR-LOGIN` with your lowercase
GitHub login. Open `build/minigames/index.html` for the generated gallery.
Every valid `submission.json` appears automatically. Leave generated files
uncommitted. CI uploads a downloadable gallery artifact; it does not publish a
website. The gallery includes the submissions present in that branch, so the
shared gallery grows as the instructor merges PRs.

See the [reference README](get-out/README.md) for controls, rules, attribution,
and deterministic engine interface. Keep copyrighted course books and private
feedback out of this public repository.
