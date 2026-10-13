# Create and test a treasure

[简体中文](../../zh-CN/tutorials/treasure.md) · [Index](../README.md)

Guide revision 2 · Mod API 1.8.0 · 2026-10-13 · [Validation scope](../reference/versions.md)

Use the first lesson's `StarterRelic` to check quality, level, eligibility, and its actual effect. This single-quality teaching treasure illustrates implementation; changing its name and values alone does not constitute a new finished design.

Prerequisite: [Your first mod](first-mod.md). The gameplay section also needs [A fixed stage](stage.md). Edit `source/ModEntry.cs` and add `source/RelicGrant.cs`. No image or music files are required.

Before installing a changed build, increment `package.json.version` as in [the first lesson](first-mod.md#4-change-one-value-and-verify-again). Different contents cannot replace an installed package under the same version.

## 1. Separate quality, level, and pools

`Rank = Common` provides only Common quality. Five versions are not generated automatically without a multi-quality implementation. Keep the edited `BaseValue` at 4 in this lesson. Both `Describe(level)` and `OnStageEntered` calculate `BaseValue × level`: 4 at level 1 and 8 at level 2.

`CategoryTags` uses `TreasureCategoryTags.Shield` for its shield role in the life system. `PoolTags` uses `CharacterTreasurePoolTags.HealingLifeBuild` for character eligibility; category does not control chest draws. Groveheart (`grove_alchemist`) allows this pool, but a random draw still does not guarantee the treasure.

See [Treasure reference](../reference/treasures.md) for properties and multi-quality content. Store temporary counters in each runtime instance and clear them in `OnSceneReset()`; see [Lifecycle](../reference/lifecycle.md).

## 2. Grant a specific reward

Copy the [claim-relic fragment](../../../templates/en/09-relic-grant.cs.txt) to `source/RelicGrant.cs` and check its namespace. It defines one test encounter whose only choice grants this package's `StarterRelic`. Add this to `Load`:

```csharp
registrar.AddContent(new RelicGrant());
```

In `PracticeStage.CreateDefinition`, immediately after `columns[0].cards.Add(guard);`, add:

```csharp
columns[0].cards.Add(
    registry.Get<EventContent>(ModEntry.PackageId + ".event.relic_grant")
        .CreateCard(Id + ".grant"));
```

The first column now stores exit, guard, and claim encounter, from bottom to top. The encounter is exposed first; choosing its reward grants the treasure and removes the card. Register `StarterRelic`, `RelicGrant`, `PracticeStage`, and `PracticeAdventure`. Keep exactly one `ModEntry`.

## 3. Reach the next stage entry

A stage-entry reward runs when a stage is entered. Receiving the treasure after entering a stage does not make an immediate shield increase a valid test of this effect.

In the only `PracticeAdventure` step, change `roundCount = 1` to `roundCount = 2`, and set `IntermissionInterval` to 1. Build and install, fully restart, and select Trail Lab. Resolve the encounter and confirm Wayfarer's Relic is in a treasure slot. Defeat the guard, use the exit, and enter the second stage through the intermission page.

The second stage should grant 4 shield on entry: level 1 with `BaseValue = 4`. Observe shield before attacking so damage does not consume it first. Do not claim a second copy during this test; each equipped copy applies its own effect. The first exit normally enters the transition flow; only the final stage's exit finishes the adventure with victory.

## 4. Check the formula and reset boundary

Temporarily return `BaseValue` to 2, rebuild, fully restart, and start a new run. The second stage should grant 2 shield, and the level-1 codex description should also show 2. Restore your chosen value and check again. Do not change only a hard-coded description number.

This treasure has no temporary counter. Granted shield is a player resource, not a pending counter inside the treasure. For other treasures with stacks, use serializable per-instance fields; static fields and shared definitions can leak state between instances. Temporary state resets at each new stage unless a cross-stage exception is explicitly declared.

## Checks and next step

- Codex quality and level are correct; description and stage-entry shield use one formula.
- The fixed encounter grants the treasure, and the next stage makes its effect observable.
- `StartingTreasureTypes` is not used as a selection reward, and category is not treated as pool membership.

Continue with [Characters and initial moves](character.md), or use [Healing and events](../reference/events.md) to design another trigger.
