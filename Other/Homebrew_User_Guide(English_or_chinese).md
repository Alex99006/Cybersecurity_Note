# Homebrew 使用指南



Homebrew 是 macOS（和 Linux）上一个非常受欢迎的**包管理器**。它能让你通过简单的命令行命令来安装、更新和管理各种软件、工具和库，而无需手动下载、解压和拖放文件。它大大简化了开发者和普通用户管理软件的过程。

------



## Homebrew 的核心概念



在使用 Homebrew 之前，了解几个基本概念会很有帮助：

- **`brew`**: 这是 Homebrew 的主命令，所有操作都通过它来完成。
- **Formulae (公式)**: 这是 Homebrew 用来安装**命令行工具**（如 `wget`, `htop`, `git` 等）的定义文件。
- **Casks (桶)**: 这是 Homebrew 用来安装 macOS **图形界面应用程序**（如 Chrome, VS Code, OBS Studio, Docker Desktop 等）的定义文件。
- **Tap (水龙头)**: 这是一个远程 Git 仓库的集合，其中包含额外的 Formulae 或 Casks。Homebrew 默认会安装 `homebrew/core` 和 `homebrew/cask` 这两个核心 Tap。你可以添加第三方 Tap 来安装更多软件。

------



## Homebrew 的基本使用





### 1. 安装 Homebrew



如果你还没有安装 Homebrew，打开 **终端 (Terminal)** 应用程序（在“应用程序” > “实用工具”中），然后粘贴以下命令并按回车键执行：

Bash

```apl
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

按照屏幕上的提示操作，可能需要输入你的管理员密码。安装完成后，终端可能会提示你将 Homebrew 的路径添加到你的 shell 配置文件中（例如 `~/.zprofile` 或 `~/.bash_profile`），请按照提示操作，通常会是类似这样的命令：



```apl
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```



（注意：`/opt/homebrew/bin` 是 Apple Silicon Mac 上的默认路径，Intel Mac 可能是 `/usr/local/bin`）



### 2. 检查 Homebrew 是否正常工作



安装完成后，运行这个命令来确保一切就绪：

```apl
brew doctor
```

如果它显示“Your system is ready to brew.”，那么恭喜你，Homebrew 已经准备就绪！如果它提示任何警告或错误，请按照提示解决。



### 3. 安装软件 (Formulae)



安装命令行工具，比如 `wget`（一个下载工具）：

```apl
brew install wget
```



### 4. 安装应用程序 (Casks)



安装图形界面应用程序，比如 Google Chrome：

```apl
brew install --cask google-chrome
```

你也可以安装其他流行的应用，比如：

- VS Code: `brew install --cask visual-studio-code`
- Docker Desktop: `brew install --cask docker`
- VLC 播放器: `brew install --cask vlc`



### 5. 搜索软件



如果你不确定一个软件叫什么，或者想看看 Homebrew 是否支持它，可以使用 `search` 命令：

```apl
brew search node
```

这会列出所有名字中包含“node”的 Formulae 和 Casks。



### 6. 更新 Homebrew 自身



定期更新 Homebrew 和它的 Formulae/Casks 定义非常重要，以确保你能安装最新版本的软件：

```apl
brew update
```



### 7. 更新已安装的软件



更新所有通过 Homebrew 安装的软件到最新版本：

```apl
brew upgrade
```

你也可以只更新特定的软件，例如：

```apl
brew upgrade wget
```



### 8. 卸载软件



如果你不再需要某个软件，可以轻松卸载它：

```apl
brew uninstall wget
```

卸载 Cask 应用：

```apl
brew uninstall --cask google-chrome
```



### 9. 清理旧版本和缓存



Homebrew 会保留旧版本的软件和下载的安装包，你可以清理它们以节省磁盘空间：

```apl
brew cleanup
```



### 10. 查看已安装软件列表



查看所有通过 Homebrew 安装的 Formulae：

```apl
brew list
```

查看所有通过 Homebrew Cask 安装的应用程序：

```apl
brew list --cask
```

------



## 常见问题和提示



- **权限问题：** Homebrew 被设计为在不需要 `sudo` (管理员权限) 的情况下运行。如果你遇到权限错误，通常是由于安装过程中的某些问题或手动更改了 Homebrew 目录的权限。
- **网络连接：** Homebrew 需要连接到互联网来下载软件和更新定义。
- **日志：** 如果安装失败，Homebrew 会提供详细的日志文件路径，你可以查看这些日志来排除故障。
- **社区支持：** Homebrew 有一个非常活跃的社区。如果你遇到问题，通常可以在网上找到解决方案。



# Homebrew Usage Guide



Homebrew is a very popular **package manager** for macOS (and Linux). It allows you to install, update, and manage various software, tools, and libraries with simple command-line commands, eliminating the need for manual downloads, extractions, and drag-and-drop operations. It significantly simplifies the process of managing software for both developers and general users.

------



## Core Concepts of Homebrew



Before diving into usage, it's helpful to understand a few basic concepts of Homebrew:

- **`brew`**: This is the main Homebrew command; all operations are performed through it.
- **Formulae**: These are definition files Homebrew uses to install **command-line tools** (e.g., `wget`, `htop`, `git`, etc.).
- **Casks**: These are definition files Homebrew uses to install macOS **graphical applications** (e.g., Chrome, VS Code, OBS Studio, Docker Desktop, etc.).
- **Tap**: This is a collection of remote Git repositories containing additional Formulae or Casks. Homebrew by default installs the `homebrew/core` and `homebrew/cask` core taps. You can add third-party taps to install more software.

------



## Basic Homebrew Usage





### 1. Install Homebrew



If you haven't installed Homebrew yet, open the **Terminal** application (found in Applications > Utilities), then paste the following command and press Enter:

Bash

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Follow the on-screen prompts; you may need to enter your administrator password. After installation, the terminal might prompt you to add Homebrew's path to your shell configuration file (e.g., `~/.zprofile` or `~/.bash_profile`). Please follow these instructions, which usually involve commands similar to this:

Bash

```
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

