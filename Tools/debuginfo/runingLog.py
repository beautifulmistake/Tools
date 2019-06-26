"""
这是将运行程序时将运行日志显示在控制台的模块
"""
import logging

import coloredlogs


def debug_info():
    """
    在控制显示程序运行时的日志信息
    :return:
    """
    p = logging.getLogger()
    console_formatter = logging.StreamHandler()
    console_formatter.setFormatter(
        coloredlogs.ColoredFormatter('%(asctime)s - %(module)-14s[line:%(lineno)3d] - %(levelname)-8s: %(message)s')
    )
    p.addHandler(console_formatter)
    p.setLevel(logging.DEBUG)
