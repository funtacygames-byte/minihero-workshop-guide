# 给宝物加一个三次上限

[English](../../en/tutorials/rules-and-state.md) · [目录](../README.md)

做一件“练习量瓶”：治疗后获得治疗量 10% 的护盾，每场景最多 3 次。你会用四瓶药剂看到前三次加盾、第四次停止，再进入下一场检查次数重置。

**需要已有：**[宝物课](treasure.md)的领取奇遇和两场景练习。暂时只保留本课的加盾来源，避免把其他宝物的收益算进来。

| 文件 | 本课操作 |
| --- | --- |
| `source/PracticeCounterRelic.cs` | 新建，复制量瓶源码 |
| `source/RelicGrant.cs` | 将奖励改为练习量瓶 |
| `source/PracticeItems.cs` | 新建或复用月露药剂，改为恢复 10 |
| `source/ModEntry.cs` | 注册量瓶和药剂 |
| `source/PracticeStage.cs` | 放四瓶药剂，保留奇遇、守卫和出口 |

## 1. 领取这件量瓶

把[量瓶源码](../../../templates/zh-CN/13-stateful-relic.cs.txt)复制到 `source/PracticeCounterRelic.cs`，命名空间与入口一致。在原 `Load` 里注册：

```csharp
registrar.AddContent(new PracticeCounterRelic());
```

打开 `RelicGrant.cs`，将 `rewardContentId` 改为 `ModEntry.PackageId + ".treasure.practice_counter"`。保留领取奇遇的放牌代码，只替换奖励，不再同时奖励首课宝物。对应名称和说明也改为领取练习量瓶。

量瓶只有传说品质、一级：源码用 `GetStateVariants()` 明确只返回这一种。你不用为它再补四档数值。它的护盾分类和生命构筑池与前课一样，获取仍用明确奖励。

## 2. 摆四瓶恢复 10 的药剂

如果还没做[道具课](items-and-events.md)，把[道具源码](../../../templates/zh-CN/12-items.cs.txt)复制为 `source/PracticeItems.cs`，使用相同命名空间。已有该文件就直接修改，不再复制同名类。

将 `MoonDewPotion` 的 `Heal => 6` 改为 `Heal => 10`。把源码默认说明及两语言 `item.moon_dew.description` 的 6 一并改为 10。在 `Load` 中注册一次：

```csharp
registrar.AddContent(new MoonDewPotion());
```

在 `PracticeStage.CreateDefinition` 的列创建完毕后、返回定义之前，加入：

```csharp
columns[1].cards.Clear();
for (int i = 0; i < 4; i++)
{
    columns[1].cards.Add(registry.Get<ItemContent>(
        ModEntry.PackageId + ".item.moon_dew_potion").CreateCard(Id + ".heal." + i));
}
```

这会让第二列从上到下依次露出四瓶药剂，每张都有独立实例 ID。第一列仍是领取奇遇、守卫和出口。按[文本合并步骤](assets-and-text.md#合并专题片段的文本)加入量瓶和药剂的中英文条目。

## 3. 回游戏喝四次

保存、递增包版本、构建安装、完整重启。新开林径练习，先领量瓶，再依次点击第二列的药剂。没有其他治疗修正时，记录每次的护盾变化：

| 第几瓶 | 本次新增护盾 | 已触发次数 |
| --- | ---: | ---: |
| 1 | 1 | 1 |
| 2 | 1 | 2 |
| 3 | 1 | 3 |
| 4 | 0 | 仍为 3 |

满血也能用于这项检查：治疗量为 10，即使生命条没有增加，仍应按 10 计算护盾。只缺 2 点生命时也是同样的 1 点护盾。加治疗增减效果后，改用修正后的治疗量计算。

打败守卫，通过出口和整备进入第二场。先不要点新场景的领取奇遇，直接喝第一瓶药剂，应再次加 1 护盾。这一步先确认单件的次数重置；要继续通关时再处理奇遇。观察新增量，不把上一场留下的其他资源当作本次触发。

## 4. 代码如何记住次数

量瓶的 `healingTriggers` 是这件运行时宝物自己的计数。`OnAfterHealing` 先检查治疗量和上限，再增加计数并加盾；`OnSceneReset` 在换场景时归零。

如果用 `static` 字段，两件量瓶可能共用次数；如果存在 UI 对象上，保存恢复也会失去正确来源。这个例子使用可序列化类中的公开整数，便于保存每件宝物各自的状态。

这里读取 `AfterHealingEvent.requested`，表示结算后的治疗量；`actual` 只是生命条真正增加的部分。字段名容易让人误会，具体含义见[治疗事件](../reference/events.md)。

### 准备分享前，再多试几步

触发三次后保存并继续游戏，第四次仍不应加盾。两件量瓶应各算各的次数。连续查看操作预览不能消耗真正的次数，预览和执行要走同一个公式。修改规则时一起检查上限、换场景和保存恢复，详见[生命周期](../reference/lifecycle.md)。

想让整场冒险都受同一规则影响、又不占宝物槽，可以继续查 `AdventureRuleContent`：它需要注册，并通过 `AdventureRuleIds` 或难度的 `adventureRuleIds` 激活。字段与默认值见[规则参考](../02-content-creation.md)。这不是完成量瓶的前置步骤。
