# MiniHero 创意工坊制作教程

**简体中文** · [English](README.md)

用 C# 制作宝物、角色、敌人和关卡，并加入自己的图片、音乐和双语文本。教程从一个可观察的成果开始，再按目标扩展。

教程修订 2 · Mod API 1.8.0 · 2026-10-13 · [版本与验证范围](docs/zh-CN/reference/versions.md)

## 第一次制作

从[运行并修改第一个模组](docs/zh-CN/tutorials/first-mod.md)开始：创建工程，保留生成入口，构建安装，完整重启，在宝物图鉴查看旅者遗物，再改一次数值。随后用[固定关卡](docs/zh-CN/tutorials/stage.md)走通守卫和出口；[宝物课](docs/zh-CN/tutorials/treasure.md)提供确定奖励以验证真实效果。

需要游戏、代码编辑器与 .NET SDK。玩家不需要 Unity 或完整游戏工程；开发引用由游戏生成，不能从此教程仓库代替取得。

## 按制作目标阅读

| 目标 | 本篇完成什么 |
| --- | --- |
| [宝物](docs/zh-CN/tutorials/treasure.md) | 品质、等级、候选池和明确奖励 |
| [角色与初始招式](docs/zh-CN/tutorials/character.md) | 注册组合、选角入口、双目标验收 |
| [敌人与特性](docs/zh-CN/tutorials/enemy.md) | 实例创建、伤害窗口、独立计数 |
| [第一个固定关卡](docs/zh-CN/tutorials/stage.md) | 守卫→出口，固定列和玩法验证 |
| [连接多个场景](docs/zh-CN/tutorials/adventure.md) | 步骤、整备、场景 ID、保存恢复 |
| [图片、音乐与双语文本](docs/zh-CN/tutorials/assets-and-text.md) | 真实槽位、包内路径、共同参数 |
| [打包、发布与更新](docs/zh-CN/tutorials/publish.md) | 本地构建和 Steam 交付分别验收 |

## 模组出了问题

打开[排错指南](docs/zh-CN/troubleshooting.md)，按“不能编译”“编译后加载失败”“效果没触发”“图片不显示”等症状定位。需要完整签名、默认值与状态语义时查[API 与规则参考](docs/zh-CN/README.md#reference)。

## 手册与辅助资料

- [工程与构建](docs/zh-CN/01-project-and-build.md)
- [内容制作与进阶规则](docs/zh-CN/02-content-creation.md)
- [资源与表现](docs/zh-CN/03-assets-and-presentation.md)
- [完整测试与发布](docs/zh-CN/04-testing-and-publishing.md)

[完整目录](docs/zh-CN/README.md) · [功能片段与依赖](templates/README.zh-CN.md) · [AI 制作入口](docs/zh-CN/ai-authoring.md) · [术语表](docs/zh-CN/glossary.md) · [维护说明](CONTRIBUTING.md)

本仓库收录教程、有限功能片段、共用示意图和必要的界面截图，不附完整冒险包或独立游戏美术素材。配置和 JSON 的后端兼容能力不表示游戏存在对应玩家编辑页。

反馈时附游戏/API 版本、教程修订号、具体步骤和实际错误。提交前移除个人路径、存档和账号信息，见[贡献说明](CONTRIBUTING.md)。
