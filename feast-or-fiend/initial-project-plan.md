# Feast or Fiend — Initial Project Plan (G1 → G2/G3)

**Status:** Initial G1 plan; proposed commitments, not verified builds  
**Owner:** Student as Executive Producer and Creative Director  
**Version:** 0.2 — November 15, 2026

> **Calendar basis:** G1 November 15/16, Braintrust replies November 19, and feedback by November 23 come from the G1 assignment. Dates for the November 23 technical checkpoint, November 28 first-playable recording, November 30 G2/G3, December 5 Gold recording, December 7 G4, December 14 G5, and December 17–23 presentations are **provisional dates taken from a classmate's Initial Project Plan**, not independently verified against the course syllabus. Confirm them with CourseWorks before relying on them.

## 1. Gate calendar and deliverables

| Date | Gate / checkpoint | Feast or Fiend evidence |
|---|---|---|
| **Nov 15, 11:59 p.m.** | G1 discussion post | 3–5 minute recording, Slides, Initial GDD, Configuration, Project Plan |
| **Nov 16** | G1 Concept review | Approve/Hold decision request for a narrow vertical slice |
| **Nov 17** | Expected gate decision | Record corrective work if Hold |
| **Nov 19, 11:59 p.m.** | Braintrust replies | Two specific notes on classmates with fewer than two replies |
| **Nov 23** *(provisional)* | Technical checkpoint | Deployed live model call, isolated encounter/session state, and forced-timeout scripted fallback |
| **Nov 23** | G1 graded feedback expected | Incorporate comments without inflating approved scope |
| **Nov 28** *(provisional)* | First playable recording | Capture a complete, reproducible ingredient → cooking → boss loop |
| **Nov 30** *(provisional)* | Combined G2 Prototype / G3 Production review | First playable, initial external playtest, scripted comparison, update GDD/configuration, risk register, feasible production scope |
| **Dec 5** *(provisional)* | Gold build recording | Record and identify the release candidate |
| **Dec 7** *(provisional)* | G4 Final / Pre-Launch | Gold build, evaluation harness, release instructions, final GDD/configuration |
| **Dec 14** *(provisional)* | G5 Retrospective / Closure | Final game, After-Action Review, final Playtest Log and archive |
| **Dec 17–23** *(provisional)* | Final course presentations | Design/engineering retrospective and walkthrough |

**Important constraint:** Nov 29–Dec 1 is too late for the original AI integration plan if G2/G3 occurs Nov 30. We must demonstrate the **minimal live agent + validator + timeout** by Nov 23, then integrate it into the first playable before Nov 28.

## 2. Gate decision and minimum prototype

**G1 approval request:** authorization to prototype one connected gameplay loop: get ingredients from carrot/lettuce enemies, cook one dish, see restaurant progression, and face a Cake Boss that reacts to a strawberry feeding event. Compare **bounded AI boss decisions** against a **scripted baseline** with identical abilities and game rules.

**Not authorized / deferred:** multiplayer, seasons, procedural map, multiple boss relationships, a broad farming economy, extensive customer AI, complete Dark Cuisine system, elaborate visuals.

**First cut:** replace growing crops with direct ingredient drops. **Second cut:** reduce restaurant management to menu unlock + price/progression feedback. **Never cut first:** authoritative state validation, scripted fallback, and a fair comparison.

## 3. Dependency-based tasks through G2/G3

| ID | Task / planned outcome | Owner; delegated role | Dependencies | Acceptance evidence | Priority |
|---|---|---|---|---|---|
| T1 | Confirm Godot 4 or an approved alternative; make runnable starter | Student; Tech Lead | G1 feedback | Project launches, scene loads, instructions recorded | P0 |
| T2 | Define world-state schema, boss action catalog, filtered observations | Student; Design Lead + Tech Lead | T1 | Engine owns HP, inventory and drops; action schema and hidden-state boundary documented | P0 |
| T3 | Create tiny map, movement, encounter trigger and restart | Student; Tech Lead + Art Lead | T1 | Player navigates, triggers arena and restarts | P0 |
| T4 | Implement simple ingredient pickups and recipe unlock | Student; Tech Lead + Design Lead | T2–T3 | Collect vegetable resource, cook, see unlocked dish and restaurant progress | P0 |
| T5 | Implement Cake Boss and deterministic scripted baseline | Student; Tech Lead + QA | T2–T3 | Repeatable legal attacks, telegraphs and deterministic logs | P0 |
| T6 | Implement deployed model call + validator + isolated session state | Student; AI/Tech Lead + QA | T2, T5 action schema | One real model decision is logged; response cannot write world state or leak unrelated sessions | P0 |
| T7 | Force model timeout/error and validate fallback | Student; QA + Tech Lead | T5–T6 | 3-second timeout triggers legal scripted action; no invalid state transition | P0 |
| T8 | Add strawberry feeding and deterministic Cake Boss transformation | Student; Design Lead + Tech Lead | T4–T5 | Same feeding rule and reward apply in AI and scripted modes | P1 |
| T9 | Integrate and record first playable | Student; Producer + Tech Lead | T3–T8 (except optional polish) | Recorded complete loop; both modes selectable; setup instructions work | P0 |
| T10 | Conduct external playtest and bounded agent evaluation | Student; QA + BI | T9 | Player actions observed; logs of latency, costs, invalid actions, tactics/replay; limitations stated | P0 |
| T11 | Revise one finding, rerun regression checks, compile G2/G3 evidence | Student; Producer + QA + Documentation | T10 | Change evidence; updated GDD/config, Initial Playtest Log, risk register, scope-lock recommendation | P0 |

