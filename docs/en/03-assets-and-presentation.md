# 03 Assets and presentation

[简体中文](../zh-CN/03-assets-and-presentation.md) · [Guide index](README.md)

Guide revision 6 · Mod API 1.10.0 · 2026-10-17

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

The loader accepts genuinely encoded PNG, JPG and JPEG files, up to 8192 pixels on either side. Those limits do not make every aspect ratio suitable for every slot. Prepare two separate character images: character main art with a complete background and a portrait with a painted background.

| Use | Slot/folder | Suggested proportion and size |
| --- | --- | --- |
| Main character art in selection | `Icon` / `assets/icons` | 71:128 tall art, 284×512 display frame; sources may be 568×1024 or larger, with a complete opaque scene background |
| Character avatar portrait | `Avatar` / `assets/portraits` | 4:5, such as 1024×1280, with a full background; the battle status bar uses 4:5 and small selection avatars use the top square |
| Character compatibility fallback | `Portrait` | Optional; may share the main `Icon` file, but does not replace a separate 4:5 `Avatar` |
| Enemy battle art | `BattleArt` / `assets/portraits` | 1:1, preferably 512×512 or 1024×1024 |
| Treasure, move, and intent icons | `Icon`, `IntentIcon` / `assets/icons` | 1:1, preferably 512×512 or larger |
| Stage background | `StageBackground` / `assets/backgrounds` | 16:9, such as 1672×941 |

![Artwork proportions](../../images/asset-dimensions.svg)

The diagram separates character main art with a complete background from the portrait with a background and its top-square crop. For a 1024×1280 portrait, the top 1024×1024 becomes the small avatar; the bottom 256 pixels are omitted. Keep the face and identifying features within that upper region. Older square avatars remain compatible, but the battle status bar crops their sides to 4:5. Make new portraits at 4:5 so the composition fits both uses.

Both character images need complete scene backgrounds filling every corner, with fully opaque pixels. A transparent cutout, checkerboard, plain white or black canvas does not replace that scene. Use RGB PNG or RGBA with Alpha 255 throughout; an extra transparency channel is not required. The loader's ability to decode Alpha does not make transparency the artwork requirement.

284×512 is the character-selection frame's size; 71:128 is the target aspect ratio, not a requirement that source files contain only 284×512 pixels. You can export at 568×1024 or a larger equivalent size. Current formal-scene main images are mostly around 929×1672 and avatar portraits around 4:5. These describe the existing assets, not mandatory loader resolutions.

Use the game's warm, clear, low-pixel Western fantasy style. Main art keeps the character and environment in a tall composition. Create a separate head-and-shoulders or half-body avatar, preserving the face, outfit and background mood. Leave out baked-in UI frames, names and text. Compose treasure, move and enemy art for its own purpose rather than turning every subject into a background-free cutout. See the [AI artwork request](ai-authoring.md#prepare-full-body-art-and-an-avatar-for-one-character).

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

The large selection image reads `Icon`. The battle status bar prefers `Avatar` and displays it at 4:5. Binding only `Portrait` does not replace these two explicit slots. `Portrait` is an optional fallback. If both slots share art, bind both to the same `assets/icons/...png` and import it once rather than duplicating it. Use the tall 284×512 frame for main art and a separate 4:5 `Avatar` with a background. Paths must stay inside the package; absolute paths and `../` are forbidden.

## 3. Asset validation during builds

**Build and Install** checks image headers, true format, dimensions, file size, and decoding, and generates `assets/asset-index.json`. Do not edit the index manually. A successful build does not establish that the background, composition or pixel style is right. Check the exported width and height in an image editor, confirm both character images have complete backgrounds and no transparent pixels, and test the portrait's top-square crop. Re-encode WebP rather than merely renaming it `.png`, and preserve the character's proportions when fitting the canvas.

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
