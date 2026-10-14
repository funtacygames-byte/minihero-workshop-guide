# 兼容接口与暂未接通的行为

[English](../../en/reference/compatibility.md) · [目录](../README.md)

教程修订 4 · Mod API 1.8.0 · 2026-10-13

当前基准 1.8.0。本页用于维护旧模组和查边界；第一次制作不依赖这些能力。

## 配置 API

`IModRegistrar.AddConfig(ModConfigDefinition definition)` 声明并校验定义。读取签名：

```csharp
public static string Get(string packageId, string id, string fallback = "");
public static bool GetBool(string packageId, string id, bool fallback = false);
public static int GetInt(string packageId, string id, int fallback = 0,
    int minimum = int.MinValue, int maximum = int.MaxValue);
public static double GetDecimal(string packageId, string id, double fallback = 0d,
    double minimum = double.MinValue, double maximum = double.MaxValue);
```

当前无玩家 Mod 配置页，也无现有玩家界面写入设置。注册定义存在时，宿主优先读取合法历史值，否则使用定义 DefaultValue；没有宿主解析器时 getter 才使用调用方 fallback。让这两种默认保持一致，不承诺玩家能调滑块、Choice 或文本。不要自行修改游戏配置文件。

旧配置中保留稳定 Choice values，例如 `default`、`weighted`。`choiceDisplayNames` 按同序提供翻译标签，不能把保存值翻译掉；GetChoice 按允许列表校验保存值；调用方应保证回退值本身也在列表中，接口不会替你校验回退值。完整构造函数查[API 表面](api-surface.md)。

早期旅者遗物脚手架描述写 `level * 2`，执行读 `shield_per_stage`，配置变化时可能不一致。本地修订的生成器与首课共用 BaseValue 公式，并把配置移出起点。已有源项目不会自动被改写；按首课统一或自行维护兼容。

## 已声明不等于已发放或已播放

| 接口／字段 | 当前边界 | 可用替代 |
| --- | --- | --- |
| StartingTreasureTypes | 选角只登记校验，不发奖 | 明确奇遇奖励 |
| StartingMoveTypes 后续项 | 不自动装进普通槽 | 首课只声明一个初始招式 |
| Victory 音乐 cue | 未接 Mod 胜利页 | 只验已接通的 StageExplore/BossBattle |
| DLL 同进程重载 | 不支持真正热卸载 | 最终完整退出并重启 |

玩法通过 C# Sources 制作。历史声明式包读取器属于兼容实现，不作为玩家制作路线；C# 图路线与旧富事件见[内容总览](../02-content-creation.md)。包信息与翻译表仍属于辅助数据。

## 更新时保留证据

先查看[版本页](versions.md)，核对实际使用的接口和当前游戏引用。稳定 ID 与键不随文案更新迁移。源码改动从 Sources 重建；记录旧包版本、哈希、存档验证和未覆盖场景。

整数／小数 getter 对成功解析的值按传入范围钳制，解析失败直接返回 fallback；调用者须保证 fallback 本身合法。配置操作步骤见[配置课](../tutorials/configuration.md)。
