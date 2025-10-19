# checksec 命令详解

`checksec` 是一款常用的安全检测工具，用于分析 ELF 可执行文件、进程以及内核是否启用了安全防护机制。它在漏洞利用、逆向工程和渗透测试中非常常见。

---

## 🧩 检测的安全特性
- **RELRO**：重定位表保护（Partial / Full）
- **Canary**：栈溢出保护
- **NX (DEP)**：不可执行栈和堆
- **PIE**：位置无关可执行文件
- **RPATH / RUNPATH**：动态库加载路径
- **FORTIFY**：编译时的 `_FORTIFY_SOURCE` 检查
- **ASLR / KASLR / SMEP / SMAP**：内存随机化及内核保护

---

## 🛠️ 基本语法
```apl
checksec [选项] <目标文件或进程ID>
```



------

## **📌 参数详解**

### **1. 帮助与版本**

- --help

  显示帮助信息。

- --version

  显示 checksec 版本。

------

### **2. 文件检测**

- --file <binary>

  检查指定 ELF 二进制文件的安全特性。

  示例：

```apl
checksec --file /bin/ls
```

- --file=<binary1> <binary2> ...

  一次检测多个 ELF 文件。

- --fortify-file <binary>

  检查指定文件是否启用了 _FORTIFY_SOURCE 机制。

- --fortify-functions

  列出 ELF 文件中使用了 FORTIFY 的函数。

------

### **3. 进程检测**

- --proc <pid>

  检查指定进程的安全特性。

  示例：

```apl
checksec --proc 1234
```

- --proc-libs <pid>

  检查进程加载的共享库安全特性。

- --proc-maps <pid>

  检查进程内存映射，查看 NX、R/W/X 等权限。

- --proc-all

  检查系统上所有正在运行的进程安全特性。

------

### **4. 内核检测**

- --kernel

  检查内核是否启用了安全机制（如 ASLR、SMEP、KASLR 等）。

- --kernel-verbose

  显示更详细的内核安全检测信息。

------

### **5. 输出与格式控制**

- --format=json

  以 JSON 格式输出检测结果，便于脚本化处理。

- --format=csv

  以 CSV 格式输出结果。

- --output=<file>

  将结果保存到指定文件。

------

## **🔹 常用示例**

```apl
# 检查 ELF 文件
checksec --file /bin/bash

# 检查多个 ELF 文件
checksec --file /bin/ls /bin/cat

# 检查进程 ID = 1234 的进程
checksec --proc 1234

# 检查进程加载的共享库
checksec --proc-libs 1234

# 检查进程内存映射
checksec --proc-maps 1234

# 检查系统所有进程
checksec --proc-all

# 检查内核安全机制
checksec --kernel

# 详细内核安全信息
checksec --kernel-verbose

# 检查文件中的 FORTIFY 函数
checksec --fortify-file /bin/ls --fortify-functions

# 输出 JSON 格式结果
checksec --file /bin/bash --format=json

# 输出到文件
checksec --file /bin/bash --output=result.txt
```



------

## **✅ 总结**

- checksec 用于检测 **二进制文件、进程和内核** 的安全机制。
- 最常用的参数是：--file、--proc、--kernel。
- 在渗透测试或漏洞利用前，可以快速判断目标是否启用了常见防护机制，从而决定利用方式。

## ==例子==

明白了，我们来详细分析你 checksec 的回显信息，并讲解它意味着什么、可利用性如何，以及渗透测试或漏洞利用中可能的操作。你给出的回显是针对一个 **MIPS 32-bit 大端 ELF** 文件的：

```apl
Arch:       mips-32-big
RELRO:      Partial RELRO
Stack:      No canary found
NX:         NX unknown - GNU_STACK missing
PIE:        No PIE (0x400000)
Stack:      Executable
RWX:        Has RWX segments
Stripped:   No
```



------

## **1️⃣ Arch: mips-32-big**

- **意思**：这是一个 **MIPS 32位大端**架构的 ELF 文件。

