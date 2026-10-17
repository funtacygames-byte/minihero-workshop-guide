# Making mods with AI

[简体中文](../zh-CN/ai-authoring.md) · [Index](README.md)

If you are learning C#, an AI assistant can explain the source, change a value or help add a treasure. You still create and build the project in Adventure Workshop. The code it gives you needs to go into that project before it can run in the game.

Start by [creating a project in the first lesson](tutorials/first-mod.md#1-create-a-practice-project). Ask for one small change first, check the result, then add more features.

## 1. Explain your project and your goal

Give the assistant these three things:

1. **What you want to see in the game.** “Gain 4 shield when entering the next stage” is easier to act on than “improve my treasure.”
2. **The relevant lesson links.** For your starter treasure, share [the first lesson](tutorials/first-mod.md) and [the treasure lesson](tutorials/treasure.md). For options, share [Card choices](tutorials/card-choice.md).
3. **Your current files.** Start with `source/ModEntry.cs` and `package.json`. For a problem, add the first error and the relevant source. If the assistant can read local files, tell it where the project is.

A chat assistant that cannot read your files needs you to paste or attach them. Asking it to read the guide does not give it access to the pages. Do not upload the whole game, game DLLs or personal saves. Replace personal paths in errors with `<project>`.

## 2. Try a small request first

This prompt is for a starter relic whose level-1 shield is still 2. Replace the bracketed parts with your details:

```text
I am making a C# mod for MiniHero using the guide's Wayfarer's Relic.
Please read: [first-lesson link] and [treasure-lesson link].
Goal: change its level-1 shield on stage entry from 2 to 4.
Here is my ModEntry.cs: [paste source]
Here is my package.json: [paste contents]

Tell me which file to edit and which section to replace, and explain the change.
Keep my package ID, namespace, entry class and localization keys.
Use the same formula for the description and effect; do not hard-code the description value.
If you need another file or the current API does not support something, explain what is missing.
Finish with steps to build, restart and check the result in the game.
```

If you already changed the value to 4 in the first lesson, ask it to explain how `BaseValue` drives both the description and the shield. You can also choose another value and update the expected result.

## 3. Describe the rules for new content

Start with what the player experiences. For example: “After healing, gain shield equal to 10% of the healing amount, up to 3 times per stage. Reset the counter in the next stage.” This describes the trigger, reward, limit and reset. Add which character and stage you want to use, how to obtain the treasure and whether you have artwork.

Here is a request for expanding your fixed stage:

```text
I finished the first-mod and fixed-stage lessons and can complete Trail Lab.
Please read: [card-choice lesson link].
I want a Camp Supplies card with these options:
- Free option: restore 5 HP.
- Paid option: pay 2 gold to gain 1 defense.
Use the lesson's CardChoiceEventContent and keep the guard and exit.

Here are my entry and stage files: [paste or provide relevant files]
Give me the complete new .cs file, registration lines for Load,
where to place the card in the fixed columns and the Chinese/English text entries.
Do not recreate the project or add another ModEntry.
Finish with steps to try the free option, paid option and insufficient-gold case.
```

If you have no artwork, start without custom image bindings. To learn as you go, add: “Explain the code before changing it, and give an example when introducing a new term.”

### Prepare full-body art and an avatar for one character

Both character images need complete scene backgrounds. `Icon` is the tall main selection image. `Avatar` is the battle status bar's 4:5 portrait, whose top square also serves small selection avatars. Earlier instructions described the avatar as square and left backgrounds unspecified. Inferring a transparent cutout from the name `portraits` or “character art” does not match the current game. Follow the [artwork specifications](03-assets-and-presentation.md) and actual slots.

Provide a character reference with the request below. Make and check each image separately:

```text
Read: [the guide's Assets and Presentation page].
Make two separate images of the same character. Keep the face, clothing, equipment and colors consistent.
Character brief and references: [describe the character and attach references]
Style: warm, clear, low-pixel Western fantasy matching the reference.

1. Main character art: assets/icons/lantern-ranger.png
   71:128 tall canvas, matching the 284×512 display frame; export a genuine PNG at 568×1024 or a larger equivalent size.
   Include the character and a complete environment filling every corner, with fully opaque pixels.
   Follow the current main-art composition. No transparent cutout, checkerboard, plain white/black canvas, frame or text.
2. Avatar portrait: assets/portraits/lantern-ranger-avatar.png
   Final size 1024×1280, 4:5 portrait canvas, PNG, fully opaque pixels.
   Head-and-shoulders or half-body composition with a complete environment background filling every corner.
   Keep the face and identifying features within the top 1024×1024; the game's small avatar omits the bottom 256 pixels.
   Both images need scene backgrounds. Compose them separately rather than shrinking the full-body main image into the avatar frame.

Each file contains one character, not a collage, sprite sheet or labelled preview.
If the generator cannot output the final size, preserve the composition, then crop, extend and resize on export without stretching the character.
Deliver both final files and list each path, actual encoding, pixel dimensions, Alpha behavior and slot.
Open the exported files to verify them. List unfinished processing steps honestly; renaming an extension is not format conversion.
```

Open both files in an image editor. Check that backgrounds cover the canvas, no transparent pixels remain, and actual dimensions and encoding match the delivery list. The avatar's top-square crop must retain the face. Use [the asset lesson](tutorials/assets-and-text.md#add-character-and-enemy-artwork) to place and bind them, then inspect `Icon` in character selection and `Avatar` in the battle status bar. Decodable format, the right background and a composition that fits the game are separate checks.

## 4. Put the code back into the game

1. Back up the source you will edit. Save each file under the supplied name; new source files end in `.cs`.
2. Check that your original `packageId`, namespace and entry class are intact. New content also needs registration in `Load` and a place in a character pool or stage.
3. Increase `package.json.version`, return to Develop Mods and choose **Build and Install**.
4. Fully exit and restart the game. Start a new run and follow the lesson's actions. Check the result yourself, even if the assistant says it is finished.

If a build fails, send back the **first** error, filename and nearby source. If it builds but has no effect, say which character and card you used and give the values before and after. Follow [Troubleshooting](troubleshooting.md) and solve one problem at a time.

## 5. Check the assistant's answer

Look for clear answers to these questions:

- Where does each file go? Are you replacing code or adding it? Are any required classes missing?
- How will the content appear in the game? A class alone still needs registration and a way to appear.
- Do the description, values, caps, targets and resets match your request?
- Did it actually build or run the mod? If it cannot run the game, it should give you checks to perform and identify what remains untested.

AI can guess APIs incorrectly. If it asks you to find a nonexistent menu, write private save files or install Unity for an ordinary mod, check the relevant lesson before continuing. The game currently has no player-facing mod configuration menu. Updating loaded C# code requires a full restart.

### Give file-reading assistants a reference

Ask it to start at [llms.txt](../../llms.txt) in the repository root and find the relevant lesson. It can then use the [API declarations](reference/api-surface.md) for exact signatures. These are tool references; you do not need to read them all or run the repository's documentation-maintenance scripts. The guide covers API 1.10.0; builds must use the references generated by your installed game.
