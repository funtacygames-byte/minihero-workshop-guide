# Add a potion and a damage item to your stage

[简体中文](../../zh-CN/tutorials/items-and-events.md) · [Index](../README.md)

Place two usable items beside the guard in Trail Lab: a Moondew Potion that restores 6 HP and an Ember Vial that deals 5 damage to a chosen enemy. Try them first, then look at how their code paths differ.

**You need:** [A fixed stage](stage.md). Copy all of [the item source](../../../templates/en/12-items.cs.txt) to a new `source/PracticeItems.cs`, matching the namespace in `ModEntry.cs`. Edit your existing `ModEntry.cs` and `PracticeStage.cs`; no images are needed. If these classes already exist in your project, use those files instead of copying them again.

## 1. Register and place the items

Register both classes in the existing entry:

```csharp
registrar.AddContents(new MoonDewPotion(), new EmberVial());
```

After creating `columns` and before returning the fixed-stage definition, place items on top of columns two and three. Keep the guard and exit in column one:

```csharp
columns[1].cards.Add(registry.Get<ItemContent>(
    ModEntry.PackageId + ".item.moon_dew_potion").CreateCard(Id + ".potion"));
columns[2].cards.Add(registry.Get<ItemContent>(
    ModEntry.PackageId + ".item.ember_vial").CreateCard(Id + ".vial"));
```

`CreateCard` turns static content into independent card instances. Use distinct instanceIds; do not place the same mutable CardState in several columns. Random layouts instead use templates in `appearancePool`; fixed layouts do not fill from that pool.

## 2. Try the items in the game

Merge the fragment's four `item.*` keys into both locales. Use 月露药剂 / Moondew Potion and 余烬药瓶 / Ember Vial, retaining healing 6 and selected-enemy damage 5. Empty art bindings let you check rules first; add your own icons through the [asset lesson](assets-and-text.md).

1. Save, increment the package version, build and install, fully restart and start a new Trail Lab run.
2. Click the Moondew Potion in column two. It should be used and removed. An unchanged HP bar is normal at full health; if injured, you should see HP restored.
3. To check visible healing separately, let the guard hurt your character first. If it cannot deal damage, temporarily raise its `attack` above your defense and its `hp` enough to survive at least one attack. Rebuild and restart after edits, then take damage and use the potion.
4. For the vial, reset the guard to `attack: 1, defense: 0, hp: 8`, increment the version, build, restart and start anew. **Hold the Ember Vial in column three, drag it onto the exposed guard and release.** The full-health guard should have 3 HP left, the vial should disappear and other enemies should be unharmed.
5. Finish through the exit. For a further damage-reduction check, repeat with a guard that has nonzero defense. Update descriptions and the package version with every value change.

If an item cannot be used, check card type, activationKind, targetKind, exposed target and pendingChoice. If a face displays without a reward, check the execution path before changing UI click handlers.

## 3. Activation determines settlement

`CardType.Medicine` reads `Heal` and uses potion healing. The direct attribute path for `CardType.Elixir` reads `Effect`. Ember Vial overrides `CreateCard`, sets `Targeted` plus `Enemy`, and adds a `CardEffectType.Damage` effect; targeting an exposed enemy uses the core targeted-damage path. It does not call `ItemContent.Execute`, so do not apply damage there a second time.

For area damage, set `CardActivationKind.Direct` and `CardEffectType.DamageAllEnemies` in CreateCard. Change those two fields and the description together. Verify defense, traits, enemy defeats and rewards through real damage settlement. Item damage is not an attack response and does not trigger its `OnRoundStart`.

## 4. Choose an encounter path

| Goal | Implementation | Note |
| --- | --- | --- |
| Direct attribute reward | `EventContent.Effect`, default Action=None | Retain default Execute |
| Attribute reward list | `Action=Meditation` plus `Choices` | Does not also apply Effect or draw treasures |
| Branch costs, specified rewards, follow-ups | `richEventChoices` | At most three branches; see reference for timing |
| Any number of real card faces, specialized resolver | `CardChoiceEventContent` | Use the [new card-choice lesson](card-choice.md) |
| Teaching grant of a specified treasure | [fragment 09](../../../templates/en/09-relic-grant.cs.txt) | Register reward ID; test empty and full slots |

A rich event's `rewardContentId` can reference a treasure, move or item; an item reward executes immediately, rather than becoming an inventory card. A new card choice's `effect` is StatEffect and does not grant treasure from the display card's contentId automatically. Do not combine paths on one event card; see the [content manual](../02-content-creation.md).
