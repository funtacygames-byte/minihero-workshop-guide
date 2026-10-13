# MiniHero Workshop Guide

[简体中文](README.zh-CN.md) · **English**

Create C# mods for MiniHero: treasures, characters, enemies, items, events, stages, artwork, music, and localization.

This repository contains the authoring guide, focused code snippets, and language-neutral reference diagrams. Start with the guide and build your own project in the game's Adventure Workshop.

**Reviewed:** October 13, 2026 · **Current Mod API:** 1.8.0

## Read the guide

| Chapter | What you will learn |
| --- | --- |
| [1. Project and build](docs/en/01-project-and-build.md) | Create a project, edit C#, build, install, reload, and understand package hashes |
| [2. Content creation](docs/en/02-content-creation.md) | Register content, select rule events, manage state, and connect characters, enemies, and adventures |
| [3. Assets and presentation](docs/en/03-assets-and-presentation.md) | Bind artwork, add stage music, localize text, and understand configuration limits |
| [4. Testing and publishing](docs/en/04-testing-and-publishing.md) | Verify gameplay, diagnose errors, package a mod, and prepare a Steam upload |

[Guide index](docs/en/README.md) · [Code snippets](templates/README.md) · [Instructions for AI assistants](docs/en/ai-authoring.md) · [Terminology](docs/en/glossary.md)

## First project

1. Open **Adventure Workshop → Develop Mods** in the game and create a C# project.
2. Open the generated `Sources/<packageId>` folder in your editor. Install the .NET SDK if the development page reports that it is missing.
3. Read chapter 1, edit `source/ModEntry.cs`, and keep the generated build references and output paths.
4. Choose a focused snippet when you need another type of content. Follow chapter 3 to add your own art and text.
5. Use the game's **Build and Install** action. After changing an already loaded C# DLL, fully restart the game and follow chapter 4.

The game supplies `MiniHero.ModApi.dll` and `MiniAdventureWorld.Core.dll` as development references. Tutorial source files are not a replacement for these assemblies. You do not need Unity or the game's full source project to author a mod.

## Repository layout

```text
docs/
  zh-CN/       Simplified Chinese guide
  en/          English guide
templates/     Focused .cs.txt snippets and instructions
images/        Diagrams shared by both languages
```

The snippets are reference fragments: replace `your.package`, register the referenced content, and integrate only what you need into your own project. They are not complete installable mods. The current game has no player-facing mod configuration page; use and test the defaults in your source. The JSON backend remains available for compatibility, with no player-facing JSON editor.

If you report a documentation issue, include your game/API version, chapter link, and the error or behavior you observed. Remove personal file paths and private data from any logs you share.
