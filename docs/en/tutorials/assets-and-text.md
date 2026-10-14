# Add your own artwork, music and text

[简体中文](../../zh-CN/tutorials/assets-and-text.md) · [Index](../README.md)

Give Wayfarer's Relic a new icon, change its names in two languages, then add an exploration track to Trail Lab. These are separate tasks. If you only have an image, you can complete just the first section.

**You need:** the project from [Your first mod](first-mod.md). Music also needs [A fixed stage](stage.md). Start with your own square PNG; for music, prepare an OGG or WAV you have permission to use.

The `assets`, `music` and `localization` folders belong in the project opened by **Open Source**. Create a missing folder when needed. After edits, save, increment `package.json.version`, build and install. Fully restart for changes that include C#.

## 1. Give the relic a new icon

Name your image `starter-relic.png` and put it in your project's `assets/icons` folder. Its final path should be `assets/icons/starter-relic.png`; leaving it on your desktop is not enough.

Open `source/ModEntry.cs`. In the `StarterRelic` declaration, add `, IModPresentationContent` after `TreasureContent`. Add this property inside that class, outside its other methods:

```csharp
public ModPresentation Presentation => ModAssets.Icon("assets/icons/starter-relic.png");
```

Save, increment the version, build and install, then fully restart. Find Wayfarer's Relic in the codex to see your icon. If the subject is cropped, add margins or make the image square in your image editor, then rebuild.

![Image slots and aspect ratios](../../../images/asset-dimensions.svg)

The build generates `assets/asset-index.json`; you do not write the index yourself. A six-image sheet is not a single icon. Export the intended image first, as in [the crop illustration](../reference/visual-walkthrough.md#5-export-only-the-intended-icon).

### Add character and enemy artwork

The character and enemy lessons start without custom bindings. Once your files are ready, add `, IModPresentationContent` to the relevant class declaration, then add one `Presentation` property as shown below.

| Class | Files to prepare | Ratio |
| --- | --- | --- |
| `SilverBolt` | `assets/icons/silver-bolt.png` | 1:1 |
| `LanternRanger` | `assets/icons/lantern-ranger.png` and `assets/portraits/lantern-ranger-avatar.png` | Main art 284×512 or 71:128; avatar 1:1 |
| `MossWolf` | `assets/portraits/moss-wolf.png` | 1:1 |

Add inside `SilverBolt`:

```csharp
public ModPresentation Presentation => ModAssets.Icon("assets/icons/silver-bolt.png");
```

Add inside `LanternRanger`:

```csharp
public ModPresentation Presentation => ModAssets.Create(
    (ModPresentationSlot.Icon, "assets/icons/lantern-ranger.png"),
    (ModPresentationSlot.Portrait, "assets/icons/lantern-ranger.png"),
    (ModPresentationSlot.Avatar, "assets/portraits/lantern-ranger-avatar.png"));
```

Add inside `MossWolf`:

```csharp
public ModPresentation Presentation => ModAssets.Enemy("assets/portraits/moss-wolf.png");
```

Add a binding only when that class's images are ready. For missing-resource errors, check the path and letter case. Character main art uses `Icon`, while the avatar uses `Avatar`; do not put a square avatar directly into the portrait-shaped main slot. See [Presentation](../reference/presentation.md) for more slots.

## 2. Change names without changing lookup keys

Open your project's `localization/zh-Hans.json` and `localization/en.json`. Find these entries in each file's `entries` list:

| Keep this `key` | Chinese `value` | English `value` |
| --- | --- | --- |
| `content.starter_relic.name` | 旅者遗物 | Wayfarer's Relic |
| `content.starter_relic.description` | 进入场景时获得 {0} 点护盾。 | Gain {0} shield when entering a stage. |

Give the treasure a name you like by changing `value` in each language. Keep `key`: the code uses it to find the text. Keep `{0}` in the description too. The code replaces it with `BaseValue × level`, so later value changes do not need another manual description edit.

Keep the file's `locale` and other entries, and ensure `package.json.supportedLocales` includes `zh-Hans` and `en`. Rebuild, install and restart. Switch languages in the game settings, search for each name in the codex and check that the level-1 description shows the same value.

### Merge text for topic fragments

New character, enemy and encounter text is in the [Chinese sample catalog](../../../templates/zh-CN/localization.json) and [English sample catalog](../../../templates/en/localization.json). Pick the entries you need rather than replacing your whole file.

1. Find the relevant keys using the table below.
2. Copy each `{ "key": …, "value": … }` object into your file's existing `entries` array, alongside its current entries. Separate objects with commas; do not add another `entries` wrapper.
3. If a key already exists, edit its `value` instead of adding a duplicate.
4. Add the same keys to the other language's file with their translations. Keep numbers and placeholders such as `{0}` consistent.
5. Build and install. After switching languages, start a new run or open a new choice to check the text.

| Content | Search the sample catalog for |
| --- | --- |
| Trail Lab | `stage.practice.`, `adventure.practice.` |
| Claim Relic | `event.relic_grant.` |
| Lantern Ranger | `character.lantern_ranger.`, `trait.lantern_sight.`, `move.silver_bolt.` |
| Moss Wolf | `enemy.moss_wolf.`, `enemy_trait.wounded_rage.` |
| Potion and vial | `item.moon_dew.`, `item.ember_vial.` |
| Camp Supplies | `event.camp_choice.`, `choice.camp.` |
| Chained choice | `event.two_step_supplies.`, `choice.supply.` and the reused `choice.camp.` |
| Practice Flask | `treasure.practice_counter.` |
| Camp Guide page | `ui.camp.` |
| Dynamic continuation | `adventure.continuation_lab.` |

Adding JSON does not translate strings still hard-coded in C#. The lesson fragments already use `ModText.Get` or `ModText.Format`. Missing translations show the source fallback. Existing cards may store text snapshots, so use a fresh run or choice after changing languages.

## 3. Add an exploration track to Trail Lab

Place the audio at `music/trail-explore.ogg`. For WAV, use an actual `.wav` file and change the path below accordingly. Renaming an extension does not convert audio.

Inside the existing `Load` in `ModEntry.cs`, add this beside your other registrations:

```csharp
registrar.AddMusicTheme(new ModMusicTheme(
    ModEntry.PackageId + ".music.trail",
    new Dictionary<ModMusicCue, string>
    {
        [ModMusicCue.StageExplore] = "music/trail-explore.ogg"
    }));
```

Keep `using System.Collections.Generic;` at the top of the entry file. In `PracticeStage.cs`, find the `new StageDefinition { … }` returned by `CreateDefinition`. Add `music = ModEntry.PackageId + ".music.trail",` alongside fields such as `id` and `name`.

Save, increment the version, build and install, then fully restart. Begin a new Trail Lab run and listen for your track in the ordinary stage. If it is silent, check music volume in the game settings, then check the file path and matching theme IDs.

For boss stages you can add `BossBattle`. A missing boss track falls back to the same theme's exploration track, then built-in music. `Victory` currently does not replace mod victory-page music; start-page music has a separate entry point. See the [music manual](../03-assets-and-presentation.md).

Next, [prepare to publish](publish.md). If a translated name is too long, rephrase it naturally and check it in the game. Keep its numbers and rules instead of shrinking the original UI's font or changing text boxes to make it fit.
