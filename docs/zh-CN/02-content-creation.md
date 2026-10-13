# 02 内容制作

[English](../en/02-content-creation.md) · [教程目录](README.md)

教程修订 2 · 核对日期：2026-10-13 · Mod API：1.8.0。

第一次制作先读[首课](tutorials/first-mod.md)。本文是工程手册；按目标制作见[任务目录](README.md)。

本篇集中讲所有玩法内容。重点不是背代码，而是理解内容之间怎样绑定、宝物应该选择哪个规则事件、品质和等级怎样表示，以及带计数的效果如何安全重置。

## 目录

1. 注册规则和稳定 ID
2. 宝物类逐行解释
3. 从需求句选择事件
4. 常用宝物事件与功能配方
5. 品质、等级和多品质数值
6. 累计次数、场景重置和永久状态
7. 角色、特性、技能和专属宝物池
8. 敌人、敌人特性和关卡
   - StageGraph 节点路线与条件边
9. 道具与奇遇事件
10. 完整内容的注册检查

## 一、注册规则和稳定 ID

每个内容类都要满足：`public`、可实例化、公开无参构造函数、稳定且唯一的内容 ID、在 `Load` 中注册。ID 必须以当前包 ID 加点号开头，例如：

```text
local.alice.lantern-trail.treasure.amber_lantern
local.alice.lantern-trail.character.lantern_ranger
local.alice.lantern-trail.enemy.moss_wolf
```

显示名称可以修改，稳定 ID 不应随名称变化。角色和关卡的跨内容引用依赖 ID 或 C# 类型，随意改 ID 会让旧存档或其他内容失去绑定。

入口注册示例：

```csharp
public override void Load(IModRegistrar registrar)
{
    registrar.AddContents(
        new LanternSight(),
        new SilverBolt(),
        new AmberLantern(),
        new MoonGlassBottle(),
        new LanternRanger(),
        new WoundedRage(),
        new MossWolf(),
        new MoonDewPotion(),
        new TwilightMeadowStage(),
        new WhisperingGroveStage(),
        new LanternRuinsStage(),
        new LanternExpedition());
}
```

## 二、宝物类逐行解释

```csharp
[System.Serializable]
public sealed class AmberLantern : TreasureContent, IModPresentationContent
{
    public AmberLantern()
        : base(ModEntry.PackageId + ".treasure.amber_lantern") { }

    public override string Name => ModText.Get(
        ModEntry.PackageId, "treasure.amber_lantern.name", "琥珀提灯");
    public override TreasureRank Rank => TreasureRank.Rare;
    public override int BaseValue => 3;
    public override int SellGold => 4;
    public override int MaxLevel => 3;
    public override IReadOnlyList<string> CategoryTags =>
        new[] { TreasureCategoryTags.Shield };
    public override IReadOnlyList<string> PoolTags =>
        new[] { "treasure_pool.local.alice.lantern" };

    public override string Describe(int level) =>
        $"进入场景时获得 {BaseValue * level} 点护盾。";

    public override void OnStageEntered(StageEnteredEvent e)
    {
        e?.Runtime?.AddShield(BaseValue * e.SourceLevel);
    }

    public ModPresentation Presentation =>
        ModAssets.Icon("assets/icons/amber-lantern.png");
}
```

- 构造函数只确定稳定 ID，不应读取当前存档。
- `Rank` 是默认/最高品质。
- `BaseValue` 是基础效果值；是否乘等级由真实规则决定。
- `SellGold` 是回收基础价值。
- `MaxLevel` 是宝物可升级上限。
- `CategoryTags` 是图鉴和构筑语义，不参与角色抽取池。
- `PoolTags` 决定角色候选池，与角色允许 Tag 任意一项相同即可入池。
- `Describe(level)` 必须与真实执行走同一公式。
- `SourceLevel` 是当前宝物等级；`Runtime` 提供护盾、恢复、伤害、闪避和永久属性等统一结算能力。
- `Presentation` 绑定包内图片。

## 三、从需求句选择事件

不要只写“做一个回血宝物”。先把需求拆成六项：

1. 触发：进场、承伤、治疗后、击杀、清列、道具还是招式？
2. 输入：基础属性、治疗量、实际伤害、列位置还是累计次数？
3. 主收益：恢复、护盾、属性、金币、招式次数还是伤害？
4. 状态：立即、持续、场景累计、场景重置还是整局永久？
5. 目标：玩家、随机敌人、最高生命敌人、某一列还是全体？
6. 限制与代价：每场景次数、品质、上限、生命损失或负面效果？

例如：

> 每次药剂治疗后，按治疗量的 30% 获得护盾；每场景最多触发 3 次，换场景重置；只进入药剂角色池。

这句话已经明确了触发、输入、收益、状态、上限和池归属，代码生成会比“做一个药剂宝物”可靠很多。

## 四、常用宝物事件与功能配方

| 需求 | 事件 | 关键字段/接口 |
| --- | --- | --- |
| 固定或百分比属性 | `OnTreasureStats` | `attackFlat`、`defenseFlat`、`maxHpFlat`、`wisdomFlat`、百分比字段 |
| 进入场景奖励 | `OnStageEntered` | `Runtime.Heal/AddShield/GainDodge` |
| 治疗增幅 | `OnBeforeHealing` | `bonusFlat/bonusPercent` |
| 治疗结算后触发 | `OnAfterHealing` | `requested/actual/overflow/potion` |
| 承伤增减 | `OnBeforePlayerDamage` | `bonusPercent` |
| 承伤结果 | `OnPlayerDamageTaken` | `damage/absorbed/hpDamage` |
| 击杀 | `OnEnemyKilled` | `columnIndex/allEnemiesDefeated/restoreMoveUses` |
| 招式使用次数 | `OnMoveCapacity` | `baseMaxUses/bonusMaxUses` |
| 招式前强化 | `OnBeforeMoveResolved` | `targetCount/damagePercent/damageFlat/preferHighestHp` |
| 招式后奖励 | `OnAfterMoveResolved` | `automatic/totalDamage/defeatedEnemies/shield` |
| 道具强化 | `OnBeforeItemEffect` | `bonusPercent/extraUseCount` |
| 使用道具后 | `OnItemUsed` | `item/potion/restoreMoveUses` |
| 普通攻击 | `OnNormalAttackResolved` | `damageDealt/hits/restoreMoveUses` |
| 清空一列 | `OnColumnCleared` | `columnIndex/automaticInitialMoveTriggers` |

固定攻击：

```csharp
public override void OnTreasureStats(TreasureStatsEvent e)
{
    e.attackFlat += 2 * e.SourceLevel;
}
```

治疗增加 20%：

```csharp
public override void OnBeforeHealing(BeforeHealingEvent e)
{
    e.bonusPercent += 20;
}
```

同类百分比会先相加再以基础值统一计算，不要在每件宝物中自行连续乘法。

击杀恢复招式次数：

```csharp
public override void OnEnemyKilled(EnemyKilledEvent e)
{
    e.restoreMoveUses += Math.Min(2, e.SourceLevel);
}
```

