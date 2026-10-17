# 你想制作什么？

[English](../en/README.md) · [首页](../../README.zh-CN.md)

第一次制作建议按下面三步完成。所有修改都在游戏为你创建的模组项目里进行。

## 入门：从改一个数字到玩自己的关卡

| 顺序 | 本课做什么 | 完成后你会看到 |
| --- | --- | --- |
| 1. [第一个模组](tutorials/first-mod.md) | 创建项目，把进场护盾从 2 改成 4 | 图鉴里的旅者遗物显示新数值 |
| 2. [第一个关卡](tutorials/stage.md) | 在固定牌列摆守卫和出口 | 自己的关卡入口，击败守卫后可以通关 |
| 3. [把宝物放进关卡](tutorials/treasure.md) | 加一张领取宝物的奇遇，再接一个场景 | 下一场景进场时获得 4 点护盾 |

遇到按钮或文件位置问题，先看[操作配图](reference/visual-walkthrough.md)。不能构建或结果不对时，看[排错](troubleshooting.md)。想让 AI 帮你解释和改代码，可以从[使用 AI](ai-authoring.md)开始。

## 扩展你的模组

先完成入门三课，再选择感兴趣的主题。每篇开头说明需要哪些已完成的内容。

| 主题 | 做出来的内容 |
| --- | --- |
| [角色与初始招式](tutorials/character.md) | 提灯游侠、灯辉视野特性和银辉箭 |
| [敌人与特性](tutorials/enemy.md) | 受伤后变强的苔背魔狼，两只狼各自保存状态 |
| [道具与奇遇](tutorials/items-and-events.md) | 恢复生命的药剂和指定敌人受伤的药瓶 |
| [卡牌抉择](tutorials/card-choice.md) | 免费治疗或付金币获得防御，还可扩展连续选择 |
| [次数与状态](tutorials/rules-and-state.md) | 每场景最多三次、治疗后加盾的练习量瓶 |
| [连接多个场景](tutorials/adventure.md) | 出口、整备和下一个场景组成的冒险 |
| [种子与循环](tutorials/adventure-modes.md) | 固定挑战、每日种子、三轮循环和有限续接 |
| [新增与复制难度](tutorials/level-difficulty.md) | 给已有地图追加独立难度，复制别处的参数后修改 |
| [职业与永久进度](tutorials/profession-progress.md) | 击败敌人获得训练点，在已有强化页购买永久职业强化 |
| [素材与双语文本](tutorials/assets-and-text.md) | 自己的图标、探索音乐与中英文名称说明 |
| [自定义页面](tutorials/custom-ui.md) | 有按钮、动态文字和原菜单入口的营地手册 |
| [发布与更新](tutorials/publish.md) | 整理发布资料，上传并更新同一个 Steam 条目 |

## 需要时再查

- [调试自己的模组](tutorials/debugging.md)：缩小问题范围，记录能重复发生的操作。
- [配置兼容](tutorials/configuration.md)：维护旧配置值；当前游戏没有玩家 Mod 配置菜单。
- [全部可用功能](feature-map.md)：已有经验时，按功能查支持范围。
- [代码片段](../../templates/README.zh-CN.md)：找到专题对应文件及复制位置。

<a id="reference"></a>

## 接口与规则参考

查某个类、属性或事件时使用；第一次制作不必逐篇通读。

| 你正在查…… | 参考 |
| --- | --- |
| 入口类、包 ID、内容注册 | [入口与注册](reference/entry.md) |
| 品质、等级、角色宝物池 | [宝物](reference/treasures.md) |
| 角色、招式、敌人特性 | [角色与敌人](reference/actors.md) |
| 固定列、步骤、关卡与冒险 | [关卡与冒险](reference/stages.md) |
| 治疗、伤害、攻击等触发窗口 | [事件](reference/events.md) |
| 计数、预览、换场景与存档 | [生命周期与状态](reference/lifecycle.md) |
| 卡面选项、代价、回合与续选 | [卡牌选择](reference/card-choice.md) |
| 页面、按钮与导航 | [自定义页面](reference/custom-ui.md) |
| 分支或卡牌选项的条件表达式 | [条件](reference/conditions.md) |
| 图片槽位、音乐与翻译 | [展示与文本](reference/presentation.md) |
| 版本不匹配或功能限制 | [兼容](reference/compatibility.md)、[版本](reference/versions.md) |
| 类型和方法的准确签名 | [公开 API 声明](reference/api-surface.md) |

完整手册：[工程与构建](01-project-and-build.md) · [内容制作](02-content-creation.md) · [资源与表现](03-assets-and-presentation.md) · [发布前检查](04-testing-and-publishing.md)。它们按系统组织，适合做完首课后查阅。

[术语](glossary.md) · [反馈文档问题](../../CONTRIBUTING.md)

- [职业与水晶强化](tutorials/profession.md)：创建独立职业并复用内置强化。
