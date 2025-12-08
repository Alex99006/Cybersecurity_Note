# Dlink-M30解密/English version at the bottom

最近在 dlink 官网看到了新品路由器，出于好奇，就点进去看了下固件，找到了 M30 的固件，在官网随便下载了一1.10 版本的固件打算看看有没有什么漏洞，当准备开始提取文件系统的时候，发现该固件已经被加密了。当时想的就是问题不太大，按照之前的解密方式来解密一下就好了。但是并没有成功。这时候打算去看下最低版本是否可能找到一些有用的信息。但是只是得到了最低版本也是加密的。是采用了AES-128 Encryption。

![](/Image/M30_img/m30-5.png)

这时候打算再去收集一些信息看看有没有什么别的办法可以借鉴一下，通过搜索得知如果有硬件的情况下，还是可以通过 UART 链接后可以拿到未加密的固件的，但是我们并没有实体设备而实体设备的价格过高。

![](/Image/M30_img/m30-6.png)

至此已经没什么办法了，只能正面“开干”了

> 现在唯一知道的两点已知信息是来自 binwalk和dlink官网对应型号的发行版本信息可以知道
>
> 1. 加密方式是 AES-128-Encryption
>
> 2. 偏移 0x41 存在 OpenSSL Salted 格式的密文块
>
>    （Salted__ + salt + ciphertext）
>
> (可以看到一个非常漂亮且笔直并绝望的"直线")

![](/Image/M30_img/m30-1.png)

![](/Image/M30_img/m30-2.png)

## 一、分析 binwalk 后的结果中已知的信息

1. 由binwalk 的结果可以推测到0x41 是加密区的开始地址，但是这里疑点，因为加密数据是在 0x41 开始机密的

   所以这里推测在加密数据前很可能存在一段头部结构(目前还不知道是什么)

2. 接下来就是需要去验证加密区的格式，需要确认一下 salted__结构是否真实存在

   ![](/Image/M30_img/m30-3.png)

3. 通过上图我们也可以了解到了固件采用 OpenSSL salted__加密的

4. 此时我们需要去了解一下OpenSSL Salted__ 格式，经查阅资料发现

   OpenSSL Salted__ 格式的文件由三个连续的部分组成：

   | **序号** | **组成部分**                  | **大小（字节）** | **作用**                                       |
   | -------- | ----------------------------- | ---------------- | ---------------------------------------------- |
   | **1**    | **Magic Header (魔术头)**     | 8 bytes          | 识别文件格式。                                 |
   | **2**    | **Salt (盐)**                 | 8 bytes          | 随机生成的数据，用于防止彩虹表攻击和密钥派生。 |
   | **3**    | **Encrypted Data (加密数据)** | 可变             | 使用派生密钥和 IV 加密后的原始文件内容。       |

5. 通过查阅了资料我们 知道了固件加密并不是自行实现的，而是基于 **OpenSSL EVP_BytesToKey** 系列逻辑

   这意味着 key 与 IV 不是直接存储，而是根据 password + salt 派生出来。

## 二、了解**AES-CBC**

1. AES-CBC 解密必须要 key + IV，上面也提到了，OpenSSL EVP_BytesToKey是根据 password + salt 派生出来
2. 16 字节 key
3. 16 字节 IV
4. ciphertext

~~~apl
Salted__ 只提供：
	salt
	ciphertext
#  注意：Salted__ 并不包含 key，也不包含厂商自定义的 IV
#  众所周知既然固件能够被升级程序解密，那么 key 和 IV 必然存在于某处。如果不在加密区中，它们只能放在加密区之前，这里就可以大胆的去推测这个就是上面我们提到的0x41之前未知的区域。
~~~



## 三、**推断 MH01 固件头结构**(验证猜想)

~~~apl
xxd -g 1 -l 64 M30A1_FW110B02.bin
~~~



![](/Image/M30_img/m30-4.png)

1. 我们可以看到提取到信息为MH01，还有一个可疑的数据(0x20-0x3F)
2. 首先“MH01” 不属于任何常见文件系统或压缩格式，又放在文件开头（offset 0），它的意义不可能是随机数因此合理推断这是厂商的自定义封装格式。
3. 这时我们可以假设0x00..(某位置) 是 MH01 固件头，0x41 是加密段起始位置

