# dev 或者 prod
import os

MONITOR_ENV = "dev"

# 家目录
home = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

API_FILE = os.path.join(home, "config/live_api.yaml")
REPORT_RECORD = os.path.join(home, "result/record.json")
TMP_DATA = os.path.join(home, "result/tmp_data.yaml")

# 上报slack
is_send_slack = False
# slack webhook
slack_webhook = "https://hooks.slack.com/services/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"

# 上报到QA-dms平台
is_send_platform = True
test_platform = "http://qatest-monitor.mxplay.com/energy/error_info/insert"

# 上报到钉钉
is_send_dingding = True
DINGDING = [
    (
        'https://oapi.dingtalk.com/robot/send?access_token=a9dcebdc33c2aadd15cf7e07d1dfaf122b0fe7fbd12d3b48850e1dd9062140a3',
        'SEC8ffa4eee1c4cb8fe5b3f52d4ccc722603e8ad9cd79b86aa5437182987fbc1e9f'
    ),
    (
        'https://oapi.dingtalk.com/robot/send?access_token=6c6a45639c6bd60c0086820ae5900e82ae9764a3e83c51cb1bb0001bdeee0700',
        'SECdb3ec5c8a1701c0adac9c2d73f18e226b6d11197b6fe1ed0ce4aacb5b0f69c67'
    ),
    (
        'https://oapi.dingtalk.com/robot/send?access_token=776dac7708f25eef245adcfd628f86834c5f3677258c68a967204e043b5e54a1',
        'SEC4fac0160022842784e2b687198b2d7c170c1fe44ecd0ccc755a449ee24db8e08'
    ),
    (
        'https://oapi.dingtalk.com/robot/send?access_token=a3b33233a588fffb40304c328fffb3e21eea9ec0dfef05da2f87a1693f06f231',
        'SECcf6f195d5dcb470b4cb9365722491bf36f66b7384ba4701c478a6b7315782f8e'
    ),
    (
        'https://oapi.dingtalk.com/robot/send?access_token=01ed5d121afbaf2d4cef6d4a3f68f9b1aa2827241d125264d6a0c2e98c8008f7',
        'SECcc2ff0ea928a3e744847eca8a707df437e8102605c73b85d082c47d3702a7a0c'
    )
]

PROD_URL = "https://liveapi.mxplay.com"
DEV_URL = "https://liveapi.dev.mxplay.com"

dev_public_key = os.path.join(home, "config/mxlive_rsa_public_3072.pem")
prod_public_key = os.path.join(home, "config/mxlive_prod_rsa_public_3072.pem")

HEADERS = {
    'accept-encoding': 'gzip,deflate,br',
    'user-agent': 'okhttp/3.12.11',
    # 'User-Agent': 'PostmanRuntime/7.29.2',
    'accept': 'application/json',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'x-platform': '1',
    # 'x-userid': 'f929bba8-1894-4b72-bc4e-07544b72ada565379',
    'x-os-version': '31',
    'x-timezone': 'Asia/Shanghai',
    'x-density': '3.0',
    'x-env-type': '0',
    # 'x-aid': 'a22b4e17-7ec6-4e11-8df9-df85294b69d9',
    'x-debug-nocheck': '1',  # 不校验x-guard-key
    'x-debug-nosign': '1',  # 请求body不需要加密，返回内容不需要解码
    'x-mcc': '404',     # 钱包只有印度开了
    'x-app-version': '11201',
}
# 生成签名前添加的headers
AUTH_HEADERS = {
    'x-time-server': '1',
    'x-timestamp': '',
    'x-guard-version': '2',
    'x-guard-key-version': '2'
}

Anchor_ID = {
    "dev": "1300dkI",
    "prod": "11013iCEb",
    "dev_friend": "130082r",
    "prod_friend": "11017zblc",
    # "gift_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ7XCJhbW91bnRcIjozODAuMCxcIm5hbWVcIjpcIlwiLFwiZW1haWxcIjpcIlwiLFwiY29udGFjdFwiOm51bGwsXCJwdXJwb3NlXCI6bnVsbCxcInBsYXRmb3JtXCI6XCJsaXZlX2FuZHJvaWRcIixcIm14dXNlcklkXCI6XCIxMzAwZGtJXCIsXCJjdXJyZW5jeVwiOlwiSU5SXCIsXCJyZXF1ZXN0SWRcIjpcIjAxX2RldjAwMTRsdVwiLFwiZnJlcXVlbmN5XCI6bnVsbCxcImZpcnN0UmVxdWVzdElkXCI6bnVsbCxcInBheW1lbnRSZXF1ZXN0SWRcIjpudWxsLFwicGF5bWVudERlc2NyaXB0aW9uXCI6bnVsbCxcInNlcnZpY2VJZFwiOlwibGl2ZW1vbmV5XCIsXCJjb3VudHJ5XCI6bnVsbCxcIm1lcmNoYW50TmFtZVwiOlwiTVggUGxheWVyXCIsXCJtYXhBbGxvd2VkUmV0cmllc1wiOjEsXCJyZWN1cnJpbmdTdXBwb3J0XCI6XCJESVNBQkxFRFwifSIsImV4cCI6MTY2MzA3ODI2Mn0.ERJPm_ylrqbYrv5RMTW34yraqOEvoc-lWH0i4PkPSBL0dl2yL5Co_X4J0IfeVa3gXHt7Fz5L3FDFHO1aqz3bjA",
}


