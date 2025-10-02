#!/bin/bash

# 脚本名称: setup_tap_and_disable_aslr.sh
# 作用: 1. 关闭 ASLR 2. 创建并配置 TAP 虚拟网卡
#
# 用法示例: sudo ./setup_tap_and_disable_aslr.sh tap0 192.168.3.1/24

# --- 配置及参数检查 ---
INTERFACE=$1  # 第一个参数: 接口名称 (e.g., tap0)
IP_ADDRESS=$2 # 第二个参数: IP 地址/掩码 (e.g., 192.168.3.1/24)

# 检查是否以 root 权限运行
if [ "$(id -u)" != "0" ]; then
    echo "错误: 此脚本必须使用 sudo 运行。"
    echo "用法: sudo ./setup_tap_and_disable_aslr.sh <接口名> <IP/掩码>"
    echo "示例: sudo ./setup_tap_and_disable_aslr.sh tap0 192.168.3.1/24"
    exit 1
fi

# 检查参数是否完整
if [ -z "$INTERFACE" ] || [ -z "$IP_ADDRESS" ]; then
    echo "错误: 缺少必要的参数 (接口名或 IP 地址)。"
    echo "用法: sudo ./setup_tap_and_disable_aslr.sh <接口名> <IP/掩码>"
    echo "示例: sudo ./setup_tap_and_disable_aslr.sh tap0 192.168.3.1/24"
    exit 1
fi

# -----------------------------------------------------------
## 核心步骤 1: 关闭地址空间布局随机化 (ASLR)
# -----------------------------------------------------------

echo "=========================================="
echo "[*] 正在关闭 ASLR (地址空间布局随机化)..."
# 将 0 写入 /proc/sys/kernel/randomize_va_space
# 0 表示完全禁用 ASLR
echo 0 > /proc/sys/kernel/randomize_va_space

# 验证 ASLR 状态
CURRENT_ASLR_STATE=$(cat /proc/sys/kernel/randomize_va_space)

if [ "$CURRENT_ASLR_STATE" -eq 0 ]; then
    echo "[+] ASLR 关闭成功！当前状态: ${CURRENT_ASLR_STATE}"
else
    echo "[!] ASLR 状态验证失败！当前状态: ${CURRENT_ASLR_STATE}"
fi
echo "=========================================="


# -----------------------------------------------------------
## 核心步骤 2: 配置 TAP 虚拟网卡
# -----------------------------------------------------------

echo "[*] 正在创建并配置 ${INTERFACE} 虚拟网卡..."

# 1. 创建 TAP 接口
echo "  -> 正在创建 ${INTERFACE}..."
tunctl -t ${INTERFACE} -u $(logname)

# 2. 为接口设置 IP 地址和掩码并激活
echo "  -> 正在设置 IP 地址 ${IP_ADDRESS} 并激活接口..."
ifconfig ${INTERFACE} ${IP_ADDRESS} up

echo "[+] ${INTERFACE} 配置成功！IP 地址: ${IP_ADDRESS}"
echo "[*] 请使用 ip a show ${INTERFACE} 检查状态。"