## 四、**推断 0x20-0x3F 处是 IV**

1. 在上面验证猜想的时候我们也看到可疑的数据

   ![](/Image/M30_img/m30-7.png)

2. 观察 0x20 之后的 32 字节发现这些字节全部是 ASCII（“0–9”“a–f”），正好是 32 个 hex 字符也就是16 字节，已经符合 AES-128-CBC IV 的所有特征。这时我们需要去在验证一下，因为如果 0x20 不是 IV，那么整个解密会失败，我们必须先验证它确实是 IV。

   ~~~apl
   dd if=M30A1_FW110B02.bin bs=1 skip=$((0x20)) count=32 > iv.hex
   xxd -r -p iv.hex > iv.bin
   ls -l iv.bin
   ~~~

   ![](/Image/M30_img/m30-8.png)

3. Ok，结果为16 字节，假设成立。

## 五、**推断 0x18 是加密数据长度 encrypted_size**

~~~apl
hexdump -s 0x18 -n 4 -e '1/4 "%u\n"' M30A1_FW110B02.bin
~~~

![](/Image/M30_img/m30-9.png)

1. 观察 0x18~0x1B，得到一个合理的长度，为什么推断它是加密大小呢？

   位置恰好位于头部中（非随机数据区）

   长度与文件整体大小逻辑匹配

   必须要有一个字段告诉升级程序加密区有多长

2. 于是可以确认，0x18 是加密数据长度字段

## 六、**提取加密区**

~~~apl
ENCSIZE=$(hexdump -s 0x18 -n 4 -e '1/4 "%u\n"' M30A1_FW110B02.bin)
echo "ENCSIZE=$ENCSIZE"
ENCSIZE=38871424
dd if=M30A1_FW110B02.bin of=raw_enc.bin bs=1 skip=$((0x41)) count=$ENCSIZE 
~~~

![](/Image/M30_img/m30-10.png)

1. 这里说一下为什么不去使用 binwalk 去提

   binwalk 有时会误判结束位置

   固件可能包含多个区域（binwalk无法处理厂商定制结构）

   加密大小是最权威的数据来源

## 七、提取 salt和提取纯 ciphertext

~~~apl
dd if=raw_enc.bin bs=1 skip=8 count=8 > salt.bin
dd if=raw_enc.bin bs=1 skip=16 > cipher.bin
~~~

![](/Image/M30_img/m30-11.png)

1. 这里说一下为什么要手动去提取 salt 和 ciphertext 呢

   Salted__ 区块是 OpenSSL EVP 的标准格式

   盐必须参与 key 派生

   ciphertext 才是真正要解密的数据

   如果不跳过前 16 字节，openssl enc 会报错

2. 到了这里，我们现在的已知条件开始变的多了起来

   盐

   密文

   IV

   加密模式

## 八、**为什么认为厂商使用 EVP_BytesToKey（SHA256 版）？**

1. ok，到这里我们就说一下为什么是要认定厂商是使用EVP_BytesToKey

   Salted__ 是 EVP_BytesToKey 的专属产物

   固件本身使用 OpenSSL 加密（从格式可知）

   多数 IoT 厂商沿用 EVP（方便实现）

   若使用 AES-128-CBC，最常见实现是：

   - password
   - salt
   - key = SHA256 (sha256 的一个变种)

   通过上面的判断和研读了《深入浅出密码学》中相关 AES-CBC 的文章后，因此推断使用 EVP_BytesToKey (SHA256 的一个变种) 是合理的。它的核心算法只有两轮

2. 接下来的任务就是需要找到这个非常关键的 **KEY**，当然，我们通过一些特殊的方法来获取到了这个 **KEY**

## 九、为什么要说EVP_BytesToKey(SHA256 变种) 核心算法只有两轮

