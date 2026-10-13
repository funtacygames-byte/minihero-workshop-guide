# 制作与测试宝物

[English](../../en/tutorials/treasure.md) · [目录](../README.md)

教程修订 2 · Mod API 1.8.0 · 2026-10-13 · [验证范围](../reference/versions.md)

本课沿用首课的 `StarterRelic`，完成品质、等级、候选池与实际效果的检查。它是教学用单品质宝物；不应把换名字和数值当成新的成品设计。

前置：[首个模组](first-mod.md)。实际效果部分还需完成[固定关卡](stage.md)。修改 `source/ModEntry.cs`，新增 `source/RelicGrant.cs`；不需要任何图片或音乐。

安装修改后的构建前，按[首课](first-mod.md#4-修改一次并重新验证)递增 `package.json.version`；同一已安装版本不能对应不同内容。

## 1. 先分清品质、等级与池

`Rank = Common` 只提供普通品质；没有实现多品质时，不会自动生成五个版本。`BaseValue` 是每级护盾，本课沿用修改后的 4。`Describe(level)` 与 `OnStageEntered` 都计算 `BaseValue × level`；一级 4，二级 8。

`CategoryTags` 使用 `TreasureCategoryTags.Shield`，表达生命体系中的护盾用途。`PoolTags` 使用 `CharacterTreasurePoolTags.HealingLifeBuild`，决定角色候选；分类本身不控制宝箱。林地药师（`grove_alchemist`）允许这个池，但随机抽取仍不保证出现。

完整属性和多品质写法见[宝物参考](../reference/treasures.md)。带临时计数的效果应保存在本件运行时实例并在 `OnSceneReset()` 清空，见[生命周期](../reference/lifecycle.md)。

## 2. 用明确奖励取代等待随机宝箱

将[领取遗物片段](../../../templates/zh-CN/09-relic-grant.cs.txt)复制为 `source/RelicGrant.cs`，核对命名空间。它只定义一张测试奇遇，唯一选项奖励本包的 `StarterRelic`。在 `Load` 增加：

```csharp
registrar.AddContent(new RelicGrant());
```

在 `PracticeStage.CreateDefinition` 中，紧接 `columns[0].cards.Add(guard);` 后添加：

```csharp
columns[0].cards.Add(
    registry.Get<EventContent>(ModEntry.PackageId + ".event.relic_grant")
        .CreateCard(Id + ".grant"));
```

现在第一列从底到顶是出口、守卫、领取遗物。事件先暴露，选择后发奖并移除。全部注册包括 `StarterRelic`、`RelicGrant`、`PracticeStage` 和 `PracticeAdventure`。确认只有一个 `ModEntry`。

## 3. 让进场事件有下一次触发机会

进场奖励发生在进入场景时。场景已经进入后才领到的宝物，不能用当前护盾是否立刻增加来判断本效果。

在 `PracticeAdventure` 的唯一 step 将 `roundCount = 1` 改为 `roundCount = 2`，`IntermissionInterval` 改为 1。构建安装，完整重启，选择林径练习。先完成事件选项，确认宝物栏有旅者遗物；打败守卫后点击出口，通过整备页进入第二场景。

第二场景进场应获得 4 点护盾（宝物一级、`BaseValue = 4`）。先观察护盾再攻击，避免受伤消耗护盾影响判断。测试时不要再领取第二件同名宝物；多件会分别生效。点击第一场景出口通常进入过渡流程，最后一场景的出口才结算整个冒险胜利。

## 4. 用边界检查确认公式与重置

将 `BaseValue` 临时改回 2，重新构建并完整重启，新开一局后第二场景应获得 2。图鉴一级也显示 2。恢复到自己选择的值，再做一次检查。不要只改描述字符串中的数字。

本件没有临时计数，护盾是已经兑现的玩家资源，不是宝物内部待清空的计数。为其他宝物加入层数时，使用自己的可序列化实例字段；静态字段和共享定义会串到其他实例。默认新场景重置临时状态，跨场景例外必须明确声明。

## 验收与下一步

- 图鉴品质与等级正确，描述和进场护盾走同一公式。
- 固定事件能明确授予宝物，下一场景能观察效果。
- 不把 `StartingTreasureTypes` 当作选角发奖，也不把分类当作池。

继续[角色与初始招式](character.md)，或查[治疗与事件](../reference/events.md)设计其他触发窗口。
