# Characters, moves, and enemies

[简体中文](../../zh-CN/reference/actors.md) · [Index](../README.md)

Guide revision 4 · Mod API 1.8.0 · 2026-10-13

Baseline: 1.8.0. See [API declarations](api-surface.md), the [character lesson](../tutorials/character.md), and the [enemy lesson](../tutorials/enemy.md).

## CharacterContent

`Role`, `School`, and `BaseStats` are abstract. `Description` defaults to empty; `IncludeInDefaultRoster` defaults to true. Trait, starting-treasure, starting-move, and treasure-pool tag lists default to empty.

`public virtual CharacterDefinition CreateDefinition(GameContentRegistry registry)` resolves registered type references and returns a definition with copied data. A null registry throws an argument error. Trait content supplies the combined trait description; without traits, character `Description` is the fallback. `BaseStats` returns a `PlayerState` with fields such as hp/maxHp, attack, defense, and wisdom. Do not retain a live run's player object.

| Declaration | Current behavior |
| --- | --- |
| `TraitTypes` | Resolves IDs; current character traits participate in rules |
| `StartingMoveTypes` | First entry becomes the initial move; later entries are not equipped |
| `StartingTreasureTypes` | Stored and validated; not granted on selection |
| `TreasurePoolTags` | Creates the default allowed-tag list |
| `TreasurePool` | Include/Exclude/SetWeight overrides determine final eligibility |

`TreasurePoolDefinition.FromBuiltInCharacter(string characterId)` copies the current full built-in pool without changing its source. The new character can adjust it. Game updates to the source pool affect subsequently created copies. `BuiltInCharacterIds.RuneHunter` and `.GroveAlchemist` expose stable IDs; localized names are not references.

## TraitContent and MoveContent

`TraitContent` defines name and description and responds to shared content events. In `OnBeforeNormalAttackTargets(BeforeNormalAttackTargetsEvent e)`, `additionalRandomTargets` is an additive field for extra random attack targets.

For moves, `TargetKind` controls targeting, `MaxUses` sets uses per stage, and `AttackMultiplier` sets base damage scaling. `MoveTargetKind.Enemy` needs a specific exposed enemy. Automatic calls have no explicit target column; use a suitable `RandomEnemy` path when automatic enemy selection is intended, and test it. Requested triggers are not successful resolutions.

Structured `MultiHit` resolves damage per hit, but `MoveUsed` still runs once per use. Use multiple hits only when presentation can show each hit; use one Damage node for a single presentation. See the [overview](../02-content-creation.md).

## EnemyContent and EnemyTraitContent

Override `Description`, `Attack`, `Defense`, `MaxHp`, and `RewardGold`. `Icon` and `EnemyTraitId` default to empty. `public virtual CardState CreateCard(string instanceId = null)` retains the definition ID in `contentId` and uses the supplied instance ID, or definition ID, for `id`. Give multiple cards distinct instance IDs.

One `EnemyTraitId` can identify a composite trait with several callbacks. `OnAfterDamaged(EnemyTraitEvent e)` runs only after positive HP loss. `OnRoundStart(EnemyTraitEvent e)` is the enemy response window after a basic attack; defeated or no longer exposed enemies do not participate. It is not a stage-entry or universal player-action callback.

| EnemyTraitEvent member | Access/meaning |
| --- | --- |
| `State` | Read-only property referencing this run |
| `Owner` | Read-only reference to this enemy's CardState; its instance fields can change |
| `ColumnIndex` | Read-only column index |
| `DamageDealt` | Read-only, nonnegative damage data |
| `Runtime` | Shared queued damage/death operations |

`EnemyTraitDamageEvent` supplies `IncomingDamage`, `FinalDamage`, `Prevented`, `AddDamage(int)`, `ReduceDamage(int)`, and `PreventDamage()`. The result properties are not directly assignable. Keep counters off shared trait definitions. `GetRuntimeStatus(CardState owner)` and `TryGetRuntimeStatusCount(CardState owner, out int count)` expose presentation, not rule execution.

Enemy traits have no treasure-style `OnSceneReset`. New cards start fresh; cloning and saves preserve existing-card counters. Countdown uses the primary counter, so composite traits need distinct state fields. See [Lifecycle](lifecycle.md).
