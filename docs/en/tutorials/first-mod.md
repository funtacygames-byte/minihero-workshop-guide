# Build and change your first mod

[简体中文](../../zh-CN/tutorials/first-mod.md) · [Index](../README.md)

Guide revision 2 · Mod API 1.8.0 · 2026-10-14 · [Validation scope](../reference/versions.md)

By the end of this lesson, the treasure codex will show **Wayfarer's Relic**, and its level-1 description will change from 2 shield to 4. This verifies building, installation, and loading. The next lesson uses a fixed board to test the actual stage-entry effect.

You need the installed game, a code editor, and a .NET SDK that runs `dotnet --version` in a terminal. You do not need Unity or the game's source. Start without images, music, or configuration.

## 1. Create a project and check its names

Use the crossed-tools button at the lower left of the main menu to open **Adventure Workshop → Develop Mods → New C# Project…**. Use package ID `local.alice.lantern-trail`, display name **Lantern Trail**, and your own author name. If that ID already exists, choose a different one and keep the namespace generated for it.

![English Adventure Workshop screen; Develop Mods is the middle row](../../../images/ui-workshop-overview-en.png)

Actual English game UI, captured on 2026-10-13 with API 1.8.0. Choose **Open** on the middle **Develop Mods** row. Other languages use the same layout and entry point. This screenshot identifies the tutorial's starting point.

Use Open Source on the project row. You should find `package.json`, `source/ModEntry.cs`, `source/*.csproj`, and `localization`. A new project normally has no mod DLL until its first build.

If you cannot locate a button or file, see the [creation dialog, source layout, and build-result images](../reference/visual-walkthrough.md).

| Name | Value in this lesson | How to handle it |
| --- | --- | --- |
| Package ID | `local.alice.lantern-trail` | Match the directory and entry attribute; keep stable after release |
| Namespace | `LocalAliceLanternTrailMod` | Keep the generated value |
| Full entry type | `LocalAliceLanternTrailMod.ModEntry` | Match `package.json.codeEntryPoint` |
| Display name | Lantern Trail | Edit localized values without renaming these identifiers |

`codeAssembly` should point to `mod/LocalAliceLanternTrailMod.dll`. These values are case-sensitive. A different package ID generates a different entry; do not copy this table unchanged. See [Entry and registration](../reference/entry.md).

## 2. Use the same starter code

Open the [minimal entry and Wayfarer's Relic fragment](../../../templates/en/01-entry-and-config.cs.txt) and copy it into `source/ModEntry.cs`. Replace the entire file only when your package ID matches this lesson. Otherwise, first change the fragment's namespace and `PackageId` to the generated values and check the manifest. Keep the generated `.csproj` and `package.json`.

The fragment registers one treasure that grants `BaseValue × level` shield on stage entry. Its name and description use the generated `content.starter_relic.*` localization keys. `BaseValue` starts at 2 and is shared by the description and execution. The filename still contains `config` to preserve old links; the fragment no longer registers configuration.

Older game scaffolds may contain a `shield_per_stage` configuration or `gameplay.general` tags. Replacing the source in this lesson makes the shield category and life-build pool consistent. See [Compatibility](../reference/compatibility.md) for the retained configuration API.

## 3. Build and check loading

Save the file and use Build and Install on the project row. Confirm the mod is enabled in mod management. Fully exit and restart the game, then open the treasure codex. Select **all characters** in the character filter and search for `Wayfarer's Relic`; in Chinese, search for `旅者遗物`.

You should find Wayfarer's Relic. The codex may select its highest available quality by default; use the lower-left arrows to switch quality, not level. This starter does not supply different values per quality, so every quality's level-1 description grants 2 shield on stage entry. This check needs no random chest draw and does not grant the treasure.

If there is no result, use [Loading diagnostics](../troubleshooting.md) to check enabled state, entry, and language. Changing chest weights will not fix a loading failure.

## 4. Change one value and verify again

Change the `2` in this line to `4`:

```csharp
public override int BaseValue => 2;
```

Save the source and increase `package.json.version` from the generated `0.1.0` to `0.1.1` (or increment your current version). Build and install again, then fully exit and restart. The installer rejects different content under the same installed version. Apply this version increment before each later changed build you install; keep `packageId` unchanged. The level-1 codex description should now show 4 shield at every quality. Runtime effects still use `4 × level`; the codex quality arrows do not increase level. Keep `{0}` in both localized descriptions: the shared formula supplies it.

If the old value remains, confirm you edited `Sources`, check that the build succeeded, and verify every game process exited. Reloading within one process does not prove the new C# DLL ran.

## Checks and next step

- The initial build succeeds, the mod is enabled, and the codex finds the treasure by name.
- The level-1 value changes from 2 to 4 after rebuilding and fully restarting.
- Package ID, content ID, entry type, and text keys stay unchanged when display text changes.

Continue with [Creating and testing a treasure](treasure.md). To play your own board first, complete [A fixed stage](stage.md), then return to the treasure lesson to add a guaranteed reward.
