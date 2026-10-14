# 04 测试与发布

[English](../en/04-testing-and-publishing.md) · [教程目录](README.md)

教程修订 2 · 核对日期：2026-10-13 · Mod API：1.8.0。

第一次制作先读[首课](tutorials/first-mod.md)。本文是工程手册；按目标制作见[任务目录](README.md)。

本篇用于内容完成后的系统检查。不要只确认“能编译”；还要验证注册、绑定、数值、运行时重置、资源、安装安全和全新环境下的表现。

固定布局的 `CardColumnState.cards` 按**底部到顶部**存储，最后一项是 `Exposed` 明牌；出口应放在守卫之前，才能位于守卫下方。测试必须实际点击牌面，不能只检查注册与列表长度。本仓库不附完整冒险样例包。

源码项目的目录 ID 必须和 `package.json.packageId` 相同。空 ID、损坏 JSON 和 ID 不一致现在会在准备或编译前返回诊断；没有成功构建安装时，不应改变已安装版本。排查源码错误应保留个人 `Sources`，按诊断修复清单后重试。

## 目录

1. 每种内容的基础检查
2. 宝物专项测试
3. 角色、敌人和关卡测试
4. 图片与音乐测试
5. 故障定位顺序
6. 常见错误
7. API 版本与兼容
8. 权限、信任和签名
9. 发布前打包清单
10. 游戏内发布与更新
11. 浏览与配置

## 一、每种内容的基础检查

- 内容 ID 唯一，并以包 ID 加点号开头。
- 类为 `public`，有公开无参构造函数。
- 所有内容都在 `Load` 中注册。
- 描述中的数字、上限、持续时间和真实执行一致。
- 本地化缺失时仍有可阅读的后备文本。
- 图片路径、音乐路径和代码大小写完全一致。
- 修改 C# 后在完整重启环境中至少验证一次。

## 二、宝物专项测试

每件宝物至少覆盖：

- 一级和最高等级；
- 所有实际提供的品质；
- 满血、低血、零护盾、高护盾；
- 没有敌人、单个敌人、多个敌人；
- 第一次触发、达到阈值、一次跨越多个阈值；
- 场景触发上限；
- 离开场景后计数是否按描述重置；
- 永久属性是否在场景切换后保留；
- 预览和真实执行是否一致；
- 与另一件同类百分比宝物叠加是否按统一规则结算。

功能审查还要比较：触发时机、输入依据、主收益、状态结构、目标范围、限制和代价。六项高度相同的宝物通常只是换皮，应改变决策价值或明确替换关系。

清列与自动招式专项：确认 `OnColumnCleared` 只在整列最后一张卡被移除后触发；只击败敌人但其下仍有牌时不触发。一次动作清空多列时每个新清空列各触发一次；补牌后再次清空可以再次触发。由宝物写入 `automaticInitialMoveTriggers` 后，核心才尝试自动初始招式；此字段是请求数，不是实际成功数。自动调用不带明确目标列，因此 `MoveTargetKind.Enemy` 即使面对存活敌人也无法自行选中；若需求是自动选取明牌目标，应改用 `MoveTargetKind.RandomEnemy` 并实测有目标与无目标两种情况。用 `OnAfterMoveResolved` 且 `automatic == true` 统计成功结算次数，并覆盖没有合法目标时自动招式提前停止的情况。按成功次数发护盾时使用 `e.shield += amount`，不再同时调用 `Runtime.AddShield`。当前没有把某个清列请求与其自动招式结果相关联的标识。

## 三、角色、敌人和关卡测试

角色：基础属性正确；特性显示并生效；唯一声明的开局技能确实加载为 `State.initialMove`；角色池 Tag 与宝物 `PoolTags` 有预期交集。当前选角流程不授予 `StartingTreasureTypes`，也不加载列表第二项到普通招式槽；不要把这两种声明当作已生效功能。

