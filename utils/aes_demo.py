# # 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
# import random
# from binascii import b2a_base64, a2b_base64
#
# from Crypto.Cipher import AES
#
#
# def encrypt(key, iv, text):
#     cryptor = AES.new(key, AES.MODE_CBC, iv)
#     # 处理明文
#     content_padding = pkcs7padding(text)
#     # # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
#     # length = 16
#     # count = len(text)
#     # if count % length != 0:
#     #     add = length - (count % length)
#     # else:
#     #     add = 0
#     # text = text + ('\0' * add)
#     ciphertext = cryptor.encrypt(content_padding)
#     # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
#     # 所以这里统一把加密后的字符串转化为16进制字符串b2a_hex(ciphertext) ,当然也可以转换为base64加密的内容，可以使用b2a_base64(ciphertext)
#     return ciphertext
#
#
# # 解密后，去掉补足的空格用strip() 去掉
# def decrypt(key, iv, text):
#     cryptor = AES.new(key, AES.MODE_CBC, iv)
#     # 解密
#     plain_text = cryptor.decrypt(a2b_base64(text))
#     # 重新编码
#     result = str(plain_text, encoding='utf-8')
#     # 去除填充内容
#     result = pkcs7unpadding(result)
#     return result
#
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
#
# def pkcs5padding(data):
#     return pkcs7padding(data, 8)
#
# def pkcs7padding(data, block_size=16):
#     if type(data) != bytearray and type(data) != bytes:
#         raise TypeError("仅支持 bytearray/bytes 类型!")
#     pl = block_size - (len(data) % block_size)
#     return data + bytearray([pl for i in range(pl)])
#
#
# # def pkcs7padding(text):
# #     """
# #     明文使用PKCS7填充
# #     最终调用AES加密方法时，传入的是一个byte数组，要求是16的整数倍，因此需要对明文进行处理
# #     :param text: 待加密内容(明文)
# #     :return:
# #     """
# #     bs = AES.block_size  # 16
# #     length = len(text)
# #     bytes_length = len(bytes(text, encoding='utf-8'))
# #     # tips：utf-8编码时，英文占1个byte，而中文占3个byte
# #     padding_size = length if(bytes_length == length) else bytes_length
# #     padding = bs - padding_size % bs
# #     # tips：chr(padding)看与其它语言的约定，有的会使用'\0'
# #     padding_text = chr(padding) * padding
# #     return text + padding_text
#
#
# def pkcs7unpadding(text):
#     """
#     处理使用PKCS7填充过的数据
#     :param text: 解密后的字符串
#     :return:
#     """
#     length = len(text)
#     unpadding = ord(text[length-1])
#     return text[0:length-unpadding]

#
# text = "hello"
# secretkey = get_key(32)
# secretkey = get_key(32)
# print("*"*20)
#
# key = secretkey[:16]
# iv = secretkey[16:]
#
# print(secretkey)
# print(key)
# print(iv)
#
# en_str = encrypt(key, iv, text)
# print(en_str)
# de_str = decrypt(key, iv, en_str)
# print(de_str)