**Accountability:** The student reviews all agent-generated code/content, accepts or rejects scope recommendations, and submits work; role agents cannot approve gate decisions.

## 4. Work cycles and internal checkpoints

**Cycle A — Nov 16–19: foundations.** Lock one tiny game loop; complete T1–T3 and start T5. Submit two Braintrust replies by November 19. Exit: a controllable player and documented boss action/state schema.

**Cycle B — Nov 20–23: technical checkpoint.** Prioritize T5–T7 over polish: one script-controlled boss, an actual deployed model call, state isolation, and forced-timeout fallback. Exit: reviewer can inspect one genuine model response and a repeatable timeout test. Do **not** label a fixture as live evaluation.

**Cycle C — Nov 24–28: first playable.** Complete T4, T8 if feasible, integrate modes, and record T9 by Nov 28. Exit: ingredient → cooking → reward → boss; both AI and baseline demonstrable. Cut simulated crop growth if it blocks the recording.

**Cycle D — Nov 29–30: evidence and G2/G3.** Run T10, apply a focused fix and finish T11. Deliver playtest observations, measured latency/cost, updated initial documents, full risk register, and production scope recommendation. Avoid adding new mechanics.

## 5. Risk register preview

| Dimension | G1 rating / evidence | Detection before G2 | Mitigation and cut |
|---|---|---|---|
| IP / Concept | **Low:** original food-boss theme; commercial game references only | Asset/source review | Original or licensed art, record sources/terms |
| Business / Audience | **Medium:** untested farming+combat audience | Voluntary recipe experimentation and replay | Focus on readable menu progress |
| Technology | **High:** LLM speed/validation in action setting unproven | Live call, p50/p95 latency, forced timeout, invalid-action test | Discrete decision points, validator and scripted fallback |
| Team | **Medium:** agent-generated work requires handoffs | Review quality and integration failures | Student approves changes, narrow role ownership |
| Genre / Mechanics | **High:** four coupled systems | Can tester finish loop without coaching? | One boss and recipe; cut detailed gardening |
| Timeline | **High:** checkpoint and playable are close | Missing P0 tasks, unrecordable build | T5–T7 first; cut cosmetic polish and economy |

**Shared High-risk cause:** ambitious integration against a compressed calendar. The critical path is **T1 → T2/T3 → T5 → T6/T7 → T9 → T10/T11**. Ingredient/cooking systems should be independently developed where possible.

## 6. G2/G3 evidence checklist

- [ ] Runnable first playable with setup/play/test commands and build SHA
- [ ] A real deployed model call and separate test showing state isolation
- [ ] Forced-timeout scripted fallback and invalid-output regression tests
- [ ] AI boss and comparable scripted encounter using the same abilities and rewards
- [ ] At least one external player observation and an Initial Playtest Log
- [ ] Actual latency, tokens, costs, and failure counts (not just G1 assumptions)
- [ ] Updated GDD and Configuration with implemented vs planned vs verified marked
- [ ] Updated Risk Register and feasible G3 production scope
- [ ] First-playable recording and evidence links; Asana ownership/tasks after G1

## 7. Open questions

- **[OPEN]** Verify the provisional post-G1 dates in the official course syllabus.
- **[OPEN]** Confirm engine/platform and hosting permissions (Cloudflare is the course-taught option).
- **[OPEN]** Select a live model/provider and secure credentials without committing secrets.
- **[OPEN]** Confirm real development hours and which student-directed agent roles are executable.
- **[OPEN]** Select a fair boss-behavior comparison and sample size for external playtest.
- **[OPEN]** Choose an appropriate high-risk cut if latency exceeds budget.
- **[OPEN]** Define internal Alpha/Beta readiness checks without inventing official course dates.

**G1 boundary:** Planned estimates and proposed scope are not evidence of implemented or verified gameplay; the instructor remains Gate Approver.
