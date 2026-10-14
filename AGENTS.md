# Instructions for contributors and AI assistants

This is a bilingual tutorial repository. Keep English and Simplified Chinese chapters aligned in mechanics, numbers, conditions, limitations, and code identifiers. Read `docs/en/ai-authoring.md` or `docs/zh-CN/ai-authoring.md` before changing authoring instructions.

- Publish tutorials, focused fragments, and neutral reference diagrams. Do not add complete adventure examples or Starfall Expedition assets without a new user request.
- Check claims against the current game/API rather than historical plans. The reviewed baseline is guide revision 4, API 1.8.0 on 2026-10-14; state unverified behavior accurately.
- Author gameplay in C# content classes. Do not route players or AI to declarative gameplay JSON, contentIndex recipes or a JSON authoring editor. Generated manifests, translation catalogs and saves are auxiliary data; identify their purpose clearly.
- Keep package/content IDs, localization keys, and API names stable. Translate displayed values.
- MiniHero uses Western fantasy/fairy-tale adventure. Yaoguang is the explicitly authorized ancient Chinese heroine exception.
- Healing-linked rules read settled `AfterHealingEvent.requested`, including overflow. `actual` serves only HP resources and presentation; explicit overflow effects read `overflow`.
- Treasure temporary state resets on new-stage entry unless explicitly specified otherwise. Keep per-instance state, preview/execution agreement, shared percentage settlement, and base-stat conversions.
- Category, pool, and appearance tags have separate purposes. Pool matching uses any intersection.
- Preserve caps, targets, costs, durations, and special conditions in both languages. Use natural concise text; do not resize game UI to fit translations.
- Do not claim player configuration or JSON editor pages exist. Distinguish local export from online Steam verification and reloading from full-restart DLL verification.
- Never package game binaries, saves, private paths, credentials, Unity caches, or development references. Do not start or duplicate Unity projects for documentation validation.

- Read `llms.txt` and `docs/capabilities.json` to route tasks; capability status is not test evidence. New card choices use preview-only card faces and stable registered resolvers; do not inherit legacy rich-event branch limits.
