# 给关卡加一瓶药剂和一瓶伤害道具

[English](../../en/tutorials/items-and-events.md) · [目录](../README.md)

在林径练习旁边放两张能用的道具牌：月露药剂恢复 6 点生命，余烬药瓶对选中的敌人造成 5 点伤害。先用起来，再看不同道具的代码入口有什么区别。

**需要已有：**[固定关卡](stage.md)。将[道具源码](../../../templates/zh-CN/12-items.cs.txt)完整复制到新文件 `source/PracticeItems.cs`，命名空间与 `ModEntry.cs` 一致。修改原 `ModEntry.cs` 和 `PracticeStage.cs`，不用增加图片。若已经复制过同名类，直接使用已有文件。

## 1. 注册道具，再把它们摆出来

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

## 2. 回游戏使用道具

按片段四个 `item.*` 键合并两种 locale，名字分别使用月露药剂／Moondew Potion、余烬药瓶／Ember Vial；描述分别保留恢复 6、指定敌人伤害 5。素材留空仅检查规则，之后按[素材课](assets-and-text.md)绑定自己的图标。

1. 保存、递增包版本、构建安装并完整重启，新开林径练习。
2. 点击第二列的月露药剂，它应被使用并移除。满血时生命条不增加是正常的；如果之前受伤，应看到生命恢复。
3. 要单独检查可见回血，可以让守卫先打伤角色。原守卫若不能造成伤害，临时将它的 `attack` 调到超过角色防御，并调高 `hp`，让它至少撑过一次攻击。改完重新构建、重启，再受伤喝药。
4. 另测药瓶时，把守卫改回 `attack: 1, defense: 0, hp: 8`，递增版本、构建、重启并新开局。**按住第三列的余烬药瓶，拖到明牌守卫上松开**。满生命守卫应剩余 3 生命，药瓶移除，其他敌人不受伤。
5. 最后走通出口。想进一步比较减伤，再用非零防御的守卫重复试药瓶。每次数值修改都同步说明和包版本。

打不开或用不出时先核对牌类、activationKind、targetKind、当前目标是否暴露、是否有 pendingChoice。显示了卡面但没奖励时核对真实执行路径，而不是修改 UI 点击脚本。

## 3. 使用路径决定结算入口

`CardType.Medicine` 读取 `Heal`，走药剂治疗；`CardType.Elixir` 的直接属性路径读取 `Effect`。余烬药瓶覆写 `CreateCard`，标记 `Targeted`＋`Enemy` 并在效果列表中加入 `CardEffectType.Damage`，玩家对当前明牌敌人操作后走核心目标伤害路径。这一路不会调用 `ItemContent.Execute`，不要再在 Execute 中造成第二次伤害。

群体伤害的拓展是在 CreateCard 上设置 `CardActivationKind.Direct` 与 `CardEffectType.DamageAllEnemies`。只改这两个字段并同步说明；通过真实伤害规则验证敌人防御、特性、击杀与奖励。道具伤害不是普通攻击回应，不应预期触发其 `OnRoundStart`。

## 4. 选择合适的事件路径

| 目标 | 实现 | 注意 |
| --- | --- | --- |
| 点击后直接属性收益 | `EventContent.Effect`，默认 Action=None | 沿用默认 Execute |
| 属性奖励列表 | `Action=Meditation`＋`Choices` | 不同时发放 Effect；不是宝物抽取 |
| 分支代价、指定内容奖励、续接 | `richEventChoices` | 最多三个分支；条件与代价时机见参考 |
| 任意数量正式卡面、具体类专属处理 | `CardChoiceEventContent` | 用[新卡牌选择课](card-choice.md) |
| 指定宝物教学奖励 | [片段 09](../../../templates/zh-CN/09-relic-grant.cs.txt) | 奖励 ID 先注册，空槽／满槽分别验证 |

富事件的 `rewardContentId` 可指宝物、招式或道具；道具奖励立即执行内容效果，不变成背包卡。新卡牌选择的 `effect` 是 StatEffect，不会凭显示卡的 contentId 自动发放宝物。不同路径不要叠写成一张事件卡，详见[内容手册](../02-content-creation.md)。
