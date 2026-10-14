# Give a treasure a three-trigger limit

[简体中文](../../zh-CN/tutorials/rules-and-state.md) · [Index](../README.md)

Make a **Practice Flask**: after healing, gain shield equal to 10% of the healing amount, up to 3 times per stage. Four potions let you see three shield gains followed by none. Then enter the next stage to check that the counter resets.

**You need:** the reward encounter and two-stage adventure from [the treasure lesson](treasure.md). Use only this lesson's shield source for now, so other treasures do not obscure the result.

| File | What you do |
| --- | --- |
| `source/PracticeCounterRelic.cs` | Create it and copy the flask source |
| `source/RelicGrant.cs` | Change the reward to Practice Flask |
| `source/PracticeItems.cs` | Add or reuse Moondew Potion, changing its healing to 10 |
| `source/ModEntry.cs` | Register the flask and potion |
| `source/PracticeStage.cs` | Place four potions; keep the encounter, guard and exit |

## 1. Collect the flask

Copy [the flask source](../../../templates/en/13-stateful-relic.cs.txt) into `source/PracticeCounterRelic.cs`, matching your entry's namespace. Register it inside the existing `Load`:

```csharp
registrar.AddContent(new PracticeCounterRelic());
```

In `RelicGrant.cs`, change `rewardContentId` to `ModEntry.PackageId + ".treasure.practice_counter"`. Keep the code that places the encounter. Replace its reward rather than also granting the starter relic, and change its displayed name and description to refer to the flask.

The flask has one Legendary, level-1 variant. Its `GetStateVariants()` explicitly returns only that variant; you do not need four more quality values. It uses the same shield category and life-build pool as before, and you still obtain it through a specified reward.

## 2. Place four potions that heal for 10

If you have not done [the item lesson](items-and-events.md), copy [the item source](../../../templates/en/12-items.cs.txt) to `source/PracticeItems.cs` with the same namespace. If that file already exists, edit it rather than adding duplicate classes.

Change `MoonDewPotion` from `Heal => 6` to `Heal => 10`. Change 6 to 10 in its source fallback description and in both languages' `item.moon_dew.description`. Register it once in `Load`:

```csharp
registrar.AddContent(new MoonDewPotion());
```

After the columns are created in `PracticeStage.CreateDefinition`, but before it returns, add:

```csharp
columns[1].cards.Clear();
for (int i = 0; i < 4; i++)
{
    columns[1].cards.Add(registry.Get<ItemContent>(
        ModEntry.PackageId + ".item.moon_dew_potion").CreateCard(Id + ".heal." + i));
}
```

Column two now exposes four potions in sequence, each with its own instance ID. Keep the reward encounter, guard and exit in column one. Use [the text-merging steps](assets-and-text.md#merge-text-for-topic-fragments) to add the flask and potion entries in both languages.

## 3. Drink all four in the game

Save, increment the package version, build and install, then fully restart. Start a new Trail Lab run, collect the flask and use the potions in column two. Without other healing modifiers, record the shield change each time:

| Potion | Shield gained this time | Triggers used |
| --- | ---: | ---: |
| 1 | 1 | 1 |
| 2 | 1 | 2 |
| 3 | 1 | 3 |
| 4 | 0 | Still 3 |

You can check this at full health: the healing amount is 10, so the flask still uses 10 even though the HP bar does not increase. With only 2 HP missing, it also grants 1 shield. With healing modifiers, use the healing amount after those modifiers instead.

Defeat the guard, use the exit and pass through preparation to stage two. Leave the new reward encounter unopened while checking the first potion: it should grant 1 shield again. This checks one flask's reset. Resolve the encounter afterward if you want to finish the run. Check the gain from that action rather than treating existing resources as a new trigger.

## 4. How the code remembers uses

`healingTriggers` belongs to this runtime treasure. `OnAfterHealing` checks the healing amount and cap, then increments the counter and grants shield. `OnSceneReset` clears the counter when stages change.

A `static` field could make two flasks share a counter. Storing it on a UI object would also give saves the wrong source of state. This example uses a public integer in a serializable class to preserve each treasure's own count.

It reads `AfterHealingEvent.requested`, which means settled healing. `actual` is only the amount added to the HP bar. The field name can be misleading; see [healing events](../reference/events.md) for the exact meaning.

### Before sharing, try a few more checks

After three triggers, save and continue the game; a fourth heal should still grant no shield. Two flasks should keep separate counts. Repeated action previews must not consume real uses, and preview and execution should use the same formula. For rule changes, check caps, stage changes and saves together; see [Lifecycle](../reference/lifecycle.md).

For an adventure-wide rule that does not occupy a treasure slot, look up `AdventureRuleContent`. Register it, then activate it through `AdventureRuleIds` or a difficulty's `adventureRuleIds`. Fields and defaults are in [the content reference](../02-content-creation.md). You do not need this to finish the flask.
