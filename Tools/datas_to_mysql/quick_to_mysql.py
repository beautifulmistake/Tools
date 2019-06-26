import json
import time
from peewee import *
from playhouse.db_url import connect


# 第一种连接数据库的方式
mysql_db = MySQLDatabase('database', host='your host', port=3306, user='user_name',
                         passwd='your password', charset='utf8')

# 使用数据库URL连接数据库
# mysql_db = connect('mysql://user:passwd@ip:port/my_db')
mysql_db = connect('mysql://reptile:QDsmZw@0422&@40.73.37.111:22822/tengxun_all')


class BaseModel(Model):
    """ A base model that will use our MySQL database",之后所有的类都继承于此类"""
    class Meta:
        database = mysql_db


class Goods(BaseModel):
    """
    创建一个类继承于 BaseModel ，该类就对应数据库中的一张表
    """
    # 定义一些字段
    one = CharField(verbose_name="one", max_length=100, primary_key=True, null=False)


def process_your_website(filepath):
    """
    自定义字段处理方法，数据可以是存储在txt文件或者 json 文件之中
    :param filepath: 文件路径
    :return:
    """
    _field_list = Goods._meta.sorted_field_names
    _field_list.remove("id")

    def process_data(data):
        """
        根据不同的数据格式采取不同的方法处理处理
        这里以JSON数据为例说明
        :param data:
        :return:
        """
        d = dict()
        d['search_key'] = data['search_key']
        d['game_type'] = data['game_type']
        d['game_name'] = data['game_name'] if data['game_name'] else "暂无"
        d['publish_time'] = data['publish_time']
        d['game_category'] = data['game_category']
        d['developer'] = data['developer']
        d['platform'] = data['platform']
        d['pic'] = data['pic']
        if d['game_name'] == "暂无":
            return
        return d

    ddd = []
    with open(filepath, "r", encoding="utf8", errors='ignore') as f:
        lines = f.readlines()
        for r in lines:
            r = json.loads(r, encoding="utf8")
            data = process_data(r)
            if data:
                ddd.append(data)

    if not Goods.table_exists():
        """
        表如果不存在，则以类名的小写拼音命名表名并创建表
        """
        mysql_db.create_tables([Goods])

    start_time = time.time()

    NUM = len(ddd)
    with mysql_db.atomic():
        for i in range(0, NUM, 5000):
            Goods.insert_many(ddd[i: i + 5000]).execute()

    print("插入{}条数据, 花费: {:.3}秒".format(NUM, time.time() - start_time))
