# Maintain defaults in a mod with older configuration code

[简体中文](../../zh-CN/tutorials/configuration.md) · [Index](../README.md)

This page is for authors working with existing `AddConfig` code. **To change the starter treasure's value, edit `BaseValue` in [the first lesson](first-mod.md) and skip this page.** The game currently has no player-facing mod configuration menu.

The example defines an integer with a default of 2 and a range of 1–10, then uses the same setting for the treasure's description and effect. You need the first lesson's `source/ModEntry.cs`: register the setting inside `Load` and read it inside `StarterRelic`.

## 1. Separate declaration from reading

Register in the existing ModEntry.Load:

```csharp
registrar.AddConfig(new ModConfigDefinition("shield_per_stage", "Stage-entry shield",
    ModConfigValueKind.Integer, "2", minimum: 1, maximum: 10, requiresReload: true));
```

Replace BaseValue in StarterRelic:

```csharp
public override int BaseValue => ModConfig.GetInt(ModEntry.PackageId,
    "shield_per_stage", fallback: 2, minimum: 1, maximum: 10);
```

Describe and OnStageEntered already read BaseValue, avoiding a second hardcoded 2. Both locations need `using MiniHero.ModApi;`. Keep declaration, read fallback and description formula aligned. With a registered definition, the current host uses a valid historical stored value or the definition default. Without a host resolver, ModConfig uses the caller's fallback. Changing only fallback does not change the host definition's default.

## 2. Types and stored values

Toggle, Integer, Decimal, Choice and Text are definition kinds, not five available player controls. Integer/Decimal getters can clamp to explicit bounds and fall back on parsing failure. Choice uses `GetChoice` and an allowed list, such as `default` and `weighted`. Translate labels, preserving stored values. The caller's fallback must itself be allowed; the function does not validate that argument for you.

`RequiresReload` is metadata, not DLL unloading. Code changes still require a full restart. Mods must not call ConfigureResolver or write private settings files; custom pages have no SetConfig method.

## 3. Check defaults and descriptions

For release, resolve displayName/description with ModText keys, keeping default 2, bounds 1–10 and reload requirement identical. In an environment with no stored value, check level-one 2 and level-two 4 in both description and effect. If you have settings saved by an older version of your mod, check how those values are read. Without old settings, start by learning the defaults. You do not need to edit a save file for this step.

When changing default 2 to 3, update definition defaultValue, caller fallback, both descriptions and version. A fresh run with no stored value should show level-one 3. A valid historical setting may still override the new default; that alone does not mean compilation failed. See the [compatibility page](../reference/compatibility.md) for diagnostics and other limits.
