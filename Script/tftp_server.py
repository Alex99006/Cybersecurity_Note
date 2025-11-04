import tftpy
import logging

# 设置日志级别，方便排查
logging.basicConfig(level=logging.DEBUG)

# TFTP 根目录
root_dir = "/Users/Hacker_learn/tftpboot"

# 创建 TFTP 服务实例
server = tftpy.TftpServer(root_dir)

# 启动服务
# 注意：U-Boot 默认使用 UDP 69，需要 root 权限
try:
    print("TFTP server starting on 0.0.0.0:69 ...")
    server.listen('0.0.0.0', 69)
except Exception as e:
    print("Error:", e)
