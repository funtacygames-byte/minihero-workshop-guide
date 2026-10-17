# TreasureContent 与品质、等级、池

[English](../../en/reference/treasures.md) · [目录](../README.md)

教程修订 6 · Mod API 1.10.0 · 2026-10-17

用途：定义宝物、创建运行时宝物实例，并响应统一规则事件。当前基准 1.10.0；[完整公开声明](api-surface.md)，[实际制作步骤](../tutorials/treasure.md)。

## 常用属性及默认值

| 属性／方法 | 类型／默认 | 语义 |
| --- | --- | --- |
| `Id` | `string`，构造函数指定 | 稳定内容 ID，不是显示名 |
| `Name` | `string` | 玩家名称，通常覆写 |
| `Rank` | `TreasureRank` | 默认／最高品质，多品质下与当前 `Quality` 区分 |
| `BaseValue` | `int` | 定义基础效果值，是否乘等级由具体规则决定 |
| `Describe(int level)` | `string`，abstract | 当前等级的准确描述 |
| `SellGold` | `int = 1` | 回收基础价值 |
| `MaxLevel` | `GameRules.TreasureMaxLevel` | 可升级等级上限 |
| `Exclusive` | `Rank == Legendary` | 默认传说视为专属 |
| `IncludeInDefaultChestPool` | `!Exclusive` | 是否进入默认宝箱候选；仍受其他条件约束 |
| `CategoryTags` | 默认沿用 `PoolTags` | 旧内容兼容默认；新内容显式分类 |
| `PoolTags` | 空列表 | 角色池候选标签 |
| `GetPoolWeight(string poolTag)` | `float = 1f` | 指定池内的相对权重 |
| `FunctionTags` | 空列表 | 构筑检索，独立于分类与池 |
| `ActivationKind` | `Passive` | 主动／被动入口 |
| `MaxUses` | 被动 0，否则 1 | 主动宝物每场景额度 |
| `CreateState(int level = 1)` | `TreasureState` | 限制等级范围，创建独立运行时状态 |

`Quality`、`EffectValue` 是多品质运行时实例数据，setter 为 protected；不要把最高品质 `Rank` 当成每个实例的当前品质。`IMultipleVariantEffect.GetVariants()` 返回实际提供的品质版本。五／四／三／两档分别从普通／优良／稀有／史诗到传说，不补缺失数值。完整实现见[内容总览](../02-content-creation.md)。

不实现 `IMultipleVariantEffect` 且不覆写 `GetStateVariants()` 的普通内容，默认提供五档品质；`Exclusive` 内容默认只提供传说。仅写 `Rank => Common` 不会把默认品质列表限制为普通，也不会自动为不同品质生成不同效果值。首课因此在各品质共用同一公式。图鉴默认选最高可用品质，品质箭头不改变宝物等级；想限定档位或配置分档数值，要显式提供实际版本。

## 事件与状态契约

```csharp
public abstract string Describe(int level);
public virtual TreasureState CreateState(int level = 1);
public virtual void OnStageEntered(StageEnteredEvent gameEvent);
public virtual void OnSceneReset();
public virtual GameActionResult Execute(TreasureState treasure, TreasureActivationContext context);
```

这是签名查询，`OnStageEntered` 和 `OnSceneReset` 继承自公共内容基类。入场事件的 `SourceLevel` 是这件宝物等级，`Runtime` 提供统一结算。`Execute` 默认返回 `passive_treasure` 失败，被动宝物无需覆写；主动执行失败不消耗次数。

宝物类加 `[System.Serializable]` 并提供公开无参构造函数。进度、层数、待用奖励和额度保存于具体运行时实例；按默认新场景重置，不用 static。简单值字段会随实例克隆，引用型可变集合必须特别核对深拷贝与存档行为，不能仅因 `CloneRuntime()` 存在就假定所有内部集合独立。

## 三种标签与筛选

`CategoryTags` 只表达玩法分类；`PoolTags` 与角色允许标签按任意交集形成候选；`RequiredAppearanceTags` 是额外出场条件。角色 `TreasurePool` 的 Include/Exclude 和品质、专属、出场条件仍可能影响最终候选。允许入池不保证一次随机抽到。

护盾、最大生命、恢复和相关循环属于当前生命体系分类。伤害招式强化使用通用招式事件；不要因规则读攻击值就自动归通用。池内权重用数值，禁止加第二个 Tag 代替倍率。

## 验证提示

比较一级／最高等级、所有提供品质、触发上限、换场景、读档、预览／执行和同类百分比叠加。描述与执行共用公式。确定获得宝物的办法见[宝物课](../tutorials/treasure.md)；完整条件见[测试总览](../04-testing-and-publishing.md)。
