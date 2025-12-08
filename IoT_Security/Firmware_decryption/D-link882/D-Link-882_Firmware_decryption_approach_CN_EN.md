# D-Link-882解密CN/English version at the bottom

### 1、先解压文件夹,会发现有两个`pdf`文件

![](/Image/882-1.png)

### 2、查看`pdf`文件

~~~bash
阅读 pdf 文件后可以推断出 v1.10版本是需要 v1.04 版本解密后再去生成的
~~~

![](/Image/882-2.png)

### 3、使用 `binwalk`验证

![](/Image/882-3.png)

### 4、现在明确了大致的逻辑后，开始解包 v1.04版本

~~~apl
binwalk -Me DIR882A1_FW104B02_Middle_FW_Unencrypt.bin  # 解包 104 版本后进入
find ./ -name *decrypt* 2>/dev/null  #  检索带有关键字decrypt的文件  得到 imgdecrypt
~~~

![](/Image/882-4.png)

------

### 4.1为什么搜索 `*decrypt*`？

在固件和二进制程序中，文件名或函数名常常遵循清晰的命名约定，这些名称是查找特定功能的最佳线索。

- **程序逻辑：** 如果固件文件在启动或升级时需要解密，那么它几乎必然包含一个负责“解密（decrypt）”操作的程序或脚本。
  - **示例文件名：** `imgdecrypt` (映像解密)、`firmware_decrypt_tool`、`updater_decrypt.sh`。
- **库函数：** 即使没有单独的程序，**解密操作**也需要被某个库函数调用。搜索包含 `decrypt` 关键字的文件（例如共享库文件 `.so` 或静态库 `.a`）可能会直接指向包含解密函数的库。
- **效率：** 这是最直接、最具针对性的搜索方法，能迅速排除大量无关文件。

------

## 4.2.固件逆向中可搜索的通用关键词

除了 `decrypt`，您应该搜索以下几类关键词，以全面定位固件中的安全和核心功能：

| 关键词类别    | 关键词 (英文/常见缩写)                                       | 搜索目的                                         | 示例文件名/函数                             |
| ------------- | ------------------------------------------------------------ | ------------------------------------------------ | ------------------------------------------- |
| **加密/解密** | `encrypt`, `crypto`, `aes`, `rsa`, `key`, `ssl`, `cert`, `tls`, `ssh` | 查找所有加密、签名、证书和密钥管理组件。         | `libcrypto.so`, `ssl_config`, `keygen`      |
| **升级/配置** | `update`, `upgrade`, ,`download`,`config`, `settings`, `flash`, `factory` | 查找固件更新机制、配置存储或恢复出厂设置的逻辑。 | `do_upgrade.sh`, `/etc/config`, `mtd_write` |



### 5、去检索一下和`imgdecrypt`相关联的文件

~~~apl
grep -ir "imgdecrypt"  #  检索关联文件 找到了 prog.cgi
#  所以说 prog.cgi 和 imgdecrypt是关联的
#  由下面的解释可以知道 是prog.cgi调用了imgdecrypt
~~~

![](/Image/882-5.png)

### 5.1分析一下启动项

~~~apl
我们在 etc_ro下去寻找一下我们熟悉的rcS
# etc_ro:许多启动脚本、网络配置脚本
cat rcS # 发现 goahead&已经注释了，所以说我们的启动服务可能不是 gahead 服务了
所以我们现在需要去找到启动的服务
我们知道etc_ro 里面包括了了许多启动脚本、网络配置脚本等，所以在 etc_ro 文件夹下去 ls 看一下，会发现一个叫 lighthttpd 的文件夹(可疑)
进入文件夹后会找到一个名为lighthttpd.conf配置文件
当我们使用 cat 去查看这个文件的时候会发现 所有以规定格式结尾的文件请求，都将被发送给 /bin/prog.cgi 来处理。
~~~

![](/Image/882-10.png)

### 5.2验证猜想

~~~apl
ls ../bin/ | grep lighttpd   #  在 bin目录下发现了lighttpd服务
~~~



## `prog.cgi` 在固件中的作用

在许多使用 Web 服务器的嵌入式系统中，`prog.cgi` 是一个非常**中心化**的程序。它通常不只是处理一个功能，而是处理**多个核心管理任务**：

1. **处理配置变更：** 接收用户提交的新 Wi-Fi 密码、端口转发规则等，然后将这些设置写入 **NVRAM**（非易失性存储器）或其他配置文件。
2. **执行核心操作：** 处理重启、升级固件、恢复出厂设置等敏感请求。
3. **API 接口：** 尤其在现代设备中，`prog.cgi` 或类似的 CGI 程序可能被配置为处理特定的 API 请求，例如 **HNAP（Home Network Administration Protocol）** 或其他 SOAP/JSON 格式的管理流量。

------

##  `prog.cgi` 对逆向工程的重要性

对于固件逆向工程和安全分析来说，`prog.cgi` 是一个**高价值的目标**，因为它暴露了设备的核心逻辑：

