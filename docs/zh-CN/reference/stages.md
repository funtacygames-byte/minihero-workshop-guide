# 素材关卡与完整冒险

[English](../../en/reference/stages.md) · [目录](../README.md)

教程修订 2 · Mod API 1.8.0 · 2026-10-13

当前基准 1.8.0。先做[固定关卡课](../tutorials/stage.md)，再查字段；公开声明见[API 表面](api-surface.md)。

## StageContent

```csharp
public abstract string Subtitle { get; }
public virtual bool IncludeInDefaultCampaign { get; }
public abstract StageDefinition CreateDefinition(GameContentRegistry registry);
```

`IncludeInDefaultCampaign` 默认 true；自有练习素材显式设 false，避免默认冒险收录。`CreateDefinition` 返回独立牌场定义，通过 registry 解析注册内容。Stage 定义本身不会创建 Adventure 选关入口。

| StageDefinition 字段 | 用途／边界 |
| --- | --- |
| `id/name/subtitle` | 稳定素材 ID 与玩家显示文字 |
| `appearancePool` | 随机候选池；随机布局在此校验出口 |
| `fixedColumns` | 非空时完全覆盖随机布局，完整列从底到顶克隆 |
| `columnCount/generatedCardCount` | 随机布局计数；固定布局按实际列与牌数计算 |
| `allowedCharacterIds` | 空表示素材不限角色，非空只允许给定稳定 ID |
| `music` | 已注册的音乐主题 ID |
| `boss` | 场景的首领标记，音乐据此选槽位 |
| `victoryConditions` | 点击出口时检查的胜利条件 |
| `generationProfile` | 生成预设，见下文 |

当前 C# 校验在 `fixedColumns` 非空时检查固定牌中的出口，否则检查候选池；池中可保留 Exit 模板以兼容较早版本。运行时不把该模板加入固定列。不能半边固定半边随机补牌。出口可达与条件成立必须通过实际点击验收；击败普通敌人不会自动胜利，存活首领会阻止离场。

## AdventureContent 与步骤

需要定义 `Description`、`PreviewImageId`、`SourceStageId`、`Steps`、`Difficulties`；`Name/Id` 继承公共内容基类。`IncludeInSelection` 默认 true；`IntermissionInterval` 默认 2；规则列表默认空，Loop/Seed 默认 null。

`public virtual AdventureDefinition CreateDefinition()` 复制步骤、难度和规则列表，不在此处保存某局进度。宿主把 Adventure 合并到关卡选择页，再按步骤创建实际场景。

| AdventureStepDefinition | 默认／语义 |
| --- | --- |
| `id` | 唯一步骤 ID；展开场景是 `<id>-round-<从1开始轮次>` |
| `sourceStageId` | 已注册的 Stage 素材 ID |
| `columnCount` | `GameRules.ColumnCount` |
| `roundCount` | 6；教学可显式设 1 或 2 |
| `cardsPerRound` | `GameRules.CardsPerStage`，随机布局数量 |
| `boss` | false；首领步骤在末轮标记 Boss |
| `intermissionMode` | `Default`，与间隔共同决定整备 |
| `generationProfile` | 空时继承素材预设 |

`AdventureDifficultyDefinition` 默认 difficulty=1、maxHeroCount=4，角色与规则列表空；攻击、防御、生命、奖励强化默认 0，crystalRewardMultiplier=1。成长字段和按 section 数组用于进阶设计；不因字段存在就要求首课填写。

三种 ID 不能互换：Adventure 是选关 ID，Stage 是素材，step ID 展开成实际场景。`nextStageId` 指向当前运行实际场景列表；只注册素材不足以跳转。


包括固定布局在内的所有步骤都必须满足：`columnCount` 为 1～5、`roundCount >= 1`、`columnCount <= cardsPerRound <= 100`；否则注册报告 `AW_ADVENTURE_STEP_RANGE`。练习片段使用 `cardsPerRound = GameRules.ColumnCount`（5）通过元数据校验，实际固定牌场仍只有所给的两张牌。当前冒险校验还要求首领步骤的素材 `appearancePool` 含 `isBoss` 敌人，即使素材使用固定列；同时确认实际固定牌场也放入了预期首领。

## 随机生成与进阶入口

公开预设为 `StageGenerationProfiles.Default/Weighted/Layered/Branching/LayeredBranching`。预设影响抽取与发牌，不代替合法出口与玩法检查。Boss 卡用 `CardState.isBoss`，与素材和步骤标记共同核对；自动保证出现还需 `guaranteedInStage` 等实际生成约束。

循环 `maximumLoops = 3` 总共三轮，0 无上限；动态续接空数组结束冒险；每日种子明确 UTC 偏移。StageGraph 的 C# 节点需填 `card`，图的 Victory/Failure 节点不取代实体出口。详细代码和条件语法放在[进阶总览](../02-content-creation.md)，本页不把它们作为基础制作前提。
