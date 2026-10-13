# 中英术语

[English](../en/glossary.md) · [教程目录](README.md)

| 中文 | 英文 | 技术依据 |
| --- | --- | --- |
| 创意工坊／冒险工坊 | workshop / Adventure Workshop | 游戏模组制作与管理 |
| 模组 | mod | `MiniHeroMod`、内容包 |
| 包 ID／内容 ID | package ID / content ID | 稳定技术标识，不翻译 |
| 宝物 | treasure | `TreasureContent` |
| 角色特性／敌人特性 | character trait / enemy trait | `TraitContent/EnemyTraitContent` |
| 招式／角色技能 | move | `MoveContent` 的 API 用语 |
| 普通攻击 | basic attack | 区分招式回调时使用，普通玩家说明默认 attack |
| 道具 | item | `ItemContent` |
| 奇遇 | encounter | `EventContent`；谈接口／JSON 类型时用 event |
| 大关卡／完整冒险 | selectable level / adventure | `AdventureContent`、关卡选择入口 |
| 素材关卡 | source stage | 冒险步骤引用的 `StageContent` |
| 场景 | stage | 一次可玩场景／展开后的轮次，也是重置边界 |
| 明牌 | exposed card | `Exposed`，从底到顶列表的最后一项 |
| 治疗量 | healing amount | 治疗增减结算后的 `requested` |
| 生命条增加量 | HP-bar increase | `actual`，只用于资源与表现 |
| 溢出治疗 | overflow healing | `overflow`，只用于明确溢出转换 |
| 护盾／智慧 | shield / wisdom | 通用结算／`wisdom` 属性 |
| 品质／等级 | quality / level | `TreasureRank/SourceLevel`，不是同一维度 |
| 普通／优良／稀有／史诗／传说 | Common / Uncommon / Rare / Epic / Legendary | 枚举为 `Common/Uncommon/Rare/Epic/Legendary` |
| 构建／安装／重载 | build / install / reload | 独立步骤，C# 验收另需重启 |

本地化键、内容 ID、Choice 保存值、枚举与方法名属于技术契约；翻译显示值，不顺手改技术标识。当前英文目录中 `grove_alchemist` 显示为 **Groveheart**，中文为林地药师，技术引用始终使用稳定 ID。