招式额外攻击一个目标：

```csharp
public override void OnBeforeMoveResolved(BeforeMoveResolvedEvent e)
{
    e.targetCount += 1;
}
```

按最大生命获得护盾：

```csharp
public override void OnStageEntered(StageEnteredEvent e)
{
    int maxHp = Math.Max(0, e?.State?.player?.maxHp ?? 0);
    int shield = e?.Percent(maxHp, 10) ?? 0;
    e?.Runtime?.AddShield(shield);
}
```

`Percent` 使用游戏统一取整规则。不要直接找场景 GameObject、改 UI 或手工扣敌人生命；规则必须通过事件字段和 `Runtime`，才能保证预览、实战和多宝物叠加一致。

`OnColumnCleared(ColumnClearedEvent e)` 只在某列的整份 `cards` 列表变空后触发；只移除敌人但下面还有事件、出口或其他卡牌时不算清列。核心比较操作前后的空列数量，按净增加值为新清空列派发事件，同一次结算最多对每个新清空列派发一次；之后若该列重新补牌、后来再变空，可再次触发。`columnIndex` 是本次清空的列下标。

`automaticInitialMoveTriggers` 是监听器累加的**自动初始招式请求次数**，初始为 0；所有 `OnColumnCleared` 监听器处理完后，核心再按该数调用自动招式。它不是实际成功结算次数，也不会被核心回写结果。没有初始招式或没有合法目标时，自动招式会提前停止。若要统计已成功结算的自动招式，可监听 `OnAfterMoveResolved` 并检查 `automatic == true`；这个字段只表示本次招式自动结算，不能说明它由哪次清列请求触发。

自动初始招式不带玩家指定的目标列（内部目标列为 `-1`）。`MoveTargetKind.Enemy` 需要一个明确的目标列，因此即使场上有敌人，也不能靠这种自动调用选中目标；如果设计要求自动招式从明牌敌人中自行选目标，应使用 `MoveTargetKind.RandomEnemy`，并分别验证有目标与无目标时的结果。普通手动指定目标的招式仍可用 `MoveTargetKind.Enemy`。

`OnAfterMoveResolved` 的 `shield` 是招式后护盾结果的共享累加字段。监听器应使用 `e.shield += amount`，核心会在所有监听器结束后统一应用；若在同一回调里同时调用 `e.Runtime.AddShield(amount)` 并增加 `e.shield`，护盾会结算两次。该字段可与 `automatic` 一起用于按成功自动招式结算护盾。

承伤字段要分清：`damage` 是减伤后的总承伤，包含护盾吸收；`absorbed` 是护盾实际吸收；`hpDamage` 是生命实际损失。治疗字段中，`requested` 是治疗增减结算后的完整治疗量，包含满血时的治疗与溢出；治疗关联规则统一读取它。`actual` 是生命条增加量，只用于资源与表现；`overflow` 只用于明确转换溢出部分的效果。玩家说明默认写“治疗量”。

## 五、品质、等级和多品质数值

代码枚举与显示品质对应：

| 显示品质 | 代码 |
| --- | --- |
| 普通 | `Common` |
| 优良 | `Uncommon` |
| 稀有 | `Rare` |
| 史诗 | `Epic` |
| 传说 | `Legendary` |

品质和等级不是一回事。品质决定稀有度与基础数值版本，等级是局内升级，通常读取 `SourceLevel`。固定公式、没有多档数值的宝物可直接做传说单版本。五档依次为普通至传说；四档从优良开始，三档从稀有开始，两档从史诗开始。只有设计明确给出多档数值时才实现 `IMultipleVariantEffect`，不要擅自补齐缺失品质。

描述应说明数值依据、等级关系、上限、持续时间和触发次数。宝物临时状态默认进入新场景重置，无需逐条重复；跨场景保留机制必须明确写出。预览和真实执行必须复用同一数值来源，避免描述显示 6 点、实战只给 3 点。

## 六、累计次数、场景重置和永久状态

```csharp
[System.Serializable]
public sealed class TinkerAbacus : TreasureContent
{
    private int itemUses;
    private int rewardsThisScene;

    public TinkerAbacus()
        : base(ModEntry.PackageId + ".treasure.tinker_abacus") { }
    public override string Name => "工匠算珠";
    public override TreasureRank Rank => TreasureRank.Rare;
    public override int BaseValue => 4;
    public override string Describe(int level) =>
        $"每使用 3 次道具，获得 {BaseValue * level} 点护盾；每场景最多触发 2 次。";

    public override void OnItemUsed(ItemUsedEvent e)
    {
        itemUses++;
        if (itemUses < 3 || rewardsThisScene >= 2) return;
        itemUses -= 3;
        rewardsThisScene++;
        e.Runtime?.AddShield(BaseValue * e.SourceLevel);
    }

    public override void OnSceneReset()
    {
        itemUses = 0;
        rewardsThisScene = 0;
    }
}
```

局内计数存放在运行时宝物实例字段。需要每场景重置的字段必须在 `OnSceneReset` 清零。真正的整局永久属性使用 `Runtime.AddPermanentAttack`、`AddPermanentDefense`、`AddPermanentMaxHp`；不能靠“忘记重置计数”模拟永久效果。

累计治疗量的写法：

```csharp
private int accumulatedHealing;
private int rewardsThisScene;

public override void OnAfterHealing(AfterHealingEvent e)
{
    if (e == null || e.requested <= 0) return;
    CountAmount(
        ref accumulatedHealing,
        ref rewardsThisScene,
        e.requested,
        10,
        2,
        () => e.Runtime?.AddPermanentMaxHp(1));
}

public override void OnSceneReset()
{
    accumulatedHealing = 0;
    rewardsThisScene = 0;
}
```

## 七、角色、特性、技能和专属宝物池

```csharp
public sealed class LanternRanger : CharacterContent
{
    public LanternRanger()
        : base(ModEntry.PackageId + ".character.lantern_ranger") { }
    public override string Name => "提灯游侠";
    public override string Role => "猎人";
    public override string School => "林地巡守";
    public override string Description => "以提灯与轻弩保护旅队。";
    public override PlayerState BaseStats => new PlayerState
    { hp = 24, maxHp = 24, attack = 6, defense = 1, wisdom = 2 };

    public override IReadOnlyList<Type> TraitTypes =>
        new[] { typeof(LanternSight) };
    public override IReadOnlyList<Type> StartingMoveTypes =>
        new[] { typeof(SilverBolt) };
    // 当前运行时不会在选角时发放 StartingTreasureTypes：
    // public override IReadOnlyList<Type> StartingTreasureTypes => new[] { typeof(AmberLantern) };
    public override IReadOnlyList<string> TreasurePoolTags =>
        new[] { "treasure_pool.local.alice.lantern" };
}
```

