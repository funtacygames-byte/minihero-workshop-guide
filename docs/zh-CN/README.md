# 教程目录

[English](../en/README.md) · [仓库首页](../../README.zh-CN.md)

第一次制作按顺序阅读；排查具体问题时打开对应章节，使用 GitHub 的文档大纲跳转。

1. [工程与构建](01-project-and-build.md)：创建、目录、代码结构、编译安装、重载、哈希与信任。
2. [内容制作](02-content-creation.md)：事件、品质、状态、角色池、敌人、关卡、道具与奇遇。
3. [资源与表现](03-assets-and-presentation.md)：图片槽位、音乐、本地化与配置限制。
4. [测试与发布](04-testing-and-publishing.md)：边界测试、错误诊断、兼容、打包与发布。

配套阅读：[功能片段](../../templates/README.zh-CN.md)、[给 AI 的制作入口](ai-authoring.md)、[中英术语](glossary.md)。

随游戏发布的教程目录是官方只读内容；`Sources/<packageId>` 是个人可编辑工作区。阅读教程不会覆盖个人源码。源码修改应通过 `Sources → Build → Install` 生效。

![源码构建安装流程](../../images/build-flow.svg)

图中 `Sources` 为源码，`Build` 为构建快照，`Installed` 为安装版本；C# 更新后需完整重启验证。
