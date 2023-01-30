import hashlib

from Crypto.Cipher import AES
from base64 import b64decode, b64encode

import random

BLOCK_SIZE = AES.block_size
# 不足BLOCK_SIZE的补位(s可能是含中文，而中文字符utf-8编码占3个位置,gbk是2，所以需要以len(s.encode())，而不是len(s)计算补码)
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE).encode()
# 去除补位
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


class AESCipher:
    def __init__(self, secretkey: bytes):
        self.key = secretkey[:16]  # 密钥
        self.iv = secretkey[16:]  # 偏移量

    def encrypt(self, text):
        """
        加密 ：先补位，再AES加密，后base64编码
        :param text: 需加密的明文
        :return:
        """
        # 包pycrypto的写法，加密函数可以接受str也可以接受bytes
        text = pad(text)
        # 包pycryptodome 的加密函数不接受str
        # text = pad(text).encode()
        cipher = AES.new(key=self.key, mode=AES.MODE_CBC, IV=self.iv, segment_size=128)
        encrypted_text = cipher.encrypt(text)
        # 进行64位的编码,返回得到加密后的bytes，decode成字符串
        # return b64encode(encrypted_text).decode('utf-8')
        return encrypted_text

    def decrypt(self, encrypted_text):
        """
        解密 ：偏移量为key[0:16]；先base64解，再AES解密，后取消补位
        :param encrypted_text : 已经加密的密文
        :return:
        """
        # encrypted_text = b64decode(encrypted_text)
        cipher = AES.new(key=self.key, mode=AES.MODE_CBC, IV=self.iv)
        decrypted_text = cipher.decrypt(encrypted_text)
        # return unpad(decrypted_text).decode('utf-8')
        return unpad(decrypted_text).decode('utf-8')

#
# def get_key(n):
#     """
#     获取密钥 n 密钥长度
#     :return:
#     """
#     c_length = int(n)
#     source = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
#     length = len(source) - 1
#     result = ''
#     for i in range(c_length):
#         result += source[random.randint(0, length)]
#     return result

# def get_key(self):
#     instance = bytes(self.str_key, encoding="utf-8")
#     sha256 = hashlib.sha256()
#     sha256.update(instance)
#     key = sha256.digest()[:32]
#     return key

# text = "hello"
# secretkey = get_key(32)
# encrypted_text = AESCipher(secretkey).encrypt(text)
# print(encrypted_text)
#
# decrypted_text = AESCipher(secretkey).decrypt(encrypted_text)
# print(decrypted_text)
#


