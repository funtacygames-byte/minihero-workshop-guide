# Compatibility APIs and unwired behavior

[简体中文](../../zh-CN/reference/compatibility.md) · [Index](../README.md)

Guide revision 6 · Mod API 1.10.0 · 2026-10-17

Baseline: 1.10.0. Use this page to maintain older mods and inspect limits. These features are not prerequisites for a first mod.

## Configuration API

`IModRegistrar.AddConfig(ModConfigDefinition definition)` declares and validates settings. Read signatures:

```csharp
public static string Get(string packageId, string id, string fallback = "");
public static bool GetBool(string packageId, string id, bool fallback = false);
public static int GetInt(string packageId, string id, int fallback = 0,
    int minimum = int.MinValue, int maximum = int.MaxValue);
public static double GetDecimal(string packageId, string id, double fallback = 0d,
    double minimum = double.MinValue, double maximum = double.MaxValue);
```

There is no player Mod configuration page or existing player UI that writes these settings. With a registered definition, the host prefers a valid historical value, otherwise its DefaultValue. Without a host resolver, the getter uses the caller fallback. Keep both defaults aligned without promising editable sliders, Choice, or text. Do not modify game configuration files yourself.

Keep stable Choice values such as `default` and `weighted`. `choiceDisplayNames` supplies translated labels in the same order without translating stored values. GetChoice validates saved values against the allowed list. Supply a fallback that is itself in that list; the API does not validate the fallback for you. See [API surface](api-surface.md) for full constructors.

Older Wayfarer's Relic scaffolds described `level * 2` while reading `shield_per_stage` during execution, allowing a mismatch after configuration changes. The current first lesson shares `BaseValue` between description and effect, and changes that value directly. Existing source projects are not automatically rewritten; follow the first lesson or maintain their compatibility yourself.

## Declaration versus active behavior

| API/field | Current boundary | Available approach |
| --- | --- | --- |
| StartingTreasureTypes | Stored/validated at selection, not granted | Explicit encounter reward |
| Later StartingMoveTypes entries | Not equipped in ordinary slots | Declare one initial move |
| Victory music cue | Not connected to mod victory pages | Verify wired StageExplore/BossBattle cues |
| Same-process DLL reload | No true hot unload | Fully exit and restart for final checks |

Create gameplay in C# Sources. Historical declarative package readers remain implementation details for compatibility; they are not the player authoring route. C# graph routes and legacy rich choices are documented in the [content overview](../02-content-creation.md). Package metadata and translation catalogs remain auxiliary data.

## Update evidence

Read [Versions](versions.md), then check used members against current game references. Display-text changes do not migrate stable IDs or keys. Rebuild changes from Sources. Record prior package version/hash, save compatibility, and untested cases.

Integer/decimal getters clamp successfully parsed values to caller bounds. Parsing failure returns fallback directly; the caller must keep that fallback valid. Follow the [configuration lesson](../tutorials/configuration.md).
