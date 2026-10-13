# MiniHero 创意工坊制作教程

**简体中文** · [English](README.md)

学习用 C# 制作 MiniHero 模组：宝物、角色、敌人、道具、奇遇、关卡，以及图片、音乐和多语言文本。

本仓库提供制作教程、独立功能片段和不含中文文字的通用示意图。先阅读教程，再在游戏的冒险工坊中创建自己的项目。

**核对日期：** 2026-10-13 · **当前 Mod API：** 1.8.0

## 教程

| 章节 | 内容 |
| --- | --- |
| [1. 工程与构建](docs/zh-CN/01-project-and-build.md) | 新建工程、C# 结构、编译、安装、重载与哈希 |
| [2. 内容制作](docs/zh-CN/02-content-creation.md) | 内容注册、规则事件、状态重置、角色与关卡绑定 |
| [3. 资源与表现](docs/zh-CN/03-assets-and-presentation.md) | 图片槽位、素材规格、音乐、本地化与配置限制 |
| [4. 测试与发布](docs/zh-CN/04-testing-and-publishing.md) | 玩法验收、故障定位、打包与 Steam 发布准备 |

[教程目录](docs/zh-CN/README.md) · [功能片段](templates/README.zh-CN.md) · [给 AI 的制作入口](docs/zh-CN/ai-authoring.md) · [中英术语](docs/zh-CN/glossary.md)

## 第一次制作

1. 在游戏里打开「冒险工坊 → 开发模组」，新建 C# 项目。
2. 在代码编辑器里打开生成的 `Sources/<packageId>`。若开发页提示缺少 .NET SDK，先安装 SDK。
3. 按第一篇教程修改 `source/ModEntry.cs`，保留生成工程的编译引用与输出路径。
4. 按制作目标选择功能片段，按第三篇加入自己的图片与文本。
5. 在游戏里执行「构建并安装」。修改已加载的 C# DLL 后，完整重启游戏，按第四篇验收。

游戏会提供 `MiniHero.ModApi.dll` 与 `MiniAdventureWorld.Core.dll` 开发引用。教程源码不能代替这两份程序集；玩家制作模组不需要 Unity 或完整游戏工程。

## 目录

```text
docs/
  zh-CN/       简体中文教程
  en/          英文教程
templates/     .cs.txt 功能片段与使用说明
images/        双语教程共用的规格示意图
```

片段用于按需整合：替换 `your.package`，注册被引用的内容，再放入自己的工程；它们不是可直接安装的完整模组。当前游戏没有玩家可打开的 Mod 配置页，制作和验收以源码默认值为准。JSON 后端保留兼容能力，当前没有玩家可打开的 JSON 内容编辑器。

反馈教程问题时，请附游戏/API 版本、章节链接和观察到的错误或行为；分享日志前删去个人磁盘路径与私密信息。
