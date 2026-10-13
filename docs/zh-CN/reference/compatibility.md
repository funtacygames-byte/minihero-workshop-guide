# 兼容接口与暂未接通的行为

[English](../../en/reference/compatibility.md) · [目录](../README.md)

教程修订 2 · Mod API 1.8.0 · 2026-10-13

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

当前无玩家 Mod 配置页，也无现有玩家界面写入设置。读取可以使用历史保存值或回退值；新包按回退值设计实际默认行为，不承诺玩家能调滑块、Choice 或文本。不要自行修改游戏配置文件。

旧配置中保留稳定 Choice values，例如 `default`、`weighted`。`choiceDisplayNames` 按同序提供翻译标签，不能把保存值翻译掉；GetChoice 按允许列表校验保存值；调用方应保证回退值本身也在列表中，接口不会替你校验回退值。完整构造函数查[API 表面](api-surface.md)。

早期旅者遗物脚手架描述写 `level * 2`，执行读 `shield_per_stage`，配置变化时可能不一致。本地修订的生成器与首课共用 BaseValue 公式，并把配置移出起点。已有源项目不会自动被改写；按首课统一或自行维护兼容。

## 已声明不等于已发放或已播放

| 接口／字段 | 当前边界 | 可用替代 |
| --- | --- | --- |
| StartingTreasureTypes | 选角只登记校验，不发奖 | 明确奇遇奖励 |
| StartingMoveTypes 后续项 | 不自动装进普通槽 | 首课只声明一个初始招式 |
| Victory 音乐 cue | 未接 Mod 胜利页 | 只验已接通的 StageExplore/BossBattle |
| 结构化 JSON 编辑 | 后端兼容，无玩家 JSON 编辑器 | C# Sources 流程 |
| DLL 同进程重载 | 不支持真正热卸载 | 最终完整退出并重启 |

JSON 仍可能与 codeAssembly 合并注册，避免重复 ID。StageGraph、富事件与条件等后端格式放在[内容总览](../02-content-creation.md)；不能把后端文件存在写成玩家有编辑菜单。

## 更新时保留证据

先查看[版本页](versions.md)，核对实际使用的接口和当前游戏引用。稳定 ID 与键不随文案更新迁移。源码改动从 Sources 重建；记录旧包版本、哈希、存档验证和未覆盖场景。
