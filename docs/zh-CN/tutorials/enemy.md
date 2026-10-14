# 制作敌人与独立实例状态

[English](../../en/tutorials/enemy.md) · [目录](../README.md)

教程修订 4 · Mod API 1.8.0 · 2026-10-14 · [验证范围](../reference/versions.md)

目标：将林径练习的通用守卫替换为已注册的苔狼；受伤后攻击提高 1。摆两只狼时，只有真正受伤的那只增长。

前置：[固定关卡](stage.md)。新增 `source/MossWolf.cs`，修改 `PracticeStage.cs` 和入口注册。片段绑定敌人图；规则验证时可移除自定义展示接口和属性，正式素材由你提供。

安装修改后的构建前，按[首课](first-mod.md#4-修改一次并重新验证)递增 `package.json.version`；同一已安装版本不能对应不同内容。

## 1. 注册敌人及其特性

复制[敌人与特性片段](../../../templates/zh-CN/04-enemies-and-traits.cs.txt)。它有 `WoundedRage` 和 `MossWolf`，在 `Load` 添加：

```csharp
registrar.AddContents(new WoundedRage(), new MossWolf());
```

敌人通过 `EnemyTraitId` 引用特性。不是把特性说明写进敌人名称就会生效。当前片段生命 18、攻击 6、防御 1、金币奖励 5；这些是教学数值，按自己的角色和测试目标调整。

## 2. 通过注册表创建敌人卡

在 `PracticeStage.CreateDefinition` 中，用下面代码替换原 `ContentCards.Enemy(...)` 创建 guard 的整段声明；后续 `columns[0].cards.Add(guard)` 保留：

```csharp
EnemyContent wolf = registry.Get<EnemyContent>(ModEntry.PackageId + ".enemy.moss_wolf");
CardState guard = wolf.CreateCard(Id + ".wolf.one");
```

注册表查找使用内容 ID；`CreateCard` 参数是这张卡的实例 ID。两只狼应分别用 `.wolf.one` 和 `.wolf.two`，避免同场重复实例 ID。第二只可以放到 `columns[1].cards` 里，出口仍在第一只下方。

## 3. 先测试单只，再测试两只

构建安装、完整重启，新开练习。用能让狼存活的一次攻击或直伤道具造成正数生命伤害。观察该狼的攻击增加 1；零伤害不能用来验证此回调。

摆两只后分别记录它们的攻击，只伤害第一只，确认第二只没有增加。敌人普通攻击后的回应、招式伤害和道具伤害不是同一个触发窗口，必要时分别测试；不要把 `OnRoundStart` 理解成所有玩家操作都会调用的通用回合开始。

当前角色若一次击败狼，适当提高测试敌人的生命或降低测试伤害，使一次受伤后仍可观察。回收、倒计时移除和被击败也可能走不同流程，不能只凭名称代换事件。

## 4. 把状态放在正确对象

`WoundedRage` 修改 `e.Owner.enemyTraitAttackDelta`。特性定义可能被很多狼共享，不能给特性对象加 `int hits` 来记录一只狼的进度。若需要计数，使用该卡的 `enemyTraitCounter`、`enemyTraitSecondaryCounter` 等字段并安排单一含义；倒计时会使用主计数器，不要重用。

当前事件签名、伤害窗口和存档规则见[角色与敌人参考](../reference/actors.md)及[生命周期](../reference/lifecycle.md)。本例未给增长上限；如果设计需要上限，应在描述和实现中一起增加，并测试达到上限后不会继续增长。

## 验收与下一步

- 敌人和特性都注册，`EnemyTraitId` 能解析。
- 正数扣血后增长正确，多个实例不串状态。
- 新建敌人实例初始值正确，存档恢复保留现存实例数据。

继续[连接多个场景](adventure.md)，或按[资源课](assets-and-text.md)加入自己的战斗图。


本课使用的片段名称与说明已接入 ModText。按[双语文本课](assets-and-text.md)合并示例 entries；不合并时仍显示源码 fallback。已有牌／定义快照不保证即时重译，切语言后新开局检查。
