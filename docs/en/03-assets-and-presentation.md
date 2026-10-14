# 03 Assets and presentation

[简体中文](../zh-CN/03-assets-and-presentation.md) · [Guide index](README.md)

Guide revision 5 · Mod API 1.8.0 · 2026-10-14

This manual groups fields and rules by system. For guided steps, [add artwork and text to a working mod](tutorials/assets-and-text.md), then return here when you need a reference.

This chapter explains artwork bindings, stage music, localization, and compatibility configuration.

## Contents

1. Artwork folders, formats, and names
2. Presentation slots and code
3. Asset validation during builds
4. Stage music in C# mods
5. Music fallback and current limits
6. Localized text
7. Configuration parameters

## 1. Artwork folders, formats, and names

```text
assets/icons/         Treasure, move, and intent icons
assets/portraits/     Character art, avatars, enemy battle art
assets/backgrounds/   Stage backgrounds, map thumbnails, arrival art
assets/_inbox/        Temporary import area, excluded from builds
```

PNG, JPG, and JPEG are supported, up to 8192 pixels on either side. Use PNG for transparency. Square icons should have a safe margin; keep characters and enemies away from image edges, and match backgrounds to the game's frame.

| Use | Slot/folder | Suggested proportion and size |
| --- | --- | --- |
| Main character art in selection and battle | `Icon` / `assets/icons` | 284×512 (71:128); provide a separate workshop cover |
| Character battle avatar | `Avatar` / `assets/portraits` | 1:1, such as 1024×1024; used for the small selection avatar and status-bar crop |
| Character portrait compatibility slot | `Portrait` / `assets/portraits` | Optional; 284×512 like `Icon`, for older UI or status displays |
| Enemy battle art | `BattleArt` / `assets/portraits` | 1:1, preferably 512×512 or 1024×1024 |
| Treasure, move, and intent icons | `Icon`, `IntentIcon` / `assets/icons` | 1:1, preferably 512×512 or larger |
| Stage background | `StageBackground` / `assets/backgrounds` | 16:9, such as 1672×941 |

![Artwork proportions](../../images/asset-dimensions.svg)

The diagram shows proportions and pixel specifications. Check cropping and transparent margins in the game.

For several generated enemies or icons, a 3×2 sheet can be sliced into six square files. Keep the sheet in `art-source` or `assets/_inbox`; bind only individual sliced images to `BattleArt` or `Icon`. Slice equal cells using an image tool, then check margins, cell separation, and that every result is a valid PNG.

Use lowercase English letters, digits, and hyphens in filenames, such as `amber-lantern.png`. Match path casing exactly. Renaming an extension does not convert the image format.

## 2. Presentation slots and code

Implement `IModPresentationContent` on the content class and return the relevant slots.

Treasure or move icon:

```csharp
public ModPresentation Presentation =>
    ModAssets.Icon("assets/icons/amber-lantern.png");
```

Main character art and avatar:

```csharp
public ModPresentation Presentation => ModAssets.Create(
    (ModPresentationSlot.Icon, "assets/icons/lantern-ranger-icon.png"),
    (ModPresentationSlot.Avatar, "assets/portraits/lantern-ranger-avatar.png"),
    (ModPresentationSlot.Portrait, "assets/portraits/lantern-ranger-portrait.png"));
```

To reuse the main art as a compatibility portrait, point `Icon` and `Portrait` at the same file:

```csharp
public ModPresentation Presentation => ModAssets.Create(
    (ModPresentationSlot.Icon, "assets/icons/mossfire-hunter.png"),
    (ModPresentationSlot.Portrait, "assets/icons/mossfire-hunter.png"),
    (ModPresentationSlot.Avatar, "assets/portraits/mossfire-hunter-avatar.png"));
```

Enemy battle art:

```csharp
public ModPresentation Presentation =>
    ModAssets.Enemy("assets/portraits/moss-wolf.png");
```

Stage background, map thumbnail, and arrival art:

```csharp
public ModPresentation Presentation => ModAssets.Stage(
    "assets/backgrounds/lantern-trail.png",
    "assets/backgrounds/lantern-map.png",
    "assets/backgrounds/lantern-arrival.png");
```

Match slots to folders. Use `icons` for `Icon/IntentIcon`, normally `portraits` for `Portrait/Avatar/BattleArt`, and `backgrounds` for the three stage slots. The compatibility loader also accepts a `Portrait` path that refers to an imported Icon in `icons`.

Character selection and the main character display in battle read `Icon`. Binding only `Portrait` may leave the main art missing. `Portrait` is an optional fallback. If both slots share art, bind both to the same `assets/icons/...png` and import it once rather than duplicating it. Use the tall 284×512 frame for main art and a separate square `Avatar`. Paths must stay inside the package; absolute paths and `../` are forbidden.

## 3. Asset validation during builds

