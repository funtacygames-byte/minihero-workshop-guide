# Instructions for AI-assisted mod authoring

[简体中文](../zh-CN/ai-authoring.md) · [Guide index](README.md)

Reviewed: October 13, 2026. Current Mod API: 1.8.0.

Use this document with the [task lessons and references](README.md), four manuals, and relevant [code snippets](../../templates/README.md). It does not replace the game assemblies or an actual test environment.

## Reading order and sources

Start with [the first mod](tutorials/first-mod.md) and the lesson for the requested task. Read the matching API/rule reference; use the manuals for advanced details. Before delivery, follow [Testing and publishing](04-testing-and-publishing.md) and report the [verified scope](reference/versions.md).

The latest user request, applicable project instructions, and current game implementation take priority over old plans or translations. MiniHero uses warm Western fantasy and fairy-tale adventure. Yaoguang is a specifically authorized ancient Chinese heroine exception; do not apply that exception to the whole world or infer the setting from legacy technical names.

## Available capabilities and limits

| Goal | Public entry point and boundary |
| --- | --- |
| Characters, traits, treasures, moves, enemies, items, events | Public C# content classes; `registrar.AddContent/AddContents` |
| Selectable adventure | `AdventureContent` + source `StageContent` + steps/difficulties; registering a Stage alone does not add a level-selection entry |
| Fixed puzzle layout | `StageDefinition.fixedColumns`; bottom-to-top lists, last card exposed |
| Daily/fixed challenge | `AdventureSeedSettings`; explicitly set `utcOffsetMinutes` for daily rollover |
| Looping growth | `AdventureLoopSettings`; `maximumLoops = 3` means 3 loops total, `0` unlimited |
| Dynamic continuation | `IAdventureContinuationContent.CreateNextStages`; read isolated context, return an empty array to end |
| Adventure rules | `AdventureRuleContent`, activated by adventure/difficulty `adventureRuleIds` |
| Custom screen/start screen | `registrar.AddScreen`, `ModUi` tree, `ModScreenController`; the host creates Unity UI |
| Art and music | Package-local paths, generated asset index, presentation slots, and music themes |
| Configuration | Compatibility `AddConfig/ModConfig`; no player-facing configuration page |
| JSON | Retained backend compatibility; no player-facing JSON editor |
| Starting content | Traits and the first starting move work; `StartingTreasureTypes` and additional starting moves are not granted on selection |
| DLL updates | Final verification requires a full restart; in-process reload is insufficient proof |
| Steam | Local validation/export is separate from proven upload, subscription, or download |

Do not invent host methods, event fields, configuration menus, or connected music cues. Check the current public references. If an interface is absent, explain the limit rather than defining a fake replacement just to make compilation pass.

## Deliverable structure

A runtime package contains `package.json`, `mod/<AssemblyName>.dll`, and `localization/<locale>.json`, plus needed assets/index/music. An editable source project also contains `source/*.csproj`, `source/ModEntry.cs`, and game-generated `.tmode-sdk` references.

- Keep the package ID, folder ID, entry-point attribute, and manifest consistent.
- `codeEntryPoint` is the namespace-qualified type; `codeAssembly` is the package-relative DLL path. Both must match actual output.
- Custom content IDs begin with `packageId + "."`. New localization keys use ASCII English semantic identifiers; translations belong in values.
- Entry/content classes are public with parameterless constructors. Treasures are independently serializable. Keep exclusive behavior in the concrete content class and use shared runtime settlement.
- Declare `code.execute`; code runs with the current user's permissions rather than in a sandbox.
- Target `netstandard2.1` and reference current `MiniHero.ModApi.dll` and `MiniAdventureWorld.Core.dll`. Exclude both from the mod payload.
- Generate and verify distributable hashes through the workshop. Exclude local build reports, references, `bin/obj`, temporary folders, and personal saves from publication.

A machine authoring mods needs both game assemblies. Obtain them by creating a project in the installed game. Public tutorial source cannot replace the Core DLL. Keep game project directories out of temporary projects and do not share them through filesystem links.

## Rule conventions

- Compare a proposed treasure's trigger, input, benefit, state, scope, and cost with the current catalog before designing it.
- Keep categories, pool tags, and appearance conditions separate. Character pools match any shared pool tag; weights are numeric rather than extra tags.
- Quality tiers end at Legendary. Five/four/three/two tiers start at Common/Uncommon/Rare/Epic. Do not supply unspecified tier values.
- Healing rules read the complete settled healing amount; explicit overflow conversions read only overflow. Normally say “healing amount” in player text.
- Reset temporary treasure counters, stacks, pending enhancements, and use quotas on new-stage entry. Explicitly state and test cross-stage exceptions and save restoration.
- Convert from base stats and round down. Combine same-kind percentages before settlement. Share preview and execution rules.
- Fixed columns are stacks: `{ exit, guard }` requires the guard before the exit. Test card clicks rather than list counts.
- Use “attack” in player-facing English; use “basic attack” when distinguishing it from moves or other damage. Technical `NormalAttack` identifiers remain unchanged.

## Evidence before delivery

State the player experience, package ID, minimum API, and complete folder structure. Report commands actually run and their results. Verify registration, hashes, installation, enabling/disabling, localization, and loading with the real loader.

Play through key effects, boundaries, victory/failure, stage resets, continuation/loops, and save restoration. Check images/audio and localized controls at their existing font size and layout; shorten translations naturally rather than resizing UI. Verify C# changes after fully restarting.

State untested parts accurately. A test file is not evidence that it ran, compilation is not gameplay verification, and a local export is not an online Steam upload. For project-level Unity checks, use the already-open official Editor only; do not start another Editor or open `Temp/PlayerBuildProject`.
