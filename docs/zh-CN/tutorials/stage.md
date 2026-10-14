# 做一场能通关的小冒险

[English](../../en/tutorials/stage.md) · [目录](../README.md)

现在给你的模组做一个“林径练习”入口。进入后只有一名守卫，出口藏在它下面。你会亲手击败守卫、点击出口，再把守卫生命从 4 改到 8，确认自己的关卡也能修改。

**接着哪一步做：**完成[首课](first-mod.md)，保留其中的 `ModEntry` 和 `StarterRelic`。本课不需要图片和音乐。

| 文件 | 本课操作 |
| --- | --- |
| `source/PracticeStage.cs` | 新建，放入关卡源码 |
| `source/ModEntry.cs` | 在 `Load` 中增加一行注册 |
| `package.json` | 每次安装修改后的内容前递增版本 |

## 1. 把关卡代码加入项目

通过工坊项目行的“打开源码”进入自己的项目。在 `source` 文件夹新建 **`PracticeStage.cs`**，将[固定关卡源码](../../../templates/zh-CN/08-fixed-stage-lab.cs.txt)的全部内容复制进去。

如果你的项目没有使用首课的默认包 ID，把新文件的 `namespace LocalAliceLanternTrailMod` 换成自己 `ModEntry.cs` 中的命名空间。其他地方继续使用 `ModEntry.PackageId`，不用重新创建入口或项目。

这个文件包含两个类：`PracticeStage` 决定桌面摆哪些牌，`PracticeAdventure` 让你能从关卡选择页进入这场冒险。保留两者。

打开 `source/ModEntry.cs`，找到原来的 `Load` 方法，在旅者遗物注册后面加一行。修改后这个方法是：

```csharp
public override void Load(IModRegistrar registrar)
{
    registrar.AddContent(new StarterRelic());
    registrar.AddContents(new PracticeStage(), new PracticeAdventure());
}
```

这里只替换原 `Load` 方法。`ModEntry.cs` 中的其他代码保留，尤其是后面的 `StarterRelic` 类。新文件保存后应叫 `.cs`，而不是 `.cs.txt`。

## 2. 看懂守卫为什么在出口上面

在 `PracticeStage.cs` 中找到这两行：

```csharp
columns[0].cards.Add(exit);
columns[0].cards.Add(guard);
```

代码先放出口，再放守卫。牌列按**从底到顶**的顺序保存，最后放进去的守卫露在最上面，所以玩家先打它，打完才看到出口。`columns[0]` 是第一列，`columns[1]` 才是第二列。

![牌列在代码中从底到顶保存，游戏先显示最上方的守卫](../../../images/fixed-column-order.svg)

这份代码已经创建了完整的列结构，其他列为空。不需要向空列补牌，也先不要改 `appearancePool` 或 `cardsPerRound`。这些字段的区别可以等做完后查[关卡参考](../reference/stages.md)。

## 3. 进游戏玩一遍

1. 保存两个源码文件，在 `package.json` 中把版本提高一次。
2. 回工坊点击“构建并安装”，确认成功并启用这份模组。
3. 完整退出并重启游戏，从主菜单进入关卡选择，翻页找到“林径练习”（英文 **Trail Lab**）。
4. 选择唯一的难度和“符刃猎手”（英文 **Runehunter**），开始游戏。
5. 第一列应该露出守卫，其余列为空。点击守卫攻击，直到它被击败。
6. 守卫消失后，点击露出的出口，应该进入冒险胜利结算。

角色已有强化可能改变打败守卫需要的攻击次数；判断结果时看守卫是否被击败、出口能否通关。现在使用游戏的后备图片也可以完成流程，自己的美术以后再加。

**找不到入口？**先看 `Load` 中是否同时注册了 `PracticeStage` 和 `PracticeAdventure`。只有关卡牌面定义，没有冒险入口，选关页不会多出这一项。再检查 `IncludeInSelection` 和难度的 `availableHeroIds`，详见[关卡排错](../troubleshooting.md)。不要把 `BuiltInCharacterIds.RuneHunter` 换成中文显示名。

## 4. 把守卫生命改为 8

回到 `PracticeStage.cs`，在 `ContentCards.Enemy(...)` 中找到 `hp: 4`，改为 `hp: 8`。这只改变守卫的生命，不移动牌列或出口。

保存、递增版本、构建安装、完整重启，然后**新开**一局林径练习。现在守卫最大生命应为 8。旧局的牌已经生成，所以不要用旧存档判断这次修改是否生效。

你已经能创建一场可玩的冒险并修改其中的敌人。接着做[把宝物放进关卡](treasure.md)，让首课的护盾真正生效；也可以先看[连接多个场景](adventure.md)。

### 之后需要时再看

这份代码的 `appearancePool` 留有一个出口模板，用于兼容较早校验器；固定列运行时不会把它补进牌场，因此仍只有一个出口。固定列和随机牌池的完整约束在[参考页](../reference/stages.md)。

本课名称已使用 `ModText`。使用中文源码时默认显示中文；要在英文界面看到对应名称，按[文本合并步骤](assets-and-text.md#合并专题片段的文本)加入 `stage.practice.*` 和 `adventure.practice.*` 条目，再新开一局检查。
