# Feast or Fiend — INITIAL CONFIGURATION DOCUMENT (G1)
Status: Initial proposal; no claim that components already work.
## PROJECT SETUP
Proposed engine: Godot 4; 2D pixel-art; desktop-first; local solo play; GitHub repository to be created/confirmed. Use original placeholder art while mechanics are validated.
[OPEN] Exact repository, engine minor version, runtime hosting, agent model/provider.
## AUTHORIZED AI TASK
The runtime boss agent chooses one encounter action at discrete decision points. It does not author arbitrary executable code, alter world state, fabricate ingredients, update rewards, read hidden map information, or modify player inventory.
## INPUT CONTEXT (ALLOWLIST)
- encounter_id, decision_id
- boss_type, phase, hp_bucket
- player_distance_bucket, player_recent_action
- offered_ingredient or null
- visible_nearby_entities with coarse relationship flags
- currently legal action IDs
No full world state, finances, hidden boss positions, personal user data, network credentials, or file-system access.
## OUTPUT CONTRACT
JSON-like action decision: {action_id: one of legal_action_ids, target_id: visible valid target or null}. No free-form narrative output is executed. Parser and validator reject unknown keys/actions/targets.
## VALIDATION AND FALLBACK
Game engine is authoritative. It validates action legality, cooldown, visibility, target type, and combat phase before applying state changes. At >3 seconds or any invalid response, use predetermined baseline action. Log fallback reason for tests.
## SCRIPTED BASELINE
Finite state machine chooses actions from the same action catalog with fixed priorities/cooldowns. Compare equivalent HP, damage, telegraphs, arena, drops, and transformation rules to isolate behavioral differences.
## BUDGETS — PLANNING ASSUMPTIONS
Latency target ≤2 s per model decision, hard timeout 3 s; only event-driven calls, not per frame. Target ≤$0.02/model cost per 15-minute test, assuming up to ~12 model decisions. Example provisional token math: 12 × 800 input = 9,600 input tokens; 12 × 150 output = 1,800 output tokens. At hypothetical $0.50/M input and $2.00/M output, cost = $0.0084. Actual provider rates and usage will be measured; these are not confirmed quotations.
[OPEN] Provider, pricing, prompts, retry strategy, and measured latency.
## TEST AND OBSERVABILITY
Record encounter variant, decision context hash, selected legal action, validation result, fallback, delay, model token usage, and outcome metrics. Compare playtest behavior across agent and baseline. Do not log unnecessary personal information.
AGENT TEAM ROLE COVERAGE (DEVELOPMENT ASSISTANTS, NOT NPCS)
- Design/Planning agent: proposes mechanic refinements and challenge cases; no autonomous scope changes.
- Programming agent: helps implement Godot systems and tests, subject to review.
- QA agent: designs scripted-vs-agent checks, invalid-action tests, and playtest forms.
- Documentation agent: maintains draft GDD, configuration, risk list and references.
Human project lead: approves design, merges code, authorizes dependencies/services, and decides releases.
## ACCESS AND SECURITY
No unrestricted filesystem, deployment, billing, external messaging, or destructive permissions for assistants. Keep credentials out of prompts and repository. Explicit approval required for adding paid model endpoints.
## DEFINITION OF DONE FOR FIRST PROTOTYPE
A player can collect an ingredient, unlock a recipe, see a restaurant reward, feed or fight the Cake Boss, switch between agent/scripted conditions, and produce inspectable encounter logs. No runtime crashes during a short test.
