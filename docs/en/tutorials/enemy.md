# Create enemies with independent instance state

[简体中文](../../zh-CN/tutorials/enemy.md) · [Index](../README.md)

Guide revision 2 · Mod API 1.8.0 · 2026-10-13 · [Validation scope](../reference/versions.md)

Goal: replace Trail Lab's generic guard with a registered Moss Wolf. Taking damage increases its attack by 1. With two wolves, only the one actually damaged should grow.

Prerequisite: [A fixed stage](stage.md). Add `source/MossWolf.cs` and edit `PracticeStage.cs` and entry registration. The fragment binds enemy art. For rules-only validation, remove its custom presentation interface and property; supply your own art for release.

Before installing a changed build, increment `package.json.version` as in [the first lesson](first-mod.md#4-change-one-value-and-verify-again). Different contents cannot replace an installed package under the same version.

## 1. Register the enemy and its trait

Copy the [enemy and trait fragment](../../../templates/en/04-enemies-and-traits.cs.txt). It contains `WoundedRage` and `MossWolf`. Add this to `Load`:

```csharp
registrar.AddContents(new WoundedRage(), new MossWolf());
```

The enemy refers to its trait through `EnemyTraitId`. A description in the enemy's name does not implement a trait. This fragment uses HP 18, attack 6, defense 1, and gold reward 5 as teaching values; adjust them to your character and test.

## 2. Create a registered enemy card

In `PracticeStage.CreateDefinition`, replace the complete `ContentCards.Enemy(...)` guard declaration with this code. Keep the later `columns[0].cards.Add(guard)`:

```csharp
EnemyContent wolf = registry.Get<EnemyContent>(ModEntry.PackageId + ".enemy.moss_wolf");
CardState guard = wolf.CreateCard(Id + ".wolf.one");
```

Registry lookup uses the content ID; the `CreateCard` argument is this card's instance ID. Give two wolves distinct IDs such as `.wolf.one` and `.wolf.two`. Put the second in `columns[1].cards`; keep the exit beneath the first.

## 3. Test one enemy, then two

Build and install, fully restart, and begin a new practice run. Use an attack or direct-damage item that deals positive HP damage while leaving the wolf alive. Its attack should increase by 1. Zero damage does not verify this callback.

With two wolves, record both attack values, damage only the first, and check that the second remains unchanged. The enemy response after a basic attack, move damage, and item damage are different trigger windows. Test them separately where relevant. `OnRoundStart` is not a universal callback for every player action.

If your character defeats the wolf in one hit, raise the test enemy's HP or lower test damage so its state remains observable. Recycling, countdown removal, and defeat may also use different flows; choose events from their contracts.

## 4. Store state on the correct object

`WoundedRage` changes `e.Owner.enemyTraitAttackDelta`. Multiple wolves can share one trait definition. Do not add an `int hits` field to that definition to count one wolf's progress. Use that card's `enemyTraitCounter`, `enemyTraitSecondaryCounter`, or another appropriate instance field, with one meaning per field. Countdown behavior already uses the primary counter.

See [Character and enemy reference](../reference/actors.md) and [Lifecycle](../reference/lifecycle.md) for signatures, damage windows, and saves. This example has no growth cap. Add a cap to both description and implementation when the design needs one, and test behavior after reaching it.

## Checks and next step

- Enemy and trait are registered, and `EnemyTraitId` resolves.
- Positive HP damage causes the correct growth without leaking between instances.
- New cards start from initial state, and save restoration preserves existing-card data.

Continue with [Connecting stages](adventure.md), or add your own battle art through [Assets and text](assets-and-text.md).
