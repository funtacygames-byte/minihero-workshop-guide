# 角色、招式与敌人接口

[English](../../en/reference/actors.md) · [目录](../README.md)

教程修订 5 · Mod API 1.8.0 · 2026-10-14

当前基准 1.8.0。方法与类型查[API 声明](api-surface.md)；步骤见[角色课](../tutorials/character.md)和[敌人课](../tutorials/enemy.md)。

## CharacterContent

`Role`、`School`、`BaseStats` 为抽象属性；`Description` 默认空，`IncludeInDefaultRoster` 默认 true。`TraitTypes`、`StartingTreasureTypes`、`StartingMoveTypes`、`TreasurePoolTags` 默认空列表。

`public virtual CharacterDefinition CreateDefinition(GameContentRegistry registry)` 解析已注册的类型引用并返回独立定义；registry 为空会抛参数错误。特性说明存在时从特性内容拼接，没有特性时使用角色 `Description`。`BaseStats` 返回 `PlayerState`，例如 hp/maxHp、attack、defense、wisdom；不要缓存正在运行的玩家对象。

| 声明 | 当前实际行为 |
| --- | --- |
| `TraitTypes` | 解析 ID，当前角色的特性参与规则 |
| `StartingMoveTypes` | 第一项成为初始招式；后续项不自动装备 |
| `StartingTreasureTypes` | 登记并校验；选角不授予 |
| `TreasurePoolTags` | 默认生成允许 Tag 列表 |
| `TreasurePool` | 可覆写 Include/Exclude/SetWeight，决定最终池 |

`TreasurePoolDefinition.FromBuiltInCharacter(string characterId)` 复制本体角色当前完整池，不修改来源。新角色可继续增删和调权；游戏更新本体池也会影响以后创建的复制结果。`BuiltInCharacterIds.RuneHunter` 与 `.GroveAlchemist` 提供稳定 ID，不用显示名引用角色。

## TraitContent 与 MoveContent

`TraitContent` 定义名称和说明，并响应公共内容规则事件。`OnBeforeNormalAttackTargets(BeforeNormalAttackTargetsEvent e)` 的 `additionalRandomTargets` 是累加字段，适用于额外随机攻击目标。

`MoveContent` 的 `TargetKind` 决定目标选择，`MaxUses` 是每场景次数，`AttackMultiplier` 是基础伤害倍率。`MoveTargetKind.Enemy` 需要明确指定暴露敌人；自动调用没有明确目标列，若要自动选敌人应使用合适的 `RandomEnemy` 路径并实测。调用次数请求不等于成功结算次数。

结构化招式的多段 `MultiHit` 逐段结算伤害；一次使用的 `MoveUsed` 仍只派发一次。只有表现能逐段反馈时才使用多段，单次表现按一次 Damage 节点组织。完整招式规则见[总览](../02-content-creation.md)。

## EnemyContent 与 EnemyTraitContent

敌人需要覆写 `Description`、`Attack`、`Defense`、`MaxHp`、`RewardGold`；`Icon` 和 `EnemyTraitId` 默认空。`public virtual CardState CreateCard(string instanceId = null)` 生成卡片，`contentId` 保留定义 ID，`id` 使用给定实例 ID或定义 ID。同场多实例用不同实例 ID。

一个 `EnemyTraitId` 可以指向覆写多个回调的复合特性。`OnAfterDamaged(EnemyTraitEvent e)` 只在实际正数生命损失后调用；`OnRoundStart(EnemyTraitEvent e)` 是普通攻击后敌人的回应窗口，已击败或不再暴露的敌人不会参加，不是进场或每种操作通用回调。

| EnemyTraitEvent 成员 | 读写／意义 |
| --- | --- |
| `State` | 只读属性，当前局状态 |
| `Owner` | 只读属性引用该敌人 CardState；可改它的实例字段 |
| `ColumnIndex` | 只读列下标 |
| `DamageDealt` | 只读本次伤害数据，非负 |
| `Runtime` | 通用伤害、死亡等队列操作 |

`EnemyTraitDamageEvent` 提供 `IncomingDamage`、`FinalDamage`、`Prevented` 和 `AddDamage(int)`、`ReduceDamage(int)`、`PreventDamage()`；后两结果不能直接赋值。计数不要存在共享特性对象上。`GetRuntimeStatus(CardState owner)` 和 `TryGetRuntimeStatusCount(CardState owner, out int count)` 用于状态展示，不代替真实规则执行。

敌人特性没有宝物式 `OnSceneReset`。新卡使用初始状态，克隆/读档复制现有卡的计数。倒计时占用主计数器，复合特性须安排独立字段，见[生命周期](lifecycle.md)。
