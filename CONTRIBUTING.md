# Maintaining the bilingual guide / 双语教程维护

Keep both languages on the same technical revision. Use [English references](docs/en/README.md#reference) or [中文参考](docs/zh-CN/README.md#reference) for the reviewed API contract.

## Change procedure / 修改流程

1. Identify the source of the fact: current API/code, loader diagnostics, and actual behavior. Record API version and the affected lesson. / 先核对当前接口、加载诊断与实际行为，记录受影响页面。
2. Edit both languages, shared fragments, and expected results together. Preserve IDs, keys, formulas, conditions, and error codes. / 两种语言及片段同步，保持技术契约。
3. Update `docs/revision.json` with source and translation hashes using the command below only after reviewing both texts. / 两种语言审阅完成后再更新同步记录。
4. Run document checks. For source changes, compile against authorized current game references; for behavioral changes, use the real loader and gameplay. / 文档检查、真实编译、加载与玩法各自记录。
5. State the verified scope and remaining manual checks on the version page. / 不以窄范围检查代替整体验收。

```powershell
python tools/sync_revision.py --write
python tools/check_docs.py
```

These maintenance commands require Python 3.9 or newer; CI uses 3.13. They are optional for mod authors following the game lessons. / 维护命令需要 Python 3.9 及以上，CI 使用 3.13；玩家按游戏教程制作模组无需运行这些维护工具。

The sync command records hashes, not translation quality. Review meaning, terminology, targets, numbers, caps, state, placeholders, and English readability before marking aligned. Generated declarations have no gameplay semantics by themselves.

同步工具只记录哈希，不证明翻译质量。先核对意思、术语、目标、数字、上限、状态、参数，再进行英文冷读。接口签名不能替代运行语义。

## API changes / 接口更新

Maintainers with authorized game-source access can regenerate selected public declarations and detect drift:

```powershell
python tools/extract_api.py --source-root <authorized-game-source>
python tools/extract_api.py --source-root <authorized-game-source> --check
```

This exports signatures and relative source identifiers, not game DLLs or method bodies. Review the matching semantic reference when a declaration changes. The first lesson uses the generated namespace and manifest entry; do not silently replace them with an unrelated template namespace.

提取只导出声明和相对来源标识，不发布游戏 DLL 或方法实现。接口变化时同步审查语义页；首课保留生成命名空间与清单契约。

## Reporting a problem / 反馈格式

Provide guide revision, game/API version, page and step, expected result, actual result, and first relevant diagnostic. Share the smallest necessary source with private paths removed. Record build/loading/gameplay/Steam checks separately. / 提供版本、页面步骤、预期实际和首条诊断，只分享必要且去隐私的信息。

## Reader trials / 读者试读

Use the [reader-trial checklist](docs/en/reference/reader-trial.md) / [试读记录](docs/zh-CN/reference/reader-trial.md). Record where readers stop and how much unlisted help they need. Internal AI review is not independent player testing.

## Local checks and CI / 本地检查与自动检查

`tools/check_docs.py` uses Python standard libraries to check local links/anchors, fences, bilingual code contracts, snapshot alignment, SVG syntax, and forbidden release artifacts. It does not fetch external links, compile C#, render game UI, or verify online publishing.

`.github/workflows/docs.yml` runs these public checks when the revision is eventually pushed. It uses the documented [checkout](https://github.com/actions/checkout) and [setup-python](https://github.com/actions/setup-python) actions with read-only repository permission. This local revision has not run GitHub Actions until published. Game-reference compilation stays in an authorized local environment; do not upload references to public CI.

自动检查不证明玩家语义、界面、编译或线上发布；当前本地修订尚未推送，不把本地命令称为已执行的 GitHub Actions。
