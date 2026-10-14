# Create potions, targeted items and encounters

[简体中文](../../zh-CN/tutorials/items-and-events.md) · [Index](../README.md)

Guide revision 4 · Mod API 1.8.0 · 2026-10-14


Goal: place a Moondew Potion that restores 6 HP and an Ember Vial that deals 5 damage to a selected enemy on a fixed board, then distinguish attribute encounters from card-face choices. Prerequisite: [fixed stage](stage.md). Add `source/PracticeItems.cs` from [fragment 12](../../../templates/en/12-items.cs.txt). Do not duplicate classes already copied from the manual.

## 1. Registration does not cause appearance

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

## 2. Activation determines settlement

`CardType.Medicine` reads `Heal` and uses potion healing. The direct attribute path for `CardType.Elixir` reads `Effect`. Ember Vial overrides `CreateCard`, sets `Targeted` plus `Enemy`, and supplies `Damage`; targeting an exposed enemy uses the core targeted-damage path. It does not call `ItemContent.Execute`, so do not apply damage there a second time.

For area damage, set `CardActivationKind.Direct` and `CardEffectType.DamageAllEnemies` in CreateCard. Change those two fields and the description together. Verify defense, traits, enemy defeats and rewards through real damage settlement. Item damage is not an attack response and does not trigger its `OnRoundStart`.

## 3. Choose an encounter path

| Goal | Implementation | Note |
| --- | --- | --- |
| Direct attribute reward | `EventContent.Effect`, default Action=None | Retain default Execute |
| Attribute reward list | `Action=Meditation` plus `Choices` | Does not also apply Effect or draw treasures |
| Branch costs, specified rewards, follow-ups | `richEventChoices` | At most three branches; see reference for timing |
| Any number of real card faces, specialized resolver | `CardChoiceEventContent` | Use the [new card-choice lesson](card-choice.md) |
| Teaching grant of a specified treasure | [fragment 09](../../../templates/en/09-relic-grant.cs.txt) | Register reward ID; test empty and full slots |

A rich event's `rewardContentId` can reference a treasure, move or item; an item reward executes immediately, rather than becoming an inventory card. A new card choice's `effect` is StatEffect and does not grant treasure from the display card's contentId automatically. Do not combine paths on one event card; see the [original manual](../02-content-creation.md).

## 4. Bilingual text and acceptance

Merge the fragment's four `item.*` keys into both locales. Use 月露药剂 / Moondew Potion and 余烬药瓶 / Ember Vial, retaining healing 6 and selected-enemy damage 5. Empty art bindings let you check rules first; add your own icons through the [asset lesson](assets-and-text.md).

Increment the package version, build, install and fully restart. Injure the player before using the potion; distinguish the healing amount from HP gained. Set the practice guard's HP to 8: without damage reduction, the vial leaves 3 and must not damage another enemy. Then add nonzero guard defense and verify shared damage settlement. Check removal, item-use notification and turn handling on the actual path, then complete the exit. Update descriptions and package version with each numerical change.

If an item cannot be used, check card type, activationKind, targetKind, exposed target and pendingChoice. If a face displays without a reward, check the execution path before changing UI click handlers.