**Build and Install** checks image headers, true format, dimensions, file size, and decoding, and generates `assets/asset-index.json`. Do not edit the index manually.

For a missing image, check its standard folder, path casing, presentation interface, rebuild status, generated index, slot/folder match, and whether an image viewer can open the file.

## 4. Stage music in C# mods

A C# mod can register music themes for its stages. Put files in the package:

```text
music/lantern-explore.ogg
music/lantern-boss.ogg
```

Only package-local `.ogg` and `.wav` files are accepted. OGG is preferable for long tracks because WAV files are larger. Use paths relative to the package root.

Register the theme:

```csharp
using System.Collections.Generic;
using MiniHero.ModApi;

public static class MusicIds
{
    public const string LanternTheme =
        ModEntry.PackageId + ".music.lantern_trail";
}

public override void Load(IModRegistrar registrar)
{
    registrar.AddMusicTheme(new ModMusicTheme(
        MusicIds.LanternTheme,
        new Dictionary<ModMusicCue, string>
        {
            [ModMusicCue.StageExplore] = "music/lantern-explore.ogg",
            [ModMusicCue.BossBattle] = "music/lantern-boss.ogg"
        }));

    registrar.AddContent(new LanternTrailStage());
}
```

The theme ID must begin with the package ID and a dot and must be unique. Reference it in the stage definition:

```csharp
return new StageDefinition
{
    id = Id,
    name = Name,
    subtitle = Subtitle,
    music = MusicIds.LanternTheme,
    boss = false,
    // Other stage fields...
};
```

Set `boss = true` for a boss stage.

## 5. Music fallback and current limits

Two stage cues are currently connected:

- `StageExplore`: ordinary stages. A missing or failed mod track falls back to the game's built-in in-game playlist.
- `BossBattle`: boss stages. A missing or failed boss track first falls back to the same theme's `StageExplore`, then to the built-in playlist if that also fails or is absent.

An ordinary stage referencing a theme that defines only `BossBattle` uses the built-in playlist; it does not select the boss track. If that playlist has no playable track, the controller logs a warning. Failed decoding or audio requests follow the same fallback and also log a read failure.

The current expanded battle stage's `StageDefinition.boss` selects the cue. In an adventure, it is generated from `AdventureStepDefinition.boss` and the round. An enemy's `CardState.isBoss` marks its card and does not independently switch music. A boss step usually also needs a generatable boss card; see [Content creation](02-content-creation.md).

A custom Mod screen can specify a theme through the `ModScreenDefinition` constructor's `musicThemeId` argument. The host uses that theme's `MainMenu` track while the screen is open and restores ordinary menu music on closing. This is separate from stage music: setting a stage's `music` does not replace the original main menu. `Victory` remains unconnected as a mod victory-screen cue.

Playback respects global music volume. The game's `BackgroundMusicController` also has stage-theme enablement and relative mod-music volume parameters.

Diagnostics:

- `MH_MOD_MUSIC_ID`: duplicate theme ID or an ID outside the package namespace.
- `MH_MOD_MUSIC_ASSET`: missing file, path outside the package, or a format other than OGG/WAV.
- Unknown stage theme: the registered ID differs from `StageDefinition.music`.
- Old music after an edit: rebuild, install, and reload; fully restart if necessary to clear the audio cache.

## 6. Localized text

Use a stable key and readable fallback:

```csharp
public override string Name => ModText.Get(
    ModEntry.PackageId,
    "treasure.amber_lantern.name",
    "Amber Lantern");

public override string Describe(int level) => ModText.Format(
    ModEntry.PackageId,
    "treasure.amber_lantern.description",
    "Gain {0} shield when entering a stage.",
    BaseValue * level);
```

Corresponding `localization/zh-Hans.json`:

This is a display-text catalog. The treasure's trigger and shield formula remain in its C# class.

```json
{
  "locale": "zh-Hans",
  "entries": [
    { "key": "treasure.amber_lantern.name", "value": "琥珀提灯" },
    { "key": "treasure.amber_lantern.description", "value": "进入场景时获得 {0} 点护盾。" }
  ]
}
```

The third argument is fallback text when a translation cannot be found. Add `localization/en.json` and add `en` to `package.json.supportedLocales` for English. Keep keys and placeholders unchanged; translate their values.

The English entries for the same keys are below. Merge these entries without replacing existing translations:

```json
{
  "locale": "en",
  "entries": [
    { "key": "treasure.amber_lantern.name", "value": "Amber Lantern" },
    { "key": "treasure.amber_lantern.description", "value": "Gain {0} shield when entering a stage." }
  ]
}
```

## 7. Configuration compatibility

There is no player Mod configuration page. `AddConfig/ModConfig` remains for compatibility; see [Compatibility](reference/compatibility.md) for fields and limits. New authors can use source defaults without configuration fragments.
