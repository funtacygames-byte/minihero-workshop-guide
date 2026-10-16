# 01 工程与构建

[English](../en/01-project-and-build.md) · [教程目录](README.md)

教程修订 5 · 核对日期：2026-10-14 · Mod API：1.8.0。

这篇按系统查字段和规则。想一步步操作，先[跟着教程：创建并修改第一个模组](tutorials/first-mod.md)；做完后再回来查需要的部分。

本篇从第一次点击“新建 C# 项目”讲到 Mod 在游戏中运行。它解释界面字段、C# 工程结构、开发环境、构建与安装的区别、哈希的意义以及 C# Mod 的信任边界。

## 作者实际编写哪些文件？

宝物设计使用 C#：实现 `TreasureContent` 子类，在 `Load` 注册，再由工坊编译。这条路线不要求提交 JSON 宝物定义。

| 文件 | 作者的操作 |
| --- | --- |
| `source/*.cs` | 编写行为、公式、触发与状态；这是玩法源码 |
| 自动生成的 `source/*.csproj` | 保留目标框架与游戏引用设置 |
| 自动生成的 `package.json` | 维护版本、预览路径等包信息；不在这里实现宝物行为 |
| `localization/*.json` | 用稳定键翻译显示值；属于辅助文字数据 |
| 构建后的 `mod/*.dll` | 工坊发布包使用的编译产物；不手写或直接修改 |

构建安装与发布准备会把 DLL、所需包信息、文本和素材一起打包。最小 C# 示例见[首课](tutorials/first-mod.md)，宝物规则继续看[宝物课](tutorials/treasure.md)。

## 目录

1. 新建项目时填写什么
2. 从新建到游戏内验证
3. 一个 C# Mod 的代码结构
4. 项目目录分别做什么
5. 开发环境如何工作
6. 构建、安装、启用和重载
7. 哈希、签名与信任
8. 第一次项目的推荐做法

## 一、新建项目时填写什么

开发页不常驻显示项目配置。点击“新建 C# 项目…”后，创建窗只会在首次生成脚手架时收集三个值：

- 包 ID：稳定的技术名称，例如 `local.alice.lantern-trail`。只使用小写英文、数字、点、连字符或下划线。发布后不要更换，否则存档和其他 Mod 的引用都会把它视作另一份内容。
- 显示名称：玩家看到的名字，例如“提灯之旅”。可以使用中文，之后还能通过本地化更换。
- 作者：显示在详情和信任确认中。目前它只是包作者自己填写的声明，不是经过平台认证的身份。

创建后，作者、版本和其他包信息以项目根目录的 `package.json` 为准；显示名称的实际文字保存在 `localization` 中。包 ID 还会写入目录名、C# 入口和内容 ID 命名空间，因此它不是只改 `package.json` 就能安全替换的普通文案。

模板不放在新建界面里。开发页先生成统一、干净的 C# 工程；创建后再从教程的 [功能片段](../../templates/README.zh-CN.md) 选择宝物、角色、敌人、关卡或音乐片段。这种方式不会让一个简单宝物项目携带大量无用示例代码。

## 二、从新建到游戏内验证

1. 打开冒险工坊 → 开发模组。
2. 点击“新建 C# 项目…”，在一次性创建窗中填写包 ID、显示名称和作者，然后创建。
3. 在项目列表选中它，点击“打开源码”。
4. 编辑 `source/ModEntry.cs`，保存源码。
5. 图片放入 `assets`，音乐放入 `music`，多语言文本放入 `localization`。
6. 回到开发页点击“构建并安装”。
7. 确认模组已启用，完整退出并重启游戏后再验收 C# 内容。“构建后重载”可更新内容快照，但不能证明已加载的 DLL 被替换。
8. 在宝物图鉴选择全部角色并搜索旅者遗物，确认加载；再用固定关卡验证实际效果。

第一次不要同时制作十种内容。先注册一个进场加护盾的最小宝物，确认编译、安装和重载链路都通，再逐步加入角色和关卡。这样出错时能快速判断是哪一步造成的。

## 三、一个 C# Mod 的代码结构