1. 首先我们在上面0x41 看到了Salted__ ，这是 **OpenSSL enc** 独有的格式。只要看到这 8 字节，我们就可以立即锁定加密一定是用 OpenSSL 的 EVP 框架做的，密钥派生一定来自 EVP_BytesToKey，派生算法只存在几种（MD5 / SHA1 / SHA256 变种），也就是说，这一步就把“可能的加密实现”范围缩窄到不超过三种。

2. 排除 MD5，OpenSSL 经典的派生方式是

   ~~~~apl
   D1 = MD5(password + salt)
   D2 = MD5(D1 + password + salt)
   D3 = MD5(D2 + password + salt)
   ...
   ~~~~

3. 但是我们试过 MD5 版本后，发现解密失败了

4. 因为上面说到了，我们通过网上搜索获取相关资料，获取到了这个**KEY**了，它是 32 字节的。通过这个密钥我们可以去反推一下。

   AES-128-CBC 需要：16 字节 key、16 字节 IV。总计 32 字节。而 SHA256 输出的 block 是 32 字节，那么只用一次 SHA256（一次 D1）的话只能覆盖16 字节 key，而 16 字节的 IV 还是覆盖不到。所以至少需要两个 SHA256 输出（D1 + D2）

   ~~~apl
   D1 = SHA256(password + salt)
   D2 = SHA256(D1 + password + salt)
   ~~~

   

## 十、**验证 猜想**

![](/Image/M30_img/m30-12.png)

![](/Image/M30_img/m30-13.png)

~~~apl
#  将 P1 的值拷贝到通用变量 PASSWORD，作为后续派生流程的输入密码。
PASSWORD="$P1"
#  把 ASCII 密码和 salt（二进制形式）按顺序拼接后计算 SHA-256 二进制摘要，并把结果写入 D1.bin（生成派生链的第一块）。
{ printf "%s" "$PASSWORD"; xxd -r -p salt.hex; } | openssl dgst -sha256 -binary > D1.bin
#  将 D1（上一步产生的摘要）与密码和 salt 连接后再做一次 SHA-256，结果写入 D2.bin（生成派生链的第二块）
{ cat D1.bin; printf "%s" "$PASSWORD"; xxd -r -p salt.hex; } | openssl dgst -sha256 -binary > D2.bin
#  把 D1 与 D2 按顺序拼接成密钥材料 KM.bin（key material 的原始字节流）。
cat D1.bin D2.bin > KM.bin
#  从 KM.bin 读取前 32 字节并保存为 key32.bin，这是派生出的前 32 字节密钥材料（供截取 AES key 用）。
dd if=KM.bin of=key32.bin bs=1 count=32 status=none
#  从 KM.bin 跳过前 32 字节读取接下来的 16 字节并保存为 iv_derived.bin（这是 EVP 派生出的 IV 部分，供备用）。
dd if=KM.bin of=iv_derived.bin bs=1 skip=32 count=16 status=none
~~~



![](/Image/M30_img/m30-14.png)

![](/Image/M30_img/m30-15.png)

![](/Image/M30_img/m30-16.png)

# 十一、全流程命令梳理

1、检查头部

```
xxd -g 1 -l 4 M30A1_FW110B02.bin
# 期望看到 4d 48 30 31 （ASCII: M H 0 1）
```

2、取加密数据长度（小端，偏移 0x18）

```
hexdump -s 0x18 -n 4 -e '1/4 "%u\n"' M30A1_FW110B02.bin
# 记下输出为 ENCSIZE（字节数）
ENCSIZE=$(hexdump -s 0x18 -n 4 -e '1/4 "%u\n"' M30A1_FW110B02.bin)
echo "ENCSIZE=$ENCSIZE"
```

3、提取 IV（偏移 0x20，ASCII 十六进制 32 字节 → 16 字节）

```
dd if=M30A1_FW110B02.bin bs=1 skip=$((0x20)) count=32 status=none | tr -d '\n' > iv.hex
cat iv.hex
# 保存一份原始 IV 二进制
xxd -r -p iv.hex > iv.bin
```

4、 提取密文区（从偏移 0x41 开始，长度 ENCSIZE）

```
dd if=M30A1_FW110B02.bin of=raw_enc.bin bs=1 skip=$((0x41)) count=$ENCSIZE status=none
```

