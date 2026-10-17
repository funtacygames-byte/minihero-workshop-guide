# What would you like to make?

[简体中文](../zh-CN/README.md) · [Home](../../README.md)

For your first mod, follow the three lessons below. You will work in the mod project the game creates for you.

## Start small, then play your own stage

| Order | What you do | What you will see |
| --- | --- | --- |
| 1. [Your first mod](tutorials/first-mod.md) | Create a project and change stage-entry shield from 2 to 4 | Wayfarer's Relic with its new value in the codex |
| 2. [Your first stage](tutorials/stage.md) | Place a guard and an exit in a fixed column | A selectable stage you can complete after defeating the guard |
| 3. [Put your treasure in the stage](tutorials/treasure.md) | Add a relic reward and a second stage | 4 shield when you enter the next stage |

For button and file locations, see the [visual walkthrough](reference/visual-walkthrough.md). If a build fails or a result looks wrong, use [Troubleshooting](troubleshooting.md). To get help understanding or changing the code, try [Making mods with AI](ai-authoring.md).

## Expand your mod

After the three introductory lessons, choose a topic that interests you. Each lesson explains what you need before starting.

| Topic | What you make |
| --- | --- |
| [Characters and starting moves](tutorials/character.md) | Lantern Ranger, Lantern Sight and Silver Bolt |
| [Enemies and traits](tutorials/enemy.md) | Moss Wolves that grow stronger when hurt, with separate state for each wolf |
| [Items and encounters](tutorials/items-and-events.md) | A healing potion and a vial that damages a chosen enemy |
| [Card choices](tutorials/card-choice.md) | Free healing or defense for gold, with an optional follow-up choice |
| [Counters and state](tutorials/rules-and-state.md) | A practice flask that grants shield after healing, up to three times per stage |
| [Connected stages](tutorials/adventure.md) | An adventure with exits, preparation and a next stage |
| [Seeds and loops](tutorials/adventure-modes.md) | Fixed challenges, daily seeds, three-pass loops and bounded continuation |
| [Extend level difficulties](tutorials/level-difficulty.md) | Copy, edit and append a difficulty to an existing map |
| [Professions and progress](tutorials/profession-progress.md) | Earn training points and buy permanent profession upgrades |
| [Assets and bilingual text](tutorials/assets-and-text.md) | Your own icon, exploration music, names and descriptions in two languages |
| [Custom pages](tutorials/custom-ui.md) | A camp guide with buttons, changing text and a way back to the original menu |
| [Publishing and updates](tutorials/publish.md) | Release information, an upload and updates to the same Steam item |

## Look these up when you need them

- [Debugging your mod](tutorials/debugging.md): narrow down a problem and write steps that reproduce it.
- [Configuration compatibility](tutorials/configuration.md): maintain old configuration values; the game currently has no player-facing mod configuration menu.
- [All supported features](feature-map.md): find capabilities and limitations once you know what you need.
- [Code fragments](../../templates/README.md): find each lesson's files and where to copy them.

<a id="reference"></a>

## API and rule references

Use these to look up a class, property or event. You do not need to read them all before making your first mod.

| Looking for… | Reference |
| --- | --- |
| Entry classes, package IDs and registration | [Entry and registration](reference/entry.md) |
| Quality, levels and character treasure pools | [Treasures](reference/treasures.md) |
| Characters, moves and enemy traits | [Actors](reference/actors.md) |
| Fixed columns, steps, stages and adventures | [Stages and adventures](reference/stages.md) |
| Healing, damage and attack callbacks | [Events](reference/events.md) |
| Counters, preview, stage changes and saves | [Lifecycle and state](reference/lifecycle.md) |
| Card options, costs, turns and chained choices | [Card choices](reference/card-choice.md) |
| Pages, buttons and navigation | [Custom pages](reference/custom-ui.md) |
| Conditions on routes or card options | [Conditions](reference/conditions.md) |
| Image slots, music and translated text | [Presentation](reference/presentation.md) |
| Version differences or unsupported behavior | [Compatibility](reference/compatibility.md), [versions](reference/versions.md) |
| Exact type and method signatures | [Selected API declarations](reference/api-surface.md) |

Full manuals: [Project and build](01-project-and-build.md) · [Content](02-content-creation.md) · [Assets](03-assets-and-presentation.md) · [Before publishing](04-testing-and-publishing.md). These are organized by system and are useful after the first lesson.

[Terminology](glossary.md) · [Report a documentation problem](../../CONTRIBUTING.md)
