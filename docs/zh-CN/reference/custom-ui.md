# 页面控件与宿主边界

[English](../../en/reference/custom-ui.md) · [Index](../README.md)

教程修订 5 · Mod API 1.8.0 · 2026-10-14


制作步骤见[自定义页面课](../tutorials/custom-ui.md)，签名见[ModUi](api-surface.md#modui)、[IModUiContext](api-surface.md#imoduicontext)。这组接口定义页面数据，宿主生成 Unity UI；不是开放 Unity 场景编辑权限。

| 类／字段 | 约束 |
| --- | --- |
| `ModScreenDefinition.Id` | 包命名空间下唯一 |
| `Placement` | StartScreenReplacement、MainMenuPage、Overlay；枚举存在不表示每处自动有入口 |
| `Root` | 非 null 控件树；页面内元素 ID 全部唯一 |
| `Controller` | 可为空；有值时属于当前 Mod 程序集 |
| `Priority` | 宿主选择替换开始页时排序；不要假定所有替换同时显示 |
| `CloseOnEscape` | 默认 true；仍要提供回退原菜单路径 |
| `MusicThemeId` | 可为空；有值须本包拥有，引用已注册主题 |
| `ModUiElement` | TextKey／TextFallback、ImageAsset、ActionId、Visible、Interactable、Style |
| `ModUiStyle` | 默认 Width/Height/MinWidth/MinHeight=-1，Gap=8、FontSize=28；负尺寸按宿主自动布局解释 |

控件种类只有 Column、Row、Panel、Text、Image、Button、Spacer、Scroll。只有四种容器可含子节点；普通 Text/Image/Button/Spacer 不能装子控件。Style 数值必须有限；宽高及最小尺寸不超过 4096，FlexibleWidth/Height 非负，Gap 0～256、FontSize 1～256，Padding 四边 0～1024。颜色用 `#RRGGBB` 或 `#RRGGBBAA`，可选颜色可空。根深度为 0，最大深度 16，每页最多 256 节点；不要把页面当无限数据表。

`IModUiContext` 仅提供本页文字、可见性、可交互性、图片更新，本包页面切换、关闭及宿主命令；没有 GetConfig/SetConfig 写入或游戏战斗状态。页面 control ID 错误时可能没有更新结果，不表示调用已产生效果。用可观察文字变化定位。

宿主动作只有 StartNewGame、ContinueGame、OpenSettings、OpenAbout、ShowOriginalMenu、QuitGame。自定义按钮 ActionId 交给控制器；HostButton 交给宿主。不要把 ActionId 写成一个不存在的宿主命令。

| 诊断 | 定位 |
| --- | --- |
| `MH_MOD_SCREEN_ID` | 页面 ID 的包前缀与重复 |
| `MH_MOD_SCREEN_CONTROLLER_ASSEMBLY` | 控制器声明在正确程序集 |
| `MH_MOD_SCREEN_MUSIC_ID` | 本包主题 ID |
| `MH_MOD_SCREEN_REPLACEMENT_DUPLICATE` | 同包只一张替换开始页 |
| `MH_MOD_SCREEN_SCHEMA` | 树节点、文本后备、按钮动作、图片文件或 Style |

来源：当前 `MiniHeroModApi.cs`、`CodeModAssemblyLoader.cs`、`ModScreenHost.cs`、`MainMenuController.cs`。编译只能证明声明可用；语言刷新、页面导航、Escape、不同屏幕比例及音乐须实机验收。
