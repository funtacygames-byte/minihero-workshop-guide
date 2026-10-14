# 制作药剂、目标道具与奇遇

[English](../../en/tutorials/items-and-events.md) · [Index](../README.md)

教程修订 4 · Mod API 1.8.0 · 2026-10-14


目标：固定牌场出现一瓶恢复 6 生命的月露药剂、一瓶对指定敌人造成 5 伤害的余烬药瓶，并能区分属性奖励奇遇和卡面抉择。前置：[固定关卡](stage.md)；新增 `source/PracticeItems.cs`，使用[片段 12](../../../templates/zh-CN/12-items.cs.txt)。不与手册中同名示例重复复制。

## 1. 注册不等于出场

在现有入口注册两个类：

```csharp
registrar.AddContents(new MoonDewPotion(), new EmberVial());
```

在固定关卡的 `columns` 创建之后、返回定义之前，把道具放在第二、第三列顶部，第一列仍保留守卫与出口：

```csharp
columns[1].cards.Add(registry.Get<ItemContent>(
    ModEntry.PackageId + ".item.moon_dew_potion").CreateCard(Id + ".potion"));
columns[2].cards.Add(registry.Get<ItemContent>(
    ModEntry.PackageId + ".item.ember_vial").CreateCard(Id + ".vial"));
```

`CreateCard` 将静态内容转为独立牌实例。两个实例使用不同 instanceId；不要将同一可变 CardState 对象放入多列。随机布局则把模板放进 `appearancePool`；固定布局不会从该池补牌。

## 2. 使用路径决定结算入口

`CardType.Medicine` 读取 `Heal`，走药剂治疗；`CardType.Elixir` 的直接属性路径读取 `Effect`。余烬药瓶覆写 `CreateCard`，标记 `Targeted`＋`Enemy` 并填 `Damage`，玩家对当前明牌敌人操作后走核心目标伤害路径。这一路不会调用 `ItemContent.Execute`，不要再在 Execute 中造成第二次伤害。

群体伤害的拓展是在 CreateCard 上设置 `CardActivationKind.Direct` 与 `CardEffectType.DamageAllEnemies`。只改这两个字段并同步说明；通过真实伤害规则验证敌人防御、特性、击杀与奖励。道具伤害不是普通攻击回应，不应预期触发其 `OnRoundStart`。

## 3. 选择合适的事件路径

| 目标 | 实现 | 注意 |
| --- | --- | --- |
| 点击后直接属性收益 | `EventContent.Effect`，默认 Action=None | 沿用默认 Execute |
| 属性奖励列表 | `Action=Meditation`＋`Choices` | 不同时发放 Effect；不是宝物抽取 |
| 分支代价、指定内容奖励、续接 | `richEventChoices` | 最多三个分支；条件与代价时机见参考 |
| 任意数量正式卡面、具体类专属处理 | `CardChoiceEventContent` | 用[新卡牌选择课](card-choice.md) |
| 指定宝物教学奖励 | [片段 09](../../../templates/zh-CN/09-relic-grant.cs.txt) | 奖励 ID 先注册，空槽／满槽分别验证 |

富事件的 `rewardContentId` 可指宝物、招式或道具；道具奖励立即执行内容效果，不变成背包卡。新卡牌选择的 `effect` 是 StatEffect，不会凭显示卡的 contentId 自动发放宝物。不同路径不要叠写成一张事件卡，详见[原手册](../02-content-creation.md)。

## 4. 双语和验收

按片段四个 `item.*` 键合并两种 locale，名字分别使用月露药剂／Moondew Potion、余烬药瓶／Ember Vial；描述分别保留恢复 6、指定敌人伤害 5。素材留空仅检查规则，之后按[素材课](assets-and-text.md)绑定自己的图标。

递增包版本，构建安装并完整重启。先让角色受伤，再点药剂；检查治疗量与生命条增量的区别。将练习守卫生命改为 8，在无减伤条件下用药瓶后剩余 3，不能误伤其他敌人；再把守卫防御设为非零，验证统一伤害规则。确认道具移除、使用通知和回合符合真实路径，最后走通出口。每个数值变更都同步描述与包版本。

打不开或用不出时先核对牌类、activationKind、targetKind、当前目标是否暴露、是否有 pendingChoice。显示了卡面但没奖励时核对真实执行路径，而不是修改 UI 点击脚本。
