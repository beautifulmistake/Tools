"""
使用 RSA 公钥对 字符串数据进行加密
"""
import base64
import rsa


# 公钥处理方法
def str2key(pubKey):
    """
    对公钥进行处理
    :param pubKey: 公钥字符串
    :return: 一组加密参数
    """
    s = pubKey.encode()
    miss = 4 - len(s) % 4
    if miss:
        s += b'=' * miss
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


# str RSA 加密
def encryptInfo(message, key):
    """
    对 字符串进行 RSA 加密
    :param message: 需要加密的信息
    :param key: 一组加密参数
    :return: p
    """
    # 默认的 处理长度 117
    default_length = 117
    # 特别注意此处应先将Python dict 转换成 JSON 字符串 然后最终转换成 bytes 类型
    message = message.encode()
    # 获取 一组加密参数
    modulus = int(key[0], 16)
    exponent = int(key[1], 16)
    # 生成 公钥对象
    rsa_pubkey = rsa.PublicKey(modulus, exponent)
    print("查看第二次生成的公钥对象：", rsa_pubkey)
    # 不需要进行分段处理
    if len(message) < default_length:
        crypto = rsa.encrypt(message, rsa_pubkey)
        b64str = base64.b64encode(crypto)
        # data = binascii.b2a_hex(crypto)
        return b64str.decode('utf-8')
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
    return base64.b64encode(data).decode('utf-8')
