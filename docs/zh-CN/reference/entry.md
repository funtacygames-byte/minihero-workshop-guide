# Mod 入口与内容注册

[English](../../en/reference/entry.md) · [目录](../README.md)

教程修订 2 · Mod API 1.8.0 · 2026-10-13

用途：从包清单定位一个公开入口，注册内容定义、展示和音乐。本文按当前 1.8.0 核对；跨版本最低要求查[版本页](versions.md)，公开声明见[API 表面](api-surface.md)。

## 清单与源码契约

| 项目 | 必须对应 | 失败表现 |
| --- | --- | --- |
| `packageId` | 源目录 ID、入口 `[MiniHeroMod(...)]` | `MH_MODSOURCE_ID_MISMATCH` 或 `MH_MOD_PACKAGE_ID_MISMATCH` |
| `codeAssembly` | 本包真正输出 DLL 的相对路径 | `MH_MOD_ASSEMBLY_MISSING` |
| `codeEntryPoint` | 含命名空间的 `ModEntry` 类型名 | `MH_MOD_ENTRYPOINT_MISSING` |
| `modApiVersion` | 实际用到的 API 版本 | `MH_MOD_API_INCOMPATIBLE` |
| `permissions` | C# 包含 `code.execute` | 需要代码权限与信任确认 |

例如包 ID `local.alice.lantern-trail` 生成命名空间 `LocalAliceLanternTrailMod`，清单入口是 `LocalAliceLanternTrailMod.ModEntry`。加载器在清单入口非空时按完整类型名精确匹配，并核对入口特性的包 ID。不是只要继承 `MiniHeroMod` 就会加载。

## 入口与注册器签名

```csharp
public abstract class MiniHeroMod
{
    public abstract void Load(IModRegistrar registrar);
}

public interface IModRegistrar
{
    string PackageId { get; }
    string PackageRoot { get; }
    void AddContent(IGameContent content);
    void AddCharacterToLevel(string levelId, string characterId, int difficulty = 0);
    void AddMusicTheme(ModMusicTheme theme);
    void AddConfig(ModConfigDefinition definition);
    void AddStartScreen(ModStartScreenDefinition definition);
    void AddScreen(ModScreenDefinition definition);
}
```

这是接口声明摘录，不是需要复制进模组的类。`Load` 在建立内容快照时执行，注册静态定义；构建源码本身不会执行 Mod DLL。入口必须 `public`、非抽象、带唯一正确标记并有公开无参构造函数。

`AddContent` 返回 `void`，拒绝信息由宿主汇总到加载诊断。允许角色、角色特性、宝物、招式、敌人/特性、道具、事件、Stage、Adventure、规则和展示内容。类必须属于本包程序集，内容 ID 以本包 ID 加 `.` 开头；全局合并仍检查重复 ID。所有被引用内容都必须注册。

`AddContents(this IModRegistrar registrar, params IGameContent[] contents)` 是扩展方法，需要 `using MiniHero.ModApi;`。它依次调用 `AddContent`，并不自动扫描所有类或补齐依赖。建议按特性、招式、宝物、角色、敌人特性、敌人、道具/事件、Stage、Adventure 排列，便于人工核对。

## 角色加入大关卡

`AddCharacterToLevel` 自 1.7.0 可用。`levelId` 是关卡选择页的大关卡稳定 ID，例如 `challenge_wild_corruption_nest`；`characterId` 是已注册的本包角色。`difficulty = 0` 表示该关卡所有难度，其他值只加入对应难度，不覆盖原角色名单。

`Stage.allowedCharacterIds` 仍需允许该角色，或为空表示该素材不限角色。把角色加到 Adventure 入口，不等于清除素材的限制。

## 生命周期和最小用法

在 `Load` 中只注册，不保存当前 `GameState`，也不做玩家发奖。实例规则在运行事件中执行，见[生命周期](lifecycle.md)。最小可构建入口和全部整合步骤见[首课](../tutorials/first-mod.md)。图片注册会验证路径与槽位；缺素材时不能只靠编译通过判断加载成功。
