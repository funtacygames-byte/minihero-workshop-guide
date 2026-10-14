# Feature map: what you can build and where to start

[简体中文](../zh-CN/feature-map.md) · [Index](README.md)

Guide revision 4 · Mod API 1.8.0 · 2026-10-14

Choose a task first, then look up exact signatures. available means an authoring entry exists; backend-only is a backend or compatibility capability; partial has explicit integration limits. These statuses do not claim in-game verification of every feature in this revision.

| Goal | Status | Key boundary |
| --- | --- | --- |
| [First mod](tutorials/first-mod.md) | `available` | Generated project, full entry, build/install, restart |
| [Treasures and quality](tutorials/treasure.md) | `available` | Independent instances, quality/level, pools, specified rewards |
| [Characters and moves](tutorials/character.md) | `partial` | First initial move and trait; later moves and starting treasures not auto-granted |
| [Enemies and traits](tutorials/enemy.md) | `available` | Instance state, real damage, callback timing |
| [Items and encounters](tutorials/items-and-events.md) | `available` | Direct/targeted use; legacy rich events have at most three branches |
| [New card choices](tutorials/card-choice.md) | `available` | Any-size single choice, conditions/costs, resolver, chains, rollback and saves |
| [Fixed stages](tutorials/stage.md) | `available` | Complete bottom-to-top columns; no mixed fixed/random fill |
| [Adventures and difficulty](tutorials/adventure.md) | `available` | Entry, source Stage, steps, character list, preparation |
| [Seeds, loops and continuation](tutorials/adventure-modes.md) | `available` | Daily offset, total loop cap, isolated continuation context |
| [Rules and state](tutorials/rules-and-state.md) | `available` | Counters, preview, stage reset, adventure-rule activation |
| [Custom pages](tutorials/custom-ui.md) | `available` | Host UI tree, actions, same-package navigation; no configuration writes |
| [Configuration compatibility](tutorials/configuration.md) | `backend-only` | Declare/read defaults or legacy values; no player page or public writer |
| [Assets and bilingual text](tutorials/assets-and-text.md) | `partial` | Package paths and slots; Victory cue not connected to Mod victory page |
| [C# graph routes](02-content-creation.md) | `available` | Load-time route; supply card snapshots and conditional fallbacks |
| [Debugging and testing](tutorials/debugging.md) | `available` | Fixed inputs, deltas, reports, verification layers |
| [Publishing and updates](tutorials/publish.md) | `partial` | Local build/export verifiable; online Steam needs account environment |

Use [conditions](reference/conditions.md) for identities and grammar, [events](reference/events.md) for callback selection and [API](reference/api-surface.md) for declarations. Complete the first lesson before choosing a topic; you need not learn everything first. The machine-readable counterpart is [capabilities.json](../capabilities.json); see [versions](reference/versions.md) for verification.
