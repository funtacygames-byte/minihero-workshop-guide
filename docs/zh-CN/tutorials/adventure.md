# 连接多个场景与整备

[English](../../en/tutorials/adventure.md) · [目录](../README.md)

教程修订 4 · Mod API 1.8.0 · 2026-10-14 · [验证范围](../reference/versions.md)

目标：保留固定练习的可玩流程，扩展成两场景；第一场出口进入过渡，第二场出口胜利。理解素材关卡、步骤和实际场景 ID 的区别后，再扩展三个地区。

前置：[固定关卡](stage.md)。只编辑 `PracticeAdventure`；不需要新美术或外部源 Stage。

安装修改后的构建前，按[首课](first-mod.md#4-修改一次并重新验证)递增 `package.json.version`；同一已安装版本不能对应不同内容。

## 1. 先用一个素材展开两次

把唯一 step 的 `roundCount = 1` 改为 2，`IntermissionInterval` 改为 1。`sourceStageId` 继续指向 `.stage.practice`。每一轮会从同一个 Stage 定义重新创建牌场，因此两场都有守卫和出口。

素材 ID 是 `local.alice.lantern-trail.stage.practice`；步骤 ID 是 `local.alice.lantern-trail.adventure.practice.step.one`；实际场景 ID 在此步骤 ID 后追加 `-round-1` 和 `-round-2`。事件跳场景时必须引用本局展开后的 ID，不能用素材 ID代替。

## 2. 验证过渡而非只看列表

构建安装，完整重启并新开一局。第一场击败守卫、点击出口，观察整备或过渡入口，再进入下一场景。第二场应重新有守卫，最后出口才胜利。若加入宝物奖励，先检查下一场的进场效果。

保存并恢复第一场的进度，继续完成两场；再新开一局检查回到第一场。已有运行中的冒险不会因源码重新构建而自动重排，改结构后应新开局。

## 3. 再连接不同的素材地区

[三个地区结构片段](../../../templates/zh-CN/07-three-region-adventure.cs.txt)仅定义 Adventure，明确依赖已注册的 `.stage.region_one`、`.stage.region_two`、`.stage.region_three`。先实现这三份 Stage，再注册 `MyAdventure`。也可以从 `PracticeStage` 逐份建立不同类和 ID，但不能同时保留重复类名或内容 ID。

每个 step 指向自己的素材，并明确 `columnCount`、`roundCount`、`cardsPerRound`、生成预设和整备。固定布局用完整列定义决定牌数；随机布局才用每轮牌数和候选池生成。

实际选关名单使用难度的 availableHeroIds；当前 C# 路线中素材 allowedCharacterIds 是保留元数据。`attackEnhance` 等数值会影响生成结果，先以无额外强化的单一难度验证路线，再引入增长。不要把教学代码中的默认六轮误认为必须照搬的成品节奏。

## 4. 按需要进入进阶主题

首领要区分敌人卡的 `isBoss`、step 的 `boss` 与 Stage 的 `boss`；首领卡不会单独切换 Boss 音乐。规则、固定/每日种子、动态续接、循环和 StageGraph 见[内容总览](../02-content-creation.md)；字段查[关卡与冒险参考](../reference/stages.md)。

这些能力不是制作两场景冒险的前置条件。每新增一个机制，重新测入口、合法操作、必需内容、出口、胜负、重置与读档。

## 验收与下一步

- 第一场出口可达并进入第二场；第二场可胜利。
- 步骤、素材和实际场景 ID 区分清楚，各 ID 唯一。
- 新局和存档恢复都能到达结局，难度和角色名单对应。

下一步[加入图片、音乐和双语文本](assets-and-text.md)。


相关扩展：[种子、循环与续接](adventure-modes.md)。


本课使用的片段名称与说明已接入 ModText。按[双语文本课](assets-and-text.md)合并示例 entries；不合并时仍显示源码 fallback。已有牌／定义快照不保证即时重译，切语言后新开局检查。
