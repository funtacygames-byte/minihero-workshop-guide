# C# mod isolation

[简体中文](../../zh-CN/reference/security.md) · [Versions](versions.md)

The sandbox currently supports Windows x64 Mono builds. Local development-build checks passed on 2026-10-16; release-build verification and Steam upload remain pending. This page does not establish that an installed Steam build already includes it; older builds run mod DLLs with the game's local permissions.

In sandbox builds, downloaded C# mod code runs in a separate Windows AppContainer process. When enabled mods register gameplay content, the complete rules engine runs there too. The game renders the UI and exchanges bounded game data with that process. It does not load downloaded DLLs into the Unity process.

The worker receives independent, read-only copies of its runtime and mod packages. It receives no network capabilities, cannot start child processes, and cannot open the game's memory or interactive desktop. A startup failure, invalid reply or worker exit stops the isolated session; it never retries a DLL inside the game process.

Normal play imposes no fixed worker memory limit, CPU-rate limit or cumulative CPU-time limit. Startup handshakes, package loading, engine creation and rule/UI calls have no automatic deadline. Requests wait until they return or the isolated session is closed. Message-size, type and path checks still apply.

Keep using the existing C# content classes and package layout. Reading arbitrary files, downloading files, starting programs and manipulating Unity scene objects are outside the supported mod API. An existing DLL that relies on those operations needs changes. Mods in the same enabled package set share one worker, so isolation protects the rest of the computer; it does not prevent one enabled mod from interfering with another enabled mod's gameplay.

Save files are written by the game, using bounded state returned by the worker. Keep a recoverable copy before trying an older modded save: pre-sandbox saves containing third-party serialized types still need migration verification. Regenerate development references after updating the game.

If isolation cannot start, verify the game files, restart the game and check the workshop diagnostic. Do not work around the error by running the mod DLL yourself. Package hashes and trust confirmation still identify the exact files you enabled; they do not certify the author or the quality of a mod.

Windows enforces the process boundary. See Microsoft's [AppContainer isolation](https://learn.microsoft.com/en-us/windows/win32/secauthz/appcontainer-isolation) and [launching an AppContainer](https://learn.microsoft.com/en-us/windows/win32/secauthz/implementing-an-appcontainer) documentation.
