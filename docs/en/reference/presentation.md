# Presentation, text, and music APIs

[简体中文](../../zh-CN/reference/presentation.md) · [Index](../README.md)

Guide revision 4 · Mod API 1.8.0 · 2026-10-13

Baseline: 1.8.0. See [Assets and bilingual text](../tutorials/assets-and-text.md) for steps and the [asset overview](../03-assets-and-presentation.md) for full slot specifications.

## Image signatures and slots

```csharp
public interface IModPresentationContent
{
    ModPresentation Presentation { get; }
}
public static ModPresentation Icon(string path);
public static ModPresentation Character(string portrait, string avatar = "");
public static ModPresentation Enemy(string battleArt, string icon = "", string intentIcon = "");
public static ModPresentation Stage(string background, string mapThumbnail = "", string arrivalArt = "");
public static ModPresentation Create(params (ModPresentationSlot slot, string path)[] assets);
```

These are reference declarations for the interface and `ModAssets` factories. Factories return mappings without loading images themselves. `Character` uses the compatibility Portrait/Avatar slots. Explicitly bind current character main art to `Icon` with `Create`, as in the character fragment. Paths are package-relative and indexed at build time. Empty optional paths are skipped; nonempty paths must exist and match slot kinds.

| Slot | Specification/purpose |
| --- | --- |
| Treasure/move Icon | 1:1 icon |
| Character Icon | 284×512 or 71:128 main art |
| Character Avatar | 1:1 avatar |
| Character Portrait | Compatibility fallback, preferably 71:128 |
| Enemy BattleArt | 1:1 battle art |
| StageBackground/StageMapThumbnail/StageArrivalArt | Background/selection/arrival image, cropped for the actual slot |

Correct dimensions still require checking subject safe areas in the existing layout. Do not resize UI or change fonts to compensate for translations.

## Text signatures and failure behavior

```csharp
public static string Get(string packageId, string key, string fallback = "");
public static string Format(string packageId, string key, string fallback, params object[] arguments);
```

These are `ModText` methods. Get uses the host resolver and returns fallback when no resolver is configured. Format retrieves text and uses current-culture `string.Format`; a caught format error returns the unexpanded template. Fallback text should be readable by itself without depending on an English catalog always existing.

Workshop packages use JSON `locale` and `entries[{key,value}]` in `localization/<locale>.json`, distinct from the game's internal V2 text tables. New keys use semantic ASCII identifiers. Both languages keep the same keys and placeholder IDs. Manifest `supportedLocales/defaultLocale` must match files. `ConfigureResolver` belongs to the host and should not be called by mods.

## Music contract

`ModMusicTheme(string id, IReadOnlyDictionary<ModMusicCue, string> tracks)` registers a unique theme whose ID begins with the package ID plus a dot. Tracks are package-contained OGG/WAV files. `StageDefinition.music` references a registered theme; unknown themes report `MH_MOD_STAGE_MUSIC_MISSING`.

Ordinary stages use StageExplore. Boss stages try BossBattle, then that theme's StageExplore, then the built-in in-game list. Decode failures also follow fallback. Custom screens use MainMenu through `ModScreenDefinition.MusicThemeId`; Victory is not connected to mod victory-page music. Stage boss status chooses the cue; one enemy card alone does not.

See [Compatibility](compatibility.md) for configuration limits. Registering configuration does not create a player-editable menu.
