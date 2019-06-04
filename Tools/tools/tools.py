"""
此脚本的初衷是想减少开发爬虫在提取目标页面的目标字段时调试 xpath 语句是否完整匹配我们需要的数据所浪费的时间
该方法的使用还是脱离不了 xpath 语句,只能简化我开发,我们只需关注目标数据所在的父节点就可以
该方法的编写参考了 GitHub 上的源码:
https://github.com/Chyroc/WechatSogou/blob/master/wechatsogou/tools.py
"""
from __future__ import absolute_import, unicode_literals, print_function

import ast

import requests


def list_or_empty(content, contype=None):
    """

    :param content:
    :param contype:
    :return:
    """
    assert isinstance(content, list), 'content is not list:{}'.format(content)

    if content:
        return contype(content[0]) if contype else content[0]
    else:
        if contype:
            if contype == int:
                return 0
            elif contype == str:
                return ''
            elif contype == list:
                return []
            else:
                raise Exception('only can deal int str list')
        else:
            return ''


def get_elem_text(elem):
    """
    抽取 lxml.etree 库中 elem 对象中的文字
    这个方法适用于提取某一个标签的文本值(不论这个标签有几个子标签)
    :param elem: lxml.etree 库中的 elem 对象
    :return: elem 中的文字
    """
    if elem != '':
        return ''.join([node.strip() for node in elem.itertext()])
    else:
        return ''


def get_first_of_element(element, sub, contype=None):
    """
    抽取 lxml.etree 库中 element 对象中的文字
    此方法主要用于获得标签集合中使用,对其中的每一个元素做相应的数据提取
    :param element: lxml.etree 库中的 element 对象
    :param sub: str: xpath 语句
    :param contype:
    :return: element 对象中的文字
    """
    content = element.xpath(sub)
    return list_or_empty(content, contype)


def get_encoding_from_response(res):
    """
    获取 requests 库 get 或 post 请求返回的 Response 对象的编码
    :param res: requests 库 get 或 post 请求返回的 Response 对象
    :return: Response 对象的编码
    """
    encoding = requests.utils.get_encodings_from_content(res.text)
    return encoding[0] if encoding else requests.utils.get_encoding_from_headers(res.headers)


def _replace_str_html(s):
    """
    替换 html 中 ‘&quot;’等转义内容为正常内容
    :param s: 文字内容
    :return: 处理反转义后的文字
    """
    html_str_list = [
        ('&#39;', '\''),
        ('&quot;', '"'),
        ('&amp;', '&'),
        ('&yen;', '¥'),
        ('amp;', ''),
        ('&lt;', '<'),
        ('&gt;', '>'),
        ('&nbsp;', ' '),
        ('\\', '')
    ]
    for i in html_str_list:
        s = s.replace(i[0], i[1])
    return s


def replace_html(data):
    """
    对不同的数据类型的数据采用不同的方式处理
    :param data:
    :return:
    """
    if isinstance(data, dict):
        return dict([(replace_html(k), replace_html(v)) for k, v in data.items()])
    elif isinstance(data, list):
        return [replace_html(l) for l in data]
    elif isinstance(data, str) or isinstance(data, unicode):
        return _replace_str_html(data)


def str_to_dict(json_str):
    """
    将 json 的数据类型 转换成 json_dict 类型
    :param json_str:
    :return:
    """
    json_dict = ast.literal_eval(json_str)
    return replace_html(json_dict)


def replace_space(s):
    """
    将字符串中的空白字符替换
    :param s: 空白字符
    :return:
    """
    return s.replace(' ', '').replace('\r\n', '')
