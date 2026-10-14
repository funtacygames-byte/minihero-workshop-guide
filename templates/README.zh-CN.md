# 功能片段与依赖

[English](README.md) · [目录](../docs/zh-CN/README.md)

教程修订 4 · API 1.8.0 · 2026-10-13

`.cs.txt` 避免把全部片段自动编译进同一个模组。按任务复制为 `.cs`，保留游戏生成 csproj 与清单；这些片段不是可安装包。

## 整合规则

1. 首课的01是完整入口，只保留一个 ModEntry；其他片段添加到它所在命名空间。
2. 默认包 ID 是 local.alice.lantern-trail，namespace 是 LocalAliceLanternTrailMod。不同包 ID 必须同步代码、完整入口与清单，不能只全局替换显示名。
3. 自定义池 Tag treasure_pool.your_package.lantern 是独立技术字符串，角色与宝物两端一致。
4. Load 注册所有引用内容。非空素材绑定必须有文件；先检查规则时按教程删除展示接口与整个 Presentation 属性。

| 片段 | 用途 | 必需依赖 |
| --- | --- | --- |
| [01](zh-CN/01-entry-and-config.cs.txt) | 完整最小入口＋旅者遗物 | 无外部素材；包 ID／namespace 必须适配 |
| [02](zh-CN/02-character-trait-and-move.cs.txt) | 角色＋特性＋招式 | 三张自有图片；可按角色课移除展示绑定 |
| [03](zh-CN/03-character-treasures.cs.txt) | 专属宝物池 | 与02的角色 Tag一致；罗盘图标 |
| [04](zh-CN/04-enemies-and-traits.cs.txt) | 敌人＋特性 | 苔狼战斗图；可先移除展示绑定 |
| [05](zh-CN/05-stage-bindings.cs.txt) | 随机关卡绑定 | 02的角色、04的敌人；三张场景图；另需 Adventure |
| [06](zh-CN/06-stage-music.cs.txt) | 音乐主题 | 自有OGG/WAV；在关卡引用主题 |
| [07](zh-CN/07-three-region-adventure.cs.txt) | 三个地区的连接结构 | 三个已注册 Stage；不是独立工程 |
| [08](zh-CN/08-fixed-stage-lab.cs.txt) | 最小固定关卡＋入口 | 依赖01的 PackageId；无外部素材 |
| [09](zh-CN/09-relic-grant.cs.txt) | 明确奖励奇遇 | 01的宝物；需放到08牌列并注册 |

首个可观察成果用01；确定玩法验证用08，再按宝物课整合09。02～07是按需功能参考，不应把全部类无条件复制进去。文件01的旧名保留以兼容链接，配置接口已移到[兼容说明](../docs/zh-CN/reference/compatibility.md)。


## 新增功能片段

| 片段 | 用途 | 必需依赖 |
| --- | --- | --- |
| [10](zh-CN/10-card-choice.cs.txt) | 卡面双分支 | 01 入口；按专题注册和放牌 |
| [11](zh-CN/11-custom-page.cs.txt) | 页面＋控制器 | 01 入口；按专题注册和放牌 |
| [12](zh-CN/12-items.cs.txt) | 治疗＋目标伤害道具 | 01 入口；按专题注册和放牌 |
| [13](zh-CN/13-stateful-relic.cs.txt) | 独立计数与重置 | 01 入口；按专题注册和放牌 |

这些仍是单项源码片段；11 需 AddScreen，其余需 AddContent。13 是状态教学，不是成品宝物设计。


## 可合并的双语文本

[中文 localization.json](zh-CN/localization.json)与[英文 localization.json](en/localization.json)各提供 65 个示例键，覆盖片段中的 ModText 和 ModUi 文本。只合并需要的 entries，不用文件整体覆盖游戏生成目录；保留包名、其他已有键、locale 与清单的 supportedLocales。完整目录是教学文本集合，不是可安装包。


| Fragment | Purpose | Dependencies |
| --- | --- | --- |
| [14](zh-CN/14-dynamic-continuation.cs.txt) | 有限动态续接 | 08 的 PracticeStage；替换冒险注册，共三场景 |
| [15](zh-CN/15-chained-choice.cs.txt) | 完整两步卡牌选择 | 01 入口、08 放牌；自身处理器、后续存档与取消 |
