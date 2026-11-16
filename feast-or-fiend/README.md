# Feast or Fiend — G1 Creative Pitch

**Stage:** G1 concept proposal — not yet implemented or playtested.

## The X

*Feast or Fiend* is a 2D pixel-art restaurant adventure RPG where players hunt living food, grow ingredients, discover recipes, and challenge culinary bosses to turn a water-only restaurant into a thriving business.

## Gate 1 deliverables

- [Initial Game Design Document](./initial-gdd.md)
- [Initial Configuration Document](./initial-configuration.md)
- [Initial Project Plan](./initial-project-plan.md)
- [Google Slides — Pixel-Art G1 Pitch](https://docs.google.com/presentation/d/1OS48z4kwEGjlqCn658eXSDcTTxVg-H9tUQWE9GSaxsk/edit)
- [3–5 minute presentation recording](https://drive.google.com/file/d/1IdLTHalpZ8DhfI9jdMJyAoz8EqDl3XWU/view?usp=drive_link)
- [3–5 minute speaker script](https://docs.google.com/document/d/12LsXW0z8h4L0RrN8TqeFzkPRXDXvU3Rs5I49jIRYU2M/edit)

## Core loop

Hunt carrot and lettuce monsters → collect seeds → grow ingredients → experiment with cooking → sell dishes → encounter food bosses → unlock rare recipes → improve restaurant.

For example, feeding a strawberry to the Cake Boss transforms it into a Strawberry Cake Boss. An incorrect combination could create Dark Cuisine in a later version. Bosses with interpersonal relationships and multiplayer are part of the longer-term vision, not G1 prototype scope.

## Bounded AI experiment

The in-game boss agent chooses only from engine-defined, validated encounter actions using a filtered observation of the current encounter. It does **not** change canonical health, recipe unlocks, inventory, or drops. Compare the agent-driven boss to a fixed scripted version with equivalent mechanics, and observe whether players adapt their tactics or voluntarily replay.

## G1 decision requested

**Approve:** prototype one small connected ingredient → cooking → restaurant → Cake Boss loop, plus agent vs. scripted encounter comparison.

**Hold correction:** reduce the build to a single boss arena with a feeding transformation and fair baseline comparison.

**Evidence status:** all functionality and measurements are proposals at G1; experiments and technical cost assumptions await verification.

The project lead retains Creative Director and Executive Producer accountability. The instructor is the Gate Approver.

## Rights

No third-party game art or code is copied. Future assets must have explicit source, license, modification, and attribution entries before inclusion. The proposed Godot engine is MIT-licensed.
