# 把两个场景连成冒险

[English](../../en/tutorials/adventure.md) · [目录](../README.md)

让“林径练习”延长为两场：第一场打完经过整备，第二场打完才胜利。先复用同一份牌场，之后再换成不同地区。

**需要已有：**[固定关卡](stage.md)。这次只编辑 `source/PracticeStage.cs` 里的 `PracticeAdventure` 类，不用新建文件或准备图片。如果已经做过[宝物课](treasure.md)，两场景和整备已经设置好了，可以直接试第 2 节。

每次安装修改后的内容前，递增 `package.json.version`，构建安装并完整重启。

## 1. 让同一个牌场再出现一次

在 `PracticeAdventure.Steps` 中，把唯一一步的 `roundCount = 1` 改为 2，再把类中的 `IntermissionInterval => 0` 改为 `IntermissionInterval => 1`。`sourceStageId` 继续指向 `.stage.practice`。每一轮会从同一个 Stage 定义重新创建牌场，因此两场都有守卫和出口。

素材 ID 是 `local.alice.lantern-trail.stage.practice`；步骤 ID 是 `local.alice.lantern-trail.adventure.practice.step.one`；实际场景 ID 在此步骤 ID 后追加 `-round-1` 和 `-round-2`。事件跳场景时必须引用本局展开后的 ID，不能用素材 ID代替。

## 2. 验证过渡而非只看列表

构建安装，完整重启并新开一局。第一场击败守卫、点击出口，观察整备或过渡入口，再进入下一场景。第二场应重新有守卫，最后出口才胜利。若加入宝物奖励，先检查下一场的进场效果。

保存并恢复第一场的进度，继续完成两场；再新开一局检查回到第一场。已有运行中的冒险不会因源码重新构建而自动重排，改结构后应新开局。

## 3. 再连接不同的素材地区

[三个地区结构片段](../../../templates/zh-CN/07-three-region-adventure.cs.txt)仅定义 Adventure，明确依赖已注册的 `.stage.region_one`、`.stage.region_two`、`.stage.region_three`。先实现这三份 Stage，再注册 `MyAdventure`。可以只复制 `PracticeStage` 类，分别保存成三个地区文件，再给它们不同的类名和内容 ID；不要每份都连同 `PracticeAdventure` 一起复制。

每个 step 指向自己的素材，并明确 `columnCount`、`roundCount`、`cardsPerRound`、生成预设和整备。固定布局用完整列定义决定牌数；随机布局才用每轮牌数和候选池生成。

实际选关名单使用难度的 availableHeroIds；当前 C# 路线中素材 allowedCharacterIds 是保留元数据。`attackEnhance` 等数值会影响生成结果，先以无额外强化的单一难度验证路线，再引入增长。不要把教学代码中的默认六轮误认为必须照搬的成品节奏。

## 4. 按需要进入进阶主题

首领要区分敌人卡的 `isBoss`、step 的 `boss` 与 Stage 的 `boss`；首领卡不会单独切换 Boss 音乐。规则、固定/每日种子、动态续接、循环和 StageGraph 见[内容总览](../02-content-creation.md)；字段查[关卡与冒险参考](../reference/stages.md)。

这些能力不是制作两场景冒险的前置条件。每新增一个机制，重新测入口、合法操作、必需内容、出口、胜负、重置与读档。

## 回游戏检查，然后继续

- 第一场出口可达并进入第二场；第二场可胜利。
- 步骤、素材和实际场景 ID 区分清楚，各 ID 唯一。
- 新局和存档恢复都能到达结局，难度和角色名单对应。

下一步[加入图片、音乐和双语文本](assets-and-text.md)。

想让名称和说明随中英文切换，请按[文本合并步骤](assets-and-text.md#合并专题片段的文本)加入本课所用的条目。未合并时会显示源码中的默认文字。切换语言后新开一局检查。
