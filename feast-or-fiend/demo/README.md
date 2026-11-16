# FEAST OR FIEND — THE LAST SPOON 🍓

**A playable original pixel-art, offline desktop game demo** for the Feast or Fiend world. The demo is a hand-built vertical slice, **not** the entire planned game. It uses no external art, no network, no payment, no service account, and no model API key. All art in `game/art/` was procedurally authored for this project.

## Play on Windows

**Option A — standalone Windows EXE:** In this repository, open **Actions → Build Windows Desktop Demo → latest successful run → Artifacts → FeastOrFiend-Windows**. Download and unzip it, then launch `FeastOrFiend.exe`. No Python installation required. If Windows SmartScreen appears, this unsigned student project may require **More info → Run anyway** after you have verified the download is from your own GitHub repository.

**Option B — source ZIP:** Install Python 3.10 or later (with Tkinter, included by the standard Windows installer), unzip the project and double-click `PLAY_ON_WINDOWS.bat`. No pip install required. Alternatively run `python game/main.py`.

**To create your own EXE locally:** double-click `BUILD_WINDOWS_EXE.bat` (requires Python and internet to download PyInstaller). This creates `dist/FeastOrFiend.exe`, which runs on compatible Windows PCs without Python. Alternatively install PyInstaller manually and run `pyinstaller --onefile --windowed --name FeastOrFiend --add-data "game/artpack.b64;." game/main.py` from the demo root.

## Controls

| Key | Action |
|---|---|
| WASD / Arrow keys | Move |
| E | Talk, enter doors, plant, harvest, cook, serve, upgrade |
| J | Swing spoon / attack monsters and the boss |
| K | Offer strawberry to Lady Cake in boss arena |
| Q | Quest journal and recipes |
| Tab | Backpack and ingredient inventory |
| T | Toggle **adaptive local boss agent** vs **scripted baseline** during a boss fight |
| F5 | Save progress |
| Esc | Pause / save / quit |

You can also click the bottom-screen action controls.

## Playable story and game loop

1. Start with Grandpa's water-only restaurant, **The Last Spoon** in **Seasoning Town**.
2. Exit town **left** to **Wildflavor Meadow**; use **J** to fight carrot, lettuce and broccoli monsters, collect ingredients and seeds.
3. Plant at the three garden beds (**E**); harvest after 12 seconds. Crop growth uses wall-clock time so it continues while visiting the restaurant.
4. Enter your restaurant (red-roof building in town), cook **Garden Salad**, **Carrot Soup** or **Forest Stew** at the pot; serve the dishes at the counter. Two sales unlock the boss arena and give you a strawberry.
5. Exit town **right** to **Lady Cake**. Dodge telegraphed moves and attack with **J**. Press **K** when near her to offer a strawberry; she transforms into **Strawberry Cake** and gains stronger attacks.
6. Defeat Lady Cake to unlock the **Cake / Strawberry Cake** recipe and earn coins. Upgrade your restaurant and replay the encounter.

## What's implemented vs planned

**Implemented:** four original pixel-art scenes, title/quest UI, character dialogue (Grey, Lola, Mayor Madeline, Chester), vegetable combat, drops and respawns, three timed garden plots, three cooking recipes, selling, coins, restaurant upgrade, save/load, damage and respawn, Cake Boss, strawberry form, bounded adaptive boss action selection, scripted comparison and win screen.

**Not yet implemented:** all 24 employee stories, full five-act main story, voiced dialogue, other 10+ bosses, extensive social relationships, dark cuisine chains, multiplayer, huge maps, LLM-backed boss calls, or Windows installation wizard.

### Agent comparison integrity

In this offline demo **ADAPTIVE** is a bounded **local rule-based policy**, not a remote LLM. It reacts to player distance and boss state to choose among *charge*, *fan*, *shockwave*, and *rest*, while **SCRIPTED** uses a fixed sequence. Both share the same HP, damage rules and attack catalog. The engine validates and resolves state; the agent cannot alter the inventory, rewards or rules. **No per-session API cost.** This is a real local comparison and the starting point for a later hosted-model experiment—not a claim that an LLM is already integrated.

## Design and attribution

World, dialogue and game-mechanic concepts: Feast or Fiend original design drafts in `../working/`. Visual influences include the **genre conventions** of Kairosoft-style management games and Stardew Valley-style pastoral pixel RPGs. **No sprites, code or characters from either game were copied.** The artwork here is new and procedural. License: see `LICENSE`.

Saved game location: `%USERPROFILE%\.feast_or_fiend_demo_save.json` on Windows. To reset the demo, close it and delete this file.