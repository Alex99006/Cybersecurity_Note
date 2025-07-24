
# 🛠️ 渗透测试中常见的 RPC 服务与利用方法

---

## ✅ 1. 识别 RPC 服务

RPC 通常运行在 **端口 111**，你可以用 `nmap` 或 `rpcinfo` 查看有哪些 RPC 程序开放：

```bash
# 使用 nmap 检测 RPC 服务
nmap -sV -p 111 [目标IP]

# 使用 rpcinfo 查看远程主机的 RPC 服务列表
rpcinfo -p [目标IP]
```

示例输出：
```
   program vers proto   port
    100000    2   tcp    111  rpcbind
    100003    3   tcp   2049  nfs
    100005    1   tcp   32803 mountd
```

---

## ✅ 2. 重点服务介绍

| 程序名     | 描述                             | 常见端口 |
|------------|----------------------------------|----------|
| **rpcbind** | RPC 路由器，协助客户端找到服务   | 111      |
| **nfs**     | 网络文件系统，可远程访问共享目录 | 2049     |
| **mountd**  | 与 NFS 配套，用于挂载远程目录    | 随机端口 |
| **rusersd** | 显示系统登录用户信息             | 可用于信息收集 |
| **rstatd**  | 提供系统状态信息                 | 可用于主机探测 |

---

## ✅ 3. NFS 渗透利用（常见场景）

在 HTB 或 VulnHub 靶场中，常见 RPC 开放 NFS 的服务：

### 步骤一：发现 RPC/NFS 服务
```bash
nmap -sV -p 111,2049 [IP]
rpcinfo -p [IP]
```

### 步骤二：列出 NFS 导出的共享目录
```bash
showmount -e [IP]
```

示例输出：
```
Export list for [IP]:
/home/shared *
```

### 步骤三：挂载共享目录
```bash
mkdir /mnt/nfs
sudo mount -t nfs [IP]:/home/shared /mnt/nfs
ls /mnt/nfs
```

---

## ✅ 4. 实战提权思路（基于 NFS）

1. 在共享目录中创建一个拥有 UID=0 的 fake root 用户文件
2. 上传 shell 或编写 cron 脚本（目标自动执行）
3. 获取 root shell

---

## ✅ 5. 总结常用命令

| 工具        | 命令                                  | 功能说明                 |
|-------------|----------------------------------------|--------------------------|
| `nmap`      | `nmap -sV -p 111,2049 10.10.10.10`     | 检查 rpc 和 nfs 服务     |
| `rpcinfo`   | `rpcinfo -p 10.10.10.10`               | 查看 RPC 服务列表        |
| `showmount` | `showmount -e 10.10.10.10`             | 列出导出的 NFS 目录      |
| `mount`     | `sudo mount -t nfs IP:/path /mnt/dir` | 挂载远程共享目录         |

---

## 🎯 推荐练习靶场

- HTB：**Nibbles、Lame、Bashed**
- VulnHub：**DC-2、Stapler**
