# Fragments and dependencies

[简体中文](README.zh-CN.md) · [Index](../docs/en/README.md)

Guide revision 2 · API 1.8.0 · 2026-10-13

The `.cs.txt` extension avoids compiling every fragment into one mod. Copy only the required fragments as `.cs`, keeping the generated csproj and manifest. These files are not installable packages.

## Integration rules

1. Fragment 01 supplies the complete entry. Keep one ModEntry and put other classes in its namespace.
2. Defaults are local.alice.lantern-trail and LocalAliceLanternTrailMod. Another ID needs matching source, full entry type, and manifest; renaming display text is not enough.
3. The custom pool tag treasure_pool.your_package.lantern is a separate technical string; character and treasure sides must match.
4. Register every referenced content in Load. Nonempty art bindings require files; follow the lesson to remove the interface and entire Presentation property for rules-only checks.

| Fragment | Purpose | Required dependencies |
| --- | --- | --- |
| [01](en/01-entry-and-config.cs.txt) | Complete minimal entry + relic | No external assets; adapt ID and namespace |
| [02](en/02-character-trait-and-move.cs.txt) | Character + trait + move | Three supplied images; rules-only route in character lesson |
| [03](en/03-character-treasures.cs.txt) | Character-pool treasures | Matching character tags from 02; compass icon |
| [04](en/04-enemies-and-traits.cs.txt) | Enemy + trait | Wolf battle art, or remove binding for rules checks |
| [05](en/05-stage-bindings.cs.txt) | Random source-stage bindings | Character 02, enemy 04, three stage images, separate Adventure |
| [06](en/06-stage-music.cs.txt) | Music theme | Your OGG/WAV files; stage references theme |
| [07](en/07-three-region-adventure.cs.txt) | Three-region connection structure | Three registered stages; not a standalone project |
| [08](en/08-fixed-stage-lab.cs.txt) | Minimal fixed stage + entry | PackageId from 01; no external assets |
| [09](en/09-relic-grant.cs.txt) | Specific reward encounter | Relic 01; register and place in board 08 |

Use 01 for the first visible result, then 08 and the treasure lesson’s 09 integration for deterministic gameplay. Use 02–07 as needed rather than copying all contents. Fragment 01 retains its old filename for links; configuration is now under [Compatibility](../docs/en/reference/compatibility.md).
