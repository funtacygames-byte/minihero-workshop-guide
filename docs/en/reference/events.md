# Rule events and field semantics

[简体中文](../../zh-CN/reference/events.md) · [Index](../README.md)

Guide revision 6 · Mod API 1.10.0 · 2026-10-17

Baseline: 1.10.0. Override callbacks on public content classes, such as `public override void OnAfterHealing(AfterHealingEvent e)`. See [API surface](api-surface.md) for fields and [Lifecycle](lifecycle.md) for execution phases. Do not dispatch host events yourself.

## Shared event context

`GameRuleEvent` exposes read-only `State`, `Source`, `SourceLevel`, `IsPreview`, `TreasureState`, `MoveState`, `EnemyState`, and `Runtime`, plus `int Percent(int amount, int percent)`. The host binds them; constructing an event yourself does not create runtime context.

`State` references this settlement context. `SourceLevel` defaults to 1 and `IsPreview` to false; unbound references can be null. Read them in the relevant window without retaining them for another run. Shared accumulators and immediate Runtime calls are different execution paths; choose according to the contract.

## Common callbacks

| Callback/argument | Inputs | Additive outputs or purpose |
| --- | --- | --- |
| `OnTreasureStats(TreasureStatsEvent)` | Base stats, SourceLevel | attack/defense/maxHp flat and percent modifiers; wisdomFlat only |
| `OnStageEntered(StageEnteredEvent)` | stageIndex, stageId | Stage-entry rewards through Runtime |
| `OnBeforeHealing(BeforeHealingEvent)` | baseAmount, potion | bonusFlat, bonusPercent |
| `OnAfterHealing(AfterHealingEvent)` | requested, actual, overflow, potion | Effects based on settled healing |
| `OnBeforePlayerDamage(BeforePlayerDamageEvent)` | Incoming damage | Accumulated modifiers settled by the host |
| `OnPlayerDamageTaken(PlayerDamageTakenEvent)` | damage, absorbed, hpDamage | Distinguish shield absorption and HP loss |
| `OnEnemyKilled(EnemyKilledEvent)` | enemy, columnIndex, allEnemiesDefeated | restoreMoveUses, automaticInitialMoveTriggers |
| `OnMoveCapacity(MoveCapacityEvent)` | move, baseMaxUses | bonusMaxUses |
| `OnBeforeMoveResolved(BeforeMoveResolvedEvent)` | move, automatic | targetCount, damagePercent, damageFlat, and other modifiers |
| `OnAfterMoveResolved(AfterMoveResolvedEvent)` | hits, totalDamage, defeatedEnemies, automatic | shield accumulates shared rewards |
| `OnBeforeItemEffect(BeforeItemEffectEvent)` | item | bonusPercent, extraUseCount |
| `OnItemUsed(ItemUsedEvent)` | item, potion | restoreMoveUses |
| `OnNormalAttackResolved(NormalAttackResolvedEvent)` | damageDealt, hits, tookDamage | restoreMoveUses and other outputs |
| `OnColumnCleared(ColumnClearedEvent)` | columnIndex | automaticInitialMoveTriggers requests |

This is a common-event index, not the complete event set. Inputs are not arbitrary reward channels. Usually add with `+=` so another content's contribution is preserved.

## Healing: requested is already settled

`BeforeHealingEvent` accumulates healing modifiers before the host calculates the full healing amount. `AfterHealingEvent.requested` is that settled amount, used by all healing-linked rules even at full HP. `actual` measures HP-bar gain only; `overflow` serves rules explicitly converting overflow.

| HP before healing | Settled healing | requested | actual | overflow |
| --- | ---: | ---: | ---: | ---: |
| 20 / 30 | 15 | 15 | 10 | 5 |
| 30 / 30 | 15 | 15 | 0 | 15 |

Count healing after modifiers. Do not translate this as pre-modifier attempted healing or actual HP restored. Use natural concise “healing” in player descriptions and explain its definition here. Explicit overflow-only rules still state that condition.

## Shield after moves and automatic requests

`AfterMoveResolvedEvent.shield` may already include the move's own shield reward. Add with `e.shield += amount`; the core grants the total after dispatch. Do not also call `e.Runtime.AddShield(amount)` for the same reward.

A column is cleared only after its last card is removed. Defeating a top enemy with an exit underneath does not clear it. `automaticInitialMoveTriggers` starts at 0 and requests calls; the host does not replace it with a success count. Without an initial move or legal target, requests can fail. Count completed resolutions with `OnAfterMoveResolved` and `automatic == true`. There is currently no identifier linking a particular column-clear request to its result.

## Percentages and preview

Add percentages of the same kind before shared settlement. `Percent` uses the common percentage rule; current `AdditiveModifierMath.PercentDelta` rounds fractional deltas away from zero. Content-specific base-stat conversions follow their specified floor rule. Do not replace every percentage operation with integer division. Preview and execution share calculations; preview must not consume real uses or advance counters.

After changing a callback, test timing, empty targets, caps, stacking, stage changes, and saves. See the [content overview](../02-content-creation.md) for recipes and advanced windows.