- `TraitTypes` 绑定角色特性。
- `StartingMoveTypes` 声明角色的开局招式 ID；当前运行时只把第一项加载为 `State.initialMove`，不会把列表后续项放入普通招式槽，因此只声明一个可用开局招式。
- `StartingTreasureTypes` 目前只写入并校验 `CharacterDefinition.startingTreasureIds`；当前选角流程不会据此授予开局宝物，不要把它当作已生效的功能或向玩家承诺。
- `TreasurePoolTags` 表示以后开宝箱允许哪些池。
- 宝物 `PoolTags` 与角色允许 Tag 任意交集即可入池。
- `CategoryTags` 不参与池判断。
- `GetPoolWeight(poolTag)` 调整池内相对权重，默认 1，特色内容可用 2。

普通角色只声明 `TreasurePoolTags` 即可。需要在 Tag 基础上做少量例外时，覆写统一的
`TreasurePool`：`Exclude` 移除 Tag 原本带入的宝物，`Include` 强制加入明确宝物，
`SetWeight` 覆盖这件宝物只在当前角色池中的权重；这些操作不会修改宝物自己的 `PoolTags`。

```csharp
public override TreasurePoolDefinition TreasurePool =>
    base.TreasurePool
        .Exclude(
            "goblin_brass_scale",
            "veterans_wrap")
        .Include(
            ModEntry.PackageId + ".treasure.lantern_compass")
        .SetWeight(
            ModEntry.PackageId + ".treasure.lantern_compass",
            2f);
```

若想以游戏本体某个角色的**完整宝物池**为基础，按该角色的稳定 ID 复制后再调整：

```csharp
public override TreasurePoolDefinition TreasurePool =>
    TreasurePoolDefinition.FromBuiltInCharacter("grove_alchemist")
        .Exclude("sundered_vambrace")
        .Include(ModEntry.PackageId + ".treasure.lantern_compass")
        .SetWeight(ModEntry.PackageId + ".treasure.lantern_compass", 2f);
```

这会复制林地药师当前的 Tag、明确加入的宝物、排除项和单件权重；修改只作用于新角色，不会改动本体角色。角色定义中的 `treasurePoolTags` 会自动反映复制后的 Tag。新角色仍需照常注册，`Include` 的自制宝物也必须已注册。此引用每次建立角色定义时读取当前游戏版本的本体池，所以游戏更新本体池后，新角色会继承更新后的基础池。

若角色只允许很少几件宝物，不必先声明 Tag 再排除大量内容，可以直接建立明确清单：

```csharp
public override TreasurePoolDefinition TreasurePool =>
    TreasurePoolDefinition.Create()
        .Include(
            "goblin_brass_scale",
            ModEntry.PackageId + ".treasure.lantern_compass");
```

同一个宝物 ID 不能同时出现在 `Include` 和 `Exclude`。`SetWeight` 指向不存在或不在最终池中的宝物时，Mod 加载校验会直接报错。

特性继承 `TraitContent`，可以响应统一规则事件。技能继承 `MoveContent`：`TargetKind.Enemy` 表示需要拖到指定敌人，`MaxUses` 是每场景次数，单段伤害使用 `MoveEffectKind.Damage`。`MoveEffectKind.MultiHit` 只应用在表现层能够逐段播放命中反馈的真正连射，并分别设置 `hitCount`、`percentValue` 与 `stopWhenTargetDies`；如果 UI/特效只播放一次，应将总伤害合并为一个 `Damage` 节点。多目标、追加伤害或技能后奖励继续使用统一招式事件。

结构化 `MultiHit` 会按 `hitCount` 逐段结算；`flatValue + 攻击 × percentValue / 100` 是每一段的基础伤害，并向下取整后再结算统一伤害加成。传入伤害大于 0 的每段分别调用 `OnBeforeDamaged`；经过修正后实际扣除生命的每段会调用一次 `EnemyTraitContent.OnAfterDamaged`。被免疫、最终伤害为 0 或没有实际扣除生命的段数不会触发 `OnAfterDamaged`。致死段的受伤后事件先执行，再进入死亡处理。

多段节点锁定最初选中的敌人实例。目标死亡后，剩余段不会改打该列新露出的敌人；`stopWhenTargetDies = true` 会在确认原目标死亡后立即结束循环。设为 `false` 也不会改选其他敌人，因为后续段找不到原目标就会停止。`MoveUsed` 仍是一招一次的事件，不会按每段重复派发；需要按实际段数叠加敌人特性时，应处理受击后的 `OnAfterDamaged`。

## 八、敌人、敌人特性和关卡

```csharp
public sealed class WoundedRage : EnemyTraitContent
{
    public WoundedRage()
        : base(ModEntry.PackageId + ".enemy_trait.wounded_rage") { }
    public override string Name => "负伤狂怒";
    public override string Description => "受到伤害后，攻击增加 1。";
    public override void OnAfterDamaged(EnemyTraitEvent e)
    {
        if (e?.Owner != null) e.Owner.enemyTraitAttackDelta += 1;
    }
}

public sealed class MossWolf : EnemyContent
{
    public MossWolf() : base(ModEntry.PackageId + ".enemy.moss_wolf") { }
    public override string Name => "苔背魔狼";
    public override string Description => "潜伏于林地苔丛中的魔狼。";
    public override int Attack => 6;
    public override int Defense => 1;
    public override int MaxHp => 18;
    public override int RewardGold => 5;
    public override string EnemyTraitId =>
        ModEntry.PackageId + ".enemy_trait.wounded_rage";
}
```

敌人特性可响应静态属性、玩家攻击、受伤前后、回合开始/结束、死亡、观察其他敌人死亡和倒计时。敌人特性对象是内容定义，不要把单个敌人的变化存进特性类字段；可变状态保存在事件中的 `e.Owner`（该敌人自己的 `CardState`）上。

`CardState` 公开了这些可序列化、按敌人实例隔离的字段：`enemyTraitCounter`（主计数）、`enemyTraitSecondaryCounter`（第二计数）、`enemyTraitPhase`（阶段）、`enemyTraitTriggered`（一次性标记）、`enemyTraitAttackDelta` 和 `enemyTraitDefenseDelta`（此敌人的攻防增量）。当前没有供 Mod 自定义任意键值的通用字典 API。`enemyStatuses` 用来保存实际的状态效果，不要把它当成任意数据存储。

每张 `CardState` 只有一个 `enemyTraitId`，`EnemyContent.EnemyTraitId` 也只返回一个 ID；核心按这个 ID 查找并调用一份 `EnemyTraitContent`。若敌人有多个特性效果，把相关规则写进同一个 `EnemyTraitContent` 子类，覆写所需的多个事件方法即可，不需要给卡牌增加第二个特性 ID。内容定义对象会被多个敌人实例共享，所以所有计数、层数和累计属性都应放在事件的 `e.Owner` 上。

例如，下面这一个特性类同时处理受伤叠攻和敌方回应阶段加防。核心只会为实际扣除生命的受伤触发 `OnAfterDamaged`；每满 3 次加一层攻击，最多三层。`OnRoundStart` 在玩家的普通攻击结算后、敌人意图/反击前执行；每个仍然暴露的参与敌人各执行一次，已被击败的敌人会跳过。此回调不是场景刚进入、使用道具或使用招式时都会执行的通用回合事件。

