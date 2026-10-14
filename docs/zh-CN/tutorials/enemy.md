# 做一只受伤后变强的敌人

[English](../../en/tutorials/enemy.md) · [目录](../README.md)

把林径练习里的守卫换成“苔背魔狼”。它每次受到正数生命伤害后，攻击提高 1。做完后再放两只，看看它们是否各自变强。

**需要已有：**[固定关卡](stage.md)的项目。新建 `source/MossWolf.cs`，修改 `source/ModEntry.cs` 和 `source/PracticeStage.cs`。默认使用后备图片，不需要先找一张狼的素材。

保存后递增 `package.json.version`，构建安装并完整重启。每次测试新建一局，便于看清敌人的初始值。

## 1. 注册敌人及其特性

把[敌人与特性源码](../../../templates/zh-CN/04-enemies-and-traits.cs.txt)完整复制到 `source/MossWolf.cs`，使用自己的命名空间。它有 `WoundedRage` 和 `MossWolf`。在原 `ModEntry.cs` 的 `Load` 方法中添加：

```csharp
registrar.AddContents(new WoundedRage(), new MossWolf());
```

`EnemyTraitId` 把苔背魔狼连接到“负伤狂怒”特性。源码默认生命 18、攻击 6、防御 1、金币奖励 5。先保留这些值，等能在游戏里看到受伤增攻后再调整强弱。

## 2. 通过注册表创建敌人卡

在 `PracticeStage.CreateDefinition` 中，用下面代码替换原 `ContentCards.Enemy(...)` 创建 guard 的整段声明；后续 `columns[0].cards.Add(guard)` 保留：

```csharp
EnemyContent wolf = registry.Get<EnemyContent>(ModEntry.PackageId + ".enemy.moss_wolf");
CardState guard = wolf.CreateCard(Id + ".wolf.one");
```

注册表查找使用内容 ID；`CreateCard` 参数是这张卡的实例 ID。两只狼应分别用 `.wolf.one` 和 `.wolf.two`，避免同场重复实例 ID。在原 `columns[0].cards.Add(guard);` 后加入下方代码，第二列也会出现一只狼，出口仍在第一只下方。如果角色课已经放了第二名守卫，先删除那段 `secondGuard` 代码，再放狼。

```csharp
columns[1].cards.Add(wolf.CreateCard(Id + ".wolf.two"));
```

没有自定义图片也能试。要加战斗图时，再按[素材课](assets-and-text.md#角色和敌人也想换图)绑定图片。

## 3. 先测试单只，再测试两只

构建安装、完整重启，新开练习。用能让狼存活的一次攻击或直伤道具造成正数生命伤害。观察该狼的攻击增加 1；零伤害不能用来验证此回调。

摆两只后分别记录它们的攻击，只伤害第一只，确认第二只没有增加。如果沿用提灯游侠，使用单目标银辉箭检查；普通攻击会因角色特性额外选中第二名敌人，不适合这一步。敌人普通攻击后的回应、招式伤害和道具伤害不是同一个触发窗口，必要时分别测试；不要把 `OnRoundStart` 理解成所有玩家操作都会调用的通用回合开始。

当前角色若一次击败狼，适当提高测试敌人的生命或降低测试伤害，使一次受伤后仍可观察。回收、倒计时移除和被击败也可能走不同流程，不能只凭名称代换事件。

## 4. 把状态放在正确对象

`WoundedRage` 修改 `e.Owner.enemyTraitAttackDelta`。特性定义可能被很多狼共享，不能给特性对象加 `int hits` 来记录一只狼的进度。若需要计数，使用该卡的 `enemyTraitCounter`、`enemyTraitSecondaryCounter` 等字段并安排单一含义；倒计时会使用主计数器，不要重用。

当前事件签名、伤害窗口和存档规则见[角色与敌人参考](../reference/actors.md)及[生命周期](../reference/lifecycle.md)。本例未给增长上限；如果设计需要上限，应在描述和实现中一起增加，并测试达到上限后不会继续增长。

## 回游戏检查，然后继续

- 敌人和特性都注册，`EnemyTraitId` 能解析。
- 正数扣血后增长正确，多个实例不串状态。
- 新建敌人实例初始值正确，存档恢复保留现存实例数据。

继续[连接多个场景](adventure.md)，或按[资源课](assets-and-text.md)加入自己的战斗图。

想让名称和说明随中英文切换，请按[文本合并步骤](assets-and-text.md#合并专题片段的文本)加入本课所用的条目。未合并时会显示源码中的默认文字。切换语言后新开一局检查。
