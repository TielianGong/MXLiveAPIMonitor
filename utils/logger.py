# 定义 log 的基础内容
import logging
import logging.handlers
import os

from utils.date import TODAY


class Log:
    def __init__(self, file_name):
        """
        定制log
        :return:
        """
        # 创建logger
        self.logger = logging.getLogger("file_name")    # file_name为多个logger的区分唯一性

        # 设置格式
        log_format_str = '[%(asctime)s]  %(levelname)s  %(message)s'
        # 将 log 格式加载到 Formatter 中
        format = logging.Formatter(log_format_str)

        # 创建handler，用于写入日志文件和屏幕输出
        log_path = os.path.dirname(__file__).split("MXLiveAPIMonitor")[0] + r'MXLiveAPIMonitor/log/'
        logfile = log_path + file_name + '.log'

        mode = 'a'
        # 加入文件句柄，log 以文件格式输出，设置为追加
        h = logging.handlers.RotatingFileHandler(logfile, mode=mode, encoding="utf-8")
        h.setFormatter(format)

        # 加入输出流句柄，把 log 输出到 terminal 上
        s = logging.StreamHandler()
        s.setFormatter(format)

        # 把2个句柄追加 log 中
        self.logger.handlers = []
        self.logger.addHandler(h)
        # self.logger.addHandler(s)
        # 设置 log 等级
        self.logger.setLevel(logging.DEBUG)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)


run_log = Log(TODAY + "_run")