```csharp
using System;
using MiniAdventureWorld.Core;

public sealed class CinderplateAwakening : EnemyTraitContent
{
    public CinderplateAwakening()
        : base(ModEntry.PackageId + ".enemy_trait.cinderplate_awakening") { }

    public override string Name => "烬甲觉醒";
    public override string Description => "每承受3次有效伤害，攻击提高1（该敌人存续期间保留），最多3层；敌人回应阶段开始时，每层再提高1防御。";

    public override void OnAfterDamaged(EnemyTraitEvent e)
    {
        CardState owner = e?.Owner;
        if (owner == null || owner.enemyTraitSecondaryCounter >= 3) return;
        owner.enemyTraitCounter++;
        if (owner.enemyTraitCounter < 3) return;
        owner.enemyTraitCounter = 0;
        owner.enemyTraitSecondaryCounter++;
        owner.enemyTraitAttackDelta++;
    }

    public override void OnRoundStart(EnemyTraitEvent e)
    {
        CardState owner = e?.Owner;
        if (owner != null)
            owner.enemyTraitDefenseDelta += Math.Max(0, owner.enemyTraitSecondaryCounter);
    }
}
```

此例的防御会在每次符合条件的普通攻击回应阶段按当前层数累加；达到三层后，每次该回调都会再加 3 防御。若设计想要固定防御上限，应另用专属可序列化字段或 `enemyTraitPhase`/`enemyTraitTriggered` 规划状态转换，不能把内容对象的字段当作单个敌人的计数。

下面示例每次受伤累计一次，每满 3 次攻击增加 1，最多增加 3。进度和层数都写在每个敌人自己的 `CardState` 中：

```csharp
using System;
using MiniAdventureWorld.Core;

public sealed class ThreefoldRage : EnemyTraitContent
{
    public ThreefoldRage()
        : base(ModEntry.PackageId + ".enemy_trait.threefold_rage") { }

    public override string Name => "三叠怒意";
    public override string Description => "每受到 3 次伤害，攻击增加 1，最多增加 3。";

    public override void OnAfterDamaged(EnemyTraitEvent e)
    {
        CardState owner = e?.Owner;
        if (owner == null || owner.enemyTraitSecondaryCounter >= 3) return;

        owner.enemyTraitCounter++;
        if (owner.enemyTraitCounter < 3) return;

        owner.enemyTraitCounter = 0;
        owner.enemyTraitSecondaryCounter++;
        owner.enemyTraitAttackDelta++;
    }

    public override string GetRuntimeStatus(CardState owner) =>
        $"【受击进度 {Math.Max(0, owner?.enemyTraitCounter ?? 0)}/3｜攻击加成 {Math.Max(0, owner?.enemyTraitSecondaryCounter ?? 0)}/3】";

    public override bool TryGetRuntimeStatusCount(CardState owner, out int count)
    {
        count = Math.Max(0, owner?.enemyTraitSecondaryCounter ?? 0);
        return true;
    }
}
```

当 `Countdown` 大于 0 时，核心倒计时流程会自动增加并在触发时清零 `enemyTraitCounter`，所以不要同时把它当作另一种进度。需要第二个计数时使用 `enemyTraitSecondaryCounter`，并给每个字段安排单一含义。`CardState.Clone()` 会复制这些实例字段；存档恢复也保留当前实例状态。新建敌人卡会从初始字段值开始，换到新场景后创建的新敌人不会继承旧敌人的计数。`EnemyTraitContent` 没有 `OnSceneReset`；要显示自定义状态数量可覆写 `TryGetRuntimeStatusCount`，文字说明可覆写 `GetRuntimeStatus`。

关卡的 `appearancePool` 是随机发牌候选；`fixedColumns` 是固定列中从底到顶的牌，类型为 `List<CardColumnState>`，每列的牌保存在 `CardColumnState.cards: List<CardState>`。

只要 `fixedColumns` 非空，核心就采用完整固定布局：列数取 `fixedColumns.Count`，每列按 `cards` 原顺序克隆，空列保持为空；不会再用 `appearancePool` 随机补牌，`columnCount` 和配置的 `generatedCardCount` 也不会决定布局。运行时的场景卡牌总数改为所有固定列的牌数之和。因此目前不能把左侧固定列与其余随机列混在同一个 `StageDefinition` 中。若需要整场随机发牌，留空 `fixedColumns` 并使用 `appearancePool`；若需要固定布局，就在 `fixedColumns` 中明确提供每张牌。

当前 C# 工坊校验在 `fixedColumns` 非空时检查固定列中的 `CardType.Exit`，随机布局则检查 `appearancePool`。对应布局缺少出口时报告 `AW_STAGE_EXIT_MISSING`。池中可以保留出口模板以兼容较早版本，但固定布局运行时会忽略它，不会把它加入实际棋盘。

```csharp
EnemyContent wolf = registry.Get<EnemyContent>(
    ModEntry.PackageId + ".enemy.moss_wolf");
CardState ignoredPoolExit = ContentCards.Card(
    Id + ".ignored_pool_exit", CardType.Exit, "出口模板", "固定布局不会使用此牌。");
ignoredPoolExit.appearanceWeight = 1f;

return new StageDefinition
{
    id = Id,
    name = Name,
    subtitle = Subtitle,
    columnCount = GameRules.ColumnCount,
    appearancePool = new List<CardState> { ignoredPoolExit },
    fixedColumns = new List<CardColumnState>
    {
        new CardColumnState
        {
            cards = new List<CardState>
            {
                ContentCards.Card(Id + ".exit", CardType.Exit, "林径出口", "离开森林。"),
                ContentCards.Card(Id + ".altar", CardType.Encounter, "林间祭坛", "查看祭坛。"),
                wolf.CreateCard(Id + ".wolf")
            }
        },
        new CardColumnState { cards = new List<CardState>() },
        new CardColumnState { cards = new List<CardState>() },
        new CardColumnState { cards = new List<CardState>() },
        new CardColumnState { cards = new List<CardState>() }
    }
};
```

列表首项位于列底部，最后一项最先显露；上例中先击败魔狼，再查看祭坛，最后抵达出口。若要让守卫挡住出口，出口必须写在守卫之前。核心没有单列最大牌数限制，界面会按需要创建额外卡牌层；仍应在实际目标分辨率检查超高牌列是否便于操作。`allowedCharacterIds` 为空表示不限角色，非空表示只允许指定角色。

### 把 Mod 角色加入正式关卡

从 Mod API 1.7.0 开始，`IModRegistrar.AddCharacterToLevel` 支持把当前包已经注册的角色追加到已有大关卡。它追加角色，不覆盖正式名单；传入的是关卡选择界面的稳定大关卡 ID，不是冒险中的小关卡或敌人牌池 ID。

```csharp
registrar.AddContent(new LanternRanger());
registrar.AddCharacterToLevel(
    "challenge_wild_corruption_nest",
    ModEntry.PackageId + ".character.lantern_ranger");
```

