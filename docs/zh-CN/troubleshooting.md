# 按症状排查模组问题

[English](../en/troubleshooting.md) · [目录](README.md)

教程修订 2 · API 1.8.0 · 2026-10-14

先定位失败阶段，再修复对应文件。保留 Sources，不在 Builds 或 Installed 直接改文件。当前基准 API 1.8.0，教程修订 2。

## 先取得真实错误

先在终端执行 `dotnet --version`，回开发页执行构建。项目行“可构建”表示源项目满足构建入口条件，并不是 SDK 检测结果；当前界面没有独立的 SDK/API 状态面板。构建或安装失败时，当前界面会自动打开诊断文件夹；打开其中的 `install-failure.txt`。若自动打开失败，工坊根目录的 `InstallFailures/<packageId>/<时间戳>/` 保存同一报告。

报告包含操作、包 ID、源码/构建位置、稳定错误码、字段路径和内容 ID。先找第一条 C# `.cs(行,列): error CS...`，修复其位置，再重新构建；后续报错可能是连锁结果。管理页的包详情也显示加载诊断。报告中的个人路径在分享前替换为 `<project>`。

不要只截最后一行“构建失败”，它无法区分环境、语法、清单或资源问题。

`AW_INSTALL_FAILED` 提示“相同版本已有不同内容”：在 Sources 清单中提升 `version`，重新构建并安装，包 ID 保持稳定。安装已经被拒绝时，单纯重启无法解决。

## 不能编译

| 观察／错误码 | 下一步 | 修好后应看到 |
| --- | --- | --- |
| `MH_MODSOURCE_DOTNET` | 终端 `dotnet --version`；安装 SDK 后重进开发页 | 命令输出版本，重新构建能启动编译 |
| `MH_MODSOURCE_SDK` | 使用支持 C# 模组的 Windows Mono 游戏版本并重新生成开发引用 | 当前 API/Core 可用于编译 |
| `MH_MODSOURCE_BUILD` / CS 错误 | 从第一处文件与行号修复；检查漏 using、括号、抽象属性 | 生成本包 DLL |
| ID 目录与清单不同 | 核对源目录、packageId、入口特性；不任意重命名发布 ID | `MH_MODSOURCE_ID_MISMATCH` 消失 |
| 编辑器标红但游戏能构建 | 保留生成 csproj，刷新开发引用；检查编辑器占用 | 编辑器与游戏使用同份引用 |

## 能编译但无法加载

1. 管理页确认正确包已启用，构建安装成功；完整退出并重启。
2. `MH_MOD_ENTRYPOINT_MISSING`：`codeEntryPoint` 必须等于含命名空间的公开入口类型。参考 [入口表](reference/entry.md)。
3. `MH_MOD_PACKAGE_ID_MISMATCH`：清单 packageId 与 `[MiniHeroMod(...)]` 参数完全相同。
4. `MH_MOD_ASSEMBLY_MISSING`：`codeAssembly` 指向真实输出；不能只复制源码当安装包。
5. `MH_MOD_API_INCOMPATIBLE` / `MH_MOD_DEPENDENCY_LOAD`：使用当前游戏引用重新构建，检查不支持的 API 或依赖。游戏 API/Core 不放进 mod/。
6. `MH_MOD_LOAD_FAILED`：看完整异常和对应注册；类公开、有无参构造函数，ID唯一，被引用内容均注册，资产路径有效。

成功后先用宝物图鉴“全部角色”筛选搜索首课宝物。加载失败时不要靠随机宝箱测试。

## 内容存在，但效果没触发或宝物抽不到

先核对事件时间：进场宝物在进场后才领取，要到下一场测试。描述与执行是否共用公式？`SourceLevel` 是否被误当品质？治疗关联是否读完整 `requested`？招式后护盾是否同时累加又立即加盾？按[事件契约](reference/events.md)定位。

宝物抽不到时先查最终角色 TreasurePool、PoolTags 的任意交集、Include/Exclude、品质与出场条件；CategoryTags 不控制候选，允许入池不保证随机出现。使用[固定领取事件](tutorials/treasure.md)区分“规则效果有问题”和“随机尚未抽到”。

## 改完仍然是旧效果

编辑 Sources，保存全部文件，重新构建安装，确认无失败诊断，完整退出全部游戏进程并重新启动，新开一局验证。旧存档的已生成牌与运行时实例可能保留旧数据；结构修改需要新局检查。同进程重载不是 C# 热卸载。

## 角色或图片不完整

`AW_CHARACTER_EMPTY_TREASURE_POOL`：角色最终宝物池需要可入池的已注册宝物。角色课保留生命构筑 Tag 作为入门候选；只用自定义 Tag 时，须先注册与该 Tag 匹配的宝物再加载。

引用角色／特性／招式不存在：检查具体类是否 public、ID是否本包命名空间、Load是否注册。只有源码类还不够。StartingTreasureTypes 不发奖，后续 StartingMoveTypes 不自动装备，见[限制](reference/compatibility.md)。

`MH_MOD_PRESENTATION_ASSET`：检查文件存在、包内相对路径、大小写、标准目录、索引和槽位。角色主图检查 Icon，Portrait 只是兼容回退；1:1 头像不要直接充当 71:128 主图。图片尺寸正确仍需实机检查裁切。

## 关卡没有入口、守卫或合法出口

只注册 Stage 不创建 Adventure 入口。核对 Adventure 注册和 IncludeInSelection、难度与角色名单。固定牌从底到顶，最后一张明牌；出口先加入，守卫后加入。固定列不随机补牌。

`AW_ADVENTURE_STEP_RANGE`：列数 1～5，轮数至少1，cardsPerRound 在列数到100之间；固定布局也经过步骤字段校验，但实际牌数仍由 fixedColumns 决定。本课用名义5、实际2。

`AW_STAGE_EXIT_MISSING`：当前 C# 注册校验在固定布局检查固定列出口，随机布局检查候选池出口。兼容较早版本可保留池 Exit 模板，确认它没有混入固定牌场。条件未满足或存活 Boss 也会阻止实际离场；图 Victory 节点不代替实体出口。

## 资源、安装或发布失败

| 诊断 | 处理 |
| --- | --- |
| `MH_MOD_MUSIC_ID` / `MH_MOD_MUSIC_ASSET` | 核对主题 ID、注册、OGG/WAV 相对路径 |
| `MH_MOD_STAGE_MUSIC_MISSING` | Stage.music 对应已注册主题，或清空不需要的绑定 |
| 原始 `{0}` 直接显示 | 检查文本键、参数数量和 string.Format 语法 |
| `AW_BUILD_HASH_MISSING/MISMATCH` | 从 Sources 重建，不在构建后改文件 |
| 发布预览图无效 | 按发布准备页诊断提供最终有效文件，再校验 |
| Steam 已提交却隐藏 | 完成真实协议与可见性检查；本地导出不证明在线成功 |

## 给维护者的最小复现

提供游戏/API/教程版本、包 ID、具体教程链接与步骤、预期与实际、第一条稳定错误码和必要源码。把名称、等级、次数和目标写清，移除私密信息。复杂模组先缩到能稳定复现的少量内容；不要上传游戏 DLL、整份存档或凭据。入口、加载、玩法和线上交付记录分开，见[版本与验证](reference/versions.md)。
