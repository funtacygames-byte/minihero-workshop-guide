# 让玩家在两张补给卡中选择

[English](../../en/tutorials/card-choice.md) · [目录](../README.md)

给林径练习加一张“营地补给”：打开后，可以免费恢复 5 点生命，或支付 2 金币获得 1 防御。你会先做出这两个选项，再分别试金币够和不够的情况。

**需要已有：**[首课](first-mod.md)和[固定关卡](stage.md)。将[补给源码](../../../templates/zh-CN/10-card-choice.cs.txt)复制到新文件 `source/CampChoice.cs`，使用自己项目的命名空间。再修改已有 `ModEntry.cs` 和 `PracticeStage.cs`，不需要图片或第二个入口。

## 1. 把补给卡放在守卫上面

保存为 `source/CampChoice.cs`，使用自己的命名空间。在原 `ModEntry.cs` 的 `Load` 方法中添加：

```csharp
registrar.AddContent(new CampChoice());
```

在 `PracticeStage.CreateDefinition` 的 `columns[0].cards.Add(guard);` 后添加：

```csharp
columns[0].cards.Add(registry.Get<EventContent>(
    ModEntry.PackageId + ".event.camp_choice").CreateCard(Id + ".camp"));
```

如果之前放过领取遗物奇遇，暂时删去它的放牌代码，保留注册。本课先让第一列只有出口、守卫、补给，先点补给。保留原出口与完整列结构。递增包版本、构建安装、完整退出并重启，然后新开“林径练习”。

## 2. 补上选项名称和说明

以下文件只保存显示文字；选项创建、代价和结算仍在 `CampChoice.cs` 中。

实际结果见[中英文卡面截图](../reference/visual-walkthrough.md#6-对照真实-c-卡牌选择)。

合并到现有 `localization/zh-Hans.json` 与 `localization/en.json`，不覆盖其他键：

```json
{
  "locale": "zh-Hans",
  "entries": [
    {
      "key": "event.camp_choice.name",
      "value": "营地补给"
    },
    {
      "key": "event.camp_choice.description",
      "value": "选择治疗或防御补给。"
    },
    {
      "key": "choice.camp.heal.name",
      "value": "月露补给"
    },
    {
      "key": "choice.camp.heal.description",
      "value": "恢复 5 点生命。"
    },
    {
      "key": "choice.camp.guard.name",
      "value": "守卫补给"
    },
    {
      "key": "choice.camp.guard.description",
      "value": "2 金币换 1 防御。"
    }
  ]
}
```

英文条目可从[英文示例表](../../../templates/en/localization.json)复制；取 `event.camp_choice.*` 和 `choice.camp.*` 六个键，按[合并步骤](assets-and-text.md#合并专题片段的文本)加入现有文件。保持键及 5／2／1 一致。没有内置内容译文的预览卡使用生成时的 `ModText` 文本；换语言后新开一次抉择验证，不假定任意自定义快照文字能自动重新翻译。

## 3. 回游戏选择一次，再试付费选项

分别新开测试局，记录选择前后 HP、防御、金币和回合。金币不足 2 时守卫分支变淡且不可选，免费治疗分支仍可完成选择。若有 2 金币，守卫分支恰好扣 2、增加 1 防御；治疗分支走完整治疗流程，满血时 HP 不变不代表未触发治疗。选中后继续击败守卫、点击出口。

打开不移除补给、不扣费、不提交回合。确认时重查来源、条件与代价；同一次选择不能重复结算。选择前的初始请求默认必选，没有取消按钮。基类显式使用事件名称作为标头。

为保证能验证付费分支，不必去别的冒险攒钱。在 `PracticeStage.CreateDefinition` 返回前，临时替换第一列的顺序，并让练习守卫奖励 2 金币：

```csharp
guard.rewardGold = 2;
columns[0].cards.Clear();
columns[0].cards.Add(exit);
columns[0].cards.Add(registry.Get<EventContent>(
    ModEntry.PackageId + ".event.camp_choice").CreateCard(Id + ".camp"));
columns[0].cards.Add(guard);
```

这是第二个测试布局：先打守卫，再打开补给，最后出口。递增版本、构建安装、完整重启并新开一局；守卫给出 2 金币后记录现有金币，再选守卫分支核对恰好扣 2。保留最初布局用于不足金币测试，不在已经打开的选择中改牌列。

## 4. 再做一次可观察修改

把治疗分支 `effect.hp` 和两语言说明中的 5 同步改为 8。递增版本、重新构建、完整重启。受伤时选治疗，核对增量与治疗修正；不要只改显示卡说明。

若需要 7 张卡、取消、隐藏标头、连续选择或复杂专属效果，继续读[卡牌选择完整参考](../reference/card-choice.md)。它同时列出存档、失败回滚和错误码。旧 `richEventChoices` 是另一条最多三个分支的事件路径，不能把它的限制套在新接口上。

## 5. 想多问一步：加入连续选择

[片段 15](../../../templates/zh-CN/15-chained-choice.cs.txt)提供完整 `TwoStepSupplies` 类。复制为 `source/TwoStepSupplies.cs`，用 `registrar.AddContent(new TwoStepSupplies());` 注册，将固定列里的 `.event.camp_choice` 引用换成 `.event.two_step_supplies`，保留守卫与出口。从示例文本表合并六个新键及复用的四个 `choice.camp.*` 键。

首屏可取 3 金币，或取得 2 护盾后再选一次可取消的补给。金币分支直接完成；护盾分支先发盾，再通过 `context.OpenNext` 打开下一请求。原事件已经消费，第二请求不绑定来源，也不重复消费。第二请求的 `consumeTurn = false` 仍继承第一步的待付回合，最终确认或取消只提交该回合一次。

付费后续使用第 3 节的第二个布局：事件引用换为 .event.two_step_supplies，守卫奖励 2 金币，先击败守卫再打开储备。事件在最上方的原布局用于测试金币不足、免费治疗与取消。

递增版本、构建安装并完整重启。选护盾补给，核对 +2 护盾且尚未推进回合；在第二请求打开时保存恢复，再选守卫补给，应扣 2 金币、加 1 防御，总共一个回合。另开一局取消第二屏，保留 2 护盾，该步不花金币，但仍提交先前回合；取消不能撤销已成功的第一步。最后测试散落金币：+3 金币、没有第二屏、一个回合。失败回滚另见[结算参考](../reference/card-choice.md)。

## 想改选项结算时：分清三个 ID

`CampChoice.Id` 是注册内容和存档处理器的 ID；`CardState.id` 是来源卡或显示卡的实例 ID；`CardChoiceOption.id` 是 `heal` / `guard` 这样的分支 ID。三个身份用途不同。相同卡面可用于不同分支，分支 ID 仍须非空且唯一。

显示卡只提供卡面名称、说明和图片；点击选项不会使用那张卡原来的道具、攻击或购买行为。基类提供 `resolverContentId = Id`，因此具体类必须调用 `context.ApplyEffect`；填写了 resolver 后，宿主不会再自动应用 `effect`。不要重复扣 `cost`、删除来源或结束回合，这些由核心处理。