- **集中分析点：** 它是处理几乎所有 Web UI 交互的中央枢纽。通过逆向分析这个单一的二进制文件，您可以快速掌握设备管理的所有功能和漏洞点。
- **权限执行：** CGI 程序通常以 **root** 或其他高权限用户身份运行，这意味着如果其中存在漏洞（如命令注入、缓冲区溢出），攻击者可以轻松地获得设备的最高权限。
- **敏感信息：** `prog.cgi` 中很可能包含：
  - **硬编码的命令**（例如直接调用 `system()` 或 `exec()` 来执行 Shell 命令）。
  - **配置文件的路径**。
  - **验证和授权逻辑**（例如如何检查登录密码）。

### 6、这个时候就可以把`imgdecrypt`和`prog.cgi`丢进IDA进行分析

==imgdecrypt==

~~~apl
 IDA 看伪 c 发现 decrypt_firmar 双击进入
 发现了可疑代码 printf("key:");
 printf("key:");的前置条件是 sub_402554((int)v5)
 追踪 sub_402554 发现了 sub_40108C
 在sub_40108C 中 看到了 AES_set_decrypt_key
 到这里其实我们可以大体判断出，这个 imgdecrypt 是一个解密的文件了
~~~

------

~~~apl
进入 IDA 后通过命名发现了疑似解密函数 decrypt_firmare
进入后查看伪 C 代码
~~~



![](/Image/882-11.png)

### 相关代码分析

- 接受命令行参数：argv[1] 是要处理（解密/解包/验证）的固件或文件；可选的 argv[2] 指定公钥（默认 "/etc_ro/public.pem"）。
- 读取/初始化公钥（sub_40215C）。
- 基于公钥/RSA 逻辑生成或导出一个 16 字节对称密钥（sub_402554 填充 v5）。
- 打印该 16 字节密钥（以十六进制）。
- 使用该密钥对 argv[1] 执行解密/处理（sub_401780），输出到 /tmp/.firmware.orig。
- 若成功，则删除原文件并把解密后的文件重命名为原始文件名（替换原文件）。
- 释放 RSA 对象并返回子操作结果。

换句话说：**这是一个“用公钥派生/解密对称密钥，然后用该对称密钥解密固件文件并覆盖原文件”的工具/函数。**

![](/Image/882-12.png)

==prog.cgi==

~~~apl
搜索字符串 imgdecrypt
进入 sub_46640C 后直接查看伪C 代码,发现在调用imgdecrypt之前在HTML_hnap_xml_header中处理过
在下面图三中可以清楚的看到调用过程
所以可以确定imgdecrypt就是解密程序了
~~~

![](/Image/882-6.png)

![](/Image/882-7.png)

![](/Image/882-8.png)

### 8、开始对`v1.10`版本进行解密

~~~apl
readelf -h imgdecrypt  #  little endian
cp /usr/bin/qemu-mipsel-static  ./  
sudo chroot . ./qemu-mipsel-static ./bin/imgdecrypt DIR882A1_FW110B02.bin
#  回显  key:C05FBF1936C99429CE2A0781F08D6AD8
sudo binwalk -Me --run-as=iot DIR882A1_FW110B02.bin  # 解包成功
~~~

------

# D-Link-882 Decryption

### 1. First, extract the folder — you will find two `pdf` files

![img](/Image/882-1.png)

### 2. View the `pdf` files

```apl
After reading the PDF files, it can be inferred that version v1.10 needs to be generated after decrypting version v1.04.
```



![img](/Image/882-2.png)

### 3. Verify using `binwalk`

![img](/Image/882-3.png)

### 4. Now that the general logic is clear, start unpacking version v1.04

```apl
binwalk -Me DIR882A1_FW104B02_Middle_FW_Unencrypt.bin  # Unpack version 1.04 and enter
find ./ -name *decrypt* 2>/dev/null  # Search for files containing the keyword "decrypt", found imgdecrypt
```



![img](/Image/882-4.png)

------

### 4.1 Why search for `*decrypt*`?

In firmware and binary programs, filenames or function names often follow clear naming conventions; these names are the best clues for locating specific functionality.

- **Program logic:** If a firmware file requires decryption during startup or upgrade, it almost certainly contains a program or script responsible for the "decrypt" operation.
  - **Example filenames:** `imgdecrypt` (image decryption), `firmware_decrypt_tool`, `updater_decrypt.sh`.
- **Library functions:** Even if there is no standalone program, the **decryption operation** will be invoked by some library function. Searching for files containing the `decrypt` keyword (e.g., shared libraries `.so` or static libraries `.a`) can directly point to the library that implements the decryption function.
- **Efficiency:** This is the most direct and targeted search method — it quickly filters out many irrelevant files.

------

## 4.2 Common keywords to search in firmware reverse engineering

Besides `decrypt`, you should search for the following categories of keywords to comprehensively locate security and core functions in firmware:

| Keyword category          | Keywords (English / common abbreviations)                    | Purpose                                                      | Example filename / function                 |
| ------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------- |
| **Encryption/Decryption** | `encrypt`, `crypto`, `aes`, `rsa`, `key`, `ssl`, `cert`, `tls`, `ssh` | Locate encryption, signing, certificate and key management components. | `libcrypto.so`, `ssl_config`, `keygen`      |
| **Upgrade/Configuration** | `update`, `upgrade`, `download`, `config`, `settings`, `flash`, `factory` | Locate firmware update mechanism, configuration storage, or factory reset logic. | `do_upgrade.sh`, `/etc/config`, `mtd_write` |

