# Mod entry and content registration

[简体中文](../../zh-CN/reference/entry.md) · [Index](../README.md)

Guide revision 5 · Mod API 1.8.0 · 2026-10-14

Purpose: locate one public entry from a package manifest and register content definitions, presentation, and music. This reference is checked against 1.8.0. See [Versions](versions.md) for compatibility and [API surface](api-surface.md) for declarations.

## Manifest-to-source contract

| Field | Must match | Failure symptom |
| --- | --- | --- |
| `packageId` | Source directory ID and entry `[MiniHeroMod(...)]` | `MH_MODSOURCE_ID_MISMATCH` or `MH_MOD_PACKAGE_ID_MISMATCH` |
| `codeAssembly` | Relative path to this mod's actual output DLL | `MH_MOD_ASSEMBLY_MISSING` |
| `codeEntryPoint` | Full `ModEntry` type name, including namespace | `MH_MOD_ENTRYPOINT_MISSING` |
| `modApiVersion` | API used by the mod | `MH_MOD_API_INCOMPATIBLE` |
| `permissions` | `code.execute` for C# | Code permission and trust confirmation required |

Package `local.alice.lantern-trail` generates namespace `LocalAliceLanternTrailMod` and entry `LocalAliceLanternTrailMod.ModEntry`. A nonempty manifest entry is matched exactly against the full type name; the loader also checks the attribute's package ID. Inheriting `MiniHeroMod` alone is insufficient.

## Entry and registrar signatures

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

These are reference declarations; do not copy the types into a mod. `Load` runs while the host builds a content snapshot and registers static definitions. Compiling source does not execute the mod DLL. The entry must be public, concrete, correctly attributed, and have a public parameterless constructor.

`AddContent` returns `void`; the host collects rejection information in loading diagnostics. Supported contents include characters, traits, treasures, moves, enemies/traits, items, encounters, stages, adventures, rules, and presentation content. Classes must belong to this mod's assembly. IDs begin with the package ID plus `.`; combined registration still rejects duplicate IDs. Register every referenced content.

`AddContents(this IModRegistrar registrar, params IGameContent[] contents)` is an extension method requiring `using MiniHero.ModApi;`. It calls `AddContent` in sequence without discovering classes or adding dependencies. A consistent order—traits, moves, treasures, characters, enemy traits, enemies, items/encounters, stages, adventures—makes reviews easier.

## Add a character to a selectable level

`AddCharacterToLevel` is available from 1.7.0. `levelId` identifies a selectable level, such as `challenge_wild_corruption_nest`; `characterId` identifies a registered character from this package. `difficulty = 0` adds it to all difficulties; another value affects only that difficulty and preserves existing characters.

Actual selection rosters use the level difficulty's `availableHeroIds`. `Stage.allowedCharacterIds` is stored and reference-validated metadata; the current C# runtime does not enforce an additional roster restriction through it.

## Lifecycle and minimal use

Register in `Load` without retaining a run's `GameState` or granting player rewards there. Runtime events perform instance rules; see [Lifecycle](lifecycle.md). The [first lesson](../tutorials/first-mod.md) provides a complete minimal entry and integration steps. Presentation registration validates paths and slots, so compilation alone cannot prove asset loading.
