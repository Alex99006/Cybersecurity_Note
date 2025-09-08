## ==readelf 工具的使用==

~~~apl
# readelf 命令详解

`readelf` 是 GNU Binutils 提供的一个工具，用于显示 ELF (Executable and Linkable Format) 文件的信息。它可以查看 ELF 文件头、节区、段、符号表、调试信息等，非常适合逆向分析、调试和二进制研究。

---

## 基本语法
```bash
readelf <option(s)> elf-file(s)
~~~



------



## **参数详解**

### **通用选项**

- -a, --all

  等价于：-h -l -S -s -r -d -V -A -I，一次性显示所有常用信息。

- -e, --headers

  等价于：-h -l -S，显示 ELF 文件头、程序头、节区头。

- -H, --help

  显示帮助信息。

- -v, --version

  显示 readelf 版本号。

- @<file>

  从文件中读取选项。

------



### **文件头与段信息**

- -h, --file-header

  显示 ELF 文件头。

- -l, --program-headers 或 --segments

  显示程序头表（段信息）。

- -S, --section-headers 或 --sections

  显示节区头表。

- -g, --section-groups

  显示节区分组。

- -t, --section-details

  显示节区详细信息。

------



### **符号相关**

- -s, --syms 或 --symbols

  显示符号表。

- --dyn-syms

  显示动态符号表。

- --lto-syms

  显示 LTO 符号表。

- --sym-base=[0|8|10|16]

  指定符号大小显示的进制（默认混合，其他为八进制、十进制、十六进制）。

- -C, --demangle[=STYLE]

  解码被编译器修饰过的符号名。

  STYLE 可选：none, auto, gnu-v3, java, gnat, dlang, rust。

- --no-demangle

  禁止符号名解码（默认）。

- --recurse-limit / --no-recurse-limit

  启用或禁用解码递归深度限制。

------

### **编码与字符串显示**

- -U[dlexhi], --unicode=[default|locale|escape|hex|highlight|invalid]

  设置 Unicode 字符显示方式。

------

### **其他信息**

- -n, --notes

  显示 NOTE 段（调试或核心转储相关信息）。

- -r, --relocs

  显示重定位信息。

- -u, --unwind

  显示异常展开信息（如 .eh_frame）。

- -d, --dynamic

  显示动态段（动态链接信息）。

- -V, --version-info

  显示符号版本信息。

- -A, --arch-specific

  显示架构特定信息。

- -c, --archive-index

  显示归档文件的符号/文件索引。

- -D, --use-dynamic

  使用动态段信息显示符号。

- -L, --lint | --enable-checks

  启用检查，显示潜在问题。

------

### **数据转储**

- -x, --hex-dump=<number|name>

  以十六进制转储指定节内容。

- -p, --string-dump=<number|name>

  以字符串形式转储指定节内容。

- -R, --relocated-dump=<number|name>

  转储重定位后的节内容。

- -z, --decompress

  在转储前解压节内容。

------



### **调试信息**

- -w, --debug-dump=<选项>

  显示 DWARF 调试信息。

  子选项包括：

  

  - a 或 abbrev：缩写表
  - A 或 addr：地址信息
  - r 或 aranges：地址范围
  - c 或 cu_index：编译单元索引
  - L 或 decodedline：解析后的行信息
  - f 或 frames：堆栈帧
  - F 或 frames-interp：解释的堆栈帧
  - g 或 gdb_index：GDB 索引
  - i 或 info：调试信息入口
  - o 或 loc：位置描述符
  - m 或 macro：宏信息
  - p 或 pubnames：公共符号名
  - t 或 pubtypes：公共类型
  - R 或 Ranges：范围表
  - l 或 rawline：原始行表
  - s 或 str：字符串表
  - O 或 str-offsets：字符串偏移
  - u 或 trace_abbrev：trace 缩写
  - T 或 trace_aranges：trace 地址范围
  - U 或 trace_info：trace 信息

  

- -wk, --debug-dump=links

  显示指向单独调试文件的链接信息。

- -P, --process-links

  显示单独调试文件的非调试节内容（隐含 -wK）。

- -wK, --debug-dump=follow-links

  跟随链接到单独调试文件（默认）。

- -wN, --debug-dump=no-follow-links

  不跟随调试文件链接。

- --dwarf-depth=N

  限制显示 DWARF 信息的深度。

- --dwarf-start=N

  从指定偏移量开始显示 DWARF 信息。

------



### **CTF（Compact Type Format）**

- --ctf=<number|name>

  显示 CTF 类型信息。

- --ctf-parent=<name>

  指定 CTF 父对象。

- --ctf-symbols=<number|name>

  使用指定节作为外部符号表。

- --ctf-strings=<number|name>

  使用指定节作为外部字符串表。

------



### **统计与显示**

- -I, --histogram

  显示哈希桶长度直方图。

- -W, --wide

  允许输出超过 80 列宽。

- -T, --silent-truncation

  当符号名被截断时，不显示 [...]。

------



## **常用示例**

```apl
# 显示 ELF 文件头
readelf -h a.out

# 显示程序段信息
readelf -l a.out

# 显示节区信息
readelf -S a.out

# 查看符号表
readelf -s a.out

# 转储某个节内容（如 .text）
readelf -x .text a.out

# 查看 DWARF 调试信息
readelf -wi a.out
```



------

## **总结**

readelf 是分析 ELF 文件的利器，和 objdump 类似但更专注于 ELF 结构。常见用法是配合 -h, -l, -S, -s，进阶调试时可用 -w 系列参数查看 DWARF 信息。

