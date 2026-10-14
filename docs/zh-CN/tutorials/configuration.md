# 维护配置默认值与旧模组兼容

[English](../../en/tutorials/configuration.md) · [Index](../README.md)

教程修订 4 · Mod API 1.8.0 · 2026-10-14


目标：声明一项有范围的整数配置，在规则与说明中读取同一个值；了解当前没有玩家 Mod 配置页或公开配置写入 API。前置：[首课](first-mod.md)，此课用于维护已有配置或准备合法默认值，不承诺玩家能在游戏里调数值。

## 1. 声明和读取分开

在现有 ModEntry.Load 内注册：

```csharp
registrar.AddConfig(new ModConfigDefinition("shield_per_stage", "进场护盾",
    ModConfigValueKind.Integer, "2", minimum: 1, maximum: 10, requiresReload: true));
```

在 StarterRelic 中替换 BaseValue：

```csharp
public override int BaseValue => ModConfig.GetInt(ModEntry.PackageId,
    "shield_per_stage", fallback: 2, minimum: 1, maximum: 10);
```

原有 Describe 和 OnStageEntered 都读取 BaseValue，无需再维护另一份 2。两处需 `using MiniHero.ModApi;`，声明、读取回退及描述公式同步。当前宿主解析有注册项时优先用合法历史保存值，否则用定义默认值；无宿主 resolver 时 ModConfig 使用调用者 fallback。不能只改 fallback 就假定宿主默认也变了。

## 2. 配置类型和保存值

Toggle、Integer、Decimal、Choice、Text 是定义类型；不是已经有五种玩家控件。Integer/Decimal 的读取函数允许显式范围钳制，解析失败回退。Choice 读取用 `GetChoice` 和允许列表，例如 `default`、`weighted`；翻译显示标签，保留保存值。调用者 fallback 本身必须在允许列表中，函数不会替你合法化这个参数。

`RequiresReload` 是定义元数据，不会让 DLL 热卸载。修改代码后仍须完整重启。Mod 不能调用 ConfigureResolver 或通过私有文件写设置，自定义页面也没有 SetConfig 方法。

## 3. 双语和验收

实际发布时 displayName/description 用 ModText 查同一键，保持默认 2、范围 1～10、需重载相同。先在无旧保存值环境核对一级 2、二级 4 的描述与执行；有授权的历史配置环境再核对合法值和非法值回退。未提供该环境时明确未验证，不手改用户存档制造测试结果。

把默认从 2 改到 3 时，同时改定义 defaultValue、调用 fallback、两语言说明和版本；无历史保存值的新局应该一级 3。合法历史保存值仍可能优先于新默认，不能把这误判成编译没生效。诊断与其它兼容限制见[兼容页](../reference/compatibility.md)。