5、验证 OpenSSL 头 “Salted__” + 8 字节盐

```
head -c 16 raw_enc.bin | hexdump -C
# 前 8 字节应为 "Salted__"
# 接着的 8 字节是 salt
dd if=raw_enc.bin bs=1 skip=8 count=8 status=none | xxd -p -c 256 > salt.hex
cat salt.hex
```

6、手工派生 key（EVP_BytesToKey, SHA256）

- D1 = SHA256( password_ascii + salt )
- D2 = SHA256( D1 + password_ascii + salt )
- 连接 D1||D2，取前 48 字节：前 32 字节为 key_material（用于 AES-128 取其前 16 字节），后 16 字节本应是派生 IV，但**实际不用**（我们用固件头里的 IV）。

```
P1="b4517d9b98e04d9f075f5e78c743e097"
```

7、设定密码（先试 P1）

```
PASSWORD="$P1"
```

8、计算 D1

```
# D1 = SHA256( password_ascii + salt )
{ printf "%s" "$PASSWORD"; xxd -r -p salt.hex; } | openssl dgst -sha256 -binary > D1.bin
xxd -p D1.bin
```

9、计算 D2

```
# D2 = SHA256( D1 + password_ascii + salt )
{ cat D1.bin; printf "%s" "$PASSWORD"; xxd -r -p salt.hex; } | openssl dgst -sha256 -binary > D2.bin
xxd -p D2.bin
```

10、拼接并截取 key_material（32B）和（派生）IV（16B）

```
cat D1.bin D2.bin > KM.bin
# 取前 32 字节作为 key_material
dd if=KM.bin of=key32.bin bs=1 count=32 status=none
# 取后 16 字节本是派生 IV（不用）
dd if=KM.bin of=iv_derived.bin bs=1 skip=32 count=16 status=none

# AES-128-CBC 使用 key32 的前 16 字节
dd if=key32.bin of=key16.bin bs=1 count=16 status=none
KEY16HEX=$(xxd -p -c 256 key16.bin)
IVHEX=$(cat iv.hex)
echo "KEY16HEX=$KEY16HEX"
echo "IVHEX=$IVHEX"
```

11、去掉 OpenSSL 头，解密 AES-128-CBC（使用“固件 IV”）

12、去除 “Salted__”+salt 头，得到纯密文

```
dd if=raw_enc.bin of=cipher.bin bs=1 skip=16 status=none
```

13、使用手工 key 和固件 IV 解密

> `openssl enc -d` 会自动去 PKCS#7 填充。
>  如果报 `bad decrypt` 再用 `-nopad` 看看明文是否基本合理（通常不需要）。

```
openssl enc -d -aes-128-cbc \
    -K "$KEY16HEX" \
    -iv "$IVHEX" \
    -in cipher.bin \
    -out decrypted.bin
```



------

# Dlink-M30 Decryption

Recently, I noticed a new router on D-Link’s official website. Out of curiosity, I downloaded the firmware for the M30 model, version 1.10, to see if there were any vulnerabilities. When I tried to extract the file system, I realized that the firmware was encrypted. Initially, I thought it wouldn’t be a big problem and tried to decrypt it using previous methods, but it didn’t work. I then checked the lowest firmware version for possible clues, but it was also encrypted using AES-128 Encryption.

![img](/Image/M30_img/m30-5.png)


I also tried to gather more information to see if there were alternative methods. From research, I learned that with the physical hardware, it’s possible to obtain the unencrypted firmware via a UART connection. However, we did not have the physical device, and its price was too high.

![img](/Image/M30_img/m30-6.png)


At this point, there was no other choice but to proceed directly with reverse engineering.

> The only known information so far comes from `binwalk` and the official D-Link release version information:
>
> 1. Encryption method: AES-128 Encryption
>
> 2. At offset 0x41, there is an OpenSSL Salted format ciphertext block:
>
>    (`Salted__ + salt + ciphertext`)
>
>    (We can observe a very straight and seemingly hopeless “line”.)

![img](/Image/M30_img/m30-1.png)


![img](/Image/M30_img/m30-2.png)


