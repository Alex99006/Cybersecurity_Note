👌 那我就帮你整理一份完整的 **checksec 参数手册（Markdown 版）**，格式和之前的 readelf 保持一致，方便你上传到 GitHub。

```
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
```bash
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