苍莽幽径正式入口的稳定 ID 是 `challenge_wild_corruption_nest`。如果只想加入某一档难度，可以传第三个参数，例如 `2`；省略或传 `0` 表示所有难度。角色 ID 必须属于当前包，并且必须在调用接口前完成 `AddContent` 注册。

如果要制作独立的自定义冒险，仍然不能用 `registry.Get<StageContent>("wilderness_beasts")` 取得 UI 程序集里的正式小关卡。应按本篇规则新建自己的 `StageContent`，在 `appearancePool` 中用 `ContentCards.Enemy`/`ContentCards.Card` 创建牌实例，再把正式卡牌的 `contentId` 和 `icon` 写到这些实例上以复用卡面。自己的 `AdventureContent` 步骤引用自己的 Stage ID，生成预设使用 `StageGenerationProfiles.Layered`。

这样可以同时实现两种目标：用 `AddCharacterToLevel` 让角色出现在正式苍莽幽径中；用自建 StageContent 和 AdventureContent 做带自定义敌人、牌池或剧情的独立测试冒险。

### 首领敌人、素材关卡与冒险步骤的标记

这三个 `boss` 标记分别描述敌人卡、素材关卡和冒险步骤，不能互相代替：

- 敌人牌的 `CardState.isBoss = true` 标识首领敌人本身；战斗目标规则、首领击败流程和首领牌筛选读取这个字段。仅提高 `enemyTier` 不会把敌人变成首领。`enemyTier = 5` 是与高阶内容相符的推荐值，但 boss 回合筛选看 `isBoss`，不靠 tier 判断。
- `StageContent.CreateDefinition()` 返回的 `StageDefinition.boss = true` 表示这个素材关卡单独作为首领关使用。它要求 `appearancePool` 中包含 `isBoss` 敌人，否则加载校验报 `AW_STAGE_BOSS_MISSING`；单独模拟时也会统计是否真的抽到首领。
- `AdventureStepDefinition.boss = true` 表示完整冒险的该步骤以最后一轮作为首领轮。`LevelStageBuilder` 会把展开后的每轮 `StageDefinition.boss` 按步骤值重设，因此只把素材 Stage 标成 boss、却把 Adventure step 设为 false，不会得到首领轮。步骤为 true 时，素材关卡牌池也必须含 `isBoss` 敌人，否则加载校验报 `AW_ADVENTURE_BOSS_MISSING`。

自定义 `EnemyContent.CreateCard()` 需要显式标记 boss 卡；基类不会自动设置这些字段：

```csharp
public override CardState CreateCard(string instanceId = null)
{
    CardState card = base.CreateCard(instanceId);
    card.enemyTier = 5;
    card.isBoss = true;
    card.guaranteedInStage = true;
    return card;
}
```

把这张卡放进素材关卡的 `appearancePool`。若素材关本身也要作为独立首领关使用，将它的 `StageDefinition.boss` 设为 `true`；若完整冒险也要在该步骤生成首领轮，再将对应 `AdventureStepDefinition.boss` 设为 `true`。为避免独立模拟、冒险生成和音乐标记彼此矛盾，通常让这两个场景标记与设计意图一致。`guaranteedInStage` 确保首领卡实际进入生成牌组；仅通过加载校验不代表随机牌池每次都抽得到首领。

常用生成预设：

- `StageGenerationProfiles.Layered`：按步骤与轮次逐渐放入更高阶敌人。
- `StageGenerationProfiles.Branching`：保留牌池中所有出口；选中出口后，其 `exitBranchId` 会作为下一步生成内容时的出场 Tag。具体有效期见下方“路线 Tag 的有效期”。
- `StageGenerationProfiles.Weighted`：使用内容自身的出场权重和 Tag。

`Layered` 和 `LayeredBranching` 会用普通敌人填满剩余牌位。每个使用这两种预设的步骤，都必须在出场筛选后留有至少一张正权重、非必出的普通敌人候选；没有时生成牌组会失败。若关卡本来就是营地、商店或无战斗过渡，可改用 `Default` 或 `Branching`，但牌池仍须包含出口和至少一种通过筛选的非出口卡。

### 路线 Tag 的有效期

游戏在玩家选择任意出口时，会把该出口的 `exitBranchId` 写入当前冒险状态；空值会清空旧值。这个值不会因进入下一场景或经过整备间而自行过期，也不会把多次选择累积成一组历史 Tag。每次后续选择出口都会用新出口的值替换旧值，所以下一场景按最新一次出口筛选内容。

因此，线性冒险第一步的分支 Tag 会影响紧接着进入的第二步；玩家离开第二步后，第三步看到的是第二步出口的 Tag，而不是第一步的 Tag。`Branching` 会保留所有出口模板，出口本身不会按 `RequiredAppearanceTags` 隐藏或过滤。只设置 `exitBranchId` 和内容 `RequiredAppearanceTags`，不能让第一步的路线条件自动穿过一个普通中间步骤。

如果路线专属奖励应出现在分支后的紧接一步，给对应内容设置匹配的 `RequiredAppearanceTags`。如果要在更后面的步骤继续依据早先路线筛选，需要另外设计能保存并恢复路线历史的流程/API；不要把单个 `exitBranchId` 当作整场冒险的路线历史。

难度由 `AdventureDifficultyDefinition` 配置，支持初始攻防生命强化、地区成长、奖励金币和水晶倍率，以及每档可用角色名单。结构写法见 [三地区冒险片段](../../templates/zh-CN/07-three-region-adventure.cs.txt)。

```csharp
EnemyContent wolf = registry.Get<EnemyContent>(
    ModEntry.PackageId + ".enemy.moss_wolf");

return new StageDefinition
{
    id = Id,
    name = Name,
    subtitle = Subtitle,
    generatedCardCount = GameRules.CardsPerStage,
    appearancePool = new List<CardState>
    {
        wolf.CreateCard(Id + ".wolf"),
        ContentCards.Card(
            Id + ".exit", CardType.Exit, "林径出口", "离开森林。")
    },
    allowedCharacterIds = new List<string>
    {
        ModEntry.PackageId + ".character.lantern_ranger"
    }
};
```

### 关卡胜利条件只在出口处检查

`StageDefinition.victoryConditions` 的公开类型是 `List<string>`，条件使用有限表达式；条件列表有多项时满足任意一项即可通过。检查时机是玩家点击已显露的出口，不是敌人死亡时自动结算。动态牌池必须包含出口，因此胜利条件不会让关卡自动结束，也不能省略出口牌。

例如，要求至少击败一名敌人后才允许离开：

```csharp
public override StageDefinition CreateDefinition(GameContentRegistry registry)
{
    var stage = new StageDefinition
    {
        id = Id,
        name = Name,
        subtitle = Subtitle,
        generatedCardCount = GameRules.CardsPerStage,
        appearancePool = new List<CardState>
        {
            registry.Get<EnemyContent>(ModEntry.PackageId + ".enemy.moss_wolf")
                .CreateCard(Id + ".wolf"),
            ContentCards.Card(Id + ".exit", CardType.Exit, "林径出口", "离开森林。")
        }
    };
    stage.victoryConditions.Add("defeatedEnemies >= 1");
    return stage;
}
```