敌人：数值正确；`EnemyTraitId` 能找到已注册特性；受伤、回合、死亡和倒计时事件在正确时点触发；多个敌人实例的计数不会共享。

复合敌人特性：同一个特性类覆写多个回调；受伤计数只在实际扣血后增长；实例层数互不共享；`OnRoundStart` 只在普通攻击后的敌人回应阶段触发，击败或不再暴露的敌人不会触发；回合防御按设计增长且能从快照恢复。

直伤入口对照：目标型道具用 `CardEffectType.Damage`，每次只命中指定敌人；直接使用道具的 `DamageAllEnemies` 会逐个命中当前暴露敌人。分别检查 `OnAfterDamaged` 按实际扣血触发、过量伤害不多计、目标死亡后的列变化，以及两种道具都不会触发普通攻击专用的 `OnRoundStart`。和 `MultiHit` 对照时，后者按命中段数派发受伤事件，`MoveUsed` 仍只派发一次。

奇遇专项：分别测 `Action=None` 的直接效果、`Action=Meditation` 的属性候选过滤/数量/选择结算，以及非空 `richEventChoices` 对基础字段的优先级。丰富选项要覆盖可支付与不可支付的属性/金币代价、扣费后属性/宝物奖励、空槽与备用槽；不足以支付时不能发生部分扣费或发奖。确认宝物奖励已注册、两条分支结果互不串用，并验证 `richEventChoices` 路径不意外应用基础 `Effect`、`Choices` 或卡级 `goldCost`。工坊 JSON 富事件还要测：`richChoices` 条件筛选、空匹配时事件仍留在牌列、确认时重新检查条件、`event_condition_changed` 与 `event_cost_unavailable` 都保留待处理选择且无部分结算。`rewardContentId` 与正数 `rewardContentCount` 要同时填写，并确认 ID 对应已注册的宝物、招式或道具；`ItemContent` 奖励会立即执行其恢复/闪避/属性效果，不进入背包，例如 20/30 生命时奖励 1 点恢复应变为 21；招式作为已学招式加入；宝物按实例发放，检查数量和空槽/备用槽。奖励数 101 应确认后端结构化校验器不报上限错误，而运行时只发放 100 个；不完整 ID/count 配对由后端结构化校验器报 `AW_EVENT_CHOICE_REWARD_CONTENT`，但直接 JSON 包目前可能仍注册成功并在运行时静默不发奖。未知 ID 或已注册但类型不支持的引用也要分别验证：包可通过校验、选择可结算、奖励无诊断且不发放。成功的 `nextEventId` 应指向已注册事件并在原列顶部生成明牌；无效 ID 目前会静默跳过。`nextStageId` 要分别测仅注册但未列入当前冒险场景列表、以及确实存在于当前 `GameEngine` 场景列表的目标；有效目标先设置待转换状态，再通过整备界面的进入动作实际加载。结构化 Adventure 的展开关卡 ID 是 `<steps[].id>-round-<从1开始的轮次>`；`sourceStageId` 只是源关卡模板 ID。后端结构化校验器要求每个选项的 `nextEventId` 与 `nextStageId` 只能二选一，但加载运行层不替代引用检查。同一包混合 `contentIndex` 和 `codeAssembly` 时，测试两路内容均注册、ID 无冲突，且 DLL loader 无诊断。

关卡：已注册并进入预期冒险列表；随机牌池数量正确；固定列从底到顶顺序正确；出口存在且可点击。`fixedColumns` 非空时应只生成所给固定列，检查空列仍为空、`appearancePool` 的候选没有混入、运行时总牌数等于固定列牌数总和。当前 C# 注册校验在固定布局检查固定列出口，在随机布局检查候选池出口。为兼容较早版本而保留池 Exit 模板时，要确认它不会进入实际固定牌面。若配置 `StageDefinition.victoryConditions`，分别测试条件未满足时点击出口被拒绝、满足后可通过；该条件只在点击出口时检查，不会因敌人死亡自动结束关卡。`defeatedEnemies >= 1` 读取整场累计击败数，不识别具体敌人；普通敌人仍存活不会单独阻止出口，存活 Boss 会阻止。角色限制包含测试角色；敌人卡由注册的 `EnemyContent` 创建。

