# 功能片段使用说明

[English](README.md) · [教程目录](../docs/zh-CN/README.md)

文件采用 `.cs.txt` 后缀，避免被误当成同时编译的完整 Mod。只复制需要的部分到游戏生成的 `source/ModEntry.cs`。

1. 将所有 `your.package` 替换为自己的稳定包 ID。
2. 保证 `[MiniHeroMod(...)]`、`package.json.packageId` 与源码目录 ID 一致。
3. 在 `Load` 中注册所有用到的内容；内容 ID 必须以包 ID 加点号开头。
4. 保留生成的 `.csproj`、游戏引用和 DLL 输出路径；补上需要的 `using` 与被引用类。

| 片段 | 用途 |
| --- | --- |
| [01](zh-CN/01-entry-and-config.cs.txt) | 最小入口与底层兼容配置 API |
| [02](zh-CN/02-character-trait-and-move.cs.txt) | 角色、特性与初始招式 |
| [03](zh-CN/03-character-treasures.cs.txt) | 角色专属宝物池 |
| [04](zh-CN/04-enemies-and-traits.cs.txt) | 敌人与敌人特性 |
| [05](zh-CN/05-stage-bindings.cs.txt) | 关卡绑定敌人与可选角色 |
| [06](zh-CN/06-stage-music.cs.txt) | 关卡音乐主题 |
| [07](zh-CN/07-three-region-adventure.cs.txt) | 将已注册的素材关卡连接为冒险 |

中英文片段的技术标识和公式相同，注释与后备文本分别翻译；制作双语模组时，通过 `ModText.Get/Format` 读取 `localization/en.json` 与 `zh-Hans.json`。配置声明不会生成玩家可编辑的菜单，当前没有 Mod 配置页。

部分片段引用了需要自己提供的类或资源。这七份片段不是完整冒险、可构建工程或可安装包。整合后按[测试清单](../docs/zh-CN/04-testing-and-publishing.md)验收。
