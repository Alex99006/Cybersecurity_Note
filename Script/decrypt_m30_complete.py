#!/usr/bin/env python3
"""
D-Link M30 固件 AES-128-CBC 解密脚本

基于 delink 项目的 Rust 源代码实现
支持 M30 系列路由器固件解密

使用方法:
    python3 decrypt_m30_complete.py <input_file> [output_file]

示例:
    python3 decrypt_m30_complete.py firmware.bin firmware_decrypted.bin
"""

import struct
import hashlib
import sys
import os
from pathlib import Path

try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import unpad
except ImportError:
    print("错误: 需要安装 pycryptodome")
    print("安装命令: pip3 install pycryptodome")
    sys.exit(1)


# D-Link 设备的已知密钥列表
KNOWN_KEYS = {
    "b4517d9b98e04d9f075f5e78c743e097": "M30 v1.02 - v1.10",
    "05c79b73cf88619d7b9725505cfd718f": "M30 > v1.10",
}


def evp_bytes_to_key(password, salt, hash_type='sha256', key_len=32, iv_len=16):
    """
    OpenSSL EVP_BytesToKey 算法实现
    
    关键：与 Rust delink 实现一致
    - sha256_digest 返回的是 SHA256 哈希的十六进制字符串的字节表示
    - 即：hex::decode(sha256::digest(data))
    
    参数:
        password (str): 密码字符串
        salt (bytes): 8字节盐值
        hash_type (str): 哈希算法 ('md5' 或 'sha256')
        key_len (int): 密钥长度（字节，默认32）
        iv_len (int): IV长度（字节，默认16）
    
    返回:
        tuple: (key, iv)
    """
    total_len = key_len + iv_len
    key_material = b''
    password_bytes = password.encode('ascii')
    
    # 第一次哈希：password + salt
    pass_salt = password_bytes + salt
    
    if hash_type == 'sha256':
        # Rust 实现：hex::decode(sha256::digest(data))
        # sha256::digest 返回十六进制字符串，hex::decode 转换回字节
        hash_hex = hashlib.sha256(pass_salt).hexdigest()
        hash_result = bytes.fromhex(hash_hex)
    elif hash_type == 'md5':
        # 同样的处理
        hash_hex = hashlib.md5(pass_salt).hexdigest()
        hash_result = bytes.fromhex(hash_hex)
    else:
        raise ValueError(f"不支持的哈希算法: {hash_type}")
    
    key_material = hash_result
    
    # 循环直到 key_material 足够长
    while len(key_material) < total_len:
        # 下一次哈希：上一次的哈希结果 + password + salt
        hash_input = hash_result + pass_salt
        
        if hash_type == 'sha256':
            hash_hex = hashlib.sha256(hash_input).hexdigest()
            hash_result = bytes.fromhex(hash_hex)
        elif hash_type == 'md5':
            hash_hex = hashlib.md5(hash_input).hexdigest()
            hash_result = bytes.fromhex(hash_hex)
        
        key_material += hash_result
    
    return key_material[:key_len], key_material[key_len:total_len]


def decrypt_firmware(encrypted_data, password, iv=None):
    """
    使用 AES-128-CBC 解密固件（OpenSSL 格式）
    
    参数:
        encrypted_data (bytes): 加密的数据（包含 "Salted__" 魔数）
        password (str): 密码（十六进制字符串）
        iv (bytes): 初始化向量（可选，如果为None则派生）
    
    返回:
        bytes: 解密后的数据，如果失败返回None
    """
    try:
        # 检查 OpenSSL 魔数
        if encrypted_data[:8] != b'Salted__':
            print("错误: 加密数据不包含 'Salted__' 魔数", file=sys.stderr)
            return None
        
        # 提取盐值
        salt = encrypted_data[8:16]
        
        # 派生密钥和IV（使用32字节密钥长度，与Rust实现一致）
        key, derived_iv = evp_bytes_to_key(password, salt, 'sha256', 32, 16)
        
        # 使用前16字节的密钥进行AES-128-CBC解密
        key_16 = key[:16]
        
        # 重要：使用文件中提供的IV，而不是派生的IV
        # Rust实现中的mh01.rs调用aes_128_cbc_decrypt时传入Some(&iv)
        # 这意味着使用文件中的IV而不是派生的IV
        if iv is None:
            # 如果没有提供IV，使用派生的IV
            use_iv = derived_iv
        else:
            # 使用文件中的IV（用于MH01格式）
            use_iv = iv
        
        # 实际的加密数据从第16字节开始（跳过 "Salted__" 和盐值）
        cipher_data = encrypted_data[16:]
        
        # 创建解密器（使用16字节密钥进行AES-128-CBC）
        cipher = AES.new(key_16, AES.MODE_CBC, use_iv)
        
        # 解密
        decrypted = cipher.decrypt(cipher_data)
        
        # 移除 PKCS7 填充（Rust代码中使用 WithPadding）
        try:
            decrypted = unpad(decrypted, AES.block_size)
        except ValueError:
            # 如果 PKCS7 unpad 失败，直接返回解密后的数据
            # 这可能意味着数据没有正确的 PKCS7 填充
            pass
        
        return decrypted
    
    except Exception as e:
        print(f"解密失败: {e}", file=sys.stderr)
        return None