StageGraph：新游戏的选角前/选角后两次加载都要有可用路径；按角色 `has:` 分流时测 fallback 与选角后重算。预选时 `State.character` 为空且 `has:` 不检查候选角色列表；选角重载先设置所选角色和 `BaseStats`，数值条件读取这一刻的 `State.player`。每次重载都重建 `stageGraphVisitedNodeIds`，并在检查出边前记录当前节点，所以第二次路线不包含预览路线，但 `reach:<当前节点>` 为 true。分别验证 `reach:`/`tag:`/数值比较，检查多个匹配边按正权重抽选而不是按顺序，并用多个 seed 验证结果分布。做一条语法合法、条件始终不匹配的边，静态 registry 仍可能有效；真实 `LoadStage` 会抛 `InvalidOperationException`，指出节点在当前条件下没有可用后继。JSON 循环图应由后端结构化校验器和 registry 报 `AW_STAGE_CYCLE`。节点牌分别验证有 `card` 快照才加入 C# StageDefinition 的图路线、走到后即使 `required=false` 也被设为必出；可选牌应来自随机 `appearancePool`。分别走到 `Victory` 和 `Failure` 节点后再点击实际 Exit；Failure 在出口结算时判负，Victory 仍受出口与 `victoryConditions` 限制。检查 `contentId`：结构化 Workshop stage 会据此创建节点卡，C# `StageContent` 必须自行填 `node.card`。

结构化 JSON StageGraph：确认 `contentIndex` 的 `stage` ID 与文件根部 `id` 一致；`cards` 映射到 `appearancePool`，并含 `kind:2, guaranteed:true` 的 Exit。枚举按 Unity JSON 数值写：卡池 `Content=0/TreasureChest=1/Exit=2/Intermission=3`，节点 `Start=0/Encounter=1/Event=2/Camp=3/Exit=4/Victory=5/Failure=6`。分别注册 Event 与 Treasure 节点，核对 `contentId` 自动建卡、无需重复放进 `cards`，进入访问路线后两张卡都为必出，即使 `required:false`。用未注册节点 ID 检查 `AW_STAGE_REFERENCE`；由 Adventure 的 `steps[].sourceStageId` 引用 JSON Stage，验证其可展开并加载。实体 Exit 仍然决定最终离场结算；测试应实际点击出口。

Boss：首领卡设置 `CardState.isBoss`；首领冒险步骤设置 `AdventureStepDefinition.boss`；单独作为首领关的素材 Stage 还要设置 `StageDefinition.boss`。分别检查加载诊断、展开后的末轮 boss 标记，并确认生成牌组中的首领是否由 `guaranteedInStage` 保证。

## 四、图片与音乐测试

图片：检查图标、角色立绘、头像、敌人战斗图、关卡背景、地图缩略图和抵达图；确认透明边缘、主体安全区、缩放方式和不同分辨率下的裁切。

尺寸验收：角色主图 `Icon` 使用 284×512（71:128），`Avatar` 与 `BattleArt` 使用 1:1，`Portrait` 作为兼容回退时建议也使用 284×512，宝物和招式图标使用 1:1；3×2 原始素材表不应被代码直接引用。生成图裁切后要重新构建，使 `assets/asset-index.json` 记录最终文件。

音乐：普通关卡播放 `StageExplore`；Boss 优先 `BossBattle`；缺少 Boss 曲时先回退同主题的 `StageExplore`；探索曲缺失或加载失败时回退游戏内置游戏内音乐列表；普通关卡引用一个只含 `BossBattle` 的主题时回退游戏内置列表；全局音量和 Mod 相对音量生效；曲目结束后能继续播放；停用 Mod 或切换关卡后不会继续引用错误主题。

## 五、故障定位顺序

