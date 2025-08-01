# 枚举命令速查表



本文档整理了常见的网络服务枚举命令，旨在帮助用户快速查找和理解不同服务类型下的扫描和交互命令。



## 基础设施枚举 (Infrastructure Enumeration)



| 命令                                                      | 描述                                                       |
| --------------------------------------------------------- | ---------------------------------------------------------- |
| `curl -s https://crt.sh/?q=&output=json                   | jq .`                                                      |
| `for i in $(cat ip-addresses.txt);do shodan host $i;done` | 使用 Shodan 扫描 `ip-addresses.txt` 列表中的每个 IP 地址。 |

 



## 基于主机的枚举 (Host-Based Enumeration)





### FTP



| 命令                                                      | 描述                                                       |
| --------------------------------------------------------- | ---------------------------------------------------------- |
| `ftp <FQDN/IP>`                                           | 与目标上的 FTP 服务进行交互。                              |
| `nc -nv <FQDN/IP> 21`                                     | 通过 Netcat 与目标上的 FTP 服务进行交互。                  |
| `telnet <FQDN/IP> 21`                                     | 通过 Telnet 与目标上的 FTP 服务进行交互。                  |
| `openssl s_client -connect <FQDN/IP>:21 -starttls ftp`    | 使用加密连接与目标上的 FTP 服务进行交互（通过 STARTTLS）。 |
| `wget -m --no-passive ftp://anonymous:anonymous@<target>` | 下载目标 FTP 服务器上所有可用的文件（匿名登录）。          |

 



### SMB (Server Message Block) / CIFS



| 命令                                              | 描述                                              |
| ------------------------------------------------- | ------------------------------------------------- |
| `smbclient -N -L //<FQDN/IP>`                     | 对 SMB 服务进行空会话身份验证并列出共享。         |
| `smbclient //<FQDN/IP>/<share>`                   | 连接到特定的 SMB 共享。                           |
| `rpcclient -U "" <FQDN/IP>`                       | 使用 RPC (Remote Procedure Call) 与目标进行交互。 |
| `samrdump.py <FQDN/IP>`                           | 使用 Impacket 脚本枚举 SMB 用户名。               |
| `smbmap -H <FQDN/IP>`                             | 枚举 SMB 共享及其权限。                           |
| `crackmapexec smb <FQDN/IP> --shares -u '' -p ''` | 使用空会话身份验证枚举 SMB 共享（CrackMapExec）。 |
| `enum4linux-ng.py <FQDN/IP> -A`                   | 使用 enum4linux 进行全面的 SMB 枚举。             |

 



### NFS (Network File System)



| 命令                                                      | 描述                                              |
| --------------------------------------------------------- | ------------------------------------------------- |
| `showmount -e <FQDN/IP>`                                  | 显示目标上可用的 NFS 共享。                       |
| `mount -t nfs <FQDN/IP>:/<share> ./target-NFS/ -o nolock` | 将特定的 NFS 共享挂载到本地目录 `./target-NFS/`。 |
| `umount ./target-NFS`                                     | 卸载特定的 NFS 共享。                             |

 



### DNS (Domain Name System)



| 命令                                                         | 描述                                                |
| ------------------------------------------------------------ | --------------------------------------------------- |
| `dig ns <domain.tld> @<nameserver>`                          | 向特定的名称服务器发出 NS (Name Server) 请求。      |
| `dig any <domain.tld> @<nameserver>`                         | 向特定的名称服务器发出 ANY 请求，获取所有记录类型。 |
| `dig axfr <domain.tld> @<nameserver>`                        | 向特定的名称服务器发出 AXFR (Zone Transfer) 请求。  |
| `dnsenum --dnsserver <nameserver> --enum -p 0 -s 0 -o found_subdomains.txt -f ~/subdomains.list <domain.tld>` | 子域名暴力破解，使用特定DNS服务器和字典文件。       |

 



### SMTP (Simple Mail Transfer Protocol)



| 命令                  | 描述                                       |
| --------------------- | ------------------------------------------ |
| `telnet <FQDN/IP> 25` | 通过 Telnet 与目标上的 SMTP 服务进行交互。 |

 



### IMAP / POP3



