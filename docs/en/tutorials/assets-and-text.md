# Add images, music, and bilingual text

[简体中文](../../zh-CN/tutorials/assets-and-text.md) · [Index](../README.md)

Guide revision 4 · Mod API 1.8.0 · 2026-10-14 · [Validation scope](../reference/versions.md)

Goal: bind your own icon to a working treasure, show its name and the same value in Chinese and English, and play a chosen exploration track. Do these as separate tasks so file, text, and audio problems are easy to locate.

Prerequisite: [Your first mod](first-mod.md); music also needs [A fixed stage](stage.md). Supply a square PNG and an OGG/WAV you have permission to use. This repository contains teaching diagrams, without game art or audio.

Before installing a changed build, increment `package.json.version` as in [the first lesson](first-mod.md#4-change-one-value-and-verify-again). Different contents cannot replace an installed package under the same version.

## 1. Bind one treasure image

Place the image at `assets/icons/starter-relic.png`. Add `, IModPresentationContent` to the `StarterRelic` declaration and this property inside the class:

```csharp
public ModPresentation Presentation => ModAssets.Icon("assets/icons/starter-relic.png");
```

Rebuilding validates the image and generates `assets/asset-index.json`. Do not edit the index or bind an uncut 3×2 source sheet as one icon. After installation, inspect cropping, transparent edges, and subject scale in the codex.

See the [export illustration](../reference/visual-walkthrough.md#5-export-only-the-intended-icon) for the difference between a single image and a contact sheet.

![Asset ratio reference](../../../images/asset-dimensions.svg)

Character main art uses `Icon` at 284×512 (71:128). `Avatar`, enemy `BattleArt`, and treasure icons use 1:1. Character `Portrait` is a compatibility fallback, not a substitute for checking the main slot. All paths are relative to the package root. See [Presentation reference](../reference/presentation.md).

## 2. Edit both catalogs with the same keys

The project generates `localization/zh-Hans.json` and `localization/en.json`. Edit these entries within each file's `entries` list without removing other generated entries:

| key | Chinese value | English value |
| --- | --- | --- |
| `content.starter_relic.name` | 旅者遗物 | Wayfarer's Relic |
| `content.starter_relic.description` | 进入场景时获得 {0} 点护盾。 | Gain {0} shield when entering a stage. |

`ModText.Get` reads the name; `ModText.Format` supplies `BaseValue × level` as `{0}`. Do not translate keys or change placeholder IDs. Keep each JSON `locale` field and ensure `supportedLocales` includes `zh-Hans` and `en`.

Rebuild, install, and reload. Use a full restart for final checks that also include C# changes. Switch between Chinese and English and inspect level 1 and another level in the codex. The numbers must mean the same thing. A format error can expose the raw template; use [Troubleshooting](../troubleshooting.md) to check JSON and arguments.

### Merge text for topic fragments

The [Chinese sample catalog](../../../templates/zh-CN/localization.json) and [English sample catalog](../../../templates/en/localization.json) contain 65 keys each, covering fifteen source fragments. To merge:

1. Preserve generated locale, package-name and other entries.
2. Copy entries for the fragments you use into entries by key. Keep one entry per key and update its value.
3. Use identical keys, placeholders and rule values in both languages. Do not overwrite an existing catalog with the entire sample file.
4. Read keys with ModText.Get or Format. Adding JSON alone does not translate a string still hardcoded in C#.
5. Increment version, build/install and fully restart for source changes. Start a fresh run after changing language and inspect Name, Description, role and card text.

The sample collection does not contain all generated package metadata; omit keys for unused features. Avoid duplicate keys. Existing CardState, character and stage definitions can retain text snapshots. A getter reading a new language does not mean every old snapshot is rebuilt. Finish the current custom choice, then open a new one when no refresh callback reconstructs its text.

## 3. Add stage exploration music

Place `music/trail-explore.ogg` and register this theme in `Load`:

```csharp
registrar.AddMusicTheme(new ModMusicTheme(
    ModEntry.PackageId + ".music.trail",
    new Dictionary<ModMusicCue, string>
    {
        [ModMusicCue.StageExplore] = "music/trail-explore.ogg"
    }));
```

Set `music = ModEntry.PackageId + ".music.trail"` in the `StageDefinition` returned by `PracticeStage`. The entry file needs `using System.Collections.Generic;`. Build and install, enter the ordinary practice stage, and listen to the track. Check global music volume too.

Add `BossBattle` for boss stages if needed. A missing boss track falls back to the theme's exploration track, then the built-in list. `Victory` is not wired to mod victory-page music. Custom pages use a separate `MainMenu` entry; registering a stage does not replace the global main menu. See the [asset overview](../03-assets-and-presentation.md).

## Checks and next step

- Paths, index, and slots agree; final image ratios and cropping are correct.
- Catalog keys and placeholders agree, and names and values refresh when languages change.
- Audio plays with correct continuation and volume; missing assets fall back as expected.

Next: [Package, publish, and update](publish.md). Keep existing UI font sizes and text boxes, fitting them with natural concise translations. Configuration APIs are covered under [Compatibility](../reference/compatibility.md).
