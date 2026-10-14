# Share your mod with other players

[简体中文](../../zh-CN/tutorials/publish.md) · [Index](../README.md)

Once your mod is playable, prepare a name, description and cover, then upload it to Steam Workshop from the game. Start with Private visibility so you can inspect the item before making it public.

**Before uploading:** play through your current version. If it is still a first-lesson exercise, you can keep learning before publishing. Uploads require the game to connect to a signed-in Steam client.

## 1. Keep a working release version

Save the source. Keep the package ID in `package.json` unchanged and make sure `version` identifies the content you will publish. Build and install, fully exit and restart, then start a new run and check:

- Where players enter the content, and whether characters and stages are easy to find.
- Whether the main effects match their descriptions and the adventure can be completed.
- Whether your images, music and Chinese/English text work.
- Whether leaving and continuing the game restores progress correctly.

Choose checks relevant to your mod. A treasure-only mod does not need a custom start page just to be published. See [Debugging](debugging.md) for more cases. Further content changes need a new version and build.

## 2. Prepare a cover and description

Put a cover inside your project's `assets`, for example `assets/icons/workshop-cover.jpg`. Set `coverAsset` in `package.json` to that **package-relative path**. Add extra screenshots to `previewAssets` if needed; those image files must also be inside the package.

| Image requirement | What to prepare |
| --- | --- |
| Format | Actual PNG, JPG or JPEG; renaming an extension does not convert the file |
| Dimensions | Neither side larger than 4096 pixels |
| File size | Each image strictly smaller than 1,048,576 bytes (1 MiB) |
| Composition | A clear cover; landscape previews can use 16:9 |

A large background can have a separate compressed JPG copy for the Workshop preview. You can keep the original quality for the in-game background. Rebuild and check diagnostics for valid paths and image formats.

Begin the description with what players will experience. Then explain how to enter the content, required game/API version, whether a new run is needed and known limitations. Describe features the mod actually provides.

## 3. Open release preparation and save a draft

1. Find your project in **Develop Mods** and use the package icon at the far right of its row to open release preparation. See [the visual walkthrough](../reference/visual-walkthrough.md#2-create-and-open-source) for its location.
2. Fill in the title, description, comma-separated tags and update notes.
3. Start with **Private** visibility and check the cover and previews.
4. Choose **Save Draft**. This saves the information without uploading it.

Draft information and the linked Steam item ID are stored locally in `State/Publication/<packageId>.json` under the Workshop folder. Keep that file for normal updates; do not delete the link just to retry.

## 4. Upload and inspect the item

When ready, choose **Validate and Upload to Steam**. The game compiles and validates before uploading. For missing information or invalid images, fix the first diagnostic on the page and retry.

After success, open the Steam item and check its title, description, cover, previews and visibility. If the first upload requires accepting the Workshop agreement, open **Steam Workshop Terms** and complete the steps on Steam. The item may remain hidden until you accept it.

A successful local build, saved draft or exported package does not mean the upload succeeded. Check the game's upload result and the actual Steam item. Without a working Steam connection, finish local checks and upload later.

## 5. Play the version players receive

Before making the item public, check that the downloaded release can be installed and enabled, and that its content works after a full restart. Check whether your development machine is still loading a local copy, which could hide missing uploaded files. Players need to trust and enable code packages in mod management.

The release should contain your own mod DLL, manifest, translations and assets in use. Development references, `.tmode-sdk`, `source/bin`, `source/obj` and personal saves do not belong in it. Do not edit files in `Builds`, `Installed` or a finished export. Edit `Sources` and rebuild.

## 6. Update the same item later

Edit the original project, increase `package.json.version`, build and check it, then reopen release preparation. The button should now read **Validate and Update Steam**, using the existing item ID. Add update notes and submit the update.

Check the item's notes and previews, then the actual subscribed download. Explain compatibility in advance if a change affects old saves. Keep stable package IDs, content IDs and text keys. See [the publishing manual](../04-testing-and-publishing.md) for more fields, or [Troubleshooting](../troubleshooting.md) for failures.
