# Java 字节(Byte) 取值范围 [-128,127]
# Python3 字节(bytes) 取值范围： [0,256)

# Java数组转 Python bytes
iv = [21, 1, 21, 5, 4, 15, 7, 9, 23, 3, 1, 6, 8, 12, 13, 191]
# iv_byte = bytes(i % 256 for i in iv)
iv_byte = bytes(i % 128 for i in iv)

# Python bytes转数组
# import numpy as np
#
# byte_array = np.frombuffer(iv_byte, dtype=np.uint8)
# print(byte_array)
# print(type(byte_array))


def pb2jb(byte_arr):
    """
    python字节码转java字节码
    :param byte_arr:
    :return:
    """
    return [int(i) - 256 if int(i) > 127 else int(i) for i in byte_arr]


def jb2pb(byte_arr):
    """
    java 字节码转python字节码
    :return:
    """
    return [i + 256 if i < 0 else i for i in byte_arr]


def jb2jb(byte_arr):
    """
    [-255,256) 映射 到 [-128 ~ 127]
    @param byte_arr:
    @return: byte_arr
    """
    new_list = []
    for i in byte_arr:
        if i < -128:
            new_list.append(i + 256)
        elif i > 127:
            new_list.append(i - 256)
        else:
            new_list.append(i)
    return new_list


def hex2jb(hex_str):
    """
    十六进制数据转java字节码
    eg:
        hex_str = "5f 3c f2 81 c8 0f 88 89 c7 b1 99 77 58 c5 4c 04"
    :return:
    """
    return [int(i, 16) - 256 if int(i, 16) > 127 else int(i, 16) for i in hex_str.split(" ")]


def hex2pb(hex_str):
    """
    十六进制数据转python字节码
    eg:
        hex_str = "5f 3c f2 81 c8 0f 88 89 c7 b1 99 77 58 c5 4c 04"
    :return:
    """
    return [int(i, 16) for i in hex_str.split(" ")]


def pb2str(byte_arr, encoding="utf-8"):
    """
    python字节码转str
    :return:
    """
    return bytes(byte_arr).decode(encoding)


def jb2str(byte_arr, encoding="utf-8"):
    """
    java字节码转str
    :return:
    """
    return bytes(jb2pb(byte_arr)).decode(encoding)


def hex2str(hex_str, encoding="utf-8"):
    """
    hex转str
    :param hex_str: "2c 22 70 61 79 63 68 65 63 6b 6d 6f 64 65 22 3a"
    :param encoding:
    :return:
    """
    return bytes(hex2pb(hex_str)).decode(encoding)