`defeatedEnemies` 是整场运行的累计击败数，不区分敌人 ID。核心会先阻止仍有存活首领时离开，再检查胜利条件；普通敌人仍存活本身不会阻止点击出口。若需求是“必须击败指定敌人”，当前声明式胜利条件没有目标敌人 ID 计数器，不能用总击败数冒充目标击杀；并且 `EnemyTraitContent.OnKilled` 没有结束关卡的公开 API。

### StageGraph 节点路线与条件边

`StageDefinition.graphNodes` 的类型是 `List<StageGraphNodeDefinition>`；节点字段为 `nodeId`、`kind`、`contentId`、`required` 和 `card`。`kind` 使用 `StageGraphNodeKind`：`Start`、`Encounter`、`Event`、`Camp`、`Exit`、`Victory`、`Failure`。`StageDefinition.graphEdges` 的类型是 `List<StageGraphEdgeDefinition>`；边字段为 `fromNodeId`、`toNodeId`、`conditionExpression` 和 `weight`。这些类型和字段可用对象初始化构造。

StageGraph 是关卡装载时遍历的一次性有向路线；它不是玩家操作的地图界面。遍历从唯一 `Start` 节点开始，每到一个节点就把它写入 `stageGraphVisitedNodeIds`。若该节点有 `card`，核心会克隆它、设为必出并加入 `appearancePool`。直接使用 `StageDefinition` 时要为内容节点同时创建 `card` 快照；工坊结构化关卡则会根据非空 `contentId` 从已注册内容创建卡（敌人、道具、招式、事件或宝物），其他内容类型不能作为节点卡。`contentId` 只标识卡的来源，不会由 `kind` 自动推断。当前核心保留 `required` 字段但不读取它；走到的节点只要有卡就必出，即使 `required = false`。要做真正的可选随机卡，请放入 `appearancePool`，将它设为非必出并用正权重控制。

每条出边都在遍历到来源节点时按当前 `GameState` 求值。支持 `&&`、每项开头可选一个 `!`、`tag:<tag>`、`has:<id>`、`reach:<nodeId>`，以及数值比较 `==`、`!=`、`>`、`>=`、`<`、`<=`；不支持 `||` 或括号。数值键包括 `hp`、`maxHp`、`attack`、`defense`、`wisdom`、`gold`、`dodge`、`turn`、`stageIndex`、`defeatedEnemies`、`stagesCleared`，也可以使用 `player.hp` 等带前缀写法。`tag:` 检查状态外观 Tag 与角色池 Tag/角色 ID；`has:` 检查当前关卡、角色、已装备宝物、招式、初始招式和牌列中的卡；`reach:` 检查本次图遍历已访问过的节点。当前节点先加入访问列表，再求它的后继边。

所有条件为真的出边都会参加抽选，并按正的有限 `weight` 加权抽取一条；不会按列表顺序择优，也不保证多次加载走同一条。C# 和 JSON StageGraph 共用同一运行时抽选器。没有可用边时，`LoadStage` 会抛出 `InvalidOperationException`，消息包含关卡与节点 ID，并说明当前条件下没有可用后继；异常会从构造或选角重载处冒出。工坊静态校验检查条件语法、节点 ID、边端点、图连通、循环、死端和可达胜利/出口节点，但不会证明运行时每种状态都至少有一条条件为真的边；循环图报 `AW_STAGE_CYCLE`，始终不满足的条件边仍可能静态通过，必须为可能出现的状态留好后继。

注意新游戏构造时会先在角色选择前加载一次关卡，选择角色后再加载一次。第一次 `LoadStage` 时状态仍为 `ChoosingCharacter` 且 `State.character` 为空；`has:<角色ID>` 不检查 `startingCharacterChoices`，所以未选中的角色条件为 false。选角时核心先写入所选角色及其 `BaseStats`（包括金币），再第二次 `LoadStage`；`gold >= ...` 等数值条件读这次装载时的当前 `State.player`。起点必须为预选加载留一条有效后继，例如 `!has:<角色ID>` fallback。每次 `LoadStage` 都新建 `stageGraphVisitedNodeIds`，路线历史不会跨装载保留；遍历时当前节点先加入访问列表，再判断出边，因此 `reach:<当前节点>` 为 true。

`Victory` 和 `Exit` 节点会把图结果设为 `victory`；它们不会自动结束关卡或替代牌面出口。玩家仍须点击棋盘上的出口，且 `victoryConditions` 非空时至少一项为真才能通过。`Failure` 节点只把图结果设为 `failure`；玩家点击出口时核心先检查该结果及 `failureConditions`，任一失败条件成立就移除出口并判负，失败检查优先于胜利条件。图验证要求恰有一个 Start、所有节点从 Start 在结构上可达、没有环、非终点节点有出边，并能到达 Victory 或 Exit；条件实际互斥或无匹配仍要另做运行时探针。

一个按角色分流的最小形状如下；还应给 `appearancePool` 配置普通候选和 Exit：

```csharp
string rangerId = ModEntry.PackageId + ".character.lantern_ranger";
EnemyContent wolf = registry.Get<EnemyContent>(
    ModEntry.PackageId + ".enemy.moss_wolf");

return new StageDefinition
{
    id = Id,
    name = Name,
    subtitle = Subtitle,
    generatedCardCount = GameRules.CardsPerStage,
    appearancePool = new List<CardState>
    {
        wolf.CreateCard(Id + ".pool_wolf"),
        ContentCards.Card(Id + ".exit", CardType.Exit, "林径出口", "离开森林。")
    },
    graphNodes = new List<StageGraphNodeDefinition>
    {
        new StageGraphNodeDefinition { nodeId = "start", kind = StageGraphNodeKind.Start },
        new StageGraphNodeDefinition
        {
            nodeId = "ranger", kind = StageGraphNodeKind.Encounter,
            contentId = wolf.Id, required = false,
            card = wolf.CreateCard(Id + ".node_wolf")
        },
        new StageGraphNodeDefinition { nodeId = "fallback", kind = StageGraphNodeKind.Failure },
        new StageGraphNodeDefinition { nodeId = "victory", kind = StageGraphNodeKind.Victory }
    },
    graphEdges = new List<StageGraphEdgeDefinition>
    {
        new StageGraphEdgeDefinition
        {
            fromNodeId = "start", toNodeId = "ranger",
            conditionExpression = "has:" + rangerId, weight = 1f
        },
        new StageGraphEdgeDefinition
        {
            fromNodeId = "start", toNodeId = "fallback",
            conditionExpression = "!has:" + rangerId, weight = 1f
        },
        new StageGraphEdgeDefinition
        {
            fromNodeId = "ranger", toNodeId = "victory",
            conditionExpression = "reach:ranger && has:" + rangerId, weight = 1f
        }
    }
};
```

