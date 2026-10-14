# Versions, sources and verification scope

[简体中文](../../zh-CN/reference/versions.md) · [Index](../README.md)

Guide revision 4 · Mod API 1.8.0 · 2026-10-14

Revision 4 is a local change awaiting GitHub submission. Gameplay authoring uses C# content classes; generated manifests, translation catalogs and saves are auxiliary data. Legacy gameplay JSON recipes have been removed from player and AI routes. The guide contains fifteen task lessons, fifteen bilingual source-fragment pairs and 65 paired example text keys.

## Baseline

| Item | Evidence |
| --- | --- |
| API and target | Current MiniHero.ModApi.Version 1.8.0; generated netstandard2.1 / C# 9 projects |
| Declaration index | [87 selected types, 773 declarations](api-surface.md), including graph nodes/edges and protected extension points; not the whole SDK |
| References | Current compiled API/Core from the formal project, used locally and excluded from this repository |
| Unity | Already-open formal Editor 6000.3.19f1; temporary verification helpers removed after use; no gameplay or authored scene parameters changed |
| Compiler | Current local .NET SDK; this record does not set a minimum supported SDK |
| Capability status | [available/partial/backend-only](../../capabilities.json) describe integration, not passed tests |

The loader's accepted API range is 1.0.0–1.8.0. The same version string does not prove that an older Core contains recent choices; check the actual references for CardChoiceRequest, CardChoiceEventContent and ICardChoiceResolver. Update the game and regenerate references when types are missing. Declaration snippets cannot replace SDK assemblies.

## Checks executed for revision 4

| Check | Result and scope |
| --- | --- |
| Documents | 87 Markdown files; links, anchors, fences, 58 language pairs, C#/auxiliary JSON contracts, hashes, release boundaries and C# authoring policy |
| Source drift | 87 types / 773 declarations match current source and relative-file hashes |
| Compilation | 30 source fragments and complete configuration/seed/loop overrides compiled in both languages, zero warnings/errors |
| .NET rules | 46 checks per language compilation; preview/execution, choices, state, items, fixed/daily seeds and callbacks |
| Semantic boundaries | Eight current-assembly checks: short-circuit conditions, bare conjunction, roster metadata, parsed-value/fallback behavior, text-format failure and shared rounding |
| Real workshop services | Generated source, current SDK, C# compilation, package hashes, installation, entry loading and content registration in isolated local workshop-data folders |
| First lessons | Fixed guard/exit victory, HP 4→8 change, specified reward, two-stage preparation, next-stage 4 shield and restoration |
| Bilingual DLL | The same English-compiled package resolves Chinese/English character, enemy and stage keys |
| Stateful treasures | Public counters preserve concrete runtime types through Unity JSON; three-heal cap, no fourth reward; handbook counter survives two item uses and rewards the third |
| Card-choice interface | Fresh formal-scene regression: 26 EditMode checks and one PlayMode test for two/three/seven cards, paging, optional headers, real clicks, locale refresh and authored layout |
| Published CampChoice | One additional PlayMode test, 1920×1080, English/Chinese text at authored 15-point sizes; exact two-gold/one-defense/one-turn click and duplicate rejection |
| Complete C# chain | Fragment 15: paid guard layout, two shield then saved follow-up, source consumed once, one total turn, cancellation retaining shield, immediate three-gold branch |
| Modes | Fragment 14: three unique stages, appended-stage JSON restoration and restart. Exact loop settings: three total passes, HP 8/10/12, attack 1/2/3, stage reset, JSON restoration, victory and restart |
| Text capacity | Fixed-font temporary clones of actual card slots; revised English names/rules and new choice texts fit. Other metadata needs its own target controls |
| Meaning review | All 58 pairs reviewed for rules, terminology, dependencies, actions and readability; generated API declarations separately source-checked. Internal AI review is not independent player acceptance |

The local verification harness gave each compiled test update a distinct assembly identity because earlier tutorial DLLs were already loaded in the Editor. This isolates tests; authors should keep their normal project identity and fully restart the game for release verification. Same-process reload does not unload old code.

## Historical evidence

Revision 2's workshop screenshots and neutral diagrams remain instructional references. Revision 3 added task routes, choices/pages/conditions and AI routing. Their older results are distinct from the fresh revision-4 checks above.

## Remaining environment checks

- Standalone game exit/restart and normal installation/enabling/disabling of final release packages; old-save migration and broader provider/loop combinations.
- Additional screen ratios, custom-page navigation/Escape/original-menu fallback, user artwork cropping, audio playback and global volume.
- Steam upload/visibility/subscribed downloads and GitHub Actions; this local change has not been pushed or published.
- Independent Chinese beginner and English [reader trials](reader-trial.md).

## Maintenance evidence

Declarations and source hashes are in [api-surface.json](../../api-surface.json); bilingual hashes are in [revision.json](../../revision.json), and routes in [capabilities.json](../../capabilities.json). Follow [maintenance](../../../CONTRIBUTING.md). Hashes and compilation do not by themselves prove meaning or gameplay.
