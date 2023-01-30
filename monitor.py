import json
import yaml

from common.base_requests import url_maker, headers_maker, body_encrypt, request_model
# from common.upload import send_slack, send_platform, send_dingding
from config.config import *
from utils.date import TODAY
from utils.verity_kit import *


def api_monitor(env: str, api_file: str):
    anchor_id = Anchor_ID.get(env)
    friend_id = Anchor_ID.get(env+"_friend")
    gift_token = Anchor_ID.get("gift_token")
    with open(TMP_DATA, 'a+', encoding='utf-8') as f:
        # 将字典写入到yaml文件中
        yaml.dump({"anchor_id": anchor_id, "friend_id": friend_id, "gift_token": gift_token}, f)
        f.close()

    data = get_yaml_data(api_file)
    temp_data = {}

    result_data = []
    success_list = []
    failed_list = []
    skipped_list = []
    for api_category in data:
        api_list = data[api_category]
        for interface in api_list:
            interface_name = interface["caseName"]
            result_data.append(interface_name)
            params = interface.get("reqPara")
            body_data = interface.get("reqDict")
            check_type = interface.get("checkType")
            judge_value = interface.get("verityFiled")
            skip_flag = interface.get("isSkip")

            if skip_flag == 1:
                run_log.info(f"这条测试用例跳过：{interface_name}")
                skipped_list.append(interface_name)
                continue
            # 读取临时数据
            raw_tmp = get_yaml_data(TMP_DATA)
            run_log.debug(f"before raw_tmp: {raw_tmp}")

            url = url_maker(env, interface["reqPath"])
            headers_dict = {
                # 11013iCEb session
                "x-session": "ERlaJ3/7Bv0gXH61a6tGfS0JiACwwo17ARrg6Wn5acv4u214YAcfOdMdgzX/y62XhMUxRB1+MU0pRIDkG0l1AA==.32",
                "x-imid": anchor_id,
            }
            headers = HEADERS
            headers.update(headers_dict)

            if params is not None:
                for key, value in params.items():
                    if isinstance(value, str) and value.startswith("$"):
                        params[key] = raw_tmp.get(value[1:])
                # print(params)

            if body_data is not None:
                for key, value in body_data.items():
                    if isinstance(value, str) and value.startswith("$"):
                        body_data[key] = raw_tmp.get(value[1:])
                # print(body_data)

            # 发送请求，增加失败重试2次，跟客户端保持一致
            status_code = res_data = ""
            req = {}
            for i in range(3):
                run_log.info(f"第 {i} 次请求 {interface_name}:")
                req, res_data, status_code = request_model(url=url, method=interface["method"], headers=headers,
                                                           data=body_data, args=params)
                if status_code == 200:
                    break
            run_log.info(f"status_code: {status_code}")
            run_log.info(f"request: {req}")
            run_log.info(f"response: {res_data}")

            error_code, error_msg = verity_handler(status_code=status_code, res_data=res_data, check_type=check_type, judge_value=judge_value)
            run_log.info(f"error code: {error_code}, error msg: {error_msg}")
            error = {
                "error_code": error_code,
                "error_info": error_msg
            }
            if error_code is not None:
                upload_request_error(env=env, req=req, res=res_data, interface_name=interface_name,
                                     error=error)
                failed_list.append(interface_name)
            else:
                # 去检查文档中该id是否存在，
                # 如果存在，且是今天的数据，则发送一条恢复正常的数据到platform
                record_path = REPORT_RECORD
                record_file = open(record_path, "r")
                # 记录的全部数据
                all_data = json.load(record_file)
                record_file.close()

                for key in all_data:
                    tmp_key = key[:len(key) - 5]
                    if interface_name == tmp_key and all_data[key]["day"] == TODAY and all_data[key]["times"] > 0:
                        run_log.info(f"{interface_name} 已经恢复正常")
                        # send_platform(env, interface_name, req, res_data, 0, "请求已恢复正常。", 1)
                        # 将错误次数重置为0
                        all_data[key]["times"] = 0
                # 更新新数据
                writefile = open(record_path, "w+")
                json.dump(all_data, writefile)
                writefile.close()

                # 如果是创建直播间，请求正常时，需获取到groupId, streamId
                if interface_name == "LiveCreate":
                    group_id = res_data.get("groupId")
                    stream_id = res_data.get("streamId")
                    temp_data.update({"group_id": group_id})
                    run_log.debug(f"get group id and stream id: {group_id}, {stream_id}")
                if interface_name == "LiveTab":
                    tab_id = res_data.get("tabs")[0].get("id")
                    temp_data.update({"tab_id": tab_id})
                    run_log.debug(f"get tab id: {tab_id}")
                if len(temp_data) != 0:
                    with open(TMP_DATA, 'a+', encoding='utf-8') as f:
                        # 将字典写入到yaml文件中
                        yaml.dump(temp_data, f)
                success_list.append(interface_name)

    raw_tmp = get_yaml_data(TMP_DATA)
    run_log.debug(f"final raw_tmp: {raw_tmp}")
    # 清空文件内容
    with open(TMP_DATA, 'w', encoding='utf-8') as f:
        f.truncate(0)

    run_log.info(f"执行成功测试用例共{len(success_list)}条：{success_list}.")
    run_log.info(f"执行失败测试用例共{len(failed_list)}条：{failed_list}.")
    run_log.info(f"跳过测试用例共{len(skipped_list)}条：{skipped_list}.")
    # print(failed_list)
    # print(result_data)


