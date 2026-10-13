# 01 Project and build

[简体中文](../zh-CN/01-project-and-build.md) · [Guide index](README.md)

Reviewed: October 13, 2026. Current Mod API: 1.8.0.

This chapter takes you from **New C# Project** to a mod running in the game. It explains the creation fields, C# structure, development tools, building and installing, package hashes, and the trust boundary for code mods.

## Contents

1. Creating a project
2. From creation to an in-game check
3. C# mod structure
4. Project folders
5. Development environment
6. Build, install, enable, and reload
7. Hashes, signatures, and trust
8. Your first project

## 1. Creating a project

The development page does not keep project settings permanently on screen. Click **New C# Project…** to open the one-time creation form, which collects three values:

- **Package ID:** a stable technical name, such as `local.alice.lantern-trail`. Use lowercase English letters, digits, dots, hyphens, or underscores. Keep it after publishing; changing it makes saved games and other mods treat the package as different content.
- **Display name:** the name players see, such as “Lantern Trail.” It may contain Chinese and can later be localized.
- **Author:** shown in details and the trust prompt. This is a statement supplied by the package author, not a verified platform identity.

After creation, the project-root `package.json` controls the author, version, and other package metadata. The displayed name is stored in `localization`. The package ID also appears in the folder name, C# entry point, and content ID namespace; editing only `package.json` cannot safely rename it.

The creation form generates a clean C# project. Choose treasure, character, enemy, stage, or music fragments from the [code snippets](../../templates/README.md) afterward, as needed.

## 2. From creation to an in-game check

1. Open **Adventure Workshop → Develop Mods**.
2. Click **New C# Project…**, enter the package ID, display name, and author, and create the project.
3. Select it in the project list and click **Open source**.
4. Edit and save `source/ModEntry.cs`.
5. Put artwork in `assets`, music in `music`, and localized text in `localization`.
6. Return to the development page and click **Build and Install**.
7. Reload after building. If the game process has already loaded this DLL, fully exit and restart for a reliable check.
8. Check the content in character selection, a treasure chest, or your new stage.

Start with one treasure that grants shield on stage entry. Once compilation, installation, and loading work, add characters and stages one at a time so failures are easier to locate.

## 3. C# mod structure

The executable identifiers and formulas below are shared with the Chinese guide. Display strings are English here; chapter 3 explains how to provide multiple languages without changing identifiers.

```csharp
using MiniAdventureWorld.Core;
using MiniHero.ModApi;

namespace LanternTrailMod
{
    [MiniHeroMod(ModEntry.PackageId)]
    public sealed class ModEntry : MiniHeroMod
    {
        public const string PackageId = "local.alice.lantern-trail";

        public override void Load(IModRegistrar registrar)
        {
            registrar.AddContent(new CampfireCharm());
        }
    }

    [System.Serializable]

    public sealed class CampfireCharm : TreasureContent
    {
        public CampfireCharm()
            : base(ModEntry.PackageId + ".treasure.campfire_charm") { }

        public override string Name => "Campfire Charm";
        public override TreasureRank Rank => TreasureRank.Common;
        public override int BaseValue => 2;
        public override System.Collections.Generic.IReadOnlyList<string> CategoryTags =>
            new[] { TreasureCategoryTags.Shield };
        public override System.Collections.Generic.IReadOnlyList<string> PoolTags =>
            new[] { CharacterTreasurePoolTags.HealingLifeBuild };
        public override string Describe(int level) =>
            $"Gain {BaseValue * level} shield when entering a stage.";

        public override void OnStageEntered(StageEnteredEvent e)
        {
            e?.Runtime?.AddShield(BaseValue * e.SourceLevel);
        }
    }
}
```

- `using` makes public Core and Mod API types available to the source file.
- `namespace` names the C# type namespace. It is separate from the package ID, but should identify your mod to reduce collisions.
- `[MiniHeroMod(...)]` marks the unique entry point. Its ID must exactly match `package.json.packageId`.
- `Load` registers content, music, and configuration while the content snapshot is built. Do not cache a particular run's `GameState` here.
- Content classes must be `public`, instantiable, and have a public parameterless constructor.
- `base(...)` takes a stable content ID. Each ID must start with `packageId + "."`.
- `override` replaces a base-class name, value, or event behavior.
- `=>` is a short form for returning a value; `new[] { ... }` creates an array; `typeof(MyTrait)` gets a type; `?.` stops a call when its receiver is null; `$"{value}"` inserts a value into text.

A useful registration order is character traits → moves → treasures → characters → enemy traits → enemies → items/events → stages. Resolution mainly uses IDs and types, so this is a review convention rather than a strict ordering requirement.