### 5. Search for files associated with `imgdecrypt`

```apl
grep -ir "imgdecrypt"  # Search for associated files, found prog.cgi
# So prog.cgi and imgdecrypt are related
# From the explanation below, prog.cgi calls imgdecrypt
```

![img](/Image/882-5.png)

### 5.1 Analyze the startup items

```apl
Look in etc_ro for the familiar rcS
# etc_ro: contains many startup scripts and network configuration scripts
cat rcS # Found that goahead& has been commented out, so the startup service may not be goahead
So now we need to find which service starts
We know etc_ro contains many startup scripts, network configuration scripts, etc., so listing etc_ro shows a folder named lighthttpd (suspicious)
Entering the folder we find a configuration file named lighthttpd.conf
Using cat to view this file shows that file requests matching certain patterns are forwarded to /bin/prog.cgi for handling.
```

![img](/Image/882-10.png)

### 5.2 Verify the assumption

```apl
ls ../bin/ | grep lighttpd   # Found the lighttpd service in the bin directory
```

## Role of `prog.cgi` in the firmware

In many embedded systems that use a web server, `prog.cgi` is a highly **centralized** program. It usually handles not just a single function but **multiple core management tasks**:

1. **Handle configuration changes:** Accepts user-submitted new Wi‑Fi passwords, port-forwarding rules, etc., and writes these settings to **NVRAM** (non-volatile storage) or other configuration files.
2. **Execute core operations:** Handles sensitive requests such as reboot, firmware upgrade, and factory reset.
3. **API interface:** Especially in modern devices, `prog.cgi` or similar CGI programs may be configured to handle specific API requests such as **HNAP (Home Network Administration Protocol)** or other SOAP/JSON-based management traffic.

------

## Importance of `prog.cgi` for reverse engineering

For firmware reverse engineering and security analysis, `prog.cgi` is a **high-value target** because it exposes the device’s core logic:

- **Central analysis point:** It’s the hub that handles almost all Web UI interactions. By reversing this single binary you can quickly understand the device’s management features and vulnerability surface.
- **Privilege execution:** CGI programs usually run as **root** or another high-privilege user — if they contain vulnerabilities (e.g., command injection, buffer overflow), an attacker may gain full device privileges.
- **Sensitive material:** `prog.cgi` may contain:
  - **Hardcoded commands** (e.g., direct `system()` or `exec()` calls to execute shell commands).
  - **Configuration file paths**.
  - **Authentication and authorization logic** (e.g., how login credentials are validated).

### 6. Now put `imgdecrypt` and `prog.cgi` into IDA for analysis

==imgdecrypt==

```apl
In IDA pseudo-C view, found decrypt_firmar, double-click to enter
Found suspicious code: printf("key:");
The precondition for printf("key:") is sub_402554((int)v5)
Tracing sub_402554 leads to sub_40108C
Inside sub_40108C saw AES_set_decrypt_key
At this point we can reasonably conclude that imgdecrypt is a decryption tool
```

------

```apl
After entering IDA, by renaming we found the suspected decryption function decrypt_firmare
Enter it to view the pseudo-C code
```

![img](/Image/882-11.png)

### Related code analysis

- Accepts command-line arguments: `argv[1]` is the firmware or file to process (decrypt/unpack/verify); optional `argv[2]` specifies the public key (default `"/etc_ro/public.pem"`).
- Reads/initializes the public key (`sub_40215C`).
- Based on the public key/RSA logic, generates or derives a 16-byte symmetric key (`sub_402554` fills `v5`).
- Prints the 16-byte key (in hexadecimal).
- Uses the key to decrypt/process `argv[1]` (`sub_401780`), outputting to `/tmp/.firmware.orig`.
- If successful, deletes the original file and renames the decrypted file to the original filename (overwrite).
- Frees the RSA object and returns the sub-operation result.

In other words: **This is a tool/function that “derives/decrypts a symmetric key using the public key, then uses that symmetric key to decrypt the firmware file and overwrite the original file.”**

![img](/Image/882-12.png)

==prog.cgi==

```apl
Search for the string imgdecrypt
Enter sub_46640C and view the pseudo-C code; it shows that before calling imgdecrypt it is processed in HTML_hnap_xml_header
The call flow is clearly visible in the figures below
Therefore, imgdecrypt is confirmed as the decryption program
```

![img](/Image/882-6.png)

![img](/Image/882-7.png)

![img](/Image/882-8.png)

### 8. Start decrypting version `v1.10`

```apl
readelf -h imgdecrypt  # little endian
cp /usr/bin/qemu-mipsel-static  ./  
sudo chroot . ./qemu-mipsel-static ./bin/imgdecrypt DIR882A1_FW110B02.bin
# Output: key:C05FBF1936C99429CE2A0781F08D6AD8
sudo binwalk -Me --run-as=iot DIR882A1_FW110B02.bin  # Unpack successful
```

