# 把宝物放进自己的关卡

[English](../../en/tutorials/treasure.md) · [目录](../README.md)

图鉴里已经有旅者遗物了。现在加一张“领取遗物”奇遇，让角色拿到它，再进入下一场景，看到 4 点护盾真正加上来。

**从这里接着做：**完成[首课](first-mod.md)和[固定关卡](stage.md)。`StarterRelic.BaseValue` 保持为 4，守卫生命用 4 或 8 都可以。本课不需要图片和音乐。

| 文件 | 本课操作 |
| --- | --- |
| `source/RelicGrant.cs` | 新建一张奖励旅者遗物的奇遇 |
| `source/ModEntry.cs` | 在原 `Load` 中注册奇遇 |
| `source/PracticeStage.cs` | 在守卫上放奇遇，并让冒险包含两个场景 |
| `package.json` | 递增版本后构建安装 |

## 1. 新建领取遗物的奇遇

将[领取遗物源码](../../../templates/zh-CN/09-relic-grant.cs.txt)完整复制到新文件 `source/RelicGrant.cs`。命名空间与自己的 `ModEntry.cs` 保持一致。这个文件只增加 `RelicGrant`，不要重新复制首课入口。

在 `ModEntry.cs` 的 `Load` 方法里，保留原注册，再添加：

```csharp
registrar.AddContent(new RelicGrant());
```

现在入口应该注册 `StarterRelic`、`PracticeStage`、`PracticeAdventure` 和 `RelicGrant`。注册奇遇后，还要把它放到牌列上才能遇见它。

## 2. 把奇遇放在守卫上面

打开 `source/PracticeStage.cs`，在 `PracticeStage.CreateDefinition` 中找到 `columns[0].cards.Add(guard);`，**紧接在它后面**加入：

```csharp
columns[0].cards.Add(
    registry.Get<EventContent>(ModEntry.PackageId + ".event.relic_grant")
        .CreateCard(Id + ".grant"));
```

第一列从底到顶变成出口、守卫、领取遗物。最后放的奇遇最先露出来。它有一个奖励选项，选择后会把旅者遗物放入宝物栏，并移除奇遇卡。

## 3. 给进场效果安排下一个场景

旅者遗物在**进入场景时**加盾。你是在第一场进场后才领到它，所以要进入下一场才能看到效果。

在同一个 `PracticeStage.cs` 文件中找到 `PracticeAdventure` 类，只改这两项：

- 把 `Steps` 中唯一一步的 `roundCount = 1` 改为 `roundCount = 2`，让同一牌场生成两次。
- 把 `public override int IntermissionInterval => 0;` 中的 `0` 改为 `1`，两个场景之间就有整备。

如果已经在多场景课做过这两处修改，保持 2 和 1 即可，不要再加一份 `Steps` 或第二个冒险类。

## 4. 领取、通关，再看护盾

1. 保存源码、递增包版本，回游戏构建安装并完整重启。
2. 新开“林径练习”。先点击“领取遗物”，选择奖励，确认宝物栏出现旅者遗物。
3. 击败守卫，点击出口。第一场出口会带你进入整备流程；继续到第二场景。
4. **先不要攻击。**看角色护盾，应比这件宝物触发前增加 4 点（一级、`BaseValue = 4`）。
5. 观察完护盾后，处理第二场的领取奇遇，再打守卫、点击最后出口，完成冒险。重复牌场也会重复放这张奇遇；第二次领取发生在进场之后，不改变刚才已观察的进场收益。

建议在没有其他进场加盾效果的情况下试。先记录进场收益，再处理其他牌。重复领取会增加后续效果来源，受伤也可能消耗护盾，都会使之后的总量变复杂。第一场出口没有立刻胜利是正常的，第二场才是结局。

**有宝物却没加盾？**先确认自己已进入第二场；领取瞬间不是进场事件。再核对一级、`BaseValue`、同名宝物数量和其他加盾或消耗来源。不要只凭总护盾值猜效果。

## 5. 再试一次数值变化

把 `StarterRelic.BaseValue` 从 4 临时改为 2，保存、递增版本、构建安装、完整重启并新开局。现在图鉴一级应为 2，第二场进场也应加 2 护盾。试完恢复成自己想保留的值，再构建一次。

这个练习让你看到：**说明和效果应该用同一个公式**。不要只改说明字符串。宝物品质箭头也不会把一级升成二级；本例一级 4、二级 8，是等级倍率，各品质没有另外一套数值。

### 想让随机宝箱也出现它？

`CategoryTags` 说明它是什么类型：本例是 `TreasureCategoryTags.Shield`。`PoolTags` 决定哪些角色可以抽到它：本例是 `CharacterTreasurePoolTags.HealingLifeBuild`，林地药师允许这个池。允许入池仍不保证每次抽到，所以本课用明确奖励先试效果。完整写法见[宝物参考](../reference/treasures.md)。

以后做带次数或层数的宝物时，将状态保存在每件运行时宝物里，默认换场景重置。已经加给玩家的护盾是资源，不是宝物内部计数。可以接着做[三次上限的练习量瓶](rules-and-state.md)。

想在两种语言下显示对应名称，按[文本合并步骤](assets-and-text.md#合并专题片段的文本)加入 `event.relic_grant.*` 条目。首课的 `content.starter_relic.*` 已在生成项目中。
