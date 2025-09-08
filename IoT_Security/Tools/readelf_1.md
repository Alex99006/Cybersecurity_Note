# **readelf**

#  **完整参数指南（逐项解释 + 实例）**

readelf 是 GNU binutils 提供的 ELF（Executable and Linkable Format）解析工具，专注展示 ELF 文件结构（文件头、段/节、符号、重定位、动态段、DWARF 等）。下面把 readelf --help 列出的每个选项逐条解释并给出常用示例与如何解读输出。

------

## **语法**

```apl
readelf [选项] <elf-file(s)>
readelf @options-file   # 从文件读取选项
```

> 说明：多数选项可以组合使用（例如 readelf -h -S file 等价于 readelf -e file）。长选项用 --，短选项用 -。

------

# **常用快速命令（速查）**

```apl
readelf -h file             # 文件头（entry、arch、phoff、shoff、flags）
readelf -l file             # 程序头（segments）——运行时加载信息
readelf -S file             # 节区头（section headers）
readelf -s file             # 符号表（.symtab）
readelf --dyn-syms file     # 动态符号表（.dynsym）
readelf -d file             # 动态段（NEEDED, RPATH, RUNPATH, SONAME）
readelf -r file             # 重定位表（.rel/.rela）
readelf --debug-dump=info file   # DWARF debug_info
readelf -x .rodata file     # 十六进制转储 .rodata 节
readelf -p .strtab file     # 以字符串方式转储 .strtab 节
```



------

# **逐项详解（按 help 列表）**

## **基本与组合选项**

- -a, --all

  **等价于**：-h -l -S -s -r -d -V -A -I。

  **用途**：一次性输出绝大多数重要信息（快速全览）。

  **示例**：

```apl
readelf -a /bin/ls
```

- -H, --help

  显示帮助文本（即 readelf --help 输出）。

- -v, --version

  显示 readelf 版本信息。

------

## **文件头与加载（程序头 / segments）**

- -h, --file-header

  **功能**：显示 ELF 文件头（ELF 类型：ET_EXEC/ET_DYN/ET_REL、机器架构、入口点、程序头表偏移、节区头表偏移、flags 等）。

  **示例**：

```apl
readelf -h a.out
```

- **示例输出解读片段**：

```apl
ELF Header:
  Class:                             ELF32
  Data:                              2's complement, big endian
  Type:                              EXEC (Executable file)
  Entry point address:               0x400080
  Start of program headers:          52 (bytes into file)
  Start of section headers:          4096 (bytes into file)
```

- Entry point address：程序入口地址（影响执行流）。
- Start of program headers：程序段表（segments）偏移，用于 -l。

- -l, --program-headers, --segments

  **功能**：显示程序头（每个 PT_LOAD/INTERP/DYNAMIC/NOTE/PHDR 等）。用于了解运行时内存映射（虚拟地址、文件偏移、权限 R/W/X）。

  **示例**：

```apl
readelf -l a.out
```

- **常见用途**：

  - 判断是否有可执行栈（GNU_STACK）。
  - 查看可写可执行段（RWX）——潜在利用点。
  - 找到入口基址（若非 PIE 则固定）。

- -S, --section-headers, --sections

  **功能**：显示节区头表（.text, .data, .bss, .rodata, .symtab, .strtab, .rela.dyn 等），每个 section 的偏移、地址、大小、类型、flags（SHF_EXECINSTR / SHF_WRITE / SHF_ALLOC / SHF_COMPRESSED）。

  **示例**：

```apl
readelf -S libfoo.so
```

- **解读**：

  - 查看 SHF_EXECINSTR（可执行）和 SHF_WRITE 标志确定可写可执行节。
  - 查找 .note.ABI-tag, .comment, .gnu.hash 等帮助分析。

- -g, --section-groups

  显示节区分组信息（COMDAT/group），用于 LTO 或链接器把节分组情况，较少日常使用，但对复杂链接或 LTO 产物重要。

- -t, --section-details

  显示更详细的节区内部信息（具体实现/版本可能有差异），并非每个版本都会输出额外内容。

- -e, --headers

  **等价于**：-h -l -S。一次查看文件头 + 程序头 + 节区头。

------

## **符号相关**

- -s, --syms 或 --symbols

  **功能**：显示符号表（.symtab）——索引、值（地址/偏移）、大小、类型（FUNC/OBJECT/SECTION/FILE）、绑定（LOCAL/GLOBAL/WEAK）、可见性、节号、符号名。

  **示例**：

