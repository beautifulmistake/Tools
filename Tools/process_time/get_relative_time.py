import datetime
import time
from dateutil.relativedelta import relativedelta


def get_relative_time():
    """
    参考链接：
    https://www.cnblogs.com/zhangqunshi/p/6641167.html

    此方法用于获取当前时间的前一个月的时间
    :return: 当前时间的前一个月的时间戳
    """
    # 获取当前时间
    now = datetime.date.today()
    # 获取当前时间之前一个月的时间截止日 ---> 转换成时间戳形式
    previous = now - relativedelta(months=+1)
    return int(time.mktime(previous.timetuple()))