def decrypt_openssl_format(openssl_data, password):
    """
    使用 OpenSSL EVP_BytesToKey 解密 OpenSSL 格式的数据
    
    参数:
        openssl_data (bytes): OpenSSL 格式的加密数据（包含 "Salted__" 魔数）
        password (str): 密码（十六进制字符串）
    
    返回:
        bytes: 解密后的数据，如果失败返回None
    """
    try:
        # 检查 OpenSSL 魔数
        if openssl_data[:8] != b'Salted__':
            return None
        
        # 提取盐值
        salt = openssl_data[8:16]
        
        # 派生密钥和IV
        key, iv = evp_bytes_to_key(password, salt, 'sha256', 32, 16)
        
        # 使用前16字节的密钥进行AES-128-CBC解密
        key_16 = key[:16]
        
        # 实际的加密数据从第16字节开始
        encrypted_data = openssl_data[16:]
        
        # 创建解密器
        cipher = AES.new(key_16, AES.MODE_CBC, iv)
        
        # 解密
        decrypted = cipher.decrypt(encrypted_data)
        
        return decrypted
    
    except Exception as e:
        print(f"OpenSSL 解密失败: {e}", file=sys.stderr)
        return None


def parse_firmware_header(data):
    """
    解析固件文件头
    
    参数:
        data (bytes): 固件文件数据
    
    返回:
        dict: 包含头部信息的字典，如果解析失败返回None
    """
    if len(data) < 0x41:
        print("错误: 文件太小", file=sys.stderr)
        return None
    
    # 检查魔数
    magic = data[0:4]
    if magic != b'MH01':
        print(f"错误: 魔数不匹配。期望 'MH01'，实际 '{magic}'", file=sys.stderr)
        return None
    
    # 提取加密数据大小
    encrypted_size = struct.unpack('<I', data[0x18:0x1C])[0]
    
    # 提取IV（ASCII十六进制）
    try:
        iv_hex_ascii = data[0x20:0x40]
        iv = bytes.fromhex(iv_hex_ascii.decode('ascii'))
    except (ValueError, UnicodeDecodeError) as e:
        print(f"错误: 无法解析IV: {e}", file=sys.stderr)
        return None
    
    # 提取加密数据
    encrypted_data = data[0x41:0x41 + encrypted_size]
    
    return {
        'magic': magic,
        'encrypted_size': encrypted_size,
        'iv': iv,
        'encrypted_data': encrypted_data,
    }


def decrypt_m30_firmware(input_file, output_file=None):
    """
    解密 D-Link M30 固件
    
    参数:
        input_file (str): 输入固件文件路径
        output_file (str): 输出文件路径（可选）
    
    返回:
        bool: 成功返回True，失败返回False
    """
    # 读取输入文件
    try:
        with open(input_file, 'rb') as f:
            firmware_data = f.read()
    except IOError as e:
        print(f"错误: 无法读取文件 '{input_file}': {e}", file=sys.stderr)
        return False
    
    print(f"[*] 读取文件: {input_file}")
    print(f"[*] 文件大小: {len(firmware_data)} 字节")
    
    # 解析固件头
    header = parse_firmware_header(firmware_data)
    if header is None:
        return False
    
    print(f"[*] 魔数: {header['magic']}")
    print(f"[*] 加密数据大小: {header['encrypted_size']} 字节")
    print(f"[*] IV: {header['iv'].hex()}")
    
    # 尝试所有已知密钥
    print(f"\n[*] 尝试 {len(KNOWN_KEYS)} 个已知密钥...")
    
    for password, device_name in sorted(KNOWN_KEYS.items(), key=lambda x: x[1]):
        print(f"[*] 尝试: {device_name} ({password})")
        
        # 解密
        decrypted = decrypt_firmware(
            header['encrypted_data'],
            password,
            header['iv']
        )
        
        if decrypted is None:
            continue
        
        # 验证解密结果
        if decrypted[0:4] == b'MH01':
            print(f"\n[+] 解密成功！")
            print(f"[+] 设备: {device_name}")
            print(f"[+] 密钥: {password}")
            print(f"[+] 解密后大小: {len(decrypted)} 字节")
            
            # 保存输出文件
            if output_file is None:
                # 自动生成输出文件名
                input_path = Path(input_file)
                output_file = input_path.parent / f"{input_path.stem}_decrypted.bin"
            
            try:
                with open(output_file, 'wb') as f:
                    f.write(decrypted)
                print(f"[+] 已保存到: {output_file}")
                return True
            except IOError as e:
                print(f"错误: 无法写入文件 '{output_file}': {e}", file=sys.stderr)
                return False
    
    print(f"\n[-] 解密失败: 所有密钥都不匹配", file=sys.stderr)
    return False


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python3 decrypt_m30_complete.py <input_file> [output_file]")
        print()
        print("示例:")
        print("  python3 decrypt_m30_complete.py firmware.bin")
        print("  python3 decrypt_m30_complete.py firmware.bin firmware_decrypted.bin")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        print(f"错误: 文件不存在 '{input_file}'", file=sys.stderr)
        sys.exit(1)
    
    # 解密固件
    success = decrypt_m30_firmware(input_file, output_file)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
