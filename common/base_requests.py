import gzip
import json
import time

import requests

from config.config import HEADERS, DEV_URL, PROD_URL
from utils.aes_encrypt import AESCipher
from utils.logger import run_log


def url_maker(env, req_path):
    """
    Generate main url based on the test environment
    :param env:
    :param req_path:
    :return:
    """
    if env == "dev":
        base_url = DEV_URL
    elif env == "prod":
        base_url = PROD_URL
    else:
        base_url = DEV_URL
    url = base_url + req_path
    run_log.debug(f"生成请求url: {url}")
    return url


def headers_maker(additional_headers: dict):
    """
    请求头生成
    :param additional_headers:
    :return:
    """
    base_headers = HEADERS
    timestamp = int(round((time.time()) * 1000))
    additional_headers.update({"x-timestamp": str(timestamp)})
    # 增加x-session
    additional_headers.update(base_headers)
    run_log.debug(f"生成headers：{additional_headers}")
    # print(f"headers maker: {base_headers}")
    return additional_headers


def body_encrypt(body_data, secret_key):
    """
    post 请求 body加密
    :param body_data:
    :param secret_key:
    :return:
    """
    # 请求body先gzip，在AES加密，然后发起请求
    body = str(body_data)
    gzip_data = gzip.compress(body.encode())
    encrypted_text = AESCipher(secret_key).encrypt(gzip_data)
    return encrypted_text


def request_model(url, method, headers, data, args=''):
    """
    Send a request, 部分post接口的url带了参数，这里传进来完整的url
    :param args:
    :param data:
    :param method:
    :param headers:
    :param url:
    :return:
    """
    if method.lower() == "post":
        payload = json.dumps(data)
        res = requests.post(url=url, headers=headers, data=payload)
        # body = res.request.body
        status_code = res.status_code
        req = {
            "url": res.request.url,
            "headers": res.request.headers,
            "body": res.request.body,
            # "body": body.decode('utf-8', errors='ignore')
        }
        res_data = res.text
        if res.status_code == 200 and res_data != '':
            res_data = res.json()
        return req, res_data, status_code

    if method.lower() == "get":
        res = requests.get(url=url, params=args, headers=headers)
        status_code = res.status_code
        req = {
            "url": res.request.url,
            "headers": res.request.headers
        }
        res_data = res.text
        if res.status_code == 200 and res_data != '':
            res_data = res.json()
        return req, res_data, status_code