```apl
readelf -s a.out
```

- **示例输出行（说明）**：

```apl
Num:    Value  Size Type    Bind   Vis      Ndx Name
15: 000104e0   123 FUNC    GLOBAL DEFAULT   14 main
```

- Value：符号在内存/文件中的地址或偏移。
- Size：符号大小（字节）。
- Ndx：符号所在节索引（UND 表示未定义，即导入符号）。



- --dyn-syms

  **功能**：显示动态符号表（.dynsym），用于运行时动态链接（通常只有导出/导入对）。

- --lto-syms

  显示 LTO( Link Time Optimization ) 相关的符号表（针对使用 LTO 的二进制）。

- --sym-base=[0|8|10|16]

  **功能**：强制 Size 列使用指定基数显示（8=八进制，10=十进制，16=十六进制）。

  **示例**：

```apl
readelf --sym-base=16 -s a.out
```



------

## **名称解码 / Unicode**

- -C, --demangle[=STYLE]

  **功能**：对修饰名（mangled name，如 C++ 的 name-mangling）进行 demangle，将 __Z3fooi 等还原为 foo(int)。

  **STYLE** 可选：none、auto、gnu-v3、java、gnat、dlang、rust。默认可通过 --demangle 自动选择。

  **示例**：

```apl
readelf -sC libfoo.so
```

- **用途**：阅读 C++ 符号或其他语言修饰名更友好，便于定位函数。

- --no-demangle

  **功能**：禁用 demangle（展示原始修饰名）。

- --recurse-limit / --no-recurse-limit

  **功能**：控制 demangling 中递归限制（有些极端或恶意构造名可能导致递归过深/耗时）。

- -U[dlexhi], --unicode=[default|locale|escape|hex|highlight|invalid]

  **功能**：控制 Unicode 字符在输出中的显示方式。

  

  - default / locale：按当前 locale 显示（默认）。

  - escape：使用 \uXXXX 等转义显示。

  - hex：用 <hex sequences> 显示。

  - highlight：高亮 escape 序列。

  - invalid：把无效字符显示为 {hex sequences}。

    **示例**：

```apl
readelf -Uescape -p .rodata a.out
```



------



## **Note / Reloc / Unwind / Dynamic / Version / Arch-specific**

- -n, --notes

  显示 NOTE 节（如 build-id、ABI-tags、core dump 注记、compiler notes 等）。

  **示例**：

```apl
readelf -n core_dump
```

- -r, --relocs

  显示重定位条目（.rel 或 .rela 节），包括重定位偏移、类型、关联符号。

  **示例**：

```apl
readelf -r libfoo.so
```

- **用途**：分析 GOT/PLT、查找哪些位置会在加载时被修补（对 GOT overwrite / ret2plt 攻击很重要）。

- -u, --unwind

  显示 unwind（栈展开）信息，通常来自 .eh_frame / .debug_frame，对异常处理、栈回溯有用。

  **示例**：

```apl
readelf -u a.out
```

- -d, --dynamic

  显示 .dynamic 节内容（NEEDED, SONAME, RPATH, RUNPATH, STRTAB/STRSZ references 等）。

  **示例**：

```apl
readelf -d /usr/bin/ldd_target
```

- **常见用途**：

  

  - 查找依赖库（NEEDED）。
  - 查找 RPATH / RUNPATH（影响动态链接搜索路径）。

  

- -V, --version-info

  显示版本节（.gnu.version, .gnu.version_r），用于展示 symbol 版本信息（glibc 导出符号的版本依赖等）。

- -A, --arch-specific

  显示架构特定信息（例如 ARM 的 ABI flags、MIPS 特殊标志等）。

------

## **归档与检查**

- -c, --archive-index

  当输入是 .a 静态库时，显示 archive 的符号/文件索引（成员列表）。

  **示例**：

```apl
readelf -c libstatic.a
```

- -D, --use-dynamic

  **功能**：在显示符号时优先使用动态节信息（.dynsym）或结合动态节信息来决定可用符号。对动态库分析有帮助。

- -L, --lint 或 --enable-checks

  显示可能存在的问题或警告（节对齐问题、重叠、不一致的表等）。

  **示例**：

```apl
readelf -lL a.out
```



------

## **数据/字符串/重定位转储**

- -x, --hex-dump=<number|name>

  将指定节按字节以十六进制转储。可用节名或节索引号。

  **示例**：

```apl
readelf -x .rodata a.out
readelf -x 12 a.out
```