示例中的 fallback 只为第一次无角色的预览加载保留可走路径；`required=false` 不会让走到的狼牌变成随机牌。若把 fallback 条件删掉，构造器在选角前就可能遇到无匹配出边并抛异常。

#### 结构化 JSON StageGraph

不用写 `StageContent` 时，可把关卡作为 `contentIndex` 中的 `contentType: "stage"` 内容。索引里的 `contentId` 必须与 JSON 根部 `id` 相同；`sourceStageId` 再引用这个稳定 ID。结构化 Stage 的 `cards` 字段就是运行时 `StageDefinition.appearancePool`，JSON 中不叫 `appearancePool`。

结构化字段中的 `kind` 是 Unity `JsonUtility` 序列化的枚举数字：卡池 `Content=0`、`TreasureChest=1`、`Exit=2`、`Intermission=3`；节点 `Start=0`、`Encounter=1`、`Event=2`、`Camp=3`、`Exit=4`、`Victory=5`、`Failure=6`。下面的 ID 代表同包里已注册的事件和宝物：

```json
{
  "schemaVersion": 1,
  "contentType": "stage",
  "id": "local.alice.lantern-trail.stage.starlit-grove",
  "nameKey": "stage.starlit_grove.name",
  "subtitleKey": "stage.starlit_grove.subtitle",
  "difficultyDescriptionKey": "stage.starlit_grove.difficulty",
  "columnCount": 5,
  "rowCount": 5,
  "generatedCardCount": 5,
  "cards": [
    { "kind": 0, "contentId": "local.alice.lantern-trail.event.grove_note", "copies": 1, "weight": 1, "guaranteed": false },
    { "kind": 2, "copies": 1, "weight": 1, "guaranteed": true, "branchId": "" }
  ],
  "nodes": [
    { "nodeId": "start", "kind": 0, "required": true },
    { "nodeId": "story", "kind": 2, "contentId": "local.alice.lantern-trail.event.starlit_note", "required": false },
    { "nodeId": "token", "kind": 3, "contentId": "local.alice.lantern-trail.treasure.silverleaf_token", "required": false },
    { "nodeId": "victory", "kind": 5, "required": true }
  ],
  "edges": [
    { "fromNodeId": "start", "toNodeId": "story", "conditionExpression": "hp >= 0", "weight": 1 },
    { "fromNodeId": "story", "toNodeId": "token", "conditionExpression": "hp >= 0", "weight": 1 },
    { "fromNodeId": "token", "toNodeId": "victory", "conditionExpression": "hp >= 0", "weight": 1 }
  ]
}
```

至少提供一个 `cards` 出口项并设 `guaranteed: true`，否则结构化 Stage 校验会报 `AW_STAGE_EXIT_REQUIRED`。带内容的节点通过 `contentId` 从注册表创建节点卡，不必再把同一张卡放进 `cards`；目前支持敌人、道具、招式、事件和宝物，找不到 ID 或引用了其他类型时包会报 `AW_STAGE_REFERENCE`。走到的节点卡会加入本轮卡池并保证出现，`required` 当前只被保存，不控制节点是否可选；可选随机卡应放在 `cards` 中并设 `guaranteed: false`。Victory/Failure 图节点也不会取代 `cards` 中的实体出口。图形状静态通过后仍要按可能的条件状态验证每个运行时节点都有可用后继。

## 九、道具与奇遇事件

`ItemContent` 默认支持：`CardType.Medicine` 读取 `Heal`；`CardType.Elixir` 读取 `Effect`；其他可使用道具读取 `DodgeCharges`。若要制作直伤道具，可以覆写 `CreateCard` 并在基类生成的卡上填写 `activationKind`、`targetKind` 与 `effects`：

```csharp
using System.Collections.Generic;
using MiniAdventureWorld.Core;

public sealed class EmberVial : ItemContent
{
    public EmberVial() : base(ModEntry.PackageId + ".item.ember_vial") { }
    public override string Name => "余烬药瓶";
    public override string Description => "对指定敌人造成 5 点伤害。";
    public override CardType CardType => CardType.Elixir;

    public override CardState CreateCard(string instanceId = null)
    {
        CardState card = base.CreateCard(instanceId);
        card.activationKind = CardActivationKind.Targeted;
        card.targetKind = CardTargetKind.Enemy;
        card.effects = new List<CardEffectData>
        {
            new CardEffectData { effectType = CardEffectType.Damage, value = 5 }
        };
        return card;
    }
}
```

目标型道具只允许指定当前暴露的一名敌人，核心会读取 `CardEffectType.Damage` 并使用统一敌人伤害流程。群体直伤则保留 `CardActivationKind.Direct`，把效果设为 `CardEffectType.DamageAllEnemies`；普通直接使用道具也支持这一效果。两条路径都通过敌人特性伤害结算，所以只有实际扣除生命时才调用 `OnAfterDamaged`。目标型道具和群体道具都不会触发普通攻击回应阶段的 `OnRoundStart`。目标型路径由核心处理伤害与道具使用通知，不调用 `ItemContent.Execute`；不要在两处重复结算。

```csharp
public sealed class MoonDewPotion : ItemContent
{
    public MoonDewPotion()
        : base(ModEntry.PackageId + ".item.moon_dew_potion") { }
    public override string Name => "月露药剂";
    public override string Description => "恢复 6 点生命。";
    public override CardType CardType => CardType.Medicine;
    public override int Heal => 6;
    public override int SellGold => 2;
}
```

通过 `registry.Get<ItemContent>(id).CreateCard(instanceId)` 把道具加入关卡。宝物强化道具时使用 `OnBeforeItemEffect` 或 `OnItemUsed`，不要让道具反过来遍历玩家宝物。

奇遇继承 `EventContent`。默认 `Execute(CardExecutionContext)` 调用 `ResolveEncounter`，不需要覆写即可走核心结算。`CreateCard` 会把 `Action`、`RewardQuality`、`RewardCount`、`Effect` 和 `Choices` 复制到事件卡上。基础路径的字段含义如下：

- `Action = PendingChoiceKind.None`（默认）：触发后移除事件卡，扣除卡片的 `goldCost`，应用 `Effect`。
- `Action = PendingChoiceKind.Meditation`：从 `Choices` 中抽取属性奖励；`RewardCount > 0` 时抽指定数量，否则用全部 `Choices`。事件的 `RewardQuality` 与每个 `StatEffect` 的品质、权重、所需 Tag 一起决定候选。玩家选中后，核心自动扣除事件卡的 `goldCost` 并应用该条 `StatEffect`。此路径不应用事件卡的 `Effect`，这些字段也不会抽取宝物。
- `Action = TreasureUpgrade`、`TreasureReset` 或 `TreasureFusion`：进入对应的宝物槽选择流程。它们不会按 `Choices` 发放属性奖励。

若需要“二选一、每个选项各有属性代价和宝物奖励”，覆写 `CreateCard` 并填充 `CardState.richEventChoices`。非空时它优先于基础 `Action`/`Effect`/`Choices` 路径；默认 `Execute` 仍会自动创建选项并结算，无需自定义 UI 或覆写 `Execute`：

