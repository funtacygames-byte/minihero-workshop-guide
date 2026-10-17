# 制作你的第一个 MiniHero 模组

**简体中文** · [English](README.md)

想把自己的宝物、角色或冒险放进游戏？从一件进场获得护盾的宝物开始。你会先在游戏里找到它，再亲手改一次数值，之后就可以为它加图片、设计敌人，或做一段自己的冒险。

## 从这里开始

1. [做出第一个模组](docs/zh-CN/tutorials/first-mod.md)：创建项目，在图鉴找到旅者遗物，把护盾从 2 改成 4。
2. [做一个能通关的关卡](docs/zh-CN/tutorials/stage.md)：摆上守卫和出口，进入游戏打一场。
3. [把宝物放进关卡](docs/zh-CN/tutorials/treasure.md)：领取刚做好的宝物，在下一场景看到护盾生效。

需要已安装的 MiniHero、代码编辑器和 .NET SDK。[首课会带你检查准备工作](docs/zh-CN/tutorials/first-mod.md#开始前准备)。不用安装 Unity，也不用获取游戏源码。暂时没有自己的图片、音乐也能完成这三课。

## 接下来想做什么？

| 我想…… | 从哪篇开始 |
| --- | --- |
| 做一个新角色，配上自己的招式 | [角色与初始招式](docs/zh-CN/tutorials/character.md) |
| 设计敌人和受伤后触发的特性 | [敌人与特性](docs/zh-CN/tutorials/enemy.md) |
| 加入药剂或伤害道具 | [道具与奇遇](docs/zh-CN/tutorials/items-and-events.md) |
| 让玩家在几张卡里选一张 | [卡牌抉择](docs/zh-CN/tutorials/card-choice.md) |
| 做“每场景最多触发三次”的宝物 | [次数与状态](docs/zh-CN/tutorials/rules-and-state.md) |
| 把几个场景连成冒险 | [连接多个场景](docs/zh-CN/tutorials/adventure.md) |
| 做每日挑战或循环冒险 | [种子与循环](docs/zh-CN/tutorials/adventure-modes.md) |
| 给现有关卡增加或复制难度 | [新增难度](docs/zh-CN/tutorials/level-difficulty.md) |
| 给角色加职业强化和永久训练点 | [职业与进度](docs/zh-CN/tutorials/profession-progress.md) |
| 让自定义职业使用水晶强化 | [职业与水晶强化](docs/zh-CN/tutorials/profession.md) |
| 换上自己的图片、音乐和英文文本 | [素材与文本](docs/zh-CN/tutorials/assets-and-text.md) |
| 改一个自己的开始页面 | [自定义页面](docs/zh-CN/tutorials/custom-ui.md) |
| 把模组分享给其他玩家 | [发布与更新](docs/zh-CN/tutorials/publish.md) |

不确定该看哪篇时，打开[全部教程](docs/zh-CN/README.md)。专题可以按需阅读，不用从头读完所有接口。

## 遇到问题，或想请 AI 帮忙

- **构建失败、内容没出现、改动没生效**：按[排错指南](docs/zh-CN/troubleshooting.md)找到对应症状。
- **不熟悉 C#，想边做边学**：看[用 AI 帮你制作模组](docs/zh-CN/ai-authoring.md)，有可以直接改写的提问示例。
- **已经在写代码，想查某个字段或事件**：看[接口与规则参考](docs/zh-CN/README.md#reference)。

本教程当前核对到 Mod API 1.11.0；新功能需使用支持对应接口的游戏版本。[版本与已知限制](docs/zh-CN/reference/versions.md) · [更新记录](CHANGELOG.md) · [文档维护](CONTRIBUTING.md)
