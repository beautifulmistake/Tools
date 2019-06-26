"""
对rsa进行加解密
"""
# import base64
# from Crypto.PublicKey import RSA
# import rsa
#
#
# def encryptPassword(password, publicKeyStr):
#     # 1、base64解码
#     publicKeyBytes = base64.b64decode(publicKeyStr.encode())
#     # 3、生成publicKey对象
#     key = RSA.import_key(publicKeyBytes)
#     # 4、对原密码加密
#     encryptPassword = rsa.encrypt(password.encode(), key)
#     return base64.b64encode(encryptPassword).decode()

import base64
import rsa


def str2key(s):
    """
    对 公钥字符串进行处理，获取加密的 一组参数
    :param s: 公钥字符串
    :return: 一组加密参数
    """
    # 对字符串解码
    b_str = base64.b64decode(s)
    if len(b_str) < 162:
        return False
    hex_str = ''
    # 按位转换成16进制
    for x in b_str:
        h = hex(x)[2:]
        h = h.rjust(2, '0')
        hex_str += h
    # 找到模数和指数的开头结束位置
    m_start = 29 * 2
    e_start = 159 * 2
    m_len = 128 * 2
    e_len = 3 * 2
    modulus = hex_str[m_start:m_start + m_len]
    exponent = hex_str[e_start:e_start + e_len]
    return modulus, exponent


def encryptPassword(message, key):
    """
    对传入的 字符串进行 加密
    :param message: 需要加密的信息
    :param key: 一组加密参数
    :return: 加密后的参数
    """
    # 默认的 处理长度 117
    default_length = 117
    # 将 加密参数 转换为 bytes 类型
    message = str(message).encode()
    # 获取 一组加密参数
    modulus = int(key[0], 16)
    exponent = int(key[1], 16)
    # 生成 公钥对象
    rsa_pubkey = rsa.PublicKey(modulus, exponent)
    # 不需要进行分段处理
    if len(message) < default_length:
        crypto = rsa.encrypt(message, rsa_pubkey)
        b64str = base64.b64encode(crypto)
        # data = binascii.b2a_hex(crypto)
        return '01' + b64str.decode('utf-8')
    # 需要分段处理
    offset = 0
    res = list()
    while len(message) - offset > 0:
        if len(message) - offset > default_length:
            res.append(rsa.encrypt(message[offset: offset + default_length], rsa_pubkey))
        else:
            res.append(rsa.encrypt(message[offset:], rsa_pubkey))
        offset += default_length
    data = b''.join(res)
    return '01' + base64.b64encode(data).decode('utf-8')


# 测试代码
if __name__ == "__main__":
    message = {"1": "Android 5.1",
               "2": "866808026851625",
               "3": "866808026851625",
               "5": "38:bc:1a:d4:8b:f6",
               "7": "71MBBL527MFZ",
               "10": "79e2cacee5709a30",
               "13": "armeabi-v7a",
               "14": "m1 note",
               "15": "12953772032",
               "16": "1080*1920",
               "17": "\"TData-DongHu\"",
               "18": "Meizu",
               "19": "wifi",
               "20": "Meizu-m1 note__weibosdk__0041005000__android__android5.1"
               }
    publickKeyStr = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDHHM0Fi2Z6+QYKXqFUX2Cy6AaWq3cPi+GSn9oeAwQbPZR75JB7Netm0Ht' \
                    'BVVbtPhzT7UO2p1JhFUKWqrqoYuAjkgMVPmA0sFrQohns5EE44Y86XQopD4ZO+dE5KjUZFE6vrPO3rWW3np2BqlgKpjnYZr' \
                    'i6TJApmIpGcQg9/G/3zQIDAQAB'
    # 获取key
    key = str2key(publickKeyStr)
    print(key)
    print(encryptPassword(message, key))