```csharp
using System.Collections.Generic;
using MiniAdventureWorld.Core;

public sealed class BriarShrineEvent : EventContent
{
    public BriarShrineEvent()
        : base(ModEntry.PackageId + ".event.briar_shrine") { }

    public override string Name => "荆棘祭坛";
    public override string Description => "献出一项代价，换取一件遗物。";
    public override string ImageName => "";

    public override CardState CreateCard(string instanceId = null)
    {
        CardState card = base.CreateCard(instanceId);
        card.richEventChoices = new List<RichEventChoiceState>
        {
            new RichEventChoiceState
            {
                choiceId = Id + ".choice.attack",
                text = "献出 2 点攻击，获得苔火遗物。",
                cost = new StatEffect { attack = 2 },
                rewardContentId = ModEntry.PackageId + ".treasure.mossfire_relic",
                rewardContentCount = 1
            },
            new RichEventChoiceState
            {
                choiceId = Id + ".choice.hp",
                text = "失去 3 点生命，获得苔火遗物。",
                cost = new StatEffect { hp = 3 },
                rewardContentId = ModEntry.PackageId + ".treasure.mossfire_relic",
                rewardContentCount = 1
            }
        };
        return card;
    }
}
```

`RichEventChoiceState.cost` 可扣当前生命、最大生命、攻击、防御、智慧、闪避或金币；核心会先检查能否支付（生命和最大生命至少保留 1），再扣代价、应用可选的 `reward` 属性并发放 `rewardContentId`。宝物奖励必须是已注册的 `TreasureContent`；有空槽时立即装备，没有空槽时存入备用宝物。`rewardContentCount` 是发放数量。基础 Meditation 路径的卡片级 `goldCost` 是所有选项共用的金币门槛，并在选择时扣除；`EventContent` 没有对应属性，可在覆写 `CreateCard` 后设置 `card.goldCost`。`richEventChoices` 路径优先处理，绕过卡片级 `goldCost` 和基础奖励字段；要给每个分支单独收金币，应写入该分支的 `cost.gold`。两种选择路径不要混用。

若以工坊结构化内容 JSON 创建富事件，`package.json` 的 `contentIndex` 需要登记事件 ID、类型和相对文件路径：

```json
{
  "contentType": "event",
  "contentId": "example.forest.event.briar_shrine",
  "relativePath": "content/events/briar-shrine.json"
}
```

事件文件的 `contentType` 必须为 `event`，且 `id` 与索引里的 `contentId` 相同。选项放在事件定义顶层 `richChoices`，选项文本通过 `textKey` 本地化；字段名及位置如下：

```json
{
  "schemaVersion": 1,
  "contentType": "event",
  "id": "example.forest.event.briar_shrine",
  "nameKey": "event.briar_shrine.name",
  "descriptionKey": "event.briar_shrine.description",
  "richChoices": [
    {
      "choiceId": "example.forest.event.briar_shrine.choice.gold",
      "textKey": "event.briar_shrine.choice.gold",
      "conditionExpression": "gold >= 5",
      "cost": { "gold": 5 },
      "reward": { "hp": 2 },
      "nextEventId": "example.forest.event.followup",
      "nextStageId": ""
    }
  ]
}
```

`cost` 與 `reward` 都是 `StatEffect`，可填 `hp`、`maxHp`、`attack`、`defense`、`wisdom`、`dodgeCharges`、`gold`。`richChoices` 最多三个分支；分支条件与 StageGraph 使用相同条件语法，例如 `gold >= 5` 或 `player.gold >= 5`，支持 `&&`、项目前缀 `!`、`tag:`、`has:`、`reach:` 和数值比较，不支持 `||` 或括号。条件只在打开事件时筛选选项；代价能否支付不会隐藏选项，确认时会再检查条件和代价。条件刚打开后若已变为 false，会返回 `event_condition_changed`；代价不足会返回 `event_cost_unavailable`。这两类失败都不扣费、不发奖并保留待处理选择；待处理列表是打开时的快照，不会自动重筛。

分支还可设置 `rewardContentId` 与 `rewardContentCount` 发放已注册的 `TreasureContent`、`MoveContent` 或 `ItemContent`；后端结构化内容校验器要求 ID 与正数量同时填写，但不拒绝大于 100 的数值。运行时将实际结算次数限制在 0～100。`ItemContent` 会立即按内容配置结算恢复、闪避或属性效果，不会变成背包道具卡；`MoveContent` 会加入招式，当前没有空槽时不会装备；`TreasureContent` 没有空槽时存入备用宝物。注意，直接编写 JSON 包时，注册器不会代替后端结构化校验器检查 ID/count 配对，也不会验证奖励引用是否存在或属于支持的类型；这类 JSON 仍可能通过包注册，但选择结算时奖励会被静默跳过。编写后应在包级验证中检查配对、引用与数量。当前没有玩家可打开的 JSON 内容编辑器。

成功分支可设置 `nextEventId` 或 `nextStageId`。两者在后端结构化校验器中互斥。`nextEventId` 必须指向已注册的 `EventContent`；成功结算后原事件被移除，后续事件卡追加到原列顶部并成为新的明牌，然后提交回合。`nextStageId` 必须匹配当前冒险场景列表中的 `StageDefinition.id`；只注册 Stage 内容但未加入当前场景列表不足以跳转。结构化冒险的 `steps[].id` 会成为展开场景的 ID 前缀：每轮 ID 是 `<step.id>-round-<轮次>`，轮次从 1 开始。例如 `step.id = "grove-second"`、`roundCount = 1` 时，目标 ID 是 `grove-second-round-1`；`steps[].sourceStageId` 是生成牌组的素材 Stage ID，不能代替这个目标 ID。它只会创建待进入场景状态，玩家还需完成整备界面的「进入下一场景」动作。后端结构化校验器目前不校验这两个引用是否存在，因此应在包级验证中逐个检查。同一个 `package.json` 可以同时声明 JSON `contentIndex` 与 C# `codeAssembly`；两路注册结果合并进同一内容注册表，因此务必避免 ID 重复。

奇遇卡也要通过 `CreateCard` 加入关卡牌池。完全自定义执行时才覆写 `Execute`，仍应使用公开上下文，不直接控制 UI 或场景对象。

## 十、完整内容的注册检查

完成一组“角色＋技能＋专属宝物＋敌人＋素材关卡＋完整冒险”时，逐项检查：所有类已注册；角色引用的类型存在；宝物池 Tag 完全相同；敌人的 `EnemyTraitId` 存在；素材关卡通过注册表取得敌人并创建卡牌；首领步骤引用的素材池内存在首领；冒险步骤与难度 ID 唯一；角色限制包含测试角色；描述公式与执行公式一致；所有运行时计数都有明确的重置规则。

配套代码见 [功能片段](../../templates/README.zh-CN.md)。本仓库提供教程与独立功能片段，不附完整冒险样例包。
