# Connect two stages into an adventure

[简体中文](../../zh-CN/tutorials/adventure.md) · [Index](../README.md)

Make Trail Lab last for two stages: clear the first, pass through preparation, then clear the second to win. Reuse the same board first; you can give each region its own board later.

**You need:** [A fixed stage](stage.md). Edit only `PracticeAdventure` inside `source/PracticeStage.cs`; no new files or artwork are needed. If you completed [the treasure lesson](treasure.md), the two stages and preparation are already set up, so go straight to section 2.

Before installing changed content, increment `package.json.version`, build and install, then fully restart.

## 1. Use the same board twice

In `PracticeAdventure.Steps`, change the single step's `roundCount` from 1 to 2. Change `IntermissionInterval => 0` to `IntermissionInterval => 1` in the same class. Keep `sourceStageId` pointing to `.stage.practice`. Each round creates a new board from the same stage definition, so both contain a guard and exit.

The source ID is `local.alice.lantern-trail.stage.practice`. The step ID is `local.alice.lantern-trail.adventure.practice.step.one`. Expanded stage IDs append `-round-1` and `-round-2` to that step ID. An encounter that jumps to a stage must use an expanded ID present in this run, not the source ID.

## 2. Play through the transition

Build and install, fully restart, and start a new run. In the first stage, defeat the guard and use the exit. Observe the intermission or transition entry, then enter the next stage. A new guard should appear; only the final exit should finish with victory. If you added a treasure reward, check its next-stage entry effect first.

Save and restore first-stage progress, then finish both stages. Start another run to check it begins at the first stage. Rebuilding source does not automatically rearrange an existing run; start anew after structural changes.

## 3. Connect different source regions

The [three-region structure fragment](../../../templates/en/07-three-region-adventure.cs.txt) defines only an adventure. It depends on registered `.stage.region_one`, `.stage.region_two`, and `.stage.region_three` contents. Implement those stages before registering `MyAdventure`. You can copy just the `PracticeStage` class into separate files for the regions, giving each a unique class name and content ID. Do not copy `PracticeAdventure` into every file.

Each step identifies its source and sets `columnCount`, `roundCount`, `cardsPerRound`, a generation profile and intermission. Complete fixed columns determine fixed-board counts; random boards use configured counts and pools.

Configure the actual selection roster through the difficulty's availableHeroIds; source allowedCharacterIds is retained metadata in the current C# path. Fields such as `attackEnhance` affect generated results. First verify a single difficulty without additional enhancement, then add growth. A default six-round value in an API is not a required pacing plan.

## 4. Add advanced features when needed

Distinguish the enemy card's `isBoss`, the step's `boss`, and the source stage's `boss`. A boss card alone does not select boss music. See the [content overview](../02-content-creation.md) for rules, fixed/daily seeds, continuation, loops, and StageGraph; use [Stage and adventure reference](../reference/stages.md) for fields.

These are not prerequisites for a two-stage adventure. After adding a mechanism, recheck selection, legal actions, required content, reachable exits, results, reset, and saves.

## Try it in the game, then continue

- The first exit reaches stage two; the second can finish with victory.
- Source, step, and expanded stage IDs are distinct and unique.
- New runs and restored saves can reach the ending; difficulty and character lists agree.

Next: [Images, music, and bilingual text](assets-and-text.md).

To show names and descriptions in both languages, follow [the text-merging steps](assets-and-text.md#merge-text-for-topic-fragments) for this lesson's entries. Without them, the code's fallback text is shown. Start a new run after switching languages.

To add a tier to an existing map, follow [difficulty extension](level-difficulty.md).
