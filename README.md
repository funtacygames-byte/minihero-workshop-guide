# MiniHero Workshop Authoring Guide

**English** · [简体中文](README.zh-CN.md)

Create treasures, characters, moves, enemies, items, encounters, stages and adventures in C#. Add card choices, custom pages, package images, music and bilingual text. Each task gives prerequisites, edit locations, registration and appearance, expected results and troubleshooting links.

Guide revision 4 · Mod API 1.8.0 · 2026-10-14 · [Actual verification scope](docs/en/reference/versions.md)

## Your first mod

Complete [Build and change your first mod](docs/en/tutorials/first-mod.md): generate project → preserve entry → build/install → fully restart → find Wayfarer's Relic in the codex → change one value. Then use a [fixed stage](docs/en/tutorials/stage.md) to play through guard and exit, and a [specified treasure reward](docs/en/tutorials/treasure.md) to check real rules without relying on random draws.

You need the game, a code editor and a .NET SDK, without Unity or the full game project. The current game generates development references; this repository is not an SDK replacement. Increment package version for each changed installation and fully restart to verify the new DLL.

## Choose a task

| Goal | What the lesson completes |
| --- | --- |
| [Treasure](docs/en/tutorials/treasure.md) | Quality, level, character pool, deterministic acquisition and effects |
| [Character and initial move](docs/en/tutorials/character.md) | Referenced classes, registration, selection entry and target checks |
| [Enemies and traits](docs/en/tutorials/enemy.md) | Independent card instances, damage timing and counters |
| [Items and encounters](docs/en/tutorials/items-and-events.md) | Potions, targeted damage, attribute and specified-content rewards |
| [New card choices](docs/en/tutorials/card-choice.md) | Two real card faces, conditions/costs, source consumption and turn |
| [Counters and state](docs/en/tutorials/rules-and-state.md) | Healing measurement, three-trigger cap, isolation, preview and reset |
| [Fixed stage](docs/en/tutorials/stage.md) | Bottom-to-top columns, guard → exit and selection entry |
| [Connected stages](docs/en/tutorials/adventure.md) | Steps, stage IDs, preparation and restoration |
| [Seeds, loops and continuation](docs/en/tutorials/adventure-modes.md) | Fixed/daily seeds, date offset, three passes and dynamic continuation |
| [Custom pages](docs/en/tutorials/custom-ui.md) | Tree, buttons, controller, package navigation and original-menu fallback |
| [Configuration compatibility](docs/en/tutorials/configuration.md) | Definitions, defaults and legacy values; no current player settings page |
| [Assets and bilingual text](docs/en/tutorials/assets-and-text.md) | Image slots, package paths, music, translation catalogs and placeholders |
| [Reproducible debugging](docs/en/tutorials/debugging.md) | Fixed inputs, deltas, boundary checks and reports |
| [Publishing and updates](docs/en/tutorials/publish.md) | Separate local packaging from Steam delivery |

The first lesson and these fourteen topics form fifteen task routes. The [complete feature map](docs/en/feature-map.md) labels available, partial and backend-only capabilities.

## Before making card choices

Display cards are previews; option data or a registered concrete resolver supplies the reward. Opening charges nothing; successful confirmation settles it. The interface supports any number of single-choice cards, paging, conditions, costs, chains, rollback and saved resolvers. Start with [Camp Supplies](docs/en/tutorials/card-choice.md), then read the [fields, turns and save contract](docs/en/reference/card-choice.md).

## Troubleshooting, references and AI

Use [troubleshooting](docs/en/troubleshooting.md) for compilation, loading, appearance, triggers and missing assets. For signatures, defaults and state semantics, see [API and rule references](docs/en/README.md#reference).

- [Complete index](docs/en/README.md) and [fifteen focused fragments with dependencies](templates/README.md)
- [AI delivery contract](docs/en/ai-authoring.md), [machine capability list](docs/capabilities.json) and [llms.txt](llms.txt)
- [Terminology](docs/en/glossary.md), [versions/evidence](docs/en/reference/versions.md) and [research approach](docs/en/reference/documentation-design.md)
- [Project](docs/en/01-project-and-build.md), [content manual](docs/en/02-content-creation.md), [assets](docs/en/03-assets-and-presentation.md) and [full acceptance](docs/en/04-testing-and-publishing.md)
- [Maintenance and feedback](CONTRIBUTING.md)

This repository supplies tutorials, focused source fragments and teaching diagrams, without a complete adventure package or game-art bundle. Gameplay is authored in C# and compiled into a mod DLL; generated manifests, translation catalogs and saves are auxiliary data. Configuration compatibility does not imply a player settings page. Reports should include guide revision, actual game/API, package version, step, expected/actual result and first diagnostic, with private paths, saves and account data removed.
