# 📦 Packet Transfer（数据包传输）学习笔记  
> 日期：2025-07-04  

---

## 🖼️ 图示简介

这张图展示了在网络通信中数据如何从发送端（Sender）封装并通过各层协议传输，最后被接收端（Receiver）解封装还原的过程。

---

## 🧱 层级结构解析（Layer Breakdown）

| 层级 | 名称 | 描述 |
|------|------|------|
| Application | 应用层 | 用户使用的应用程序产生的数据，如网页、文件传输等。 |
| Transport (TCP/UDP) | 传输层 | 添加 TCP/UDP 头部，确保数据完整可靠传输。 |
| Network (IP) | 网络层 | 添加 IP 头部，决定数据包的路径和目标地址。 |
| Data Link (MAC) | 数据链路层 | 添加 MAC 头部，处理物理网络中的点对点通信。 |
| Physical | 物理层 | 将帧转化为二进制比特流，通过电信号或光纤传输。 |

---

## 🔄 数据封装过程（Sender Side: Encapsulation）

```plaintext
Data
↑
H + Data (Application Header)
↑
H + H + Data (Transport Header)
↑
IP + TCP + Data
↑
MAC + IP + TCP + Data
↑
Binary Transmission (0s and 1s)
```

---

## 🔄 数据解封装过程（Receiver Side: Decapsulation）

```plaintext
Binary Transmission
↓
MAC + IP + TCP + Data
↓
IP + TCP + Data
↓
TCP + Data
↓
Data
```

---

## 📚 各层术语汇总

| 层 | 数据单位（PDU） | 举例 |
|----|----------------|------|
| Application | Data 数据 | HTTP请求、FTP文件 |
| Transport | Segment / Datagram 段/数据报 | TCP段 |
| Network | Packet 数据包 | IP包 |
| Data-Link | Frame 帧 | Ethernet帧 |
| Physical | Bit 位 | 二进制信号（0/1）|

---

## 🧠 知识点总结（Summary）

- 每一层负责一个特定的功能，并将上层数据加上自己的“头部（Header）”再往下传。
- 数据通过 **以太网（Ethernet）** 在物理介质中传输。
- 接收端逆向进行解封装，还原原始数据。
- 理解封装和解封装对于**抓包分析**和**渗透测试**非常重要！

---