(Note: `/opt/homebrew/bin` is the default path for Apple Silicon Macs, while Intel Macs might use `/usr/local/bin`.)



### 2. Check Homebrew Installation



After installation, run this command to ensure everything is set up correctly:

Bash

```
brew doctor
```

If it displays "Your system is ready to brew.", then congratulations, Homebrew is ready! If it shows any warnings or errors, please follow the prompts to resolve them.



### 3. Install Software (Formulae)



To install a command-line tool, such as `wget` (a download utility):

Bash

```
brew install wget
```



### 4. Install Applications (Casks)



To install a graphical application, such as Google Chrome:

Bash

```
brew install --cask google-chrome
```

You can also install other popular applications, such as:

- VS Code: `brew install --cask visual-studio-code`
- Docker Desktop: `brew install --cask docker`
- VLC Player: `brew install --cask vlc`



### 5. Search for Software



If you're unsure of a software's name or want to see if Homebrew supports it, use the `search` command:

Bash

```
brew search node
```

This will list all Formulae and Casks with "node" in their name.



### 6. Update Homebrew Itself



Regularly updating Homebrew and its Formulae/Casks definitions is crucial to ensure you can install the latest versions of software:

Bash

```
brew update
```



### 7. Update Installed Software



To update all software installed via Homebrew to their latest versions:

Bash

```
brew upgrade
```

You can also update specific software, for example:

Bash

```
brew upgrade wget
```



### 8. Uninstall Software



If you no longer need a particular piece of software, you can easily uninstall it:

Bash

```
brew uninstall wget
```

To uninstall a Cask application:

Bash

```
brew uninstall --cask google-chrome
```



### 9. Clean Up Old Versions and Caches



Homebrew keeps old versions of software and downloaded installation packages. You can clean them up to save disk space:

Bash

```
brew cleanup
```



### 10. View List of Installed Software



To view all Formulae installed via Homebrew:

Bash

```
brew list
```

To view all applications installed via Homebrew Cask:

Bash

```
brew list --cask
```

------



## Common Issues and Tips



- **Permissions Issues**: Homebrew is designed to run without `sudo` (administrator privileges). If you encounter permission errors, it's usually due to issues during installation or manual changes to Homebrew directory permissions.
- **Network Connection**: Homebrew requires an internet connection to download software and update definitions.
- **Logs**: If an installation fails, Homebrew will provide the path to detailed log files, which you can check to troubleshoot the issue.
- **Community Support**: Homebrew has a very active community. If you encounter problems, you can usually find solutions online.