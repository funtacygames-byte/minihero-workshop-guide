# 对标研究与教程补全方法

[English](../../en/reference/documentation-design.md) · [Index](../README.md)

教程修订 4 · Mod API 1.8.0 · 2026-10-14


2026-10-14 阅读一手资料后的组织设计；下面是文档方法对比，不把其他游戏 API 移植为 MiniHero 功能。

| 来源 | 观察 | 本教程采用 |
| --- | --- | --- |
| [tModLoader 首课](https://github.com/tModLoader/tModLoader/wiki/Basic-tModLoader-Modding-Guide) | 生成骨架、解释文件、构建、进游戏、修改一个值 | 保留可观察的首课；专题写清编辑位置与改变后的结果 |
| [tModLoader ExampleMod](https://github.com/tModLoader/tModLoader/tree/stable/ExampleMod) | 公开示例实现供按目标查阅 | 提供有限功能片段、依赖和注册说明，不附成品冒险包 |
| [Fabric 首个物品](https://docs.fabricmc.net/develop/items/first-item) | 从注册延伸到可见入口、命名和素材，并列关联源文件 | 每项功能连接规则、玩家入口、文本与资源，不止给类型名 |
| [NeoForge 起步](https://docs.neoforged.net/docs/gettingstarted/) | 开发环境、工程、测试分开组织 | 开发引用、编译、加载、玩法及在线发布分别记录 |

当前修订补齐：道具与事件、卡牌抉择、页面、配置边界、带状态规则、种子／循环／续接和调试七条任务路径；字段参考和功能地图提供横向查询。保留旧手册路径与片段链接，不让已有读者书签失效。

C# 制作流程借鉴 [tModLoader 首课](https://github.com/tModLoader/tModLoader/wiki/Basic-tModLoader-Modding-Guide)的生成工程、具体内容类、实际结果和一次可观察修改。[Fabric 首物品课](https://docs.fabricmc.net/develop/items/first-item)则提供注册、可见入口与素材相连的讲法。本项目落实为 C# 内容类 → Load 注册 → 编译 DLL → 玩家动作验证；包信息和翻译表是辅助数据。

AI 阅读增加机器可读能力清单、llms.txt、明确任务路由与文件交付合同。每条能力注明 available／backend-only／partial，并指向双语页面和公开类型；不能因一个名词在文档出现就假定已实装玩家菜单。

质量检查分层：来源事实核对、两语语义审阅、代码契约比对、实际编译、规则测试、实机和独立读者。哈希同步不等于意思正确；AI 审阅不等于母语玩家验收。后续扩展应优先补读者卡住的步骤与可复现案例，而不是只增加页数。
