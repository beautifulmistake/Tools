import time
from functools import wraps

"""
使用装饰器测试我们自己编写的程序所运行的时间
以便我们查找自己代码的瓶颈所在
"""


def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        # 获取函数开始运行的时间
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print("Total time running %s:%s seconds" % (function.func_name, str(t1 - t0)))
        return result
    return function_timer


