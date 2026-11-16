# Feast or Fiend — INITIAL PROJECT PLAN (G1)
Status: draft schedule pending official G2/G3 dates and team staffing.
## GATES AND DEADLINES
Nov 9, 2026 — first-round oral pitch (past)
Nov 15, 2026 at 11:59 p.m. — G1 post with recording, slides, Initial GDD, Initial Configuration, and plan
Nov 16, 2026 — G1 gate review / team formation
Nov 17, 2026 — expected Approve/Hold feedback
Nov 19, 2026 at 11:59 p.m. — two Braintrust replies
Nov 23, 2026 — expected graded feedback
G2 — [OPEN: copy exact official date from class schedule]
G3 — [OPEN: copy exact official date from class schedule]
WORKSTREAMS THROUGH G2
1. Concept / scope lock (Nov 16–19)
Owner: Project lead + design assistant.
Acceptance: one-page playable loop, IN/OUT list, accepted cut order.
Dependency: Gate feedback.
2. Engine skeleton (Nov 20–22, provisional)
Owner: Programming role.
Acceptance: boots locally; movement, collisions, seed pickup, combat test stub.
Dependency: Engine/project repository chosen.
3. Ingredient + cooking loop (Nov 23–25, provisional)
Owner: Programming + design.
Acceptance: carrot/lettuce pickups, ingredient inventory, at least two recipes, displayed unlock feedback.
Dependency: Data schemas and basic inventory.
4. Cake Boss scripted baseline (Nov 26–28, provisional)
Owner: Gameplay programmer + QA.
Acceptance: repeatable encounter with telegraphs, damage, death/restart, fixed action policy, deterministic logs.
Dependency: Combat and arena.
5. Agent integration and validator (Nov 29–Dec 1, provisional)
Owner: AI integration role + QA.
Acceptance: constrained action output, legality checks, 3-second timeout, scripted fallback, event logs.
Dependency: Stable scripted baseline.
6. Comparative prototype playtest (Before G2)
Owner: QA + project lead.
Acceptance: both variants playable, behavior logged, at least one player observation and design decision recorded.
Dependency: Scripted and agent modes.
## RISK MITIGATIONS
Technology HIGH: event-driven calls, validation, fallback, measure latency before extending AI.
Genre/Mechanics HIGH: end-to-end vertical slice; restrict ingredients, bosses, customer simulation.
Timeline HIGH: weekly scope check; first cut farming simulation, second cut restaurant simulation.
## AGENT TEAM ROLES
Design/Planning, Programming, QA, and Documentation assistants may propose work; project lead accepts/rejects decisions and reviews all changes.
## OPEN QUESTIONS
[OPEN] Actual team members and owners after Nov 16.
[OPEN] Official G2 date and acceptance requirements.
[OPEN] Source repository URL.
[OPEN] Model and deployment configuration.
