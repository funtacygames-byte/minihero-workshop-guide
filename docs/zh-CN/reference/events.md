# 常用规则事件与字段语义

[English](../../en/reference/events.md) · [目录](../README.md)

教程修订 6 · Mod API 1.10.0 · 2026-10-17

当前基准 1.10.0。公共内容类覆写事件方法，例如 `public override void OnAfterHealing(AfterHealingEvent e)`；字段定义查[API 表面](api-surface.md)，运行顺序查[生命周期](lifecycle.md)。不在 Mod 中自己派发宿主事件。

## 公共事件上下文

`GameRuleEvent` 提供只读属性 `State`、`Source`、`SourceLevel`、`IsPreview`、`TreasureState`、`MoveState`、`EnemyState`、`Runtime`，以及 `int Percent(int amount, int percent)`。它们由宿主绑定；手动 `new` 一个事件不会自动得到运行时上下文。

`State` 是当前结算上下文，`SourceLevel` 默认 1，`IsPreview` 默认 false，未绑定对象可能为空。只在合适窗口读取，避免保留到下一局。修改共享累加字段与立即调用 Runtime 是两种执行方式，按契约选一种。

## 事件速查

| 回调／参数 | 读取输入 | 累加输出或用途 |
| --- | --- | --- |
| `OnTreasureStats(TreasureStatsEvent)` | 基础属性、SourceLevel | attack/defense/maxHp 的 flat 与 percent 派生值；智慧只有 wisdomFlat |
| `OnStageEntered(StageEnteredEvent)` | stageIndex、stageId | 进场奖励；Runtime 统一结算 |
| `OnBeforeHealing(BeforeHealingEvent)` | baseAmount、potion | bonusFlat、bonusPercent |
| `OnAfterHealing(AfterHealingEvent)` | requested、actual、overflow、potion | 根据完整治疗量触发具体效果 |
| `OnBeforePlayerDamage(BeforePlayerDamageEvent)` | 伤害输入 | 累加增减字段，统一结算 |
| `OnPlayerDamageTaken(PlayerDamageTakenEvent)` | damage、absorbed、hpDamage | 正确区分护盾吸收与生命损失 |
| `OnEnemyKilled(EnemyKilledEvent)` | enemy、columnIndex、allEnemiesDefeated | restoreMoveUses、automaticInitialMoveTriggers |
| `OnMoveCapacity(MoveCapacityEvent)` | move、baseMaxUses | bonusMaxUses |
| `OnBeforeMoveResolved(BeforeMoveResolvedEvent)` | move、automatic | targetCount、damagePercent、damageFlat 等 |
| `OnAfterMoveResolved(AfterMoveResolvedEvent)` | hits、totalDamage、defeatedEnemies、automatic | shield 是共享奖励累加器 |
| `OnBeforeItemEffect(BeforeItemEffectEvent)` | item | bonusPercent、extraUseCount |
| `OnItemUsed(ItemUsedEvent)` | item、potion | restoreMoveUses |
| `OnNormalAttackResolved(NormalAttackResolvedEvent)` | damageDealt、hits、tookDamage | restoreMoveUses 等结算输出 |
| `OnColumnCleared(ColumnClearedEvent)` | columnIndex | automaticInitialMoveTriggers 请求数 |

此表是常用窗口，不是全部事件。输入字段不是随意覆盖的奖励通道；累加通常使用 `+=`，避免抹掉其他内容已经提供的值。

## 治疗：requested 不是增减前请求量

`BeforeHealingEvent` 先累加治疗增减，统一计算完整治疗量；`AfterHealingEvent.requested` 是这个结算量。所有治疗关联规则读取它，满血时也计量。`actual` 只表示生命条增加量，`overflow` 供明确只转换溢出的规则。

| 治疗前 HP | 增减后治疗量 | requested | actual | overflow |
| --- | ---: | ---: | ---: | ---: |
| 20 / 30 | 15 | 15 | 10 | 5 |
| 30 / 30 | 15 | 15 | 0 | 15 |

治疗先经过增减才计量，不把“治疗量”译成增减前 attempted healing 或 actual HP restored。玩家描述直接使用自然的“治疗量”，只在专门规则参考中解释定义。明确只转溢出的规则保留溢出条件。

## 招式后护盾与自动招式

`AfterMoveResolvedEvent.shield` 可以已包含招式本身的护盾奖励。监听器使用 `e.shield += amount`；派发结束后核心统一加盾。不再同时调用 `e.Runtime.AddShield(amount)`，否则重复。

清列发生在整列最后一张卡移除后；只击败顶层敌人、下面仍有出口时不算。`automaticInitialMoveTriggers` 是请求次数，默认 0，宿主不会回写成功数。无初始招式或合法目标时请求可能失败。统计已成功结算用 `OnAfterMoveResolved` 且 `automatic == true`；目前没有把某一个清列请求关联到对应结果的标识。

## 百分比与预览

同类百分比先相加，宿主统一结算。`Percent` 使用共享百分比规则；当前 `AdditiveModifierMath.PercentDelta` 对非整数增量按远离零方向取整。读取基础属性的专属换算按规则向下取整，不要把所有百分比公式一概写成整数除法。预览与执行使用同一计算逻辑，预览不得提前消耗次数或推进真实计数。

改变一种事件选择后，实测触发窗口、空目标、上限、叠加、换场景与读档。完整配方与进阶窗口见[内容总览](../02-content-creation.md)。
