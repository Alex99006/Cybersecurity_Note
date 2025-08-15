### 第一步：创建项目文件夹



首先，创建一个文件夹来存放你的项目。这有助于组织你的文件，并为虚拟环境提供一个清晰的位置。

Bash

```
mkdir my_scrapy_project
cd my_scrapy_project
```



### 第二步：创建虚拟环境



在你的项目文件夹内，运行以下命令来创建一个名为`venv`的虚拟环境。你可以把`venv`替换成任何你喜欢的名字。

Bash

```
python3 -m venv venv
```

- `python3`: 确保你使用的是Python 3。
- `-m venv`: 这告诉Python模块运行器（`-m`）去创建一个虚拟环境（`venv`）。
- `venv`: 这是你希望创建的虚拟环境文件夹的名字。

------



### 第三步：激活虚拟环境



创建完成后，你需要**激活**它。这是最关键的一步。

Bash

```
source venv/bin/activate
```

- `source`: 这是在当前shell中执行一个脚本的命令。
- `venv/bin/activate`: 这是激活虚拟环境的脚本路径。

**激活成功后，你的命令行提示符会发生变化**，通常会在前面显示虚拟环境的名字，比如`(venv)`，这表明你当前处于这个隔离的环境中。

Bash

```
(venv) your_username@kali:~/my_scrapy_project$
```

------



### 第四步：安装 Scrapy



现在你已经进入了安全的虚拟环境，可以放心地使用`pip`来安装Scrapy及其所有依赖项。

Bash

```
pip install scrapy
```

`pip`现在会把Scrapy安装到`my_scrapy_project/venv`文件夹中，而不是系统的全局Python环境中。

------



### 第五步：验证安装



安装完成后，你可以运行一个简单的命令来验证Scrapy是否成功安装。

Bash

```
scrapy --version
```

如果你看到版本号（例如 `Scrapy 2.x.x`），就表示安装成功了。

------



### 每次使用的注意事项



**每次**当你关闭终端或者开始新的会话时，你都需要重复**第三步**来激活虚拟环境，然后才能在其中使用Scrapy。

Bash

```
cd /path/to/your_project_folder
source venv/bin/activate
```

如果你想退出虚拟环境，只需运行：

Bash

```
deactivate
```

这会将你的终端恢复到正常的系统环境。