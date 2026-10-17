# Screenshots and file locations

[简体中文](../../zh-CN/reference/visual-walkthrough.md) · [Index](../README.md)

Guide revision 7 · Mod API 1.11.0 · 2026-10-17

Use these images to find buttons and files. Workshop screenshots use English; the Chinese interface has the same layout. Alice is an example name, so enter your own name or nickname. Folder and cropping diagrams help you compare your files.

## 1. Open the workshop

![English Adventure Workshop overview](../../../images/ui-workshop-overview-en.png)

Use the crossed-tools button at the lower left of the main menu. The middle **Develop Mods → Open** row opens development; **Manage Mods** handles installation and enabling. The first lesson does not require importing the official adventure example.

## 2. Create and open source

![Creation dialog with the first lesson's ID and display name](../../../images/ui-new-project-en.png)

Enter `local.alice.lantern-trail` as **Stable Package ID**. **Display Name** is the displayed name. Choose **Create Project**; the success dialog gives your local project location. If the ID exists, choose another and check the generated namespace against the manifest entry.

![Selected files in the generated source project](../../../images/source-layout.svg)

This diagram follows the actual generated directory; it is not a File Explorer screenshot or a complete file list. The blue source-folder icon opens `Sources/<packageId>`; the hammer with a down arrow builds and installs; the rightmost package icon opens release preparation. Edit `source/ModEntry.cs`, keep the generated csproj, and do not edit source in Builds or Installed.

## 3. Check the build result

![First-lesson project v0.1.1 installed successfully](../../../images/ui-build-success-en.png)

This build uses the [first lesson](../tutorials/first-mod.md) change to 4 and version `0.1.1`. **Installation successful** at the bottom confirms installation. **Ready to build** on the row only describes source build-entry conditions; it neither detects the SDK nor verifies gameplay. Fully exit and restart, then check the level-1 description in the codex.

![Wayfarer's Relic at Common quality with the 4-shield description](../../../images/ui-codex-result-en.png)

Open **Codex → Treasures** from the main menu, choose **All Characters**, search for `Wayfarer's Relic`, and select the result. This screenshot selects Common in the actual loaded content; the default may be the highest available quality. All qualities share the level-1 value of 4 in this lesson. The quality arrows do not upgrade a treasure. This lesson binds no custom art; the icon identifies the result and is not an asset you must supply.

## 4. Find an error report

![Failure report path and first-error syntax](../../../images/diagnostic-route.svg)

On failure, the game attempts to open the report folder. If that fails, follow the workshop-root path, your package ID, and the actual timestamp to `install-failure.txt`. CS1002 only illustrates file, line/column, and error syntax; use your own first error. See [Troubleshooting](../troubleshooting.md), and remove private absolute paths before sharing.

## 5. Export only the intended icon

![A contact sheet compared with a single exported icon](../../../images/icon-crop-check.svg)

The six-cell sheet is not one treasure icon. Export the intended image separately in your drawing tool with a reasonable margin. This is a neutral illustration, not a game rendering. After binding, inspect the subject, transparent edges, and proportions in the actual codex and board; see the [assets lesson](../tutorials/assets-and-text.md).

## 6. Compare a real C# card choice

![CampChoice compiled from the lesson, shown in English](../../../images/ui-camp-choice-en.png)

This is [fragment 10's CampChoice](../tutorials/card-choice.md), compiled by the workshop and rendered at 1920×1080. Moondew Kit restores 5 HP; Guard Supplies costs 2 gold and grants 1 defense. Displayed artwork is the host fallback for this rules-only example. Choosing Guard Supplies costs 2 gold, grants 1 defense and consumes one turn. The source event remains on the board until confirmation.

![The same compiled package showing Chinese card text](../../../images/ui-camp-choice-zh-Hans.png)

After merging both translation catalogs, the same mod can show the corresponding names and descriptions. Switch languages and open a new choice to check that your text fits. An existing card may retain the text it had when opened.