- **用途**：查找嵌入字符串、静态数据或查验 shellcode bytes。

- -p, --string-dump=<number|name>

  将指定节以“字符串”形式转储（可打印字符），常对 .strtab, .rodata 有用。

  **示例**：

```apl
readelf -p .strtab a.out
```

- -R, --relocated-dump=<number|name>

  **功能**：转储应用重定位后的节内容（即把重定位项应用到节中再显示）。用于查看 GOT/PLT 在加载后实际的内存样子（在静态文件中模拟 link-time 修补效果）。

  **示例**：

```apl
readelf -R .data a.out
```



- -z, --decompress

  如果节被压缩（ELF 支持节压缩），先解压再转储。通常与 -x / -p 一起使用。

  **示例**：

```apl
readelf -z -x .debug_info a.out
```



------



## **DWARF / 调试信息（**-w 系列）

- -w, --debug-dump[...]

  显示 DWARF 调试段内容。readelf --help 列出了一系列子选项用于选择具体 DWARF 节。长选项形式更直观：--debug-dump=info、--debug-dump=frames 等。常用的一些子命令与用途：



| **子选项**        | **含义（DWARF 节）**               |
| ----------------- | ---------------------------------- |
| abbrev / a        | .debug_abbrev（缩写表）            |
| addr / A          | 地址表（辅助信息）                 |
| aranges / r       | .debug_aranges（地址范围）         |
| cu_index / c      | .debug_cu_index                    |
| decodedline / L   | 解析后的行信息（line table）       |
| frames / f        | .debug_frame / .eh_frame（帧信息） |
| frames-interp / F | 解释后的 frames                    |
| gdb_index / g     | .gdb_index                         |
| info / i          | .debug_info（最重要，包含 DIEs）   |
| loc / o           | .debug_loc（位置列表）             |
| macro / m         | 宏信息 .debug_macro                |
| pubnames / p      | .debug_pubnames                    |
| pubtypes / t      | .debug_pubtypes                    |
| Ranges / R        | .debug_ranges                      |
| rawline / l       | 原始行号表（未解析）               |
| str / s           | 字符串表 .debug_str                |
| str-offsets / O   | 字符串偏移表                       |
| trace_* / u,T,U   | Trace（调试追踪）相关              |



- **示例（长形式，清晰）**：

```apl
readelf --debug-dump=info a.out        # 显示 DWARF debug_info
readelf --debug-dump=decodedline a.out # 显示文件:line 映射（可定位源行）
readelf --debug-dump=frames a.out      # 显示帧信息（stack unwind）
```

- **组合示例**：

```apl
readelf --debug-dump=info,decodedline,frames a.out
```

- -wk, --debug-dump=links

  显示那些链接到“单独调试文件（separate debuginfo）”的节（帮助追踪分离的 debug 文件）。

- -P, --process-links

  显示单独调试文件中的非调试节内容（隐含 -wK 的行为）。

- -wK, --debug-dump=follow-links

  **默认**：跟随并解析 ELF 中对 “separate debug info” 的链接（例如 build-id 或 .gnu_debuglink 指向的外部 debuginfo 文件），这样会合并显示外部 debug 文件内容。

- -wN, --debug-dump=no-follow-links

  不跟随外部 debug 文件，只显示当前 ELF 内的 DWARF 信息。

- --dwarf-depth=N

  限制 DWARF DIE（Debug Information Entry）显示深度（减少输出量）。

- --dwarf-start=N

  从偏移量 N 开始显示 DWARF DIE（用于定位）。

**实用提示**：当目标是将地址映射回源代码（如果有 DWARF），用 --debug-dump=decodedline 能直接看到 address → source line 映射；用于追踪 bug/崩溃修复、分析函数边界、变量位置等。

------

## **CTF（Compact Type Format）相关**

- --ctf=<number|name>

  显示指定节的 CTF 信息（某些系统/工具使用的紧凑类型格式）。

  **示例**：

```apl
readelf --ctf=.ctf a.out
```

- --ctf-parent=<name> / --ctf-symbols=<number|name> / --ctf-strings=<number|name>

  用于指定 CTF 的父 archive / 外部符号表 / 字符串表等，便于解析复杂 CTF 存档。

------

## **直方图 / 格式 / 截断**

- -I, --histogram

  显示符号哈希表（.hash 或 .gnu.hash）的桶长度直方图，常用于分析动态链接查找效率或 hash 冲突情况。

