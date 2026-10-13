# MiniHero Workshop Authoring Guide

**English** · [简体中文](README.zh-CN.md)

Create treasures, characters, enemies, and stages in C#, then add your own images, music, and bilingual text. Start with a visible result and continue by task.

Guide revision 2 · Mod API 1.8.0 · 2026-10-13 · [Versions and validation](docs/en/reference/versions.md)

## Your first mod

Start with [Build and change your first mod](docs/en/tutorials/first-mod.md): create a project, preserve its generated entry, build and install, fully restart, find the relic in the codex, then change one value. Use [A fixed stage](docs/en/tutorials/stage.md) to play through guard and exit, and [Treasures](docs/en/tutorials/treasure.md) for a guaranteed reward and an actual effect check.

You need the game, a code editor, and a .NET SDK. Players do not need Unity or the full game project. The game supplies development references; this repository does not replace them.

## Choose a task

| Task | Outcome |
| --- | --- |
| [Treasures](docs/en/tutorials/treasure.md) | Quality, levels, pools, and a specific reward |
| [Characters and initial moves](docs/en/tutorials/character.md) | Registration, selection, and two-target checks |
| [Enemies and traits](docs/en/tutorials/enemy.md) | Card instances, damage windows, independent state |
| [Your first fixed stage](docs/en/tutorials/stage.md) | Guard→exit, fixed columns, and playability |
| [Connect stages](docs/en/tutorials/adventure.md) | Steps, intermissions, stage IDs, save restoration |
| [Assets, music, and bilingual text](docs/en/tutorials/assets-and-text.md) | Slots, package paths, and shared arguments |
| [Package, publish, and update](docs/en/tutorials/publish.md) | Verify local builds and Steam delivery separately |

## Something broke

Open [Troubleshooting](docs/en/troubleshooting.md) for compiler, loading, effect, and asset failures. Use [API and rule references](docs/en/README.md#reference) for signatures, defaults, and state contracts.

## Manuals and supporting material

- [Projects and builds](docs/en/01-project-and-build.md)
- [Content and advanced rules](docs/en/02-content-creation.md)
- [Assets and presentation](docs/en/03-assets-and-presentation.md)
- [Full testing and publishing](docs/en/04-testing-and-publishing.md)

[Full index](docs/en/README.md) · [Fragments and dependencies](templates/README.md) · [AI authoring](docs/en/ai-authoring.md) · [Terminology](docs/en/glossary.md) · [Maintenance](CONTRIBUTING.md)

This repository contains tutorials, focused code fragments, shared diagrams, and relevant UI screenshots. It does not include complete adventure packages or standalone game art assets. Backend configuration and JSON compatibility do not imply player editing pages.

When reporting a problem, include game/API versions, guide revision, the exact step, and observed error. Remove personal paths, saves, and account data; see [Contributing](CONTRIBUTING.md).
