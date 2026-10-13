# 给 AI 的模组制作入口

[English](../en/ai-authoring.md) · [教程目录](README.md)

核对日期：2026-10-13。当前 Mod API：1.8.0。

本文须与四篇教程和需要的[功能片段](../../templates/README.zh-CN.md)一起阅读，不能代替游戏编译引用或实际测试环境。

## 阅读顺序与事实来源

先读[工程与构建](01-project-and-build.md)，再按目标读[内容制作](02-content-creation.md)和[资源与表现](03-assets-and-presentation.md)；交付前执行[测试与发布](04-testing-and-publishing.md)。

用户最新要求、适用的项目约束和当前运行代码优先于旧方案或旧译文。MiniHero 是温馨的西式奇幻与童话冒险；瑶光是用户明确指定的中国古代女侠例外，不能扩展为整个世界的风格，也不能从旧技术命名推断题材。

## 当前能力与限制

| 目标 | 公开入口与边界 |
| --- | --- |
| 角色、特性、宝物、招式、敌人、道具、事件 | C# 公开内容类，通过 `registrar.AddContent/AddContents` 注册 |
| 可选择的完整冒险 | `AdventureContent`＋素材 `StageContent`＋步骤与难度；只注册 Stage 不会创建大关卡入口 |
| 固定布局谜题 | `StageDefinition.fixedColumns`，按底部到顶部存储，最后一张为明牌 |
| 每日／固定挑战 | `AdventureSeedSettings`；每日换种子明确指定 `utcOffsetMinutes` |
| 循环成长 | `AdventureLoopSettings`；`maximumLoops = 3` 总共三轮，`0` 无上限 |
| 动态续接 | `IAdventureContinuationContent.CreateNextStages`；读取隔离 context，空数组结束冒险 |
| 冒险规则 | `AdventureRuleContent`，由冒险／难度的 `adventureRuleIds` 激活 |
| 自定义页面／开始页 | `registrar.AddScreen`、`ModUi` 控件树与 `ModScreenController`，宿主生成 Unity UI |
| 图片与音乐 | 包内路径、自动素材索引、展示槽位与音乐主题 |
| 配置 | `AddConfig/ModConfig` 保留兼容接口，当前没有玩家配置页 |
| JSON | 后端保留兼容，当前没有玩家 JSON 编辑器 |
| 开局内容 | 特性与第一项初始招式可用；选角不发 `StartingTreasureTypes` 或后续初始招式 |
| DLL 更新 | 最终验收必须完整重启，同进程重载不足以证明新 DLL 生效 |
| Steam | 本地校验／导出与实际上传、订阅、下载分别验收 |

不要虚构宿主方法、事件字段、配置菜单或已接通的音乐位置。查当前公开引用；接口不存在时说明限制，不补一个假接口让编译表面通过。

## 交付目录

运行包含 `package.json`、`mod/<AssemblyName>.dll`、`localization/<locale>.json`，以及需要的素材、索引和音乐。源码项目另含 `source/*.csproj`、`source/ModEntry.cs` 和游戏生成的 `.tmode-sdk` 引用。

- 包 ID、目录 ID、入口特性与清单保持一致。
- `codeEntryPoint` 是含命名空间的类型名，`codeAssembly` 是包内 DLL 相对路径，均须对应真实输出。
- 内容 ID 以 `packageId + "."` 开头；新本地化键用 ASCII 英文语义标识，译文放值中。
- 入口与内容类公开并有公开无参构造函数；宝物独立、可序列化，专属行为写在具体类中，调用通用结算。
- 声明 `code.execute`；代码以当前用户权限运行，不是沙箱。
- 目标框架为 `netstandard2.1`，引用当前游戏 API/Core DLL，发布包不包含这两份引用。
- 工坊生成并校验发布哈希；不发布本机报告、开发引用、`bin/obj`、临时目录或个人存档。

制作电脑必须获得两份游戏程序集，可从已安装游戏新建项目取得。教程源码不能代替 Core DLL。不要将正式工程目录复制或链接到临时工程用于编译。

## 规则口径

- 新宝物先与当前目录比较触发、输入、收益、状态、范围、代价，避免换皮。
- 分类、池 Tag 与出场条件分开；角色池按任意交集匹配，权重用数值，不用额外 Tag。
- 品质均到传说；五／四／三／两档分别从普通／优良／稀有／史诗开始，不补未给的数值。
- 治疗关联读取完整结算治疗量；仅溢出转换读取溢出，玩家文案默认简称“治疗量”。
- 进入新场景重置宝物临时计数、叠层、待用强化与额度；跨场景例外明确写出并验证读档。
- 基础属性换算向下取整，同类百分比相加后结算；预览与执行复用规则。
- 固定列是牌堆：`{ exit, guard }` 才表示先打守卫；必须点击牌面验收。
- 英文默认用 `attack`，确需区分招式等伤害时用 `basic attack`；技术 `NormalAttack` 标识保留。

## 交付前证据

说明玩家玩法、包 ID、最低 API 和完整目录；报告真正执行过的构建命令与结果。通过实际加载器验证注册、哈希、安装、启用／停用、本地化和加载。

实际运行关键效果、边界、通关／失败、重置、续接／循环与存档恢复。检查图片、声音及文本控件，使用原字号和原版面，自然缩短译文。C# 修改在完整重启后验收。

准确列出未验证部分。测试文件存在不表示已经执行，能编译不表示玩法正确，本地导出不表示 Steam 在线上传成功。项目级 Unity 验证只用已打开的正式 Editor，不启动第二个 Editor，不打开 `Temp/PlayerBuildProject`。
