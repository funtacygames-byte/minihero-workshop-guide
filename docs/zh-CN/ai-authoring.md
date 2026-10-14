# 给 AI 的制作任务与交付合同

[English](../en/ai-authoring.md) · [Index](README.md)

教程修订 4 · Mod API 1.8.0 · 2026-10-14


把本页、[功能地图](feature-map.md)、目标任务课、对应参考和代码片段一起交给 AI。离线读取从仓库根 `llms.txt` 开始；机器索引是 [capabilities.json](../capabilities.json)，选定声明是 [api-surface.json](../api-surface.json)。教程不能代替游戏生成的开发引用。

## 1. 先识别任务，不猜宿主能力

| 用户目标 | 优先阅读 | 交付必须补齐 |
| --- | --- | --- |
| 新宝物／改数值 | [宝物](tutorials/treasure.md)、[状态](tutorials/rules-and-state.md) | 功能指纹、品质档位、描述公式、池、重置、指定获取 |
| 新卡牌抉择 | [卡牌选择](tutorials/card-choice.md)、[字段](reference/card-choice.md) | 具体类、选项 ID、卡面、收益、代价、处理器、牌场放置 |
| 道具／事件奖励 | [道具事件](tutorials/items-and-events.md) | 直接或目标路径、奖励类型、注册与出现、回合 |
| 新页面／开始菜单 | [页面](tutorials/custom-ui.md) | 控件树、控制器、AddScreen、动作、回退入口、双语 |
| 新角色／招式 | [角色](tutorials/character.md) | 引用类注册、角色入口、池、第一初始招式、实测目标 |
| 随机挑战／无限模式 | [冒险模式](tutorials/adventure-modes.md) | 种子、日期偏移、包含首轮的轮数、唯一续接 ID、终止 |
| 修改配置 | [配置](tutorials/configuration.md) | 当前没有玩家页；定义默认、getter fallback、同一公式 |

只读签名而不读语义参考容易误用 requested、来源 ID 或 consumeTurn。缺接口时说明限制，不能自己发明字段、菜单、热重载或 ModUi.SetConfig。使用卡牌选择先核对实际 Core 引用含这些类型；API 字符串同为 1.8.0 不证明旧安装已带最近新增接口。

## 2. 开始前记录六项输入

包 ID 与生成命名空间；实际 API 引用版本及是否含目标类型；已有文件与入口全名；玩家操作目标；机制六项指纹；可用素材与验证环境。先读 package.json 和生成 csproj，保留 codeEntryPoint 与唯一 ModEntry。资料缺失标未核，不把扫描失败写成零问题。

MiniHero 是西式奇幻／童话冒险；瑶光是用户明确的古代中国女侠例外。用户最近要求、适用 AGENTS 和当前运行代码优先于历史方案。不要从旧 Wuxia 类型名推断题材，不为了翻译迁移稳定 ID 或键。

## 3. 交付文件和可操作结果

玩法规则写在 C# 内容类中，不改成声明式玩法 JSON 或 contentIndex 配方。包清单是自动生成的元数据，本地化 JSON 只承载显示文字。源码在 source/*.cs，生成项目目标 netstandard2.1、C# 9；引用游戏生成的 API/Core。运行包需要 package.json、mod/<AssemblyName>.dll、localization/zh-Hans.json 与 en.json，以及真正使用的包内素材。完整 codeEntryPoint 必须对应 namespace＋类名，内容 ID 以包 ID 加点号开头。声明 code.execute；代码以用户权限执行，不是沙箱。

交付时列出新增／修改文件、Load 注册片段、被哪个角色池／关卡引用、两个 locale 的新增键、具体玩家入口和预期结果。片段中依赖的 registry/context/nextRequest 必须说明由哪里得到；不提交省略抽象成员或未定义类型的假完整类。不要发布游戏 DLL 引用、bin/obj、.tmode-sdk、个人路径或存档。源包和发布输出区别见[工程课](01-project-and-build.md)。

## 4. 必须保持的规则

- CategoryTags、PoolTags、RequiredAppearanceTags 各司其职；角色候选池按任意交集匹配，权重使用 GetPoolWeight。
- 五／四／三／两档从普通／优良／稀有／史诗到传说；固定公式只有传说时明确变体，不让默认五品质误扩展。
- 治疗关联用 AfterHealingEvent.requested 的完整结算量；actual 仅资源和表现，显式溢出用 overflow。自然描述“治疗量”／healing amount。
- 默认新场景清空宝物临时次数、层数、待用效果与额度；主动使用次数恢复。明确跨场景例外才保留交接数据。
- 基础属性换算向下取整，共同百分比先相加统一结算。预览与实战同规则，不提前推进真实状态。
- 专属行为在具体内容类；引擎只用共同结算。新选择的显示卡不执行原行为，resolver 存稳定 ID；成功返回前不自行结束回合。
- 英文默认 attack，需区分时 basic attack；保留 NormalAttack 等技术名。自然缩短译文，不擅自改宿主 UI。

## 5. 可直接复制的任务提示

```text
使用教程修订 4 和当前游戏生成的 MiniHero 开发引用。
玩法规则写成 C# 内容类。
任务：给我现有的固定测试关卡增加双卡单选。
保留包 ID、生成命名空间、现有唯一入口和无关内容。
治疗分支：免费恢复 5 生命；守卫分支：支付 2 金币，防御增加 1。
使用 CardChoiceEventContent；显示卡不执行原卡行为。
交付完整具体类、Load 注册、关卡放牌、中英文文本键、依赖及预期检查。
分别记录实际执行的编译、玩法、存档、界面和 Steam 检查。
不发明宿主接口；引用缺失或行为不支持时说明限制。
```

若要求复杂效果，先把触发、输入、收益、状态、目标、代价写全，再生成。不要把“参考其他游戏”解释成复制其 API 或图片。

## 6. 交付证据

按[调试课](tutorials/debugging.md)记录编译、加载、确定性玩法、边界、预览、重置、恢复、双语画面与在线发布。新 DLL 完整重启后验收；同进程重载不足。明确未执行项，不把已有测试或文档检查当本轮跑过。Unity 验证只用已打开的正式 Editor，不创建副本、不启动第二个 Editor、不打开 Temp/PlayerBuildProject。