```csharp
using System.Collections.Generic;
using MiniAdventureWorld.Core;
using MiniHero.ModApi;

namespace LocalAliceLanternTrailMod
{
    [MiniHeroMod(ModEntry.PackageId)]
    public sealed class ModEntry : MiniHeroMod
    {
        public const string PackageId = "local.alice.lantern-trail";

        public override void Load(IModRegistrar registrar)
        {
            registrar.AddContent(new StarterRelic());
        }
    }

    [System.Serializable]
    public sealed class StarterRelic : TreasureContent
    {
        public StarterRelic() : base(ModEntry.PackageId + ".treasure.starter_relic") { }
        public override string Name => ModText.Get(
            ModEntry.PackageId, "content.starter_relic.name", "旅者遗物");
        public override TreasureRank Rank => TreasureRank.Common;
        public override int BaseValue => 2;
        public override IReadOnlyList<string> CategoryTags => new[] { TreasureCategoryTags.Shield };
        public override IReadOnlyList<string> PoolTags => new[] { CharacterTreasurePoolTags.HealingLifeBuild };
        public override string Describe(int level) => ModText.Format(
            ModEntry.PackageId, "content.starter_relic.description",
            "进入场景时获得 {0} 点护盾。", BaseValue * level);
        public override void OnStageEntered(StageEnteredEvent e)
        {
            e?.Runtime?.AddShield(BaseValue * e.SourceLevel);
        }
    }
}
```

逐项解释：

- `using` 让源码能使用游戏 Core 和 Mod API 中公开的类型。
- `namespace` 必须与清单 `codeEntryPoint` 的类型命名空间对应。本课 ID 生成 `LocalAliceLanternTrailMod`；其他 ID 保留各自生成值。
- `[MiniHeroMod(...)]` 标记唯一入口；这里的 ID、`package.json` 的 `packageId` 必须完全一致。
- `Load` 在建立内容快照时调用，负责注册内容、音乐和配置。不要在这里缓存某一局的 `GameState`。
- 内容类必须是 `public`，必须可以实例化，并且有公开无参构造函数。
- `base(...)` 接收稳定内容 ID。每个内容 ID 都必须以 `packageId + "."` 开头。
- `override` 表示替换基类定义的名称、数值或事件行为。
- `=>` 是返回简单值的短写；`new[] { ... }` 是列表；`typeof(MyTrait)` 取得内容类型；`?.` 在对象为空时停止调用；`$"{value}"` 将数值插入文字。

`Load` 的推荐排列是：角色特性 → 技能 → 宝物 → 角色 → 敌人特性 → 敌人 → 道具/奇遇 → 关卡。解析主要依赖稳定 ID 和类型，不要求严格先后，但固定顺序便于检查。

这件宝物进入生命构筑池。测试宝箱抽取时使用池标签匹配的角色，例如林地药师（`grove_alchemist`）；只注册宝物不会让所有角色都能抽到它。

## 四、项目目录分别做什么

```text
Sources/<packageId>/
├─ package.json                 包 ID、版本、入口、DLL 和 API 版本
├─ README.md                    项目说明
├─ source/                      你编辑的 C# 源码和 csproj
├─ localization/                zh-Hans.json、en.json 等文本
├─ assets/
│  ├─ icons/                    宝物、技能、意图图标
│  ├─ portraits/                角色、头像、敌人战斗图
│  ├─ backgrounds/              关卡背景、地图缩略图、抵达图
│  ├─ _inbox/                   临时导入区，不进入构建
│  └─ asset-index.json          构建自动生成，不要手改
├─ music/                       OGG 或 WAV 关卡音乐
├─ mod/                         构建生成的你自己的 DLL
├─ .tmode-sdk/               自动维护的开发引用，不进入包
└─ .snapshots/                  构建前的源项目快照
```

工坊还有三个区域：

- `Sources` 是工作区，允许修改。
- `Builds` 是成功构建的不可编辑快照。
- `Installed` 是游戏实际安装的版本。

正确链路永远是 `Sources → Build → Install`。不要为了修一个数字直接改 `Builds` 或 `Installed`；应修改 Sources，并在安装内容变更前递增 `package.json.version`，再构建安装。

## 五、开发环境如何工作

“开发环境”只有三部分：

