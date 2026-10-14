# Documentation research and expansion approach

[简体中文](../../zh-CN/reference/documentation-design.md) · [Index](../README.md)

Guide revision 4 · Mod API 1.8.0 · 2026-10-14


Organization decisions based on primary documentation read on 2026-10-14. This compares documentation methods; it does not turn another game's APIs into MiniHero features.

| Source | Observation | Applied here |
| --- | --- | --- |
| [tModLoader first lesson](https://github.com/tModLoader/tModLoader/wiki/Basic-tModLoader-Modding-Guide) | Generate skeleton, explain files, build, play, change one value | Retain an observable first lesson; state edit locations and changed results |
| [tModLoader ExampleMod](https://github.com/tModLoader/tModLoader/tree/stable/ExampleMod) | Public implementations for task-based lookup | Focused fragments with dependencies and registration, without a complete adventure package |
| [Fabric first item](https://docs.fabricmc.net/develop/items/first-item) | Registration, visible entry, naming, assets and related source files | Connect each feature to rules, player entry, text and assets rather than only a type name |
| [NeoForge getting started](https://docs.neoforged.net/docs/gettingstarted/) | Separate environment, project and testing | Record references, compilation, loading, gameplay and online publication separately |

This revision adds seven task routes: items/events, card choices, pages, configuration boundaries, stateful rules, seeds/loops/continuation and debugging. Field references and the feature map support lookup. Existing manuals and fragment links remain available so earlier bookmarks work.

The code workflow follows the pattern illustrated by [tModLoader's C# first lesson](https://github.com/tModLoader/tModLoader/wiki/Basic-tModLoader-Modding-Guide): a generated project, one content class, a real result and one observable change. Fabric's [first-item lesson](https://docs.fabricmc.net/develop/items/first-item) also connects registration to visible entry and assets. Here, gameplay remains C# classes → Load registration → compiled DLL → player-action checks; manifests and translations are auxiliary data.

AI support adds a machine-readable capability list, llms.txt, explicit task routes and a file-delivery contract. Each capability is available, backend-only or partial, with links to both languages and public types. A term appearing in documentation does not imply an implemented player menu.

Quality layers are source checks, bilingual meaning review, code-contract comparison, compilation, rule tests, in-game checks and independent readers. Synchronized hashes do not prove meaning; AI review is not native-player acceptance. Future expansion should prioritize blocked reader steps and reproducible cases rather than page count alone.