- **利用信息**：

  - 编写 shellcode 或 ROP 链时，需要使用 MIPS 指令集。
  - 工具如 ropper, radare2, gdb-multiarch 都需要指定 MIPS 架构。

  

- **示例**：

```apl
gdb-multiarch ./vulnerable_binary
set architecture mips
```



------

## **2️⃣ RELRO: Partial RELRO**

- **意思**：

  - RELRO（Read-Only Relocations）用于防止 GOT 表被覆盖。
  - Partial RELRO：只读保护 **部分 GOT**，但 .got.plt 依然可写。

- **利用信息**：

  - 可能仍可通过 GOT 覆盖攻击（如 printf@GOT 重定向到 system）。
  - Full RELRO 会阻止这类攻击。

  

- **示例**：

```apl
// 溢出修改 GOT
*(void**)&printf_got = system;
```



------

## **3️⃣ Stack: No canary found**

- **意思**：

  - 栈保护（Stack Canary）未启用。
  - 栈溢出攻击不会触发 canary 检测。

- **利用信息**：

  - 可以尝试 **栈溢出攻击** 或 **ret2libc/ROP**。
  - 如果存在缓冲区溢出漏洞，可以直接覆盖返回地址。

  

- **示例**：

```apl
char buffer[64];
gets(buffer); // 没有 canary，直接溢出
```



------

## **4️⃣ NX: NX unknown - GNU_STACK missing**

- **意思**：
  - NX（No eXecute）不确定，因为 ELF 的 GNU_STACK 节缺失。
  - 栈可能是可执行的。
- **利用信息**：
  - **Shellcode 可以直接注入到栈上并执行**。
  - 如果 NX 已启用，则需要用 ROP 绕过。
- **示例**：

```apl
# MIPS shellcode 注入栈执行
li $v0, 4001   # sys_execve
la $a0, cmd
syscall
```



------

## **5️⃣ PIE: No PIE (0x400000)**

- **意思**：

  - 文件不是位置无关可执行文件（PIE）。
  - 基址固定在 0x400000。

- **利用信息**：

  - **ROP 链和返回地址攻击更容易**，因为地址固定。
  - 不需要泄漏基址即可利用。

  

- **示例**：

```apl
ret_addr = 0x4007a0  # fixed address
payload = b"A"*offset + p32(ret_addr)
```



------

## **6️⃣ Stack: Executable**

- **意思**：

  - 栈是可执行的。

- **利用信息**：

  - 栈上注入 shellcode 并直接执行是可行的。

  

- **示例**：

```apl
./vulnerable_binary $(python3 -c 'print(b"\x90"*100 + shellcode)')
```



------

## **7️⃣ RWX: Has RWX segments**

- **意思**：

  - 文件中存在同时可读、可写、可执行的段。

- **利用信息**：

  - 攻击者可以将数据段或 BSS 段作为 shellcode 存放区。
  - 提供了额外攻击面（如 heap shellcode）。

  

- **示例**：

```apl
# 将 shellcode 写入 RWX 段再跳转执行
j rwx_segment_start
```



------

## **8️⃣ Stripped: No**

- **意思**：

  - 符号未被剥离（binary 还保留函数名）。

- **利用信息**：

  - 逆向和漏洞分析更容易。

  - 可以直接通过函数名发现潜在漏洞（如 strcpy, gets）

    

- **示例**：

```apl
nm ./binary | grep strcpy
```



------

## **🔹 总结分析**

从你的回显可以得到：

1. **攻击面非常大**：
   - 没有栈 canary。
   - 栈可执行。
   - RWX 段存在。
   - PIE 未启用 → 地址固定。
2. **可尝试的利用手法**：
   - 栈溢出 + shellcode 注入。
   - GOT 覆盖（Partial RELRO）。
   - ROP 链利用。
   - Heap shellcode（RWX 段）。
3. **辅助信息**：
   - MIPS 架构 → 需要 MIPS 工具链。
   - 符号未剥离 → 利用 nm / objdump 定位函数。

------

![checksec_ex_img](/Image/checksec_ex_img.png)
