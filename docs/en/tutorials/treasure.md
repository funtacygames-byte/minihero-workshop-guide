# Put your treasure in your stage

[简体中文](../../zh-CN/tutorials/treasure.md) · [Index](../README.md)

Wayfarer's Relic is already in the codex. Now add a **Claim Relic** encounter, collect it and enter the next stage to see its 4 shield take effect.

**Before this lesson:** finish [Your first mod](first-mod.md) and [Your fixed stage](stage.md). Keep `StarterRelic.BaseValue` at 4. The guard can have either 4 or 8 HP. You need no artwork or music.

| File | What you do |
| --- | --- |
| `source/RelicGrant.cs` | Create an encounter that grants Wayfarer's Relic |
| `source/ModEntry.cs` | Register the encounter in the existing `Load` |
| `source/PracticeStage.cs` | Place it above the guard and give the adventure two stages |
| `package.json` | Increment the version before building and installing |

## 1. Create the relic encounter

Copy all of [the relic-reward source](../../../templates/en/09-relic-grant.cs.txt) into a new `source/RelicGrant.cs`. Match the namespace in your own `ModEntry.cs`. This adds only `RelicGrant`; do not copy the first lesson's entry again.

Keep the existing registrations in `ModEntry.cs` and add this inside `Load`:

```csharp
registrar.AddContent(new RelicGrant());
```

The entry should now register `StarterRelic`, `PracticeStage`, `PracticeAdventure` and `RelicGrant`. You still need to place the encounter on the board to meet it.

## 2. Place it above the guard

Open `source/PracticeStage.cs`. In `PracticeStage.CreateDefinition`, find `columns[0].cards.Add(guard);` and add this **immediately after it**:

```csharp
columns[0].cards.Add(
    registry.Get<EventContent>(ModEntry.PackageId + ".event.relic_grant")
        .CreateCard(Id + ".grant"));
```

Bottom to top, the first column is now exit, guard, Claim Relic. The encounter added last is exposed first. Its single reward option places Wayfarer's Relic in a treasure slot and removes the encounter card.

## 3. Give the effect another stage to trigger in

Wayfarer's Relic grants shield **when you enter a stage**. You collect it after entering the first stage, so its next trigger is the second stage.

In the same `PracticeStage.cs`, find `PracticeAdventure` and change only these values:

- In the single `Steps` entry, change `roundCount = 1` to `roundCount = 2`. This generates the same board twice.
- Change `0` to `1` in `public override int IntermissionInterval => 0;` to add preparation between stages.

If you already made these edits in the connected-stages lesson, keep 2 and 1. Do not add another `Steps` property or adventure class.

## 4. Collect it, clear the stage and check shield

1. Save, increment the package version, build and install, then fully restart the game.
2. Start a new **Trail Lab** run. Open **Claim Relic**, choose its reward and check that Wayfarer's Relic appears in a treasure slot.
3. Defeat the guard and use the exit. The first exit leads through preparation to the second stage.
4. **Do not attack yet.** Check shield: this treasure should add 4 at level 1 with `BaseValue = 4`.
5. After checking shield, resolve stage two's reward encounter, defeat the guard and use the final exit to win. Repeating the board repeats the encounter too. The second collection happens after entry, so it does not change the entry reward you just checked.

Try this without other stage-entry shield sources. Record the entry gain before using other cards. Extra copies add later effects, and damage can consume shield; both make later totals harder to read. It is normal for the first exit to continue the adventure. The second one finishes it.

**Got the relic but no shield?** Check that you entered the second stage; collecting a treasure is not a stage-entry event. Then check its level, `BaseValue`, number of copies and other shield gains or losses. A total shield value alone may hide the cause.

## 5. Try another value

Temporarily change `StarterRelic.BaseValue` from 4 to 2. Save, increment the version, build and install, fully restart and start a new run. The level-1 codex description and second-stage shield gain should both be 2. Restore your preferred value and build once more.

The lesson is that **the description and effect should share a formula**. Do not change only a description string. Quality arrows do not turn level 1 into level 2: this example gives 4 at level 1 and 8 at level 2 through its level multiplier, with no separate values per quality.

### Want it to appear in random chests too?

`CategoryTags` describes the treasure's type: here it is `TreasureCategoryTags.Shield`. `PoolTags` decides which characters can draw it: here it is `CharacterTreasurePoolTags.HealingLifeBuild`, which Groveheart allows. Eligibility does not guarantee a draw, which is why this lesson uses a specified reward first. See the [treasure reference](../reference/treasures.md) for the full rules.

For later treasures with counters or stacks, store state separately on each runtime treasure and reset it on stage changes by default. Shield already granted to the player is a resource, not an internal treasure counter. Try [the practice flask with a three-trigger limit](rules-and-state.md) next.

For names in both languages, follow [the text-merging steps](assets-and-text.md#merge-text-for-topic-fragments) and add `event.relic_grant.*`. The project already generates `content.starter_relic.*` for the starter relic.
