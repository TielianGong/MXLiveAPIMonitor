from common.log_handler import delete_log_file
# from common.upload import send_slack, send_dingding
from config.config import MONITOR_ENV, API_FILE
from monitor import api_monitor
from utils.logger import run_log

if __name__ == '__main__':
    try:
        api_monitor(env=MONITOR_ENV, api_file=API_FILE)
        delete_log_file(3)
    except Exception as e:
        run_log.info(f"MXLive API monitor run error: {e}")
        # send_slack(f"MXLive API monitor run failed. error message: {e}")
        # send_dingding("MXLive API monitor run failed.", f"MXLive API monitor run failed. error message: {e}")
