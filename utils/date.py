import time
from datetime import datetime


DateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
TimeText = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
TODAY = datetime.now().strftime("%Y-%m-%d")

def datetime_to_timestamp(dateTim):
    """
    datetime转换为时间戳
    :param dateTim:
    :return:
    """
    return time.mktime(dateTim.timetuple())


def string_to_datetime(string):
    """
    字符串转换为datetime
    :param string:
    :return:
    """
    return datetime.strptime(string, "%Y-%m-%d-%H")


def string_to_timestamp(strTime):
    """
    字符串转换为时间戳
    :param strTime:
    :return:
    """
    return time.mktime(string_to_datetime(strTime).timetuple())


def timestamp_to_string(stamp):
    """
    时间戳转换为字符串
    :param stamp:
    :return:
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stamp))

def date_to_timestamp(date):
    """
    将2021-11-19格式转化为时间戳
    :return:
    """
    # 转为时间数组
    time_array = time.strptime(date, "%Y-%m-%d")
    # 转为时间戳
    time_stamp = int(time.mktime(time_array))
    return time_stamp
