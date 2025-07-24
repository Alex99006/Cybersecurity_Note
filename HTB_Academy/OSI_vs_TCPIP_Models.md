# OSI vs TCP/IP 模型对比详解

> 📅 日期：2025-07-04  
> 📚 适用范围：HTB CPTS 路线、网络安全基础、渗透测试、抓包分析

---

## 一图三分解说明

### ① OSI 模型（Open Systems Interconnection Model）

| 层级 | 名称 | 作用 | 举例 |
|------|------|------|------|
| 7 | 应用层 (Application) | 用户与网络交互的接口 | FTP、HTTP、SSH、DNS |
| 6 | 表示层 (Presentation) | 数据编码、加密解密、格式转换 | JPG、PNG、SSL、TLS |
| 5 | 会话层 (Session) | 管理会话状态，如登录/断开连接 | NetBIOS、RPC |
| 4 | 传输层 (Transport) | 提供端到端连接，控制传输 | TCP、UDP |
| 3 | 网络层 (Network) | 路由选择，IP地址寻址 | IP、Router、L3 Switch |
| 2 | 数据链路层 (Data Link) | MAC地址、帧处理、错误检测 | Switch、Bridge、Ethernet |
| 1 | 物理层 (Physical) | 传输比特流（电信号/光信号） | 网卡、电缆、光纤 |

---

### ② TCP/IP 模型（实用通信模型）

| 层级 | 名称 | 对应 OSI 层 | 功能 |
|------|------|--------------|------|
| 4 | 应用层 (Application) | OSI 第 5-7 层 | 实际的程序/协议通信 |
| 3 | 传输层 (Transport) | OSI 第 4 层 | 端到端的可靠/非可靠传输 |
| 2 | 网络层 (Internet) | OSI 第 3 层 | IP路由、寻址 |
| 1 | 链路层 (Link) | OSI 第 1-2 层 | 帧、MAC地址、物理传输 |

---

### ③ PDU（协议数据单元）对照

| 层 | 名称 | 数据形式（PDU） |
|----|------|-----------------|
| 应用层 | Data | 数据 |
| 传输层 | Segment / Datagram | TCP 段 或 UDP 数据报 |
| 网络层 | Packet | 数据包（含 IP 头） |
| 数据链路层 | Frame | 帧（含 MAC 头） |
| 物理层 | Bit | 比特流（0/1） |

---

## 实际举例：浏览器访问 example.com

1. 应用层：HTTP 请求（Data）
2. 传输层：加 TCP头，成为 Segment（含端口号）
3. 网络层：加 IP头，成为 Packet（含 IP 地址）
4. 数据链路层：加 MAC头，成为 Frame（局域网传输）
5. 物理层：转换为 Bit 比特流通过网线传输

---

## 🎯 总结重点

- TCP/UDP：传输层协议（OSI第4层）
- IP：网络层协议，控制寻址和路由
- 数据形式随层变化（Data → Segment → Packet → Frame → Bit）
- TCP：可靠连接，UDP：快速但不可靠（如视频、DNS）

---

🧠 建议配合抓包工具如 Wireshark 理解每层数据封装过程。