# def login_auth(env, login_apis):
#     """
#     获取登录后的 x-session
#     :param env:
#     :param login_apis:
#     :return:
#     """
#     for api in login_apis:
#         url, headers, payload = request_model(env, api)
#         time, req, res_data, status_code = request_model(url=url, headers=headers, data=payload)

#
# def request_model(env, interface_data):
#     """
#     生成发送请求的url，headers, payload
#     :param env:
#     :param interface_data:
#     :return: url, headers, payload
#     """
#     url = url_maker(env, interface_data["reqPath"])
#     headers = headers_maker(AUTH_HEADERS)
#     payload = interface_data["reqDict"]
#
#     return url, headers, payload


def get_yaml_data(api_file):
    with open(api_file, "r", encoding="utf-8") as f:
        api_data = yaml.safe_load(f)
        f.close()
    return api_data


def upload_request_error(env, req, res, interface_name, error):
    """
    Reporting errors to slack or qa-dms platform
    :param env:
    :param req:
    :param res:
    :param interface_name:
    :param error:
    :return:
    """
    upload_data = f"\n监控服务:  Live" \
                  f"\n接口名称:  {interface_name}" \
                  f"\n请求url:  {req.get('url')}" \
                  f"\n请求headers:  {req.get('headers')}" \
                  f"\n请求body:  {req.get('body')}" \
                  f"\n返回内容:  {res}" \
                  f"\n报警原因:  {error.get('error_info')}"
    interface_id = interface_name + "_" + str(error.get("error_code"))
    # "interfaceName":"fetch_tabs_home_version_4_0",  //接口名称
    # "errorType":"0",  //报警的原因  0：内容为空   1：服务连接错误/api状态码非200   2：某些数据校验失败
    if error.get("error_code") == 5002:
        error_type = 0
    elif error.get("error_code") == 5001:
        error_type = 1
    else:
        error_type = 2

    # 获取到record数据，方便后续更新数据
    record_path = REPORT_RECORD
    record_file = open(record_path, "r")
    # 记录的全部数据
    all_data = json.load(record_file)
    record_file.close()

    if interface_id not in all_data:
        # 如果数据不存在，则新建数据，并上报
        # 默认上传结束时间标志为0->未上传，上传后修改为1->已上传
        record_line = {interface_id: {
            "day": TODAY,
            "error_info": error.get('error_info'),
            "times": 1,
        }}
        all_data.update(record_line)
        run_log.info(f"在这里新建并上报: {interface_id}")
        # send_slack(upload_data)
        # send_dingding(f"MXLive {interface_name} 接口报警", upload_data)
        # send_platform(env, interface_name, req, res, error_type, error.get('error_info'), 0)
    else:
        # 如果存在该interface_id，则判断是否上报
        # 拿到这条record的数据d
        record_line = all_data[interface_id]

        if record_line["day"] != TODAY:
            # 如果不是今天的数据，并且error_info一样，则更新该条记录时间和次数
            # 上报一次
            all_data[interface_id]["day"] = TODAY
            all_data[interface_id]["times"] = 1
            run_log.info(f"不是今天的数据, 更新一下时间和次数，上报：{interface_id}")
            # send_slack(upload_data)
            # send_dingding(f"MXLive {interface_name} 接口报警", upload_data)
            # "interfaceName":"fetch_tabs_home_version_4_0",  //接口名称
            # "errorType":"0",  //报警的原因  0：内容为空   1：服务连接错误/api状态码非200   2：某些数据校验失败
            # "status":"0"    //0开始，1结束
            # send_platform(env, interface_name, req, res, error_type, error.get('error_info'), 0)
        elif record_line["times"] >= 10 and record_line["day"] == TODAY:
            # 如果是今天的数据，且error_info相同，则判断times是否大于10
            # 如果上报次数 大于等于 10，则不上报，次数加一
            all_data[interface_id]["times"] += 1
            run_log.info(f"次数大于10了，不报了: {interface_id}")
        else:
            # 如果上报次数小于10，就上报一次，更新times
            run_log.info(f"正常上报一次：{interface_id}")
            # send_slack(upload_data)
            # send_dingding(f"MXLive {interface_name} 接口报警", upload_data)
            # send_platform(env, interface_name, req, res, error_type, error.get('error_info'), 0)
            all_data[interface_id]["times"] += 1

    # 更新新数据
    writefile = open(record_path, "w+")
    json.dump(all_data, writefile)
    writefile.close()