## 1. Analysis of Known Information from Binwalk

1. From the binwalk output, offset 0x41 seems to mark the start of the encrypted region. There is suspicion that before this offset, there may be a header structure that we do not yet know.
2. Next, we need to verify the format of the encrypted region and confirm the existence of the `Salted__` structure.

![img](/Image/M30_img/m30-3.png)


1. From the image above, it’s clear that the firmware uses OpenSSL’s `Salted__` encryption.
2. The OpenSSL Salted format consists of three consecutive components:

| **No.** | **Component**                 | **Size (bytes)** | **Purpose**                                                  |
| ------- | ----------------------------- | ---------------- | ------------------------------------------------------------ |
| 1       | **Magic Header** (`Salted__`) | 8                | Identifies the file format                                   |
| 2       | **Salt**                      | 8                | Randomly generated, used to prevent rainbow table attacks and for key derivation |
| 3       | **Encrypted Data**            | Variable         | Original file content encrypted using the derived key and IV |

1. The firmware encryption is based on **OpenSSL EVP_BytesToKey** logic, meaning that the key and IV are derived from a password + salt, not stored directly.

## 2. Understanding AES-CBC

1. AES-CBC decryption requires a key and IV. As mentioned above, OpenSSL EVP_BytesToKey derives them from password + salt.
2. Key: 16 bytes
3. IV: 16 bytes
4. Ciphertext

```
Salted__ provides only:
    salt
    ciphertext
# Note: Salted__ does not contain the key or any vendor-specific IV
# Since the firmware can be decrypted by the update program, the key and IV must exist somewhere.
# If they are not in the encrypted region, they are likely in the unknown region before 0x41.
```

## 3. Inferring the MH01 Firmware Header (Hypothesis)

```
xxd -g 1 -l 64 M30A1_FW110B02.bin
```

![img](/Image/M30_img/m30-4.png)


1. The first bytes show `MH01`, and there is suspicious data at offsets 0x20–0x3F.
2. `MH01` does not correspond to any known filesystem or compression format, and being at offset 0 suggests it is a custom vendor-specific header.
3. We can assume that 0x00…(some offset) is the MH01 firmware header, and 0x41 marks the start of the encrypted section.

## 4. Inferring IV at Offset 0x20–0x3F

1. From the previous analysis, the suspicious data is at offset 0x20.

![img](/Image/M30_img/m30-7.png)


1. Observing the 32 bytes after 0x20, they are ASCII characters (`0–9` and `a–f`), which corresponds to 32 hex characters or 16 bytes, fitting the AES-128-CBC IV requirement. We need to verify this.

```
dd if=M30A1_FW110B02.bin bs=1 skip=$((0x20)) count=32 > iv.hex
xxd -r -p iv.hex > iv.bin
ls -l iv.bin
```

![img](/Image/M30_img/m30-8.png)


1. Result: 16 bytes, assumption confirmed.

## 5. Inferring Encrypted Data Length at Offset 0x18

```
hexdump -s 0x18 -n 4 -e '1/4 "%u\n"' M30A1_FW110B02.bin
```

![img](/Image/M30_img/m30-9.png)


1. The 4 bytes at 0x18–0x1B match a reasonable size.
2. This offset is part of the header, not random, and corresponds logically with the firmware file size.
3. Therefore, offset 0x18 represents the encrypted data size.

## 6. Extracting the Encrypted Region

```
ENCSIZE=$(hexdump -s 0x18 -n 4 -e '1/4 "%u\n"' M30A1_FW110B02.bin)
echo "ENCSIZE=$ENCSIZE"
ENCSIZE=38871424
dd if=M30A1_FW110B02.bin of=raw_enc.bin bs=1 skip=$((0x41)) count=$ENCSIZE 
```

![img](/Image/M30_img/m30-10.png)


> Note: Binwalk may misidentify the encrypted region, especially with custom vendor structures. Using the extracted encrypted size is more reliable.

## 7. Extracting Salt and Pure Ciphertext

```
dd if=raw_enc.bin bs=1 skip=8 count=8 > salt.bin
dd if=raw_enc.bin bs=1 skip=16 > cipher.bin
```

