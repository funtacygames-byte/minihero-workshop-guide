# Compatibility APIs and unwired behavior

[简体中文](../../zh-CN/reference/compatibility.md) · [Index](../README.md)

Guide revision 2 · Mod API 1.8.0 · 2026-10-13

Baseline: 1.8.0. Use this page to maintain older mods and inspect limits. These features are not prerequisites for a first mod.

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

There is no player Mod configuration page or existing player UI that writes these settings. Reads can use saved historical values or fallbacks. Design a new package around its fallback defaults without promising editable sliders, Choice, or text. Do not modify game configuration files yourself.

Keep stable Choice values such as `default` and `weighted`. `choiceDisplayNames` supplies translated labels in the same order without translating stored values. GetChoice validates saved values against the allowed list. Supply a fallback that is itself in that list; the API does not validate the fallback for you. See [API surface](api-surface.md) for full constructors.

Older Wayfarer's Relic scaffolds described `level * 2` while reading `shield_per_stage` during execution, allowing a mismatch after configuration changes. The locally revised generator and first lesson share BaseValue and move configuration out of the starting path. Existing source projects are not automatically rewritten; follow the first lesson or maintain their compatibility yourself.

## Declaration versus active behavior

| API/field | Current boundary | Available approach |
| --- | --- | --- |
| StartingTreasureTypes | Stored/validated at selection, not granted | Explicit encounter reward |
| Later StartingMoveTypes entries | Not equipped in ordinary slots | Declare one initial move |
| Victory music cue | Not connected to mod victory pages | Verify wired StageExplore/BossBattle cues |
| Structured JSON editing | Backend compatibility, no player JSON editor | C# Sources workflow |
| Same-process DLL reload | No true hot unload | Fully exit and restart for final checks |

JSON and codeAssembly can merge into one registry; avoid duplicate IDs. Backend StageGraph, rich choices, and conditions remain in the [content overview](../02-content-creation.md). A backend format does not imply a player editing menu.

## Update evidence

Read [Versions](versions.md), then check used members against current game references. Display-text changes do not migrate stable IDs or keys. Rebuild changes from Sources. Record prior package version/hash, save compatibility, and untested cases.
