# Feature map: what you can build and where to start

[简体中文](../zh-CN/feature-map.md) · [Index](README.md)

Guide revision 7 · Mod API 1.11.0 · 2026-10-17

Use this page to check whether a feature is supported. For your first mod, start with [the three introductory lessons](README.md). You do not need these APIs first; the limitations help you choose a route later.

| Goal | Support | Keep in mind |
| --- | --- | --- |
| [First mod](tutorials/first-mod.md) | Supported | Generated project, full entry, build/install, restart |
| [Treasures and quality](tutorials/treasure.md) | Supported | Independent instances, quality/level, pools, specified rewards |
| [Characters and moves](tutorials/character.md) | Some limitations | First initial move and trait; later moves and starting treasures not auto-granted |
| [Enemies and traits](tutorials/enemy.md) | Supported | Instance state, real damage, callback timing |
| [Items and encounters](tutorials/items-and-events.md) | Supported | Direct/targeted use; legacy rich events have at most three branches |
| [New card choices](tutorials/card-choice.md) | Supported | Any-size single choice, conditions/costs, resolver, chains, rollback and saves |
| [Fixed stages](tutorials/stage.md) | Supported | Complete bottom-to-top columns; no mixed fixed/random fill |
| [Adventures and difficulty](tutorials/adventure.md) | Supported | Entry, source Stage, steps, character list, preparation |
| [Extend existing difficulties](tutorials/level-difficulty.md) | Available (API 1.10.0) | Independent copies, unique numbers, reference checks, Mod selection progress |
| [Professions and progress](tutorials/profession-progress.md) | Available (API 1.9.0) | Run-locked upgrades, separate resources, commits on successful actions |
| [Professions and crystals](tutorials/profession.md) | Supported from API 1.11 | Independent levels, copied upgrades, game crystals or package currency |
| [Seeds, loops and continuation](tutorials/adventure-modes.md) | Supported | Daily offset, total loop cap, isolated continuation context |
| [Rules and state](tutorials/rules-and-state.md) | Supported | Counters, preview, stage reset, adventure-rule activation |
| [Custom pages](tutorials/custom-ui.md) | Supported | Host UI tree, actions, same-package navigation; no configuration writes |
| [Configuration compatibility](tutorials/configuration.md) | Compatibility API | Declare/read defaults or legacy values; no player page or public writer |
| [Assets and bilingual text](tutorials/assets-and-text.md) | Some limitations | Package paths and slots; Victory cue not connected to Mod victory page |
| [C# graph routes](02-content-creation.md) | Supported | Load-time route; supply card snapshots and conditional fallbacks |
| [Debugging and testing](tutorials/debugging.md) | Supported | Fixed inputs, deltas, reports, verification layers |
| [Publishing and updates](tutorials/publish.md) | Some limitations | Local build/export verifiable; online Steam needs account environment |

Use [conditions](reference/conditions.md) for identities and grammar, [events](reference/events.md) for callback selection and [API](reference/api-surface.md) for declarations. Complete the first lesson before choosing a topic; you need not learn everything first. See [versions](reference/versions.md) for current-version limitations.