![img](/Image/M30_img/m30-11.png)


1. Manual extraction is necessary:
   - Salt is used for key derivation
   - Ciphertext is the actual encrypted data

## 8. Why EVP_BytesToKey (SHA256 variant) is assumed

1. The `Salted__` format is specific to EVP_BytesToKey.
2. Firmware uses OpenSSL encryption. Most IoT vendors stick to EVP.
3. AES-128-CBC requires 16-byte key + 16-byte IV = 32 bytes. SHA256 outputs 32 bytes, so two SHA256 iterations (D1 + D2) are required.

```
D1 = SHA256(password + salt)
D2 = SHA256(D1 + password + salt)
```

## 9. Verification of the Hypothesis

![img](/Image/M30_img/m30-12.png)


![img](/Image/M30_img/m30-13.png)


```
PASSWORD="$P1"
{ printf "%s" "$PASSWORD"; xxd -r -p salt.hex; } | openssl dgst -sha256 -binary > D1.bin
{ cat D1.bin; printf "%s" "$PASSWORD"; xxd -r -p salt.hex; } | openssl dgst -sha256 -binary > D2.bin
cat D1.bin D2.bin > KM.bin
dd if=KM.bin of=key32.bin bs=1 count=32 status=none
dd if=KM.bin of=iv_derived.bin bs=1 skip=32 count=16 status=none
```

![img](/Image/M30_img/m30-14.png)


![img](/Image/M30_img/m30-15.png)


![img](/Image/M30_img/m30-16.png)


## 10. Full Command Workflow

1. Check header

```
xxd -g 1 -l 4 M30A1_FW110B02.bin
# Expect: 4d 48 30 31 (ASCII: M H 0 1)
```

1. Extract encrypted data length (offset 0x18)

```
ENCSIZE=$(hexdump -s 0x18 -n 4 -e '1/4 "%u\n"' M30A1_FW110B02.bin)
echo "ENCSIZE=$ENCSIZE"
```

1. Extract IV (offset 0x20, ASCII hex 32 bytes → 16 bytes)

```
dd if=M30A1_FW110B02.bin bs=1 skip=$((0x20)) count=32 status=none | tr -d '\n' > iv.hex
xxd -r -p iv.hex > iv.bin
```

1. Extract ciphertext (offset 0x41, length ENCSIZE)

```
dd if=M30A1_FW110B02.bin of=raw_enc.bin bs=1 skip=$((0x41)) count=$ENCSIZE status=none
```

1. Verify OpenSSL header `Salted__` + salt

```
head -c 16 raw_enc.bin | hexdump -C
dd if=raw_enc.bin bs=1 skip=8 count=8 status=none | xxd -p -c 256 > salt.hex
```

1. Manually derive key (EVP_BytesToKey, SHA256)
2. Assign password (try P1)

```
P1="b4517d9b98e04d9f075f5e78c743e097"
PASSWORD="$P1"
```

1. Calculate D1 and D2

```
{ printf "%s" "$PASSWORD"; xxd -r -p salt.hex; } | openssl dgst -sha256 -binary > D1.bin
{ cat D1.bin; printf "%s" "$PASSWORD"; xxd -r -p salt.hex; } | openssl dgst -sha256 -binary > D2.bin
```

1. Concatenate and extract key (32B) and IV (16B)

```
cat D1.bin D2.bin > KM.bin
dd if=KM.bin of=key32.bin bs=1 count=32 status=none
dd if=KM.bin of=iv_derived.bin bs=1 skip=32 count=16 status=none
dd if=key32.bin of=key16.bin bs=1 count=16 status=none
KEY16HEX=$(xxd -p -c 256 key16.bin)
IVHEX=$(cat iv.hex)
```

1. Remove OpenSSL header, extract pure ciphertext

```
dd if=raw_enc.bin of=cipher.bin bs=1 skip=16 status=none
```

1. Decrypt using AES-128-CBC (firmware IV)

```
openssl enc -d -aes-128-cbc \
    -K "$KEY16HEX" \
    -iv "$IVHEX" \
    -in cipher.bin \
    -out decrypted.bin
```
