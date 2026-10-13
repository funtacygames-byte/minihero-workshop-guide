# Guide index

[简体中文](../zh-CN/README.md) · [Repository home](../../README.md)

Read the chapters in order for your first mod. For a specific problem, open the relevant chapter and use GitHub's document outline to jump to a section.

1. [Project and build](01-project-and-build.md): creation, folders, C# structure, build, install, reload, hashes, and trust.
2. [Content creation](02-content-creation.md): events, quality, state, character pools, enemies, stages, items, and encounters.
3. [Assets and presentation](03-assets-and-presentation.md): artwork slots, music, localization, and configuration limits.
4. [Testing and publishing](04-testing-and-publishing.md): edge cases, diagnostics, compatibility, packaging, and publishing.

Also read the [code snippets](../../templates/README.md), [AI authoring instructions](ai-authoring.md), and [terminology](glossary.md).

The guide shipped with the game is official read-only content. `Sources/<packageId>` is your editable workspace. Reading the guide does not overwrite your source. Apply your changes through `Sources → Build → Install`.

![Source, build, and installation flow](../../images/build-flow.svg)

`Sources` contains editable source, `Build` creates a snapshot, and `Installed` contains the installed version. Fully restart to verify a C# update.
