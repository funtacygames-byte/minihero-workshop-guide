# 展示、文本与音乐接口

[English](../../en/reference/presentation.md) · [目录](../README.md)

教程修订 6 · Mod API 1.10.0 · 2026-10-17

当前基准 1.10.0。操作教程见[资源与双语文本](../tutorials/assets-and-text.md)，全部槽位规格见[资源总览](../03-assets-and-presentation.md)。

## 图片签名与槽位

```csharp
public interface IModPresentationContent
{
    ModPresentation Presentation { get; }
}
public static ModPresentation Icon(string path);
public static ModPresentation Character(string portrait, string avatar = "");
public static ModPresentation Enemy(string battleArt, string icon = "", string intentIcon = "");
public static ModPresentation Stage(string background, string mapThumbnail = "", string arrivalArt = "");
public static ModPresentation Create(params (ModPresentationSlot slot, string path)[] assets);
```

这些是接口与 `ModAssets` 静态方法摘录。工厂返回展示映射，不自行加载图片。`Character` 使用 Portrait／Avatar 兼容槽位；当前角色主图应明确用 `Create` 绑定 `Icon`，见[添加角色图片](../tutorials/assets-and-text.md#角色和敌人也想换图)。路径相对于包根，构建生成索引；空可选路径会跳过，非空路径必须存在且符合槽位类型。

| 槽位 | 制作规格／用途 |
| --- | --- |
| 宝物／招式 Icon | 1:1 图标 |
| 角色 Icon | 71:128 高竖幅、完整不透明场景背景；显示框 284×512，源图可更大 |
| 角色 Avatar | 4:5 带背景肖像，如 1024×1280；选人小头像取顶部 1:1 |
| 角色 Portrait | 兼容主图回退，建议 71:128 |
| 敌人 BattleArt | 1:1 战斗图 |
| StageBackground／StageMapThumbnail／StageArrivalArt | 背景／选关图／抵达图，按实际槽位裁切 |

“规格正确”仍需实际看主体安全区与原版面；不可用扩框、改字号来补翻译问题。

## 文本签名与失败行为

```csharp
public static string Get(string packageId, string key, string fallback = "");
public static string Format(string packageId, string key, string fallback, params object[] arguments);
```

这是 `ModText` 方法。Get 使用当前宿主 resolver，未配置时返回 fallback。Format 先取字符串，再用当前文化 `string.Format` 插入参数；格式错误捕获后返回未展开模板。后备文字仍应可独立阅读，不能依赖一定存在的英文目录。

工坊包使用 `localization/<locale>.json` 的 `locale` 与 `entries[{key,value}]`，与游戏内部 V2 文本表不同。新增键用 ASCII 语义标识，两种语言键与占位符编号一致；清单 `supportedLocales/defaultLocale` 对应文件。宿主的 `ConfigureResolver` 给游戏使用，Mod 不调用。

## 音乐契约

`ModMusicTheme(string id, IReadOnlyDictionary<ModMusicCue, string> tracks)` 注册主题；ID 以包 ID 加点号开头且唯一。文件为包内 OGG/WAV，不能逃出根目录。`StageDefinition.music` 引用已注册主题，未知主题会报 `MH_MOD_STAGE_MUSIC_MISSING`。

普通场景用 StageExplore，Boss 场景优先 BossBattle，再同主题 StageExplore，再内置游戏内列表。文件存在但解码失败也走回退。自定义页面通过 `ModScreenDefinition` 的 `musicThemeId` 使用 MainMenu；Victory 未接为 Mod 胜利页音乐。槽位由场景 boss 标记决定，不由一张敌人卡单独决定。

`AddConfig/ModConfig` 的兼容限制统一放在[兼容页](compatibility.md)。配置声明不生成当前玩家可编辑菜单。
