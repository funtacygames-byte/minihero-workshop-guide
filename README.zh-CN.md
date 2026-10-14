# MiniHero 创意工坊制作教程

**简体中文** · [English](README.md)

用 C# 制作自己的宝物、角色、招式、敌人、道具、奇遇、关卡和冒险，也能制作卡牌抉择、自定义页面以及包内图片、音乐和双语文本。每条任务路径说明前置条件、修改文件、注册与出场方式、预期结果和排错入口。

教程修订 4 · Mod API 1.8.0 · 2026-10-14 · [实际验证范围](docs/zh-CN/reference/versions.md)

## 第一次制作

先完成[运行并修改第一个模组](docs/zh-CN/tutorials/first-mod.md)：生成工程 → 保留入口 → 构建安装 → 完整重启 → 图鉴查看旅者遗物 → 改一次数值。随后用[固定关卡](docs/zh-CN/tutorials/stage.md)走通守卫和出口，用[明确宝物奖励](docs/zh-CN/tutorials/treasure.md)验证真实规则，不依赖随机抽中。

需要游戏、代码编辑器与 .NET SDK；不需要 Unity 或完整游戏工程。开发引用由当前游戏生成，教程仓库不能代替 SDK。每次安装修改后的构建，递增包版本并完整重启验证新 DLL。

## 按制作目标阅读

| 目标 | 本课完成什么 |
| --- | --- |
| [宝物](docs/zh-CN/tutorials/treasure.md) | 品质、等级、角色候选池、确定获取与真实效果 |
| [角色与初始招式](docs/zh-CN/tutorials/character.md) | 引用组合、注册、选角入口与目标验收 |
| [敌人与特性](docs/zh-CN/tutorials/enemy.md) | 独立牌实例、伤害窗口与计数 |
| [道具与奇遇](docs/zh-CN/tutorials/items-and-events.md) | 药剂、目标伤害、属性与指定内容奖励 |
| [新卡牌选择](docs/zh-CN/tutorials/card-choice.md) | 正式卡面二选一、条件与代价、来源消费和回合 |
| [次数与状态](docs/zh-CN/tutorials/rules-and-state.md) | 治疗计量、三次上限、实例隔离、预览与重置 |
| [固定关卡](docs/zh-CN/tutorials/stage.md) | 底到顶牌列、守卫→出口与入口 |
| [连接多个场景](docs/zh-CN/tutorials/adventure.md) | 步骤、场景 ID、整备和保存恢复 |
| [种子、循环与续接](docs/zh-CN/tutorials/adventure-modes.md) | 固定／每日种子、日期偏移、三轮循环、动态续接 |
| [自定义页面](docs/zh-CN/tutorials/custom-ui.md) | 控件树、按钮、控制器、本包导航与原菜单回退 |
| [配置兼容](docs/zh-CN/tutorials/configuration.md) | 定义、默认与历史值读取；当前无玩家配置页 |
| [素材与双语文本](docs/zh-CN/tutorials/assets-and-text.md) | 图片槽位、包内路径、音乐、翻译表与变量 |
| [调试与可复现测试](docs/zh-CN/tutorials/debugging.md) | 固定输入、数值差、边界测试和错误报告 |
| [发布与更新](docs/zh-CN/tutorials/publish.md) | 本地打包与 Steam 交付分别验收 |

首课加上以上十四篇专题构成十五条任务路径。[完整功能地图](docs/zh-CN/feature-map.md)逐项标明当前可用、部分接入和仅后端的能力。

## 卡牌抉择需要先知道什么

新接口的显示卡只负责预览；收益来自选项数据或注册的具体处理器。打开不扣费，成功确认才结算；支持任意数量的单选卡、分页、条件、代价、多阶段抉择、失败回滚和可保存处理器。先做[营地补给课](docs/zh-CN/tutorials/card-choice.md)，再查[字段、回合与存档契约](docs/zh-CN/reference/card-choice.md)。

## 排错、参考和 AI

按[排错指南](docs/zh-CN/troubleshooting.md)定位不能编译、加载失败、没有出场、效果不触发和素材不显示。需要签名、默认值与状态语义时查[API 与规则参考](docs/zh-CN/README.md#reference)。

- [完整目录](docs/zh-CN/README.md)与[十五组功能片段及依赖](templates/README.zh-CN.md)
- [AI 制作合同](docs/zh-CN/ai-authoring.md)、[机器能力清单](docs/capabilities.json)与 [llms.txt](llms.txt)
- [术语表](docs/zh-CN/glossary.md)、[版本与证据](docs/zh-CN/reference/versions.md)、[对标研究](docs/zh-CN/reference/documentation-design.md)
- [工程](docs/zh-CN/01-project-and-build.md)、[内容手册](docs/zh-CN/02-content-creation.md)、[资源手册](docs/zh-CN/03-assets-and-presentation.md)、[完整验收](docs/zh-CN/04-testing-and-publishing.md)
- [维护与反馈](CONTRIBUTING.md)

本仓库提供教程、有限源码片段和教学示意，不附成品冒险包或游戏美术包。玩法使用 C# 内容类并编译成 Mod DLL；包清单、翻译表与存档是辅助数据。配置兼容能力不表示有对应玩家设置页。反馈时附教程修订、实际游戏/API、包版本、具体步骤、预期／实际和首条诊断，并移除私人路径、存档与账号信息。
