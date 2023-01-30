import os

from utils.date import TODAY, date_to_timestamp
from utils.logger import run_log


def write_error_log(error_log_file, error_line):
    """
    Write the error log
    :param error_log_file:
    :param error_line:
    :return:
    """
    with open(error_log_file, 'a') as f:
        f.write(error_line + "\n")


def log_request(req, res, status_code):
    """
    Joining together the log string
    :param req:
    :param res:
    :param status_code:
    :return:
    """
    url = req.get("url")
    headers = req.get("headers")
    body = req.get("body")

    request_str = f"url: {url}, headers: {headers}, body: {body}, response: {res}, status_code: {status_code}"
    # 写入日志
    run_log.info(request_str)


def error_log(error_log_file, time: str, req: dict, res: dict, status_code: int, error_info: str):
    """
    Joining together the error log string
    :param time:
    :param req:
    :param res:
    :param status_code:
    :return:
    """
    url = req.get("url")
    headers = req.get("headers")
    body = req.get("body")
    interface_name = eval(body).get("interfaceName") if (eval(body).get("interfaceName") is not None) else "null"

    request_str = f"time: {time}, url: {url}, interface_name: {interface_name}, headers: {headers}, body: {body}, " \
                  f"response: {res}, status_code: {status_code}, error_info: {error_info}"
    write_error_log(error_log_file, request_str)


def delete_log_file(days):
    """
    Delete the log file that timed out
    :param days:
    :return:
    """
    # 获取到所有.log结尾的文件名
    # 遍历文件名
    # 1. 提取出文件名日期
    # 2. 计算当前日期与文件名日期的间隔日期
    # 3. 如果间隔日期大于 days ,则删除
    file_path = os.path.dirname(__file__).split("MXLiveAPIMonitor")[0] + f"MXLiveAPIMonitor/log/"
    for root, dirs, files in os.walk(file_path):
        for file in files:
            if os.path.splitext(file)[1] == '.log':
                log_date = os.path.splitext(file)[0].split("_")[0]
                days_between = (date_to_timestamp(TODAY) - date_to_timestamp(log_date)) // 60 // 60 // 24
                if days_between > days:
                    delete_file = os.path.join(root, file)
                    run_log.info(f"删除log：{delete_file}")
                    os.remove(delete_file)
                else:
                    run_log.debug(f"{file} 还不到{days}天，不删除")