1. 先在终端运行 `dotnet --version`；保留生成的 csproj 和游戏开发引用，再执行构建。开发页的“可构建”行状态不能代替 SDK 检查。
2. 编译失败先找第一条包含 `.cs(行,列)` 的错误，后续错误可能只是连锁结果。
3. 安装失败查看哈希诊断，不要直接改 Builds。
4. 能安装但没有内容，核对包 ID、入口类型、`codeEntryPoint`、启用状态和重载结果。
5. 内容出现但绑定缺失，检查被引用类型/ID 是否已注册；如果看到 `引用不存在或类型错误: <package>.character.<name>`，先检查角色类是否 public、ID 是否仍以当前 `packageId` 开头，以及 `Load` 是否实际注册了这个角色。只写角色类但漏掉 `registrar.AddContent(new YourCharacter())` 会在重载阶段直接失败。
6. 规则不生效，检查是否覆写了正确事件、字段语义和 `SourceLevel`。
7. 图片不显示，检查标准目录、相对路径、大小写、展示槽位和素材索引。
8. 音乐不播放，检查主题注册、关卡 `music`、OGG/WAV 文件和 Boss 标记。
9. DLL 已加载过时，完整退出并重启再判断。

## 六、常见错误

- `MH_MODSOURCE_DOTNET`：无法启动 dotnet，安装或修复 .NET SDK。
- `MH_MODSOURCE_BUILD`：C# 编译错误，按文件名与行号修复。
- `MH_MOD_API_INCOMPATIBLE`：Mod 要求的 API 超出当前游戏支持范围。
- `MH_MOD_MUSIC_ID`：音乐主题 ID 不属于包或重复。
- `MH_MOD_MUSIC_ASSET`：音乐文件不存在或不是 OGG/WAV。
- `MH_MOD_PRESENTATION_ASSET`：图片路径、索引或槽位不正确。
- `AW_BUILD_HASH_MISSING`：不是构建产物或缺少哈希清单。
- `AW_BUILD_HASH_MISMATCH`：构建后文件发生变化。
- 内容 ID 不属于当前包：ID 没有以 `packageId + "."` 开头。
- 宝物抽不到：先检查角色 `TreasurePoolTags` 与宝物 `PoolTags` 是否有相同项；若角色覆写了 `TreasurePool`，再检查该 ID 是否被 `Exclude`，或是否需要通过 `Include` 强制加入。
- 角色没有技能或特性：相应类型未注册或角色引用了错误类型。
- 关卡没有敌人：没有通过注册表取得敌人并调用 `CreateCard`。

## 七、API 版本与兼容

当前 Mod API 为 **1.8.0**，最低兼容版本为 **1.0.0**。只使用旧能力的旧版 Mod 可以继续加载。使用 `AddCharacterToLevel` 把角色加入已有大关卡时，`package.json` 应写：

```json
{ "modApiVersion": "1.7.0" }
```

Mod 声明高于当前游戏的版本会被拒绝，因为运行时可能没有它调用的方法。使用冒险规则、循环、种子或动态续接等 1.8 能力时，声明 `modApiVersion: "1.8.0"`。API 的程序集主版本保持稳定，以减少只增加便捷方法时对旧 Mod 的破坏。

## 八、权限、信任和签名

C# Mod 必须声明 `code.execute`。DLL 与游戏进程拥有相同本机权限，因此只启用来源可信的代码 Mod。

哈希用于发现内容变化，不是作者签名。当前作者字段没有平台认证，系统也尚未提供证书签名。信任确认绑定精确的包 ID、版本和内容哈希；文件一变就重新确认。

## 九、发布前打包清单

- 提升 `package.json` 版本号；相同版本不要发布不同内容。
- 包含 `package.json`、自己的 Mod DLL、实际使用的本地化、图片和音乐。
- 不包含开发引用目录、`source/bin`、`source/obj`、开发缓存、游戏 API/Core DLL。
- 从全新安装状态测试一次，不只依赖现有缓存。
- 验证构建哈希和安装复制哈希一致。
- 在说明中列出依赖版本、配置项、需要重启的变更、已知限制。
- 确认没有绝对磁盘路径、个人账户目录、临时文件或私密信息。
- 保留源码版本和发布包的对应关系，便于之后复现问题。

