# import base64
# import hashlib
# import hmac
# import json
# import random
# import time
# import urllib
#
# import requests
#
# from config.config import *
# from utils.date import DateTime
# from utils.logger import run_log
#
#
# def send_slack(content=''):
#     """
#     Report to slack
#     :param content:
#     :return:
#     """
#     url = slack_webhook
#     if not is_send_slack:
#         print(f"未开启开关，上报slack：{content}")
#         return None
#     payload = {
#         'text': content,
#     }
#     headers = {'Content-Type': 'application/json'}
#     run_log.info(f"send_slack: {payload}")
#     re = requests.post(url=url, headers=headers, json=payload)
#     run_log.info(f"slack 上报返回：{re.text}")
#
#
# def send_platform(env, interfaceName, requestInfo, responseInfo, errorType, errorInfo, status):
#     """
#     Report to the qa-dms platform
#     :param env:
#     :param interfaceName:
#     :param requestInfo:
#     :param responseInfo:
#     :param errorType:
#     :param errorInfo:
#     :param status:
#     :return:
#     """
#     if not is_send_platform:
#         print(f"未开启开关，上报平台：{interfaceName}， {errorInfo}")
#         return None
#     if isinstance(responseInfo, dict):
#         responseInfo = json.dumps(responseInfo)
#     url = test_platform
#     headers = {'Content-Type': 'application/json;charset=utf-8'}
#     start_time = DateTime
#     interface_name = str(interfaceName)
#     req = str(requestInfo)
#     res = str(responseInfo)
#     error_info = str(errorInfo)
#     data = {
#         "serverName": "live",
#         "interfaceType": "api",
#         "env": env,
#         "startTime": start_time,
#         "interfaceName": interface_name,
#         "requestInfo": req,
#         "responsInfo": res,
#         "errorType": errorType,
#         "errorInfo": error_info,
#         "status": status
#     }
#     run_log.info(f"send_platform: {data}")
#     re = requests.post(url, json=data, headers=headers)
#     run_log.info(f"platform 上报：{re.text}")
#
#
# def send_dingding(title, content=''):
#     if not is_send_dingding:
#         print(f"send dingding: {title}, {content}")
#         return
#     content = "## {} \n > {}".format(title, content)
#     webhook = random.choice(DINGDING)
#     timestamp = (round(time.time() * 1000))
#     secret = webhook[1]
#     secret_enc = bytes(secret.encode('utf-8'))
#     string_to_sign = '{}\n{}'.format(timestamp, secret)
#     string_to_sign_enc = bytes(string_to_sign.encode('utf-8'))
#     hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
#     sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
#     boot_url = "{}&timestamp={}&sign={}".format(webhook[0], timestamp, sign)
#
#     data = {
#         "msgtype": "markdown",
#         "markdown": {
#             "title": title,
#             "text": str(content)
#         },
#         "at": {
#             "atMobiles": [''],
#             "isAtAll": False
#         }
#     }
#
#     headers = {'Content-Type': 'application/json'}
#     res = requests.post(url=boot_url, data=json.dumps(data), headers=headers)
#     run_log.debug(f"send dingding data: {json.dumps(data)}")
#     run_log.info(f"send dingding: {res.text}")