| 命令                                                   | 描述                                                |
| ------------------------------------------------------ | --------------------------------------------------- |
| `curl -k 'imaps://<FQDN/IP>' --user <user>:<password>` | 使用 cURL 登录 IMAPS 服务（`-k` 忽略SSL证书错误）。 |
| `openssl s_client -connect <FQDN/IP>:imaps`            | 连接到 IMAPS (IMAP over SSL/TLS) 服务。             |
| `openssl s_client -connect <FQDN/IP>:pop3s`            | 连接到 POP3s (POP3 over SSL/TLS) 服务。             |

 ~~~apl
 openssl s_client -connect <FQDN/IP>:imaps  #. s_client 是 openssl 的一个子命令，它的作用是实现一个基本的 SSL/TLS 客户端。你可以把它看作是一个简易的浏览器或邮件客户端，但它只专注于 SSL/TLS 连接的部分。  imaps可以替换为port
 tag3 FETCH 1 (BODY[]) # 链接后需要登录的话 需要先加上 tag 标签  例如：tag0  tag1  tag2  后接其他命令即可   FETCH  这是 IMAP 协议中的一个命令名称，表示“获取”或“检索”。它的作用是从邮件服务器上下载邮件的某些部分或属性。      1: 这是邮件的 序列号 (Sequence Number)。在 IMAP 协议中，在一个选定的邮箱（这里是 DEV.DEPARTMENT.INT）中，每封邮件都有一个唯一的序列号，从 1 开始递增。1 就表示你要获取的是该邮箱中的第一封邮件。     BODY[] 是一个特殊的 FETCH 数据项，它表示获取邮件的完整原始内容，包括邮件头（如发件人、收件人、主题等）和邮件体（正文）。它会返回整个 MIME 结构。
 
 #       重要说明： BODY[] 与 BODY.PEEK[] 类似，但 BODY[] 会将邮件标记为“已读”（如果服务器和客户端支持且未另行配置）。如果只想查看不修改邮件状态，通常会使用 BODY.PEEK[]。但在这个上下文中，BODY[] 是完全合法的。
 ~~~





### SNMP (Simple Network Management Protocol)



| 命令                                              | 描述                                         |
| ------------------------------------------------- | -------------------------------------------- |
| `snmpwalk -v2c -c <community string> <FQDN/IP>`   | 使用 `snmpwalk` 查询指定 OID（对象标识符）。 |
| `onesixtyone -c community-strings.list <FQDN/IP>` | 暴力破解 SNMP 服务的社区字符串。             |
| `braa <community string>@<FQDN/IP>:.1.*`          | 强制执行 SNMP 服务 OID（获取特定MIB分支）。  |

 ~~~apl
 snmpwalk -v2c -c public 10.129.163.98 | tee snmpwalk.txt  
 					#  这是指定 SNMP 协议版本的选项。
 					#  v2c 指的是 SNMP 版本 2c。这是 SNMP 的一个常用版本，比 v1 更强大，比 v3 更简单（v3 支持加密和更强的认证）。
 					#  -c public   这是指定 **社区字符串（Community String）**的选项。
 grep -m 1 -B 8 "HTB" snmpwalk.txt  #  -m 1 的意思是：只显示找到的第一个匹配项后就停止   -B 8 的意思是：在显示匹配的行之外，同时显示该匹配行之前的 8 行内容。
 ~~~





### MySQL



| 命令                                                 |                             描述                             |
| ---------------------------------------------------- | :----------------------------------------------------------: |
| `mysql -u <user> -p<password> -h <IP address>`       | 连接到 MySQL 服务器。'- p' 标志和密码之间**不应有空格。**登录到 MySQL 服务器。 |
| `show databases;`                                    |                       显示所有数据库。                       |
| `use <database>;`                                    |                     选择现有数据库之一。                     |
| `show tables;`                                       |                显示所选数据库中所有可用的表。                |
| `show columns from <table>;`                         |                    显示选定表中的所有列。                    |
| `select * from <table>;`                             |                  显示所需表格中的所有内容。                  |
| `select * from <table> where <column> = "<string>";` |               `string`在所需表中搜索所需内容。               |
| `describe  table_name; `                             | 它会显示表的列名、数据类型、是否允许为空 (NULL)、键信息 (KEY)、默认值等。 |



### MSSQL



