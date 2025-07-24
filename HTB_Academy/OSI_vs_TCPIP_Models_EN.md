# OSI vs TCP/IP Model Comparison Explained

> 📅 Date: 2025-07-04  
> 📚 For: HTB CPTS Pathway, Cybersecurity Fundamentals, Pentesting, Packet Analysis

---

## Unified Diagram Breakdown

### ① OSI Model (Open Systems Interconnection Model)

| Layer | Name | Purpose | Examples |
|-------|------|---------|----------|
| 7 | Application Layer | Interface for user-network interaction | FTP, HTTP, SSH, DNS |
| 6 | Presentation Layer | Data encoding, encryption/decryption, format conversion | JPG, PNG, SSL, TLS |
| 5 | Session Layer | Session management (login/disconnect) | NetBIOS, RPC |
| 4 | Transport Layer | End-to-end connection, data transmission control | TCP, UDP |
| 3 | Network Layer | Routing and IP addressing | IP, Router, L3 Switch |
| 2 | Data Link Layer | MAC address handling, frame error detection | Switch, Bridge, Ethernet |
| 1 | Physical Layer | Transmitting bits via physical media | Network card, cable, fiber |

---

### ② TCP/IP Model (Practical Communication Model)

| Layer | Name | Corresponding OSI Layers | Function |
|-------|------|--------------------------|----------|
| 4 | Application | OSI Layers 5-7 | Real protocols/programs communication |
| 3 | Transport | OSI Layer 4 | End-to-end reliable/unreliable transfer |
| 2 | Internet | OSI Layer 3 | IP routing and addressing |
| 1 | Link | OSI Layers 1-2 | Framing, MAC addressing, physical transmission |

---

### ③ PDU (Protocol Data Unit) Mapping

| Layer | Name | Data Format (PDU) |
|-------|------|--------------------|
| Application | Data | Raw data |
| Transport | Segment / Datagram | TCP segment or UDP datagram |
| Network | Packet | Packet (with IP header) |
| Data Link | Frame | Frame (with MAC header) |
| Physical | Bit | Bitstream (0s and 1s) |

---

## Real Example: Visiting example.com from a browser

1. Application Layer: HTTP request (Data)
2. Transport Layer: Add TCP header → Segment (includes port)
3. Network Layer: Add IP header → Packet (includes IP address)
4. Data Link Layer: Add MAC header → Frame (LAN delivery)
5. Physical Layer: Convert to Bitstream and transmit via wire

---

## 🎯 Key Takeaways

- TCP/UDP: Transport Layer protocols (OSI Layer 4)
- IP: Network Layer protocol for addressing and routing
- Data format transforms layer-by-layer (Data → Segment → Packet → Frame → Bit)
- TCP: Reliable connection | UDP: Faster but unreliable (e.g. video, DNS)

---

🧠 Tip: Use packet capture tools like Wireshark to observe layer-wise data encapsulation in action.
