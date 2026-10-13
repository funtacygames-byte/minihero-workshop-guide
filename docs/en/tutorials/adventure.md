# Connect stages and intermissions

[简体中文](../../zh-CN/tutorials/adventure.md) · [Index](../README.md)

Guide revision 2 · Mod API 1.8.0 · 2026-10-13 · [Validation scope](../reference/versions.md)

Goal: keep the fixed exercise playable while expanding it to two stages. The first exit starts a transition; the second finishes with victory. Learn the difference between source stage, step, and expanded stage IDs before connecting three regions.

Prerequisite: [A fixed stage](stage.md). Edit only `PracticeAdventure`; no new art or external source stage is required.

Before installing a changed build, increment `package.json.version` as in [the first lesson](first-mod.md#4-change-one-value-and-verify-again). Different contents cannot replace an installed package under the same version.

## 1. Expand one source twice

Change the only step's `roundCount` from 1 to 2 and `IntermissionInterval` to 1. Keep `sourceStageId` pointing to `.stage.practice`. Each round creates a new board from the same stage definition, so both contain a guard and exit.

The source ID is `local.alice.lantern-trail.stage.practice`. The step ID is `local.alice.lantern-trail.adventure.practice.step.one`. Expanded stage IDs append `-round-1` and `-round-2` to that step ID. An encounter that jumps to a stage must use an expanded ID present in this run, not the source ID.

## 2. Play through the transition

Build and install, fully restart, and start a new run. In the first stage, defeat the guard and use the exit. Observe the intermission or transition entry, then enter the next stage. A new guard should appear; only the final exit should finish with victory. If you added a treasure reward, check its next-stage entry effect first.

Save and restore first-stage progress, then finish both stages. Start another run to check it begins at the first stage. Rebuilding source does not automatically rearrange an existing run; start anew after structural changes.

## 3. Connect different source regions

The [three-region structure fragment](../../../templates/en/07-three-region-adventure.cs.txt) defines only an adventure. It depends on registered `.stage.region_one`, `.stage.region_two`, and `.stage.region_three` contents. Implement those stages before registering `MyAdventure`. You can derive separate definitions from `PracticeStage`, but keep class names and content IDs unique.

Each step identifies its source and sets columns, rounds, cards per round, generation profile, and intermission. Complete fixed columns determine fixed-board counts; random boards use configured counts and pools.

Difficulty character lists must agree with source-stage eligibility. Fields such as `attackEnhance` affect generated results. First verify a single difficulty without additional enhancement, then add growth. A default six-round value in an API is not a required pacing plan.

## 4. Add advanced features when needed

Distinguish the enemy card's `isBoss`, the step's `boss`, and the source stage's `boss`. A boss card alone does not select boss music. See the [content overview](../02-content-creation.md) for rules, fixed/daily seeds, continuation, loops, and StageGraph; use [Stage and adventure reference](../reference/stages.md) for fields.

These are not prerequisites for a two-stage adventure. After adding a mechanism, recheck selection, legal actions, required content, reachable exits, results, reset, and saves.

## Checks and next step

- The first exit reaches stage two; the second can finish with victory.
- Source, step, and expanded stage IDs are distinct and unique.
- New runs and restored saves can reach the ending; difficulty and character lists agree.

Next: [Images, music, and bilingual text](assets-and-text.md).
