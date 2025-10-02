#!/bin/bash

# 脚本名称: qemu_setup_named.sh
# 作用: 1. 关闭 ASLR 2. 配置网络接口，支持命名参数
#
# 注意: 此脚本假设您已拥有 root 权限，且没有 sudo 命令。
#
# 期望用法: ./qemu_setup_named.sh eth0 192.168.3.2/24 br0 192.168.3.3/24

# --- 变量初始化 ---
PHYSICAL_IFACE=""
ETH0_IP_CIDR=""
DUMMY_IFACE="br0" # 虚拟接口固定命名为 br0，但可以根据参数修改
BR0_IP_CIDR=""

# --- 解析命名参数 ---
while [[ $# -gt 0 ]]; do
    case "$1" in
        eth0)
            PHYSICAL_IFACE="$1"
            ETH0_IP_CIDR="$2"
            shift # 跳过 eth0 的 IP 地址
            ;;
        br0)
            DUMMY_IFACE="$1"
            BR0_IP_CIDR="$2"
            shift # 跳过 br0 的 IP 地址
            ;;
        *)
            # 忽略任何其他未知参数
            ;;
    esac
    shift # 移动到下一个参数
done

# --- 校验和默认值 ---
# 再次检查关键参数是否完整
if [ -z "$PHYSICAL_IFACE" ] || [ -z "$ETH0_IP_CIDR" ] || [ -z "$DUMMY_IFACE" ] || [ -z "$BR0_IP_CIDR" ]; then
    echo "错误: 缺少必要的参数。"
    echo "请提供物理接口和虚拟接口的 IP 地址。"
    echo "用法: ./qemu_setup_named.sh eth0 <eth0_IP/掩码> br0 <br0_IP/掩码>"
    echo "示例: ./qemu_setup_named.sh eth0 192.168.3.2/24 br0 192.168.3.3/24"
    exit 1
fi

# -----------------------------------------------------------
## 核心步骤 1: 关闭地址空间布局随机化 (ASLR)
# -----------------------------------------------------------

echo "=========================================="
echo "[*] 正在关闭 ASLR (地址空间布局随机化)..."

# 禁用 ASLR (0 表示完全禁用)
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
## 核心步骤 2: 配置网络接口
# -----------------------------------------------------------

echo "[*] 正在配置网络接口..."

# 1. 创建 Dummy 接口 (br0)
echo "  -> 正在创建虚拟接口 ${DUMMY_IFACE}..."
ip link add ${DUMMY_IFACE} type dummy 
ip link set ${DUMMY_IFACE} up

# 2. 配置物理接口 (eth0)
echo "  -> 正在配置 ${PHYSICAL_IFACE} 为 IP: ${ETH0_IP_CIDR}..."
ifconfig ${PHYSICAL_IFACE} ${ETH0_IP_CIDR} up

# 3. 配置虚拟接口 (br0)
echo "  -> 正在配置 ${DUMMY_IFACE} 为 IP: ${BR0_IP_CIDR}..."
ifconfig ${DUMMY_IFACE} ${BR0_IP_CIDR} up


# 4. 最终状态检查
echo "=========================================="
echo "[+] 网络配置完成！"
echo "[*] ${PHYSICAL_IFACE} 的 IP 地址: ${ETH0_IP_CIDR}"
echo "[*] ${DUMMY_IFACE} 的 IP 地址: ${BR0_IP_CIDR}"
echo "[*] 使用 'ifconfig' 命令检查所有接口状态。"
echo "=========================================="

