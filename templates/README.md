# Add example code to your project

[简体中文](README.zh-CN.md) · [Lesson index](../docs/en/README.md)

These `.cs.txt` files contain readable C# source. Create your project with [the first lesson](../docs/en/tutorials/first-mod.md), then copy the files you need. Downloading this repository alone does not give you an installable mod.

## Before copying

1. Use **Open Source** in the game to open your project. Put new source in its `source` folder and save it as **`.cs`**, removing the linked file's final `.txt`.
2. **Only 01 replaces `ModEntry.cs`.** Add other files to the existing project without another `ModEntry`. Match each new file's `namespace` to your entry.
3. The default package ID is `local.alice.lantern-trail`, with namespace `LocalAliceLanternTrailMod`. For another ID, adapt 01 as in the first lesson; other fragments keep using `ModEntry.PackageId`.
4. A class still needs registration in `Load` and a place in a stage or character pool. Pages use `AddScreen`; music uses theme registration. Follow the relevant lesson for placement.

## Start with these three files

| Source | Destination in your project | Follow |
| --- | --- | --- |
| [01 Starter treasure and entry](en/01-entry-and-config.cs.txt) | **Replace** `source/ModEntry.cs` | [Your first mod](../docs/en/tutorials/first-mod.md) |
| [08 Fixed stage and adventure entry](en/08-fixed-stage-lab.cs.txt) | Create `source/PracticeStage.cs` | [Your first stage](../docs/en/tutorials/stage.md) |
| [09 Relic reward encounter](en/09-relic-grant.cs.txt) | Create `source/RelicGrant.cs` | [Collect and use the treasure](../docs/en/tutorials/treasure.md) |

This route needs no external artwork or music. The word `config` in 01's filename preserves an old link; the current first lesson uses source defaults directly.

## Choose other files as needed

| Source | Suggested filename | What it needs |
| --- | --- | --- |
| [02 Character, trait and move](en/02-character-trait-and-move.cs.txt) | `source/LanternRanger.cs` | Starts with fallback artwork; add to the roster in [the character lesson](../docs/en/tutorials/character.md) |
| [03 Character treasures](en/03-character-treasures.cs.txt) | `source/CharacterTreasures.cs` | The same custom pool tag as 02; your own compass icon |
| [04 Enemy and trait](en/04-enemies-and-traits.cs.txt) | `source/MossWolf.cs` | Starts with fallback artwork; replace the guard in [the enemy lesson](../docs/en/tutorials/enemy.md) |
| [05 Random stage bindings](en/05-stage-bindings.cs.txt) | `source/LanternTrail.cs` | Character 02, enemy 04, three stage images and a separate adventure entry |
| [06 Music theme](en/06-stage-music.cs.txt) | `source/MusicIds.cs` | Your OGG/WAV files; register and reference the theme as in [music](../docs/en/tutorials/assets-and-text.md) |
| [07 Three-region structure](en/07-three-region-adventure.cs.txt) | `source/MyAdventure.cs` | Implement and register its three referenced stages first; see [connected stages](../docs/en/tutorials/adventure.md) |
| [10 Two-card choice](en/10-card-choice.cs.txt) | `source/CampChoice.cs` | Place it in 08; follow [the supply-choice lesson](../docs/en/tutorials/card-choice.md) |
| [11 Page and buttons](en/11-custom-page.cs.txt) | `source/CampPage.cs` | Use `AddScreen(CampPage.Create())`; see [custom pages](../docs/en/tutorials/custom-ui.md) |
| [12 Two items](en/12-items.cs.txt) | `source/PracticeItems.cs` | Register and place on the board; see [items](../docs/en/tutorials/items-and-events.md) |
| [13 Capped flask](en/13-stateful-relic.cs.txt) | `source/PracticeCounterRelic.cs` | Grant with 09 and test four potions; follow [the state lesson](../docs/en/tutorials/rules-and-state.md) |
| [14 Bounded continuation](en/14-dynamic-continuation.cs.txt) | `source/ContinuingPracticeAdventure.cs` | Keep 08's `PracticeStage`, replace adventure registration; three stages total |
| [15 Chained choice](en/15-chained-choice.cs.txt) | `source/TwoStepSupplies.cs` | Place this event in 08; try confirmation and cancellation in [the choice lesson](../docs/en/tutorials/card-choice.md) |
| [16 Difficulty copy](en/16-level-difficulty.cs.txt) | `source/ExtraDifficulty.cs` | Call `ExtraDifficulty.Register(registrar)` in the existing Load; [lesson](../docs/en/tutorials/level-difficulty.md) |
| [17 Profession and progress](en/17-profession-progress.cs.txt) | `source/LanternTraining.cs` | Register it and update 02's ProfessionId/Role; [lesson](../docs/en/tutorials/profession-progress.md) |

Do not copy every file at once. In particular, 07 does not include its three source regions and cannot run alone. Add files before using image bindings; character and enemy lessons can be completed without custom artwork first.

## Where is the displayed text?

The [Chinese catalog](zh-CN/localization.json) and [English catalog](en/localization.json) contain example names and descriptions. Merge only the `entries` you need, preserving your package name, other keys and `locale`. Find each lesson's key prefixes and exact steps in [Assets and text](../docs/en/tutorials/assets-and-text.md#merge-text-for-topic-fragments).

Save, increment `package.json.version`, choose **Build and Install**, fully exit and restart, then check the result using the lesson's steps.
