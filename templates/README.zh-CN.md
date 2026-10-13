# 功能片段与依赖

[English](README.md) · [目录](../docs/zh-CN/README.md)

教程修订 2 · API 1.8.0 · 2026-10-13

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
| [03](zh-CN/03-character-treasures.cs.txt) | 专属宝物池 | 与02的角色 Tag一致；提灯图标 |
| [04](zh-CN/04-enemies-and-traits.cs.txt) | 敌人＋特性 | 苔狼战斗图；可先移除展示绑定 |
| [05](zh-CN/05-stage-bindings.cs.txt) | 随机关卡绑定 | 02的角色、04的敌人；三张场景图；另需 Adventure |
| [06](zh-CN/06-stage-music.cs.txt) | 音乐主题 | 自有OGG/WAV；在关卡引用主题 |
| [07](zh-CN/07-three-region-adventure.cs.txt) | 三个地区的连接结构 | 三个已注册 Stage；不是独立工程 |
| [08](zh-CN/08-fixed-stage-lab.cs.txt) | 最小固定关卡＋入口 | 依赖01的 PackageId；无外部素材 |
| [09](zh-CN/09-relic-grant.cs.txt) | 明确奖励奇遇 | 01的宝物；需放到08牌列并注册 |

首个可观察成果用01；确定玩法验证用08，再按宝物课整合09。02～07是按需功能参考，不应把全部类无条件复制进去。文件01的旧名保留以兼容链接，配置接口已移到[兼容说明](../docs/zh-CN/reference/compatibility.md)。
