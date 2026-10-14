# 给冒险加入种子和循环

[English](../../en/tutorials/adventure-modes.md) · [目录](../README.md)

想让朋友玩到同一个随机挑战，或让通关后的敌人逐轮变强？本课先给现有冒险设置固定种子，再做每日种子和三轮循环。动态续接放在后半篇，可按需阅读。

**需要已有：**[连接多个场景](adventure.md)。前面三个例子只修改 `source/PracticeStage.cs` 里的 `PracticeAdventure`，代码放在类内部、其他方法外面。每种设置只保留一个同名属性；不要同时粘贴两份 `SeedSettings`。

每次修改后，保存、递增包版本、构建安装、完整重启并新开一局。保留能通关的旧源码，方便比较。

## 1. 固定挑战

在 PracticeAdventure 内添加：

```csharp
public override AdventureSeedSettings SeedSettings => new AdventureSeedSettings
{
    mode = AdventureSeedMode.Fixed, seed = "lantern-practice-v1"
};
```

固定值直接成为运行种子；同内容版本、难度和操作序列用于复现。固定牌列本来就不随机，用随机牌池时更容易观察种子差异。种子不保证不同游戏/API 或内容版本完全相同，也不构成排行榜、反作弊或每日奖励系统。

## 2. 每日按哪个日期变化

将上面的属性替换为：

```csharp
public override AdventureSeedSettings SeedSettings => new AdventureSeedSettings
{
    mode = AdventureSeedMode.Daily, seed = "lantern-daily-v1", utcOffsetMinutes = 480
};
```

480 是 UTC+8 的分钟偏移。每日字符串组合种子前缀、冒险 ID、难度和偏移后的 yyyy-MM-dd；偏移合法范围 -840～840，Fixed/Daily 前缀不能空。新局才使用新日期，开局种子写入存档，跨午夜继续旧局不重抽。

分别验证同日新局、不同难度、午夜边界与旧局恢复。记录用于验证的 UTC 时间和偏移；这是客户端日期规则，不会自动提供服务器每日奖励或排行榜。

## 3. 三轮循环

添加一个 LoopSettings 覆写：

```csharp
public override AdventureLoopSettings LoopSettings => new AdventureLoopSettings
{
    enabled = true, startStepIndex = 0, maximumLoops = 3,
    attackIncreasePerLoop = 1, defenseIncreasePerLoop = 0,
    healthIncreasePerLoop = 2, rewardIncreasePerLoop = 0
};
```

startStepIndex 是 Steps 的零基下标，不是展开后的 stageIndex。maximumLoops 包含首轮：1 无额外轮、3 总共三轮、0 无限。enabled 必须显式开启，所有增量和上限非负。下一轮克隆首轮模板，不在上一轮上复加漂移；原 hp=8 的守卫三轮为 8／10／12，攻击相对原值为 +0／+1／+2。

只有最后一个已展开场景的出口才准备下一批，仍走正常整备及进场重置。不要让临时宝物层数因“同冒险循环”而自动跨场景保留。有限上限最终应胜利，重开一局不得残留上局追加场景。

## 4. 动态续接

具体 AdventureContent 可实现 `IAdventureContinuationContent.CreateNextStages`。context 的 State、CompletedStage 和 CampaignStages 是独立副本；读取 Seed、ContinuationIndex 和 State.selectedBranchId 作决策。改这些副本不会授予真实玩家奖励。用 Registry 创建已注册内容，不修改共享注册对象。

返回空列表正常结束；每批最多 4096 场景。返回场景 ID 必须非空，和此前所有场景都不重复；保留合法列数、出口和首领。首个 ContinuationIndex 为 1。若同时有 continuation provider 和 LoopSettings，provider 优先，自动循环不会再另外叠加。

复杂续接先列出输出 ID、来源素材关卡、循环终止、分支与随机策略，再编写方法。无效输出会使出口续接失败，不应该先扣外部代价。产出场景加入可保存列表，续接中途恢复必须保留它们，不能只保存本地 controller 字段。

### 运行一个完整的有限续接

把[片段 14](../../../templates/zh-CN/14-dynamic-continuation.cs.txt)复制为 `source/ContinuingPracticeAdventure.cs`。保留片段 08 的 `PracticeStage`，将现有入口注册里的 `new PracticeAdventure()` 换成 `new ContinuingPracticeAdventure()`；不必为测试同一牌场同时注册两个冒险。

首场景使用自己的步骤 ID；每个出口向 provider 要下一场景，索引 1、2 分别返回 `.continuation.1` 和 `.continuation.2`，索引 3 返回空数组，因此总共三场景。它从已注册素材创建新定义，保留完整固定列与出口，再赋予唯一展开 ID。此例不会自动增加敌人数值，三场景使用相同的守卫。

从示例目录合并三个 `adventure.continuation_lab.*` 条目。递增包版本，构建安装并完整重启；选择林径接力，三次击败守卫、使用出口，并完成中间整备，第三次出口应胜利。首次追加场景后保存恢复，确认生成 ID 保留、没有重复追加；重开一局确认旧追加场景不残留。

## 5. 按顺序试，每次只加一个变化

先固定种子单局成功；再每日日期计算；再三轮无续接 provider；最后 provider 与分支。每一步记录展开 ID、种子、场景／循环索引、敌人数值、出口结果和恢复后的下一场景。每次代码变更递增版本并完整重启。图路线条件另见[条件参考](../reference/conditions.md)及[进阶手册](../02-content-creation.md)。
