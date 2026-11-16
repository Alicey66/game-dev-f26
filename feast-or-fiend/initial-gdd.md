# Feast or Fiend — INITIAL GAME DESIGN DOCUMENT (G1)
Status: Concept for prototype approval | Open questions marked [OPEN]
## 1. THE X
Feast or Fiend is a pixel-art restaurant adventure RPG in which players hunt living ingredients, grow and cook food, and challenge culinary bosses to transform an empty restaurant into a thriving destination.
2. PLAYER, EXPERIENCE, MOTIVATION
Audience: players who enjoy cozy farming, action RPG encounters, and recipe discovery; solo-player prototype. Motivations: discovery, progress, expression. Playtest evidence: participants voluntarily experiment with a new ingredient, pursue another recipe, or replay a boss encounter.
## 3. DESIGN PILLARS
- Connected progression: hunting feeds farming; farming feeds cooking; cooking feeds sales; sales motivate hunting.
- Meaningful experiments: valid combinations unlock recipes; invalid combinations provide clear feedback and, later, may enable Dark Cuisine.
- Memorable living-food characters: recognizable silhouettes, attacks, and transformation rules.
- Fair surprise: boss behavior may vary, but all AI choices are constrained to legal actions.
## 4. GAME LOOP
Player acts: move, attack, collect, plant, cook, feed, sell.
Game responds: enemy drops seeds, crops grow, pot verifies recipes, restaurant records sales, boss transforms or attacks.
Player interprets: item drops, recipe book, damage cues, customer response, boss telegraphs.
Next action: experiment, prepare, upgrade, or seek a boss.
## 5. WORLD AND STARTING STATE
Player opens with an empty restaurant, a water serving option, empty recipe book, and a small accessible outdoor zone. Food enemies include carrot and lettuce. Garden plots turn seeds into harvestable ingredients; the pot validates a small recipe table. Restaurant sales unlock a simple progression indicator.
6. BOSS CONCEPTS — FULL VISION, NOT ALL IN PROTOTYPE
Cake Boss: attacks within an arena; feeding strawberry changes its appearance and loot to Strawberry Cake recipe. Incorrect ingredient can trigger Dark Cuisine rage in a later version.
Dumpling Boss: throws meatballs.
Spaghetti Boss: fires noodles as projectile patterns.
Sushi Boss: uses fish blade in melee combat.
Tea Boss + Cake Boss: combination may form Afternoon Tea with cooperative attacks; incompatible bosses may target each other.
[OPEN] Which full-game boss interactions remain fun and readable in small arena spaces?
## 7. PROTOTYPE MECHANICS
- One map, one restaurant interior, one arena.
- Basic movement and attack with telegraphed damage.
- Two enemy types with seed drops.
- Limited garden and cooking recipes.
- Cake Boss, default and strawberry-fed variants.
- Recipe unlock and restaurant reward.
- Same boss available in agent-driven and scripted modes.
[OPEN] Exact movement style, controller support, and chosen engine physics settings.
## 8. AI AGENT HYPOTHESIS
Agent job: select the next legal boss action at discrete decision points. Inputs: current encounter phase, boss HP bracket, recent player actions, approximate distance, offered ingredient, visible neighboring entities. Legal outputs: ATTACK_A, ATTACK_B, RETREAT, REPOSITION, TARGET_PLAYER, TARGET_BOSS when supported. The engine owns damage, physics, drops, and transformation rules. Baseline: deterministic or rule-based finite state machine with identical actions, hitboxes, and health. Playtest: observe strategy switching, replay choice, and player comments about novelty. [OPEN] Whether any model calls are justified over robust scripted variation.
## 9. PLAYTEST DESIGN
Within-subject comparison with counterbalanced first mode where feasible. Participants play both scripted and agent boss conditions. Log attempted attacks, boss action sequence, player deaths, retries, tactical changes, and whether players choose to replay. Ask: 'What made you change your plan?', and 'Which fight would you replay?'. [OPEN] Recruitment count and playable session length.
10. REFERENCES, USE AND TERMS
Minecraft: inspiration for collection and farming loop; no copied assets/code.
Don't Starve: exploration and preparation; no copied assets/code.
Stardew Valley: planting and ingredient crafting; no copied assets/code.
Terraria: boss rewards and boss progression; no copied assets/code.
Godot Engine (proposed): MIT license; preserve notices if redistributed. All artwork and sound will be original, public-domain, or licensed with specific credits and license checks before integration.
[OPEN] Final asset sources and license spreadsheet.
## 11. SCOPE AND CUTS
IN: one map, two enemy types, cooking, simple garden, recipe unlock, one boss with transformation, scripted + AI comparison.
OUT: online multiplayer, seasonal bosses, open world, complex customers, broad building, boss social network, full Dark Cuisine economy.
FIRST CUT: replace detailed crop simulation with ingredient pickups. SECOND CUT: replace restaurant with menu/progression UI.
## 12. RISKS
IP/Concept LOW — original game identity; track asset licenses.
Audience MEDIUM — untested mixture; validate through short playtests.
Technology HIGH — model latency and integration; use event-triggered decisions and fallback.
Team MEDIUM — role availability; use small independent modules and placeholders.
Genre/Mechanics HIGH — many coupled systems; vertical slice only.
Timeline HIGH — short term; freeze scope and cut nonessential systems.
The three HIGH risks share the cause of excessive integrated system complexity.
## 13. OPEN DECISIONS OWNED BY PROJECT LEAD
[OPEN] Engine and movement implementation.
[OPEN] Exact starter recipes and crop times.
[OPEN] Whether transformation occurs before or during combat.
[OPEN] Agent provider/model selection, after latency/cost test.
[OPEN] G2 and G3 official milestone dates.
Project lead makes final design/scope decisions; AI assistants only recommend and help implement.