- -W, --wide

  允许输出宽度超出 80 列，不自动换行（对长符号名/行有用）。

- -T, --silent-truncation

  当符号名被截断时 **不** 添加 [...] 标识（适合机器解析或想少输出修饰信息时）。

------

## **选项文件与其他**

- @<file>

  从指定文件读取选项（文件中每行一个选项或空格分隔），适合长命令集合或自动化脚本。

------

# **实战示例与解释（把选项和典型场景结合）**

## **示例 1：快速全面检查**

```apl
readelf -a ./vuln_binary
```

**得到**：文件头、段、节、符号、重定位、动态段、版本信息、架构信息、哈希直方图。

**用途**：快速判断是否有 NX、PIE、RELRO、Canary、RWX 等用于决定利用路径。

------

## **示例 2：找可执行栈 / GNU_STACK**

```apl
readelf -l ./vuln_binary | grep GNU_STACK -A 1
```

**若发现**：GNU_STACK 且权限有 RWE 或 RW 表明栈可能可执行（或未知），便可尝试栈注入 shellcode；若 GNU_STACK 没有则 NX 启用。



------

## **示例 3：查看 GOT/PLT & 重定位**

```apl
readelf -r ./libvuln.so
readelf -s ./libvuln.so | grep printf
```



- -r 看重定位项（哪些地址会在加载/链接时被修补）。
- -s 找符号在符号表中的地址/索引，配合 -r 找到可被覆盖的位置（Partial RELRO 情况可尝试 GOT overwrite）。

------

## **示例 4：查看动态依赖与 RPATH**

```apl
readelf -d ./app | grep -E 'NEEDED|RPATH|RUNPATH|SONAME'
```

**用途**：发现可控的 RPATH / RUNPATH 或 LD_LIBRARY_PATH 注入点，或替换库实现加载劫持。



------

## **示例 5：查看 DWARF 行号映射（调试）**

```apl
readelf --debug-dump=decodedline ./a.out
```

**用途**：把地址映射到源码行，配合崩溃地址可以迅速定位源码位置（如果编译时包含 debug info）。

------

## **示例 6：转储 .rodata 查找隐藏字符串**

```apl
readelf -p .rodata ./a.out        # 可打印字符串
readelf -x .rodata ./a.out        # 十六进制查看原始 bytes
```

**用途**：查找硬编码的命令、URL、错误消息、密钥等。

------

## **示例 7：查看符号解码差异（C++）**

```apl
readelf -s libexample.so          # 显示 mangled 名
readelf -sC libexample.so         # 使用 demangle，显示 human-readable 名
```



------

# **输出字段说明（常见表格列）**

- **ELF Header**（-h）中重要字段如 Entry point address, Type, Machine, Flags。
- **Program Headers**（-l）列：Type, Offset, VirtAddr, PhysAddr, FileSiz, MemSiz, Flags（R/W/X）, Align。
- **Section Headers**（-S）列：[Nr] Name Type Addr Off Size ES Flg Lk Inf Al（Flg 包含 A=ALLOC W=WRITE X=EXEC）。
- **Symbol Table**（-s）列：Num: Value Size Type Bind Vis Ndx Name。
- **Relocations**（-r）列：Offset Info Type Sym.Value Sym.Name Addend（或 .rela 格式含 Addend）。

------

# **常见问题 & 排查技巧**

- **输出太多 / 只想看特定项**：使用 -h/-S/-l/-s/-d 单独查看，或 readelf -a file | less 分页检视。
- **找不到符号（strip）**：若 Stripped: Yes，符号被剥离，使用 --dyn-syms 看动态导出符号，或用 strings、objdump -d 静态分析。
- **DWARF 在外部（分离 debuginfo）**：readelf -wK file（默认）会尝试跟随外部 debug 文件；-wN 禁止跟随。
- **想把地址映射到源码**：若有 DWARF，使用 --debug-dump=decodedline；若没有，则需基于符号表和 objdump 输出手工推断。
- **节被压缩**：使用 -z 解压缩后再转储。

------

# **小结（实践建议）**

- readelf -h -l -S -s -d -r 是二进制快速审查的基本组合。
- 对于利用开发，重点看 **PIE/NX/RELRO/Canary/RWX/Stripped** —— readelf 能给出绝大多数线索。
- DWARF（-w）用于源码级调试与定位，但可能存在独立 debuginfo 文件。
- 当怀疑动态链接或库劫持，优先查看 -d（NEEDED / RPATH）和 --dyn-syms。

------

