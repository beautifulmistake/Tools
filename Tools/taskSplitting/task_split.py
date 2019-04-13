"""
常用的大文件拆分方法：从鹏鹏同学那而学习的
"""
import json
import sys


def check_repeat(key, file_path):
    """
    查看一批同源数据，根据指定的 key 进行匹配重复的情况
    :param key: 唯一标识一条数据的键
    :param file_path: 存储文件的路径
    :return:
    """
    fingerprint = set()     # 去重
    with open(file_path, 'r', encoding='utf-8') as f:
        # 所有的数据，一行为一条数据
        _iterable = f.readlines()
        # 行数，未去重前的行数
        true_count = len(_iterable)
        # 计数器
        count = 0
        # 重复的行数
        repeat_count = 0
        for line in _iterable:
            # 将json--->dict
            line_result = json.loads(line)
            flg = line_result.get(key)
            if flg:
                # 去重
                if flg not in fingerprint:
                    count += 1
                    fingerprint.add(flg)
                else:
                    repeat_count += 1
    # 判断总结果
    if count == true_count:
        print("没有重复数据")
    else:
        print("重复数据条数为：%d" % repeat_count)


class NotKeyError(BaseException):
    """
    自定义异常类型
    """
    def __init__(self, arg):
        self.arg = arg


class MoreKeyError(BaseException):
    def __init__(self, arg):
        self.arg = arg


def split_data(key=None, file_path=None, base_step=3000, base_file_name="info"):
    """
    任务分割函数，用来对redis或文件中的大量数据进行分割成多个小文件
    :param key: redis key
    :param file_path: 文件路径
    :param base_step: 要被分割成的小文件的行数
    :param base_file_name: 要被分割的文件名，默认的是 info
    :return:
    """
    if not key and not file_path:
        raise NotKeyError("Need one parameter key or parameter file_path")
    if key and file_path:
        raise MoreKeyError("The parameter key and the parameter file_path are mutually exclusive")
    if key:
        print("You can use file_to_db.py to export the data to a file and then use this function.")
        sys.exit(0)
    if file_path:
        # 计算主文件行数（文件按照行数分割文件）
        with open(file_path, 'r', encoding='utf-8') as f:
            file_data = f.readlines()
            i = 1
            for index, d in enumerate(file_data, 1):
                file_name = "%s_%d.txt" % (base_file_name, i)
                f2 = open(file_name, 'a', encoding='utf-8')
                f2.write(d)
                if index > int(base_step) * i:
                    f2.close()
                    i += 1


# 测试函数
if __name__ == "__main__":
    check_repeat(key="search_kw", file_path=r"C:\Users\EDZ\Desktop\db_2\data_business.txt")
    split_data(file_path="key.txt")