| 命令                                                         | 描述                                                         |
| :----------------------------------------------------------- | :----------------------------------------------------------- |
| `mssqlclient.py <user>@<FQDN/IP> -windows-auth`              | 使用 Windows 身份验证登录 MSSQL 服务器（Impacket脚本）。     |
| `master`（mssql 默认数据库名称）                             | 跟踪 SQL 服务器实例的所有系统信息                            |
| `model`  mssql 默认数据库名称）                              | 模板数据库充当每个新创建的数据库的结构。在模型数据库中更改的任何设置都将反映在更改模型数据库后创建的任何新数据库中 |
| `msdb`（mssql 默认数据库名称）                               | SQL Server 代理使用此数据库来安排作业和警报                  |
| `tempdb`（mssql 默认数据库名称）                             | 存储临时对象                                                 |
| `/usr/share/doc/python3-impacket/examples/mssqlclient.py backdoor@10.129.230.249 -windows-auth` | `-windows-auth` 指示 `mssqlclient.py` 使用**Windows 身份验证**（也称为集成身份验证或 Kerberos/NTLM 身份验证）来连接 MSSQL 服务器，而不是传统的 SQL Server 身份验证（即用户名和密码直接在 SQL Server 内部管理） |

~~~apl
# 透测试人员可能会发现 Impacket 的 mssqlclient.py 最有用，因为 SecureAuthCorp 的 Impacket 项目在安装时就存在于许多渗透测试发行版中
~~~





### IPMI (Intelligent Platform Management Interface)



| 命令                                           | 描述                               |
| ---------------------------------------------- | ---------------------------------- |
| `msf6 auxiliary(scanner/ipmi/ipmi_version)`    | 使用 Metasploit 检测 IPMI 版本。   |
| `msf6 auxiliary(scanner/ipmi/ipmi_dumphashes)` | 使用 Metasploit 转储 IPMI 哈希值。 |

 



### Linux 远程管理



| 命令                                                        | 描述                                        |
| ----------------------------------------------------------- | ------------------------------------------- |
| `ssh-audit.py <FQDN/IP>`                                    | 针对目标 SSH 服务进行远程安全审计。         |
| `ssh <user>@<FQDN/IP>`                                      | 使用 SSH 客户端登录 SSH 服务器。            |
| `ssh -i private.key <user>@<FQDN/IP>`                       | 使用私钥登录 SSH 服务器。                   |
| `ssh <user>@<FQDN/IP> -o PreferredAuthentications=password` | 强制执行基于密码的身份验证登录 SSH 服务器。 |

 



### Windows 远程管理



| 命令                                                         | 描述                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| `rdp-sec-check.pl <FQDN/IP>`                                 | 检查 RDP 服务的安全设置。                                    |
| `xfreerdp /u:<user> /p:"<password>" /v:<FQDN/IP>`            | 从 Linux 客户端登录到 RDP (Remote Desktop Protocol) 服务器。 |
| `evil-winrm -i <FQDN/IP> -u <user> -p <password>`            | 登录 WinRM (Windows Remote Management) 服务器。              |
| `wmiexec.py <user>:"<password>"@<FQDN/IP> "<system command>"` | 使用 WMI (Windows Management Instrumentation) 服务执行命令。 |

 



### Oracle TNS



| 命令                                                         | 描述                                                     |
| ------------------------------------------------------------ | -------------------------------------------------------- |
| `./odat.py all -s <FQDN/IP>`                                 | 执行各种扫描以收集有关 Oracle 数据库服务及其组件的信息。 |
| `sqlplus <user>/<pass>@<FQDN/IP>/<db>`                       | 登录 Oracle 数据库。                                     |
| `./odat.py utlfile -s <FQDN/IP> -d <db> -U <user> -P <pass> --sysdba --putFile C:\\insert\\path file.txt ./file.txt` | 使用 Oracle RDBMS 的 UTL_FILE 包上传文件。               |

~~~apl
wget https://download.oracle.com/otn_software/linux/instantclient/214000/instantclient-basic-linux.x64-21.4.0.0.0dbru.zip
wget https://download.oracle.com/otn_software/linux/instantclient/214000/instantclient-sqlplus-linux.x64-21.4.0.0.0dbru.zip

  #wget: 这是 Linux 命令，用于从网络上下载文件。

  #https://...: 这是 Oracle 官方网站上 Oracle Instant Client 的下载链接。

  #这是下载 Instant Client 的两个核心组件：

  #instantclient-basic: 包含连接到 Oracle 数据库所必需的基本库文件。

  #instantclient-sqlplus: 包含 sqlplus 工具，这是一个命令行工具，可以让你像在数据库服务器上一样，通过命令行与数据库进行交互。

