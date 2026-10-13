# Versions, sources, and validation scope

[简体中文](../../zh-CN/reference/versions.md) · [Index](../README.md)

Guide revision 2 · Mod API 1.8.0 · 2026-10-13

This page separates the guide's evidence from full game or online-release acceptance. Revision 2 is a locally reviewed draft and has not been pushed. Published revision 1 on GitHub does not update automatically.

## Applicable versions

| Component | Reviewed value/purpose |
| --- | --- |
| Guide | Revision 2, 2026-10-13, locally reviewed draft |
| Mod API | `MiniHero.ModApi` 1.8.0, checked against current declarations and behavior |
| API export | [43 selected public types](api-surface.md), not a promise of the entire engine surface |
| Unity Editor | Official project on 6000.3.19f1, matching ProjectVersion |
| .NET SDK | Tested with 10.0.401; this is the test environment, not a minimum installation requirement |
| Mod target | Generated `netstandard2.1`, C# 9 project; use its csproj and game references |

The manifest declares `modApiVersion`. The current loader accepts declarations from 1.0.0 through 1.8.0; this accepted range does not guarantee that older games contain every newer member. The first lesson targets the current 1.8.0 API. Check your references before using members such as `AddCharacterToLevel`, introduced in 1.7.0. Do not claim complete backward compatibility without compiling and playing against the older version.

The project's internal `bundleVersion = 1.0` does not establish the version released in a store. Report the game and API versions you actually run.

## Checks performed for this revision

| Check | Scope/result |
| --- | --- |
| Source review | Registration, defaults, events, fixed columns, healing, configuration, and music boundaries |
| Fragment compilation | Public fragments and complete chapter classes against current API/Core references |
| Real workshop build | Isolated documentation package in the official Editor: SDK build, hash, install, and load |
| Deterministic gameplay | Fixed columns, a specific encounter reward, enemy combat, exit use, intermission, and 4 shield on the next stage |
| Save restoration | Next-stage index and shield restored, followed by play through the final exit to victory |
| Document checks | Local links/anchors, fences, bilingual C# contracts, revision hashes, SVG/JSON, and release artifact boundaries |
| Screenshots and diagrams | English Adventure Workshop screen from the official project; four neutral rule/flow diagrams checked in the browser |
| Translation | AI-assisted bilingual meaning review and English cold reading, preserving numbers, conditions, targets, and stable identifiers |

Gameplay checks used the core and real workshop loader inside the user's existing official Editor. No second Unity project or Editor was created. Test references, binaries, saves, and private paths are excluded from this repository.

## Checks still required in the actual environment

- Fully exit and restart the standalone game to verify loading; same-process DLL loading cannot replace this.
- Inspect your own image cropping, audio playback, and text after language changes. The workshop overview screenshot does not verify these assets.
- Verify Steam submission, item visibility, and subscribed downloads. Local export does not prove any of them.
- Run an independent beginner and English-reader [trial](reader-trial.md). These have not been conducted; AI review is not independent player acceptance.
- Test older game/API versions, old-save migration, and complete advanced graph/loop combinations.

## Maintenance

`docs/api-surface.json` stores selected declarations, relative source identifiers, and source hashes. `docs/revision.json` stores paired document hashes. Hashes detect edits, not correctness. Follow [Contributing](../../../CONTRIBUTING.md), revise both languages, and rerun checks. Behavioral changes also need the affected task tested again.