This treasure belongs to the life-building pool. Use an eligible character such as Groveheart (`grove_alchemist`) when testing treasure-chest draws; registering a treasure does not automatically make it eligible for every character.

## 4. Project folders

```text
Sources/<packageId>/
├─ package.json       Package ID, version, entry point, DLL, API version
├─ README.md          Project notes
├─ source/            Editable C# source and .csproj
├─ localization/      zh-Hans.json, en.json, and other languages
├─ assets/
│  ├─ icons/          Treasure, move, and intent icons
│  ├─ portraits/      Character art, avatars, and enemy battle art
│  ├─ backgrounds/    Stage backgrounds, map thumbnails, arrival art
│  ├─ _inbox/         Temporary import area, excluded from builds
│  └─ asset-index.json  Generated during builds; do not edit manually
├─ music/             OGG or WAV stage music
├─ mod/               Your compiled DLL
├─ .tmode-sdk/        Maintained development references; excluded
└─ .snapshots/        Source snapshots taken before builds
```

The workshop has three areas:

- `Sources`: your editable workspace.
- `Builds`: successful build snapshots, treated as immutable.
- `Installed`: versions actually installed for the game.

Use `Sources → Build → Install`. To change a value, edit the source, update the version when appropriate, and rebuild.

## 5. Development environment

The environment has three parts:

1. **Code editor:** Visual Studio, Rider, or VS Code edits `.cs` files.
2. **.NET SDK:** compiles C# into a DLL. The workshop runs `dotnet build` and displays the detection result.
3. **Game references:** `MiniHero.ModApi.dll` and `MiniAdventureWorld.Core.dll`.

You do not need Unity, the full game project, or developer source. With an installed copy of the game, create a project in **Develop Mods**, then open `Sources/<packageId>` in an AI tool that can read and edit local files. Have it read the project README, this guide, and the relevant snippets. Keep edits inside that source project. The workshop still performs the final build using your local .NET SDK.

The workshop automatically places editor and command-line compilation references in the development-reference folder. A workshop build also passes the current game assembly paths; you do not need to enter SDK or DLL paths in the UI.

Keep the two game references out of `mod/`. That folder contains only your mod's DLL; the game supplies API/Core at runtime. Rebuilding after a game update refreshes the development references.

If the development page reports that the .NET SDK is missing, run:

```powershell
dotnet --version
```

If no version is printed, install the .NET SDK and reopen the development page. If the workshop builds successfully but the editor reports reference errors, the editor may be holding the reference folder open. Close it and rebuild to refresh the references.

## 6. Build, install, enable, and reload

**Build and Install** performs these steps:

1. Scan and validate artwork and other assets.
2. Run `dotnet build`.
3. Check the manifest, entry point, DLL, and API version.
4. Copy publishable files, excluding `bin`, `obj`, development references, and `_inbox`.
5. Calculate content hashes and write `content.hashes.json`.
6. Write the build report.
7. Verify the copied result and install it.

A failed build does not replace the previous successful build or installed version with incomplete output. Projects built locally in the development page can be installed and enabled directly. A code mod obtained from a repository requires a trust confirmation when enabled in management.

Reloading rebuilds the content snapshot, but loaded .NET assemblies generally cannot be unloaded. Reloading usually handles text and artwork changes. After changing already loaded C# logic, fully exit and restart to establish that the new DLL is running.

## 7. Hashes, signatures, and trust

A build hash summarizes publishable file contents using SHA-256. It is recorded during the build and checked again before installation to detect incomplete downloads, damaged copies, quarantined DLLs, edits made after the build, and mismatched caches.

A hash tells you whether files changed. Anyone able to modify a package can also regenerate its hashes, so it is not a digital signature or proof of authorship. The workshop currently has no certificate signing or online author verification.

A C# mod runs with the game process's permissions. The trust prompt displays the package ID, author, version, and content hash. Trust binds to the exact hash, so changed files require confirmation again. The author field alone is insufficient evidence of safety.

Common diagnostics:

- `AW_BUILD_HASH_MISSING`: no build manifest; rebuild from Sources.
- `AW_BUILD_HASH_MISMATCH`: files changed, disappeared, or were added after building.
- `AW_BUILD_CACHE_REPAIRED`: the damaged cache was moved to Trash and rebuilt.
- `MH_MODSOURCE_DOTNET`: dotnet could not start; check the SDK.
- `MH_MODSOURCE_BUILD`: C# compilation failed; inspect the reported file and line.

## 8. Your first project

Keep the generated `package.json` and `.csproj` and edit `ModEntry.cs`. Check that the minimal treasure builds, appears in browsing, installs, is enabled in management, appears after loading, and applies the values stated in its description. Then continue to [Content creation](02-content-creation.md).
