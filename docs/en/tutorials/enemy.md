# Make an enemy that grows stronger when hurt

[简体中文](../../zh-CN/tutorials/enemy.md) · [Index](../README.md)

Replace the guard in Trail Lab with a **Moss Wolf**. Each time it takes positive HP damage, it gains 1 attack. Then place two wolves to check that they grow independently.

**You need:** the project from [A fixed stage](stage.md). Create `source/MossWolf.cs`; edit `source/ModEntry.cs` and `source/PracticeStage.cs`. The source uses fallback artwork, so you do not need a wolf image yet.

Save, increment `package.json.version`, build and install, then fully restart. Start a new run for each test so you can see the enemy's initial values.

## 1. Register the enemy and its trait

Copy the [enemy and trait source](../../../templates/en/04-enemies-and-traits.cs.txt) into `source/MossWolf.cs`, using your namespace. It contains `WoundedRage` and `MossWolf`. Add this inside `Load` in your existing `ModEntry.cs`:

```csharp
registrar.AddContents(new WoundedRage(), new MossWolf());
```

`EnemyTraitId` connects Moss Wolf to Wounded Rage. It starts with HP 18, attack 6, defense 1 and a gold reward of 5. Keep those values until you can see its attack grow after damage, then adjust its strength.

## 2. Create a registered enemy card

In `PracticeStage.CreateDefinition`, replace the complete `ContentCards.Enemy(...)` guard declaration with this code. Keep the later `columns[0].cards.Add(guard)`:

```csharp
EnemyContent wolf = registry.Get<EnemyContent>(ModEntry.PackageId + ".enemy.moss_wolf");
CardState guard = wolf.CreateCard(Id + ".wolf.one");
```

Registry lookup uses the content ID; the `CreateCard` argument is this card's instance ID. Give two wolves distinct IDs such as `.wolf.one` and `.wolf.two`. Add the code below after the original `columns[0].cards.Add(guard);` to put another wolf in column two. The exit stays beneath the first wolf. If the character lesson already added a second guard, remove that `secondGuard` block before placing the wolf.

```csharp
columns[1].cards.Add(wolf.CreateCard(Id + ".wolf.two"));
```

You can try it without custom artwork. Add a battle image later using [Assets and text](assets-and-text.md#add-character-and-enemy-artwork).

## 3. Test one enemy, then two

Build and install, fully restart, and begin a new practice run. Use an attack or direct-damage item that deals positive HP damage while leaving the wolf alive. Its attack should increase by 1. Zero damage does not verify this callback.

With two wolves, record both attack values, damage only the first, and check that the second remains unchanged. If you kept Lantern Ranger, use the single-target Silver Bolt for this check: the character trait makes an attack select another enemy too. The enemy response after a basic attack, move damage, and item damage are different trigger windows. Test them separately where relevant. `OnRoundStart` is not a universal callback for every player action.

If your character defeats the wolf in one hit, raise the test enemy's HP or lower test damage so its state remains observable. Recycling, countdown removal, and defeat may also use different flows; choose events from their contracts.

## 4. Store state on the correct object

`WoundedRage` changes `e.Owner.enemyTraitAttackDelta`. Multiple wolves can share one trait definition. Do not add an `int hits` field to that definition to count one wolf's progress. Use that card's `enemyTraitCounter`, `enemyTraitSecondaryCounter`, or another appropriate instance field, with one meaning per field. Countdown behavior already uses the primary counter.

See [Character and enemy reference](../reference/actors.md) and [Lifecycle](../reference/lifecycle.md) for signatures, damage windows, and saves. This example has no growth cap. Add a cap to both description and implementation when the design needs one, and test behavior after reaching it.

## Try it in the game, then continue

- Enemy and trait are registered, and `EnemyTraitId` resolves.
- Positive HP damage causes the correct growth without leaking between instances.
- New cards start from initial state, and save restoration preserves existing-card data.

Continue with [Connecting stages](adventure.md), or add your own battle art through [Assets and text](assets-and-text.md).

To show names and descriptions in both languages, follow [the text-merging steps](assets-and-text.md#merge-text-for-topic-fragments) for this lesson's entries. Without them, the code's fallback text is shown. Start a new run after switching languages.