1. 代码编辑器：Visual Studio、Rider 或 VS Code，任选其一，只负责编辑 `.cs`。
2. `.NET SDK`：负责把 C# 编译成 DLL。冒险工坊会执行 `dotnet build`；先在终端用 `dotnet --version` 确认本机可调用。
3. 游戏开发引用：`MiniHero.ModApi.dll` 与 `MiniAdventureWorld.Core.dll`。

不需要 Unity、本游戏的完整工程或开发者源码。只有游戏成品的玩家，也可以先在“开发模组”中创建项目，再让 Codex 或其他能读写本地文件的 AI 工具打开 `Sources/<packageId>` 目录。AI 工具应先阅读项目 `README.md`、工坊教程和功能模板，并且只修改这个源项目；最终构建仍由冒险工坊调用本机 `.NET SDK` 完成。

新建项目时，冒险工坊自动把代码提示和命令行编译需要的引用放进开发引用目录。正式构建时又会传入当前游戏程序集的实际路径，所以你不需要在 UI 手填 SDK 或 DLL 地址。

不要把两个游戏引用复制到 `mod/`。`mod/` 只放你自己的 DLL；运行时由游戏提供 API/Core。游戏更新后再次构建，开发引用目录会自动刷新。

若构建报告 `MH_MODSOURCE_DOTNET`，或不确定 SDK 是否可调用，先在终端执行：

```powershell
dotnet --version
```

没有版本输出时安装 `.NET SDK` 后重新进入开发页。如果游戏能构建，但代码编辑器仍标红，先核对编辑器打开的是当前 source 项目，以及 csproj 的引用路径和 `.tmode-sdk` 中两份 DLL 是否存在。游戏更新后重新构建可刷新引用；若刷新报告文件被占用，关闭占用程序再重试。不要把所有编辑器提示都归因于文件锁。

## 六、构建、安装、启用和重载

“构建并安装”依次执行：

1. 扫描并验证图片等素材。
2. 调用 `dotnet build`。
3. 检查包清单、入口、DLL 和 API 版本。
4. 复制允许发布的文件，排除 `bin/obj/开发引用目录/_inbox` 等开发内容。
5. 计算内容哈希并写入 `content.hashes.json`。
6. 写入构建报告。
7. 校验复制结果后安装。

中途失败不会用半成品覆盖上一次成功构建或已安装版本。本地开发页自己构建的项目可以直接安装启用；从仓库取得的 C# Mod 在管理页启用时需要确认信任。

重载会重建内容快照，但运行中的 .NET 程序集通常无法真正卸载。只改文本或图片时重载一般足够；修改已加载的 C# 逻辑后，完整退出并重启才能确定运行的是新 DLL。

## 七、哈希、签名与信任

构建哈希是所有可发布文件内容的 SHA-256 汇总。构建时记录，安装前重新计算，可以发现：

- 下载不完整或复制损坏；
- 杀毒软件隔离了 DLL；
- 图片、配置或 DLL 在构建后被直接修改；
- 同名构建缓存实际上不是同一份内容。

哈希只回答“文件有没有变”，不回答“作者是谁”。能修改包的人也能重新生成哈希，因此它不是数字签名。当前冒险工坊尚未提供证书签名或线上作者认证。

旧游戏版本中的 C# Mod 以游戏进程权限运行。Windows 沙箱实现及其发行状态见 [C# 模组隔离](reference/security.md)。信任确认显示包 ID、作者、版本和内容哈希；信任记录绑定精确哈希，任何文件变化都会要求重新确认。作者字段只是声明，不应单独作为安全依据。

常见提示：

- `AW_BUILD_HASH_MISSING`：没有构建清单，回到 Sources 重新构建。
- `AW_BUILD_HASH_MISMATCH`：构建后出现修改、缺失或新增文件。
- `AW_BUILD_CACHE_REPAIRED`：损坏缓存已移到 Trash，并自动重建。
- `MH_MODSOURCE_DOTNET`：无法启动 dotnet，检查 SDK。
- `MH_MODSOURCE_BUILD`：C# 编译失败，查看输出中的文件名和行号。

## 八、第一次项目的推荐做法

保留自动生成的 `package.json` 和 `.csproj`，只修改 `ModEntry.cs`。完成最小宝物后依次验证：构建成功、浏览页可见、安装成功、管理页已启用、重载后内容出现、效果数值与描述一致。确认这一条链路后，再阅读《02 内容制作》扩展其他内容。
