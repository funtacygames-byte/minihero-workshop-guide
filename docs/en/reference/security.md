# C# mod isolation

[简体中文](../../zh-CN/reference/security.md) · [Versions](versions.md)

The Windows sandbox implementation was tested on 2026-10-16. It is awaiting release-build verification and upload. This page does not establish that an installed Steam build already includes it; older builds run mod DLLs with the game's local permissions.

In sandbox builds, C# mods and their gameplay rules run in a separate Windows AppContainer process. The game renders the UI and exchanges bounded game data with that process. It does not load downloaded DLLs into the Unity process.

The worker receives independent, read-only copies of its runtime and mod packages. It receives no network capabilities, cannot start child processes, and cannot open the game's memory or interactive desktop. The game limits worker memory, CPU use and call duration. A startup failure, invalid reply or timeout stops the isolated session; it never retries a DLL inside the game process.

Keep using the existing C# content classes and package layout. Reading arbitrary files, downloading files, starting programs and manipulating Unity scene objects are outside the supported mod API. An existing DLL that relies on those operations needs changes. Mods in the same enabled package set share one worker, so isolation protects the rest of the computer; it does not prevent one enabled mod from interfering with another enabled mod's gameplay.

Save files are written by the game, using bounded state returned by the worker. Keep a recoverable copy before trying an older modded save: pre-sandbox saves containing third-party serialized types still need migration verification. Regenerate development references after updating the game.

If isolation cannot start, verify the game files, restart the game and check the workshop diagnostic. Do not work around the error by running the mod DLL yourself. Package hashes and trust confirmation still identify the exact files you enabled; they do not certify the author or the quality of a mod.

Windows enforces the process boundary. See Microsoft's [AppContainer isolation](https://learn.microsoft.com/en-us/windows/win32/secauthz/appcontainer-isolation) and [launching an AppContainer](https://learn.microsoft.com/en-us/windows/win32/secauthz/implementing-an-appcontainer) documentation.
