# 功能地图：可以做什么、从哪里开始

[English](../en/feature-map.md) · [Index](README.md)

教程修订 5 · Mod API 1.8.0 · 2026-10-14

想知道某种玩法能不能做，可以从这里查。第一次制作先走[入门三课](README.md)，不需要先学这些接口。表里的限制帮助你决定采用哪条路线。

| 制作目标 | 支持情况 | 制作时留意 |
| --- | --- | --- |
| [首个模组](tutorials/first-mod.md) | 可制作 | 生成工程、完整入口、构建安装、重启 |
| [宝物与品质](tutorials/treasure.md) | 可制作 | 独立实例、品质和等级、池、指定奖励 |
| [角色与招式](tutorials/character.md) | 有部分限制 | 第一项初始招式与特性；后续招式和初始宝物不自动发放 |
| [敌人与特性](tutorials/enemy.md) | 可制作 | 实例状态、真实伤害与回调窗口 |
| [道具与奇遇](tutorials/items-and-events.md) | 可制作 | 直接／目标使用；旧富事件最多三分支 |
| [新卡牌选择](tutorials/card-choice.md) | 可制作 | 任意数量单选、条件代价、专属处理、续接、回滚与存档 |
| [固定关卡](tutorials/stage.md) | 可制作 | 底到顶完整列；不混合固定列与随机补牌 |
| [冒险与难度](tutorials/adventure.md) | 可制作 | 入口、素材 Stage、步骤、角色名单、整备 |
| [种子循环续接](tutorials/adventure-modes.md) | 可制作 | 每日偏移、总轮数上限、独立续接上下文 |
| [规则与状态](tutorials/rules-and-state.md) | 可制作 | 次数、预览、换场景重置、激活冒险规则 |
| [自定义页面](tutorials/custom-ui.md) | 可制作 | 宿主控件树、动作与本包导航；没有配置写入 |
| [配置兼容](tutorials/configuration.md) | 兼容接口 | 可声明读取默认／历史值；没有玩家配置页或公开写入 |
| [素材与双语](tutorials/assets-and-text.md) | 有部分限制 | 包内路径与槽位；Victory cue 未接 Mod 胜利页 |
| [C# 图路线](02-content-creation.md) | 可制作 | 装载时路线；显式卡快照与条件后继 |
| [调试与测试](tutorials/debugging.md) | 可制作 | 固定输入、差值、错误报告与验证层次 |
| [发布与更新](tutorials/publish.md) | 有部分限制 | 本地构建导出可验；Steam 在线须实际账号环境 |

不同身份与条件见[条件参考](reference/conditions.md)；事件选择见[事件参考](reference/events.md)；字段查[API](reference/api-surface.md)。新手先完成首课再跳读专题，不需要先学习全部功能。当前版本和常见限制另见[版本页](reference/versions.md)。
