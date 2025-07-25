# iTerm2 配置汇总



iTerm2 是 macOS 上一款功能强大的终端模拟器，通过合理的配置，可以极大提升你的工作效率和视觉体验。

------



## 1. iTerm2 的下载与安装



1. 访问 **iTerm2 官方网站**：https://iterm2.com/
2. 点击 **"Download"** 下载最新版本。
3. 解压下载的 `.zip` 文件，将 `iTerm.app` 拖拽到你的 `/Applications` 文件夹中。

------



## 2. iTerm2 基础配置



打开 iTerm2 后，你可以通过以下方式进入偏好设置：

- 点击菜单栏左上角的 **“iTerm2”**，然后选择 **“Preferences”**。
- 使用快捷键 `Command (⌘) + , (逗号)`。



### 2.1 外观主题 (Colors)



自定义终端的颜色方案，是提升视觉体验的关键。

1. 在偏好设置窗口中，点击顶部的 **“Profiles”** (描述文件) 选项卡。
2. 选择你想要配置的描述文件（通常是 **“Default”**）。
3. 点击右侧的 **“Colors”** (颜色) 选项卡。
4. **选择内置主题：** 在 **“Color Presets”** (颜色预设) 下拉菜单中选择一个预设主题。
5. **导入更多主题：**
   - 在浏览器中搜索 **“iTerm2 color schemes”**（例如访问 [iterm2colorschemes.com](https://iterm2colorschemes.com/)），下载 `.itermcolors` 文件。
   - 回到 **“Color Presets”** 下拉菜单，选择 **“Import...”** (导入...)，然后选择下载的文件。导入后即可选择并应用。
6. **手动微调：** 你也可以点击 **“Foreground”** (前景色/文字颜色)、**“Background”** (背景色)、**“Selection”** (选中) 和其他颜色方块，手动调整颜色。



### 2.2 字体设置 (Text)



选择合适的字体，尤其对于显示特殊符号和代码连字至关重要。

1. 在“Profiles”设置中，点击 **“Text”** (文本) 选项卡。
2. 点击 **“Change Font”** (更改字体) 按钮。
3. 在弹出的字体选择器中，选择你喜欢的字体和字号。
   - **重要提示：** 如果你想使用 Oh My Zsh 的高级主题（如 Agnoster、Powerlevel10k）并正确显示特殊符号（箭头、Git 图标等），你需要安装 **Nerd Fonts**。



#### **如何安装 Nerd Fonts：**



- 打开 iTerm2 终端。

- 使用 Homebrew Cask 安装（推荐）：

  - 安装 MesloLGS NF (常用且推荐)：

    Bash

    ```
    brew install --cask font-meslo-lg-nerd-font
    ```

  - 或安装 FiraCode Nerd Font (支持编程连字)：

    Bash

    ```
    brew install --cask font-fira-code-nerd-font
    ```

  - **注意：** 旧的 `homebrew/cask-fonts` 仓库已废弃，直接运行 `brew install --cask` 即可。

- 手动安装（如果 Homebrew 有问题）：

  1. 访问 Nerd Fonts 官方 GitHub 发布页面：https://github.com/ryanoasis/nerd-fonts/releases。
  2. 下载你想要的字体 `.zip` 文件，解压。
  3. 双击 `.ttf` 或 `.otf` 字体文件，通过 macOS 的 **“字体册” (Font Book)** 应用安装。

1. 字体安装后，回到 iTerm2 的“Text”选项卡，点击 **“Change Font”**，选择你安装的 Nerd Font 字体（确保名称中带有 "NF" 或 "Nerd Font"）。
2. **（可选，但推荐）勾选“Use ligatures”** (使用连字，如果你的字体支持如 Fira Code)。
3. 确保 **“Anti-aliased”** (抗锯齿) 是勾选状态，使字体显示更平滑。



### 2.3 窗口外观 (Window)



调整窗口透明度和模糊度，与桌面壁纸融合。

1. 在“Profiles”设置中，点击 **“Window”** (窗口) 选项卡。
2. 调整 **“Transparency”** (透明度) 滑块。
3. 调整 **“Blur”** (模糊度) 滑块。
4. 在 **“Background Image”** (背景图片) 部分，勾选 **“Image”**，点击 **“Browse...”** 选择背景图，并调整 **“Blending”** (混合) 和 **“Scale”** (缩放) 选项。

------



## 3. iTerm2 的高效功能配置





### 3.1 全局快捷键启动 (Hotkey Window)



设置一个全局快捷键，随时快速呼出或隐藏 iTerm2。

1. 在偏好设置窗口中，点击顶部的 **“Keys”** (快捷键) 选项卡。
2. 在底部找到 **“Hotkey”** (热键) 部分，并**勾选**启用。
3. 点击 **“Configure Hotkey Window”** (配置热键窗口) 按钮。
4. **勾选** **“Show/hide all windows with a system-wide hotkey”**。
5. 点击下方的文本框，**按下你想要的全局快捷键组合**（例如：`Control (⌃) + Space` 或 `Option (⌥) + Space`）。
6. **重要：** 确保**勾选** **“Opens at startup”** (开机启动)。**这样可以确保 iTerm2 随系统启动并运行在后台，从而让你的全局快捷键在iTerm2完全退出后也能再次启动它。**
7. 点击 **“OK”** 确认。

**注意：** 如果你手动用 `Command (⌘) + Q` 退出 iTerm2，它是完全关闭的，此时全局快捷键将无法唤醒它。快捷键只作用于**后台运行**的 iTerm2 进程。为了让热键始终有效，请避免用 `Command + Q` 退出，而是使用你的热键来隐藏/显示窗口。



### 3.2 窗格分屏 (Split Panes)



在同一个 iTerm2 窗口内分割成多个独立的命令行会话。

- **垂直分割 (左右)：** `Command (⌘) + D`
- **水平分割 (上下)：** `Command (⌘) + Shift (⇧) + D`

**窗格间导航：**

- **切换焦点：** `Command (⌘) + Option (⌥) + 方向键` (↑ ↓ ← →)
- **调整大小：** `Command (⌘) + Shift (⇧) + 方向键`
- **关闭当前窗格：** `Command (⌘) + W`

------



## 4. 增强 Shell 功能 (Zsh & Oh My Zsh)



iTerm2 本身只是终端模拟器，要获得更强大的功能和语法高亮，需要配置 Shell，尤其是 **Zsh** 配合 **Oh My Zsh**。



### 4.1 安装 Oh My Zsh



如果你的终端显示 `ls: /Users/Hacker_learn/.oh-my-zsh: No such file or directory` 或 `curl: (56) Recv failure: Operation timed out` 等错误，说明 Oh My Zsh 未正确安装或下载失败。

**重新安装 Oh My Zsh 的正确方法：**

1. 打开 iTerm2 终端。

2. 运行安装命令：

   Bash

   ```
   sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
   ```

3. 安装过程中，如果询问是否将 Zsh 设为默认 Shell，**输入 `Y` 并回车**。

4. 耐心等待安装完成。



### 4.2 配置命令语法高亮 (Syntax Highlighting)



这是 Zsh 的一个插件，让你的命令、参数等显示不同颜色。

1. **安装插件：**

   Bash

   ```
   brew install zsh-syntax-highlighting
   ```

2. **启用插件：**

   - 打开你的 `.zshrc` 配置文件：`nano ~/.zshrc`

   - 找到 `plugins=(...)` 这一行。

   - 在括号内添加 `zsh-syntax-highlighting`。例如：

     Bash

     ```
     plugins=(git zsh-autosuggestions zsh-syntax-highlighting)
     ```

     （如果 `zsh-autosuggestions` 未安装，可暂时不添加。）

3. **保存并应用：** 保存 `.zshrc` 文件，然后在终端运行 `source ~/.zshrc`，或重启 iTerm2。



#### **解决 `plugin 'xxx' not found` 错误：**



如果 Oh My Zsh 提示插件未找到，通常是因为插件不在 Oh My Zsh 的默认查找路径中。建议将插件克隆到 Oh My Zsh 的自定义插件目录：

1. **卸载 Homebrew 版本（可选）：**

   Bash

   ```
   brew uninstall zsh-autosuggestions
   brew uninstall zsh-syntax-highlighting
   ```

2. **克隆插件到 Oh My Zsh 目录：**

   

   

   Bash

   ```
   git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
   git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
   ```

3. **在 `.zshrc` 中启用插件**（同上一步骤）。

4. **保存并应用**（同上一步骤）。



### 4.3 配置文本选择高亮 (Selection Highlight)



当你用鼠标选中文本时，显示的颜色。

1. 打开 iTerm2 偏好设置 (`Command (⌘) + ,`)。
2. 进入 **Profiles** > **Colors** 选项卡。
3. 在底部找到 **“Selection”** (选中) 旁边的颜色方块，点击并调整你喜欢的选中背景色和文字色。



### 4.4 终端提示符样式 (`-> ~`)



如果你看到终端前面变成了 `-> ~`，这通常表示你已成功启用了 **Oh My Zsh 的 `agnoster` 主题**。

- `->` 是 `agnoster` 主题的箭头样式。
- `~` 表示你当前位于用户主目录。

如果显示乱码或你不喜欢此样式，可以：

1. **安装 Powerline/Nerd Fonts 并设置 iTerm2 字体**（参考 2.2 字体设置）。
2. **更换 Oh My Zsh 主题：**
   - 打开 `.zshrc` 文件：`nano ~/.zshrc`
   - 找到 `ZSH_THEME="agnoster"` 这一行。
   - **将 `"agnoster"` 替换成其他你喜欢的主题名称。你可以访问 Oh My Zsh 的主题库进行预览和选择：https://github.com/ohmyzsh/ohmyzsh/wiki/Themes**
   - 保存 `.zshrc` 文件，然后 `source ~/.zshrc` 或重启 iTerm2。



------

好的，这是 iTerm2 配置汇总的英文版文档，以 Markdown 格式呈现：

------



# iTerm2 Configuration Summary



iTerm2 is a powerful terminal emulator for macOS. With proper configuration, it can significantly enhance your workflow efficiency and visual experience.

------



## 1. iTerm2 Download and Installation



1. Visit the **official iTerm2 website**: https://iterm2.com/
2. Click **"Download"** to get the latest version.
3. Unzip the downloaded `.zip` file and drag `iTerm.app` into your `/Applications` folder.

------



## 2. iTerm2 Basic Configuration



After launching iTerm2, you can access its preferences via:

- Clicking **“iTerm2”** in the top-left menu bar, then selecting **“Preferences”**.
- Using the keyboard shortcut `Command (⌘) + , (comma)`.



### 2.1 Appearance (Colors)



Customizing your terminal's color scheme is key to improving the visual experience.

1. In the Preferences window, click the **“Profiles”** tab at the top.
2. Select the profile you wish to configure (usually **“Default”**).
3. Click the **“Colors”** tab on the right.
4. **Choose a Built-in Theme:** Select a preset theme from the **“Color Presets”** dropdown menu.
5. **Import More Themes:**
   - Search for **“iTerm2 color schemes”** in your browser (e.g., visit [iterm2colorschemes.com](https://iterm2colorschemes.com/)) and download a `.itermcolors` file.
   - Go back to the **“Color Presets”** dropdown menu, select **“Import...”**, then choose the downloaded file. Once imported, you can select and apply it.
6. **Fine-tune Manually:** You can also click the color swatches next to **“Foreground”**, **“Background”**, **“Selection”**, and other options to manually adjust colors.



### 2.2 Font Settings (Text)



Choosing the right font is crucial for clear display of special characters and code ligatures.

1. In the “Profiles” settings, click the **“Text”** tab.
2. Click the **“Change Font”** button in the “Font” section.
3. In the font picker that appears, select your preferred font and font size.
   - **Important Tip:** If you plan to use advanced Oh My Zsh themes (like Agnoster, Powerlevel10k) and want to display special symbols (arrows, Git icons, etc.) correctly, you need to install **Nerd Fonts**.



#### **How to Install Nerd Fonts:**



- Open your iTerm2 terminal.

- **Install using Homebrew Cask (Recommended):**

  - To install MesloLGS NF (commonly used and recommended):

    Bash

    ```
    brew install --cask font-meslo-lg-nerd-font
    ```

  - Or, to install FiraCode Nerd Font (supports programming ligatures):

    Bash

    ```
    brew install --cask font-fira-code-nerd-font
    ```

  - **Note:** The old `homebrew/cask-fonts` tap is deprecated. Just run `brew install --cask` directly.

- **Manual Installation (if Homebrew has issues):**

  1. Visit the official Nerd Fonts GitHub releases page: https://github.com/ryanoasis/nerd-fonts/releases.
  2. Download the `.zip` file for your desired font, and extract it.
  3. Select all `.ttf` or `.otf` font files in the extracted folder.
  4. **Double-click** them, or drag them into macOS's **“Font Book”** application. Click “Install Font.”

1. After the font is installed, go back to iTerm2's “Text” tab, click **“Change Font”**, and select your newly installed **Nerd Font** (ensure the name contains "NF" or "Nerd Font").
2. **Optionally (but recommended), check “Use ligatures”** (if your chosen font, like Fira Code, supports programming ligatures).
3. Ensure **“Anti-aliased”** is checked for smoother font rendering.



### 2.3 Window Appearance (Window)



Adjust window transparency and blur to blend with your desktop background.

1. In the “Profiles” settings, click the **“Window”** tab.
2. Adjust the **“Transparency”** slider.
3. Adjust the **“Blur”** slider.
4. In the **“Background Image”** section, check **“Image”**, click **“Browse...”** to select a background image, and adjust **“Blending”** and **“Scale”** options.

------



## 3. iTerm2 Advanced Features Configuration





### 3.1 Global Hotkey Window



Set a system-wide shortcut to quickly show or hide iTerm2 at any time.

1. In the Preferences window, click the **“Keys”** tab at the top.
2. At the bottom, locate the **“Hotkey”** section and **check** the box to enable it.
3. Click the **“Configure Hotkey Window”** button.
4. **Check** **“Show/hide all windows with a system-wide hotkey”**.
5. Click the text box below (usually showing “Click to Set”) and **press your desired global hotkey combination** (e.g., `Control (⌃) + Space` or `Option (⌥) + Space`).
6. **Crucially:** Ensure **“Opens at startup”** is **checked**. **This ensures iTerm2 launches with your system and runs in the background, allowing your global hotkey to activate it even if all its windows are closed.**
7. Click **“OK”** to confirm.

**Note:** If you manually quit iTerm2 using `Command (⌘) + Q`, it is completely shut down, and the global hotkey will not be able to reactivate it. The hotkey only works if the iTerm2 process is running in the background. To keep the hotkey always functional, avoid quitting with `Command + Q`; instead, use your hotkey to hide/show the window.



### 3.2 Pane Splitting (Split Panes)



Divide your iTerm2 window into multiple independent command-line sessions.

- **Vertical Split (Left/Right):** `Command (⌘) + D`
- **Horizontal Split (Top/Bottom):** `Command (⌘) + Shift (⇧) + D`

**Navigating Between Panes:**

- **Switch Focus:** `Command (⌘) + Option (⌥) + Arrow Keys` (↑ ↓ ← →)
- **Resize:** `Command (⌘) + Shift (⇧) + Arrow Keys`
- **Close Current Pane:** `Command (⌘) + W`

------



## 4. Enhancing Shell Functionality (Zsh & Oh My Zsh)



iTerm2 is a terminal emulator; to gain powerful features and syntax highlighting, you need to configure your Shell, especially **Zsh** in conjunction with **Oh My Zsh**.



### 4.1 Installing Oh My Zsh



If your terminal shows errors like `ls: /Users/Hacker_learn/.oh-my-zsh: No such file or directory` or `curl: (56) Recv failure: Operation timed out`, it indicates that Oh My Zsh was not installed correctly or download failed.

**Correct Way to Reinstall Oh My Zsh:**

1. Open your iTerm2 terminal.

2. Run the installation command:

   Bash

   ```
   sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
   ```

3. During installation, if prompted to set Zsh as your default shell, **type `Y` and press Enter**.

4. Wait patiently for the installation to complete.



### 4.2 Configuring Command Syntax Highlighting



This is a Zsh plugin that colors your commands, arguments, etc.

1. **Install the Plugin:**

   Bash

   ```
   brew install zsh-syntax-highlighting
   ```

2. **Enable the Plugin:**

   - Open your `.zshrc` configuration file: `nano ~/.zshrc`

   - Find the `plugins=(...)` line.

   - Add `zsh-syntax-highlighting` inside the parentheses. For example:

     Bash

     ```
     plugins=(git zsh-autosuggestions zsh-syntax-highlighting)
     ```

     (If `zsh-autosuggestions` is not installed, you can omit it for now.)

3. **Save and Apply:** Save the `.zshrc` file, then run `source ~/.zshrc` in the terminal, or restart iTerm2.



#### **Resolving `plugin 'xxx' not found` errors:**



If Oh My Zsh indicates a plugin is not found, it's often because the plugin is not in Oh My Zsh's default lookup path. It's recommended to clone plugins into Oh My Zsh's custom plugins directory:

1. **Uninstall Homebrew versions (optional):**

   Bash

   ```
   brew uninstall zsh-autosuggestions
   brew uninstall zsh-syntax-highlighting
   ```

2. **Clone plugins into Oh My Zsh directory:**

   

   

   Bash

   ```
   git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
   git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
   ```

3. **Enable plugins in `.zshrc`** (same as the step above).

4. **Save and Apply** (same as the step above).



### 4.3 Configuring Text Selection Highlighting



This controls the background color when you select text with your mouse.

1. Open iTerm2 Preferences (`Command (⌘) + ,`).
2. Go to the **Profiles** > **Colors** tab.
3. At the bottom, find the color swatch next to **“Selection”**. Click it and adjust your preferred selection background and text colors.



### 4.4 Terminal Prompt Style (`-> ~`)



If your terminal prompt now looks like `-> ~`, this usually means you have successfully enabled the **`agnoster` theme** for Oh My Zsh.

- `->` is the arrow style of the `agnoster` theme.
- `~` indicates your current directory is your user's home directory.

If it shows garbled characters or you don't like this style, you can:

1. **Install Nerd Fonts and set them in iTerm2** (refer to 2.2 Font Settings).
2. **Change your Oh My Zsh Theme:**
   - Open your `.zshrc` file: `nano ~/.zshrc`
   - Find the line `ZSH_THEME="agnoster"`.
   - **Change it to another theme you prefer. You can visit the Oh My Zsh Themes Wiki to preview and choose: https://github.com/ohmyzsh/ohmyzsh/wiki/Themes**
   - Save the `.zshrc` file, then run `source ~/.zshrc` or restart iTerm2.