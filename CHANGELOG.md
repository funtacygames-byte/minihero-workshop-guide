# Guide revisions / 教程修订

## Unreleased — 2026-10-16

- Documented the Windows AppContainer implementation, supported C# contract and pending release verification. / 补充 Windows AppContainer 隔离实现、受支持的 C# 接口范围及待完成的发行验证。
- Updated the sandbox policy: no fixed memory, CPU-rate or cumulative CPU-time quotas, and no automatic startup, loading or call deadlines; permission isolation and protocol validation remain. / 同步沙箱策略：不设固定内存、CPU 速率和累计 CPU 时间配额，不设启动、加载或调用的自动超时；保留权限隔离与协议校验。
- Clarified that local Windows x64 Mono development-build checks passed; release-build verification and Steam upload remain pending. / 明确本地 Windows x64 Mono 开发构建检查已通过，仍待发行构建验证和 Steam 上传。
- Distinguished old in-process builds from sandbox builds in both safety sections. / 在两处安全说明中区分旧版进程内加载与沙箱版本。

## Guide revision 5 — 2026-10-14

- Rewrote the home pages and introductory route around making, playing and changing a mod. / 首页和入门三课按玩家能做出的结果组织。
- Reworked AI help into optional prompts, file-sharing guidance and steps for using the answer. / AI 页改为玩家如何提问和使用结果。
- Clarified copy destinations, registration, text merging, paid-choice testing and four-potion counter checks. / 补清文件、注册、文本合并、付费选择和四瓶药剂的操作。
- Character and enemy fragments now start with fallback artwork; custom images are added in the asset lesson. / 角色和敌人默认使用后备图片，美术绑定放入素材课。
- Moved earlier verification records to contributor notes and kept existing tutorial and fragment URLs. / 历史检查归入维护资料，保留原页面和片段链接。

## Guide revision 4 — 2026-10-14

- Kept gameplay authoring in C# and removed declarative gameplay JSON recipes from player/AI routes.
- Added bounded continuation and complete chained-choice classes, 65 bilingual text keys and 87 selected API types / 773 declarations.
- Corrected serializable counters, roster metadata, graph-validation limits, build/version/restart instructions and fixed-font text.
- Ran current-SDK builds, real workshop services, Unity state restoration, loop/chain checks and formal-scene bilingual choice clicks. Verification limits remain on both version pages.

## Revision 3 — 2026-10-14 (local changes / 本地改动)

- Add seven bilingual task lessons for items/events, new card choices, stateful rules, custom pages, configuration, adventure modes and debugging. / 新增七条双语任务路径。
- Add four fragment pairs and choice/UI/condition contracts with costs, turns, rollback and saves. / 增加四组片段及完整结算契约。
- Add a feature map, 16-capability machine index and llms.txt; rewrite the AI delivery contract. / 增加功能地图、16 项机器索引和 AI 制作合同。
- Expand selected declarations from 43 types/415 declarations to 84 types/755 declarations, including protected extension points and enums. / 扩充真实 API 索引。
- Check bilingual JSON keys/numbers/placeholders and capability routes; fix the missing Chinese asset JSON example. / 加强双语检查并补齐旧手册示例。
- Compile 26 fragment files plus inline configuration/mode overrides; run 46 pure rule checks per language. / 双语编译与规则验证。
- Keep prior paths and historical UI evidence; no GitHub push or Steam publication. / 保留旧链接，分开记录本轮与历史验证。

See [current scope](docs/en/reference/versions.md) / [本轮验证范围](docs/zh-CN/reference/versions.md).

## Revision 2 — 2026-10-14 (local draft / 本地修订)

- Add eight task lessons in English and Simplified Chinese, with prerequisites and observable checks. / 增加八篇双语任务教程。
- Unify the entry and starter; add fixed-board and explicit-reward fragments. / 统一入口与入门宝物，补固定牌场和明确奖励。
- Separate references, lifecycle, diagnostics, versions, and compatibility. / 分离接口、生命周期、排错、版本与兼容。
- Correct current fixed-layout exit validation and adventure step-count requirements. / 修正固定布局出口和步骤牌数校验说明。
- Fix tutorial dependencies exposed by real loading: nonempty character pools, version increments, and the generated English relic name. / 根据真实加载修正角色空池、安装版本递增和生成英文名称。
- Add selected generated API declarations and local document maintenance tools. / 增加公开声明提取和维护检查。
- Add four English UI screenshots and seven shared diagrams, including source layout, reports, and icon export. / 增加四张英文实机图及七张共用示意图，含源码目录、报告与图标导出。
- Correct visible SDK-check instructions and codex quality/level behavior after actual UI review. / 实机复核后修正 SDK 检查入口、图鉴品质与等级说明。
- Preserve all four original manual paths and existing fragment links. / 保留原手册和片段路径。

See [validation scope](docs/en/reference/versions.md) / [验证范围](docs/zh-CN/reference/versions.md). No complete adventure package or standalone game art assets are included.

## Revision 1 — 2026-10-13

Initial bilingual manuals, seven fragment pairs, terminology, AI entry, and two neutral diagrams. Published baseline commit: `f05df128d040a6f8ed5c76022e5126e631968911`.
