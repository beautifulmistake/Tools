"""
此脚本用于将从redis或者原生的Json文件转换为 csv 类型文件
在使用此脚本前需要确保传入的参数为一个字典类型的数据，如果不是
需要先将要转换为 csv 的字段提取转换为字典的类型
"""
import csv


class NotKeyError(BaseException):
    """
    自定义异常类
    """
    def __init__(self, arg):
        self.arg = arg


class KeyTypeError(BaseException):
    def __init__(self, arg):
        self.arg = arg


class JsonToCsv(object):

    def __init__(self, file_path=None, title=None):
        """
        初始化 csv 文件对象
        :param file_path: 转换后 csv 文件的保存路径
        :param title: csv 文件行首的标题 传入的是一个列表
        """
        # 转换后的文件路径
        self.path = file_path   # r'G:\工作\招聘网站爬虫\Boss\Position.xls'
        # 文件对象
        self.csvfile = open(self.path, 'a+', newline='', encoding='utf-8', errors='ignore')  # python3下需要这样写
        # 文件写入对象
        self.writer = csv.writer(self.csvfile, delimiter='\t')
        # csv文件的标题, 传入的是一个列表
        # ["position", "salary", "companyLocation", "experience","education",
        #  "companyName", "companyType", "isListed", "companySize"]
        self.title = title

    def write_title(self):
        """
        将行首的标题写入文件
        :return:
        """
        if not self.path and not self.title:
            raise NotKeyError("Need one parameter key or parameter file_path")
        if not isinstance(self.title, list):
            raise KeyTypeError(" Need type of list, check your title's type")
        # 将列标题写入文件
        self.writer.writerow(self.title)

    def record_to_file(self, data):
        """
        传入每一行的数据，将数据写入文件
        :param data: dict 类型
        :return:
        """
        if not isinstance(data, dict):
            raise KeyTypeError(" Need type of dict, check your data's type")
        # 将values数据一次一行的写入csv中----每一列的数据放在一个列表中统一写入
        self.writer.writerow(list(data.values()))


# 测试代码
if __name__ == "__main__":
    # 创建对象
    j = JsonToCsv(file_path=r'G:\工作\招聘网站爬虫\Boss\lianxi.xls',
                  title=["position", "salary", "companyLocation", "experience"])
    # 调用标题方法
    j.write_title()
    # 调用写入文件的方法
    j.record_to_file({"position": "程序猿", "salary": "吃土", "companyLocation": "皇城", "experience": "积累"})
