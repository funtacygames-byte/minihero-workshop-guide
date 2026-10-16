# C# 模组隔离

[English](../../en/reference/security.md) · [适用版本](versions.md)

Windows 沙箱实现在 2026-10-16 完成了本机验证，仍待发行构建验证和上传。本页不能证明玩家已安装的 Steam 构建包含沙箱；旧版本中的 Mod DLL 仍以游戏的本机权限运行。

带沙箱的版本将 C# Mod 和玩法规则放在独立的 Windows AppContainer 进程中运行。游戏负责绘制界面，并与该进程交换有大小限制的游戏数据。下载的 DLL 不会加载到 Unity 主进程。

隔离宿主只获得运行时和模组包的独立只读副本，不获得网络能力，不能启动子进程，也不能打开游戏主进程的内存或交互桌面。游戏限制其内存、CPU 用量和每次调用时长。启动失败、返回数据不符合协议或调用超时，都会停止该隔离会话，不会改为在游戏进程内运行 DLL。

继续使用现有的 C# 内容类和包目录即可。读取任意文件、下载文件、启动程序和操作 Unity 场景对象均不属于受支持的模组 API；依赖这些操作的旧 DLL 需要修改。同一组启用的模组共用一个隔离宿主，因此沙箱保护的是电脑上的其他内容，不保证启用的模组之间互不影响玩法。

存档由游戏根据隔离宿主返回的有大小限制的状态写入磁盘。试用旧模组存档前保留可恢复副本：沙箱启用前含第三方序列化类型的存档仍需迁移验证。更新游戏后，重新生成开发引用。

隔离启动失败时，先验证游戏文件、重启游戏并查看工坊诊断，不要自行运行 Mod DLL 绕过错误。包哈希和信任确认仍用于标识本次启用的精确文件，不能证明作者身份或模组质量。

进程权限边界由 Windows 执行，机制说明见微软的 [AppContainer 隔离](https://learn.microsoft.com/en-us/windows/win32/secauthz/appcontainer-isolation)和[启动 AppContainer](https://learn.microsoft.com/en-us/windows/win32/secauthz/implementing-an-appcontainer)文档。
