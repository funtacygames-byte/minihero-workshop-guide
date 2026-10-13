# Terminology

[简体中文](../zh-CN/glossary.md) · [Guide index](README.md)

| Chinese concept | English used in this guide | Technical context |
| --- | --- | --- |
| 创意工坊／冒险工坊 | workshop / Adventure Workshop | Game mod authoring and management |
| 模组 | mod | `MiniHeroMod`, package |
| 包 ID | package ID | `packageId`; stable, untranslated |
| 内容 ID | content ID | Content namespace; stable, untranslated |
| 宝物 | treasure | `TreasureContent` |
| 角色特性 | character trait | `TraitContent` |
| 敌人特性 | enemy trait | `EnemyTraitContent` |
| 招式／角色技能 | move | `MoveContent`; API terminology |
| 普通攻击 | basic attack | Used when distinguishing the attack callback from moves; player text otherwise uses “attack” |
| 道具 | item | `ItemContent` |
| 奇遇 | encounter | `EventContent`; “event” when discussing its API/JSON type |
| 大关卡／完整冒险 | selectable level / adventure | `AdventureContent`, level-selection entry |
| 素材关卡 | source stage | `StageContent` used by adventure steps |
| 场景 | stage | One playable scene/expanded round; reset boundary |
| 明牌 | exposed card | `CardColumnState.Exposed`; last item in bottom-to-top `cards` |
| 治疗量 | healing amount | `AfterHealingEvent.requested` after modifiers |
| 生命条增加量 | HP-bar increase | `AfterHealingEvent.actual`; resources/presentation only |
| 溢出治疗 | overflow healing | `overflow`; explicit overflow conversion |
| 护盾 | shield | Shared shield settlement |
| 智慧 | wisdom | `wisdom` stat |
| 品质／等级 | quality / level | `TreasureRank` / `SourceLevel`; distinct |
| 普通／优良／稀有／史诗／传说 | Common / Uncommon / Rare / Epic / Legendary | `Common/Uncommon/Rare/Epic/Legendary` |
| 构建／安装／重载 | build / install / reload | Separate steps; C# verification also needs restart |
| 旅者遗物 | Wayfarer's Relic | Generated `content.starter_relic.name` English value; keep this exact search term |
| 符刃猎手 | Runehunter | Current `character.rune_hunter.name`; technical ID remains `rune_hunter` |
| 林径练习 | Trail Lab | Teaching stage/adventure in fragment 08; not built-in content |
| 提灯游侠／银辉箭 | Lantern Ranger / Silver Bolt | Teaching character/move in fragment 02 |
| 苔背魔狼／负伤狂怒 | Moss Wolf / Wounded Rage | Teaching enemy/trait in fragment 04 |

Keys, IDs, stored Choice values, enum names, and method names are technical contracts. Translate display values rather than renaming those contracts. The built-in character ID `grove_alchemist` is displayed as **Groveheart** in the current English catalog; use the ID for references regardless of its localized name.