## 十、游戏内发布与更新

1. 进入「开发模组」，选择自己的源码项目。「打开选中源码」可修改 `package.json` 的版本、封面和预览图路径。教程正文从随游戏发布的只读目录读取，个人 `Sources` 是作者可编辑工作区。
2. 点击「发布准备」，填写发布标题、简介、逗号分隔的标签和版本说明；可见性默认私密。
3. 「保存草稿」只保存元数据，允许尚未填写完整，草稿位于工坊根目录 `State/Publication/<包ID>.json`。
4. 「校验并上传 Steam」会检查必填信息、编译 C#、校验包、图片路径和构建哈希，再导出到 `Exports/<包ID>/<版本>-<唯一编号>/`。游戏不会安装或执行该 DLL。校验通过后，游戏通过 Steam 创建新条目，或更新本机已绑定的同一条目。
5. 首次创建获得的 Steam 条目 ID 会立即写入 `State/Publication/<包ID>.json`；上传失败时可重试同一条目，不要删除此文件。更新前提升 `package.json` 的版本号。导出目录中 `content/` 是上传内容，`publication.json` 是导出时的元数据。`coverAsset` 会作为 Steam 条目主封面上传；`previewAssets` 会作为详情页的额外展示图上传。更新时会复用同一个条目，并按当前 `previewAssets` 列表替换旧展示图。
6. 默认可见性为「私密」。上传按钮旁可打开 Steam 创意工坊协议；首次发布后若 Steam 要求接受协议，条目在接受前会保持隐藏。

封面必须通过清单 `coverAsset` 指定包内图片相对路径；可选的 `previewAssets` 保存详情页额外展示图路径。游戏将封面与展示图交给 Steam，当前本地校验只接受真实格式正确的 PNG、JPG 或 JPEG，不接受 GIF。每张图片的任意一边不得超过 4096 像素，文件必须严格小于 **1,048,576 字节**（1 MiB，界面简称 1 MB）。横向展示图建议使用 16:9，例如 1280×720 或 1672×941，再压缩文件体积。冒险封面可使用独立的 1:1 图片；角色主图与头像继续服务角色界面，不兼任工坊封面。

发布前逐个检查 `coverAsset` 和 `previewAssets` 的真实文件大小。游戏内的 `StageBackground` 可以继续使用高分辨率 PNG，但不要直接把它当作工坊展示图；例如 `1672×941` 的复杂背景 PNG 很容易超过 1 MB，应另存为压缩后的 JPG 展示图，再把 JPG 路径写入 `previewAssets`。只改文件扩展名不会压缩文件，必须真正重新编码并重新构建。

游戏上传仅在 Steam 客户端成功初始化、当前 App ID 为 `5302070` 时执行；还需要相应 Steamworks 工坊权限与后台配置。当前代码已接入订阅扫描、下载请求和下载后的包导入；代码包下载后仍需在管理页信任并启用。真实 Steam 客户端下的上传、订阅、更新和下载仍应分别实测。没有 Steam 账号和后台权限时，可以完成本地构建与校验，但无法完成在线流程验证。

## 十一、浏览与配置

模组浏览按包 ID 合并重复来源和历史版本，优先提供最新可用包；可筛选未安装、可更新、需要修复，按名称、最近修改或体积排序。安装成功后可以直接前往管理，代码模组仍需信任确认和启用。

当前没有玩家可打开的 Mod 配置页。`AddConfig` 与 `ModConfig` 保留底层兼容接口；制作与验收使用源码中的默认值。不要在发布说明中承诺玩家可在工坊修改开关、枚举、数字或文本。修改 C# 默认值后重新构建安装，并完整重启游戏验证。
