import base64
import hashlib
import os
import random

from common.base_requests import url_maker
from config.config import HEADERS
from utils.logger import run_log
from utils.rsa_encrypt import rsa_encrypt
from utils.transform_bytes import *


def get_guard(env, url, api_data, headers):
    """
    获取到签名数据
    :param url:
    :param env:
    :param api_data: {'caseName': 'Login', 'method': 'post', 'reqPath': '/v1/login', 'reqPara': None, 'reqDict': {'type': 'phone', 'token': '+8617778186053_1234'}}
    :param headers:
    :return: x-guard-key, x-guard-value
    """
    method = api_data.get("method").upper()
    args = api_data.get("reqPara")
    t = 0
    args_str = ""
    if args is not None:
        for arg in args:
            if not isinstance(arg, str):
                arg = str(arg)
            args_str = args_str + arg + "=" + str(args[arg])
            t += 1
            if t < len(args):
                args_str += "&"
    url = url + "?" + args_str
    # 拼接method, url
    sign = method.encode() + method.encode() + url.encode()

    # 筛选出所有以x-开头的headers
    keys_list = []
    for header in headers:
        if header.startswith('x-') or header.startswith('X-'):
            keys_list.append(header)
    run_log.debug(f"before sort headers: {keys_list}")
    # 把筛选出的headers key 进行排序
    keys_list.sort()
    run_log.debug(f"after sort headers: {keys_list}")
    # 把筛选后的headers 的值写进去
    headers_bytes_str = b''
    for i in range(len(keys_list)):
        for header in headers:
            if header == keys_list[i]:
                headers_bytes_str += headers[header].encode()
    # print(headers_bytes_str)
    # 拼接排序后的headers的value
    sign += headers_bytes_str

    # 当有body时，body编码
    body = api_data.get("reqDict")
    if body is not None:
        sign += str(body).encode()

    # 生成随机32位bytes
    python_key = random.randbytes(32)
    secret_key = python_key
    # print(python_key)
    # java中bytes 取值范围 [-128,127]，转换一下，确保没有大于127的数
    secret_key = bytes(i % 127 for i in python_key)
    # run_log.debug(f"secret_key: {secret_key}")

    sign += secret_key
    sign += secret_key
    # print(sign)
    sign += b'111111'
    # print("签名字符串：", sign)

    # 对签名字符串进行md5计算，生成x-guard-value
    m2 = hashlib.md5()  # 导入md5算法
    m2.update(sign)     # 把值传给md5算法
    # 区分加密是hash.digest() 还是hash.hexdigest()，之前一直用的是hexdigest方法导致加密的结果不正确
    x_guard_value = base64.b64encode(m2.digest())
    # x_guard_value = m2.digest()  # 生成一个二进制字符串

    # 使用公钥对32位aes key 加密转成base64，生成x_guard_value
    x_guard_key = rsa_encrypt(message=secret_key, env=env)
    # print("x_guard_key: ", x_guard_key)
    # print("x_guard_value: ", x_guard_value)
    return secret_key, x_guard_key, x_guard_value




# case = {'caseName': 'sms', 'method': 'post', 'reqPath': '/v1/sms', 'reqPara': {'usage': 1}, 'reqDict': {'type': 'message', 'phone': '+8617778186053', 'lang': 'en | hi', 'hash_str': 'xxx'}}
# headers = HEADERS
# get_guard('dev', case, headers)