mkdir -p /opt/oracle:   # 创建一个名为 oracle 的目录，并将其放在 /opt 目录下。/opt 是一个标准的 Linux 目录，用于存放可选的、非系统的软件包。-p 参数确保如果父目录 /opt 不存在，也会一并创建。

sudo unzip -d /opt/oracle instantclient-basic-linux.x64-21.4.0.0.0dbru.zip
sudo unzip -d /opt/oracle instantclient-sqlplus-linux.x64-21.4.0.0.0dbru.zip

  #unzip: 解压 .zip 格式的压缩文件。

  #-d /opt/oracle: 指定解压的目标目录为 /opt/oracle。

  #这将下载的 Instant Client 组件解压到我们刚刚创建的 /opt/oracle 目录中。解压后会生成一个名为 instantclient_21_4 的子目录，所有文件都在其中。

export LD_LIBRARY_PATH=/opt/oracle/instantclient_21_4:$LD_LIBRARY_PATH
export PATH=$LD_LIBRARY_PATH:$PATH

  #export: 在当前 shell 会话中设置环境变量。

  #LD_LIBRARY_PATH: 这是一个非常重要的环境变量，它告诉系统在运行时去哪里查找共享库文件（如 .so 文件）。

  #PATH: 这是一个告诉系统去哪里查找可执行程序的变量。

  #第一行将 Instant Client 库文件所在的目录 (/opt/oracle/instantclient_21_4) 添加到 LD_LIBRARY_PATH 中。这确保了像 Python 的 cx_Oracle 模块在运行时能够找到所需的 Oracle 库文件。

  #第二行将 Instant Client 的路径添加到 PATH 中。这使得你可以在任何目录下直接运行 sqlplus 等工具，而不需要输入完整路径。

source ~/.bashrc

  #source: 该命令用于在当前 shell 中执行一个脚本文件。

~/.bashrc: #. 这是 Bash shell 的一个配置文件，通常用于存储用户自定义的命令和环境变量。 export 命令只对当前会话有效。如果你想让这些变量永久生效，你应该将它们添加到 ~/.bashrc 文件中，然后用 source 命令重新加载这个文件，使更改立即生效。但你给的代码只在当前会话中生效，这行代码在这里可能只是为了刷新环境变量。

安装 ODAT 及其依赖
这是下载 ODAT (Oracle Database Attacking Tool)，然后安装它所需的所有 Python 库和系统依赖。

cd ~
git clone https://github.com/quentinhardy/odat.git
cd odat/
git clone ...:
cd odat/: 
pip install python-libnmap
git submodule init
git submodule update
pip3 install cx_Oracle
sudo apt-get install python3-scapy -y
sudo pip3 install colorlog termcolor passlib python-libnmap
sudo apt-get install build-essential libgmp-dev -y
pip3 install pycryptodome

  # git submodule ...: odat 工具依赖于其他 Git 仓库中的代码，这些代码被称为 submodules。这两行命令用于初始化并更新这些子模块，确保所有依赖的代码都已正确下载。

  # cx_Oracle: 这是一个 Python 库，用于连接和操作 Oracle 数据库。ODAT 工具需要它才能正常工作。

apt-get install ...: 
  # python3-scapy: Scapy 是一个强大的 Python 库，用于发送、嗅探、解析和伪造网络数据包。ODAT 可能使用它来进行网络层面的探测。

  # colorlog, termcolor, passlib, python-libnmap: 这些都是 ODAT 工具所需的 Python 库，用于日志着色、终端文本颜色、密码哈希处理以及 Nmap 集成。

build-essential, libgmp-dev:

  # build-essential: 这是一个元包，包含了编译软件所必需的基本工具（如 gcc, g++, make 等）。

libgmp-dev: GMP (GNU Multiple Precision Arithmetic Library) 的开发库。

pycryptodome: 这是一个加密库，ODAT 可能使用它来处理加密和哈希相关的操作。

为什么这样做？: ODAT 是一个功能复杂的工具，需要许多外部库和系统工具才能正常运行。这些命令就是为了确保所有依赖项都已安装到位，从而让 ODAT 能够顺利编译和执行。
~~~

