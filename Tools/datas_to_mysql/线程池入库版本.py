import time
import math
from peewee import *
from playhouse.db_url import connect
from twisted.python import threadpool


# mysql_db = connect('mysql://user:passwd@ip:port/my_db')
mysql_db = connect('')
redis_client = redis_client.RedisClient(settings.REDIS_PARAMS).redis_client


class BaseModel(Model):
    class Meta:
        database = mysql_db


class T_Applicant_2019(BaseModel):
    applicant_cn = CharField()
    flag = IntegerField(default=0)


class T_Applicant_2019_20w(BaseModel):
    applicant_cn = CharField()
    flag = IntegerField(default=0)


def get_item_range(key: str, start: int, counts: int, base: int):

    def func(*args):
        """获取数据"""
        _key, _start, _end, _c = args
        data_list = redis_client.lrange(name=_key, start=_start, end=_end)
        data_list = [{"applicant_cn": data} for data in data_list]
        return data_list

    def on_result(_, result):
        start_time = time.time()
        NUM = len(result)
        with mysql_db.atomic():
            for i in range(0, NUM, 1000):
                # T_Applicant_2019.insert_many(result[i: i + 1000]).execute()
                T_Applicant_2019_20w.insert_many(result[i: i + 1000]).execute()
                print(f"执行插入 1000 条, 当然进度为 {i}: {NUM}")
        print("插入{}条数据, 花费: {}秒".format(NUM, time.time() - start_time))

    cycle_num = math.ceil(counts / base)
    params_list = []

    end = base - 1
    th_pool = threadpool.ThreadPool()

    for c in range(cycle_num):
        params_list.append((key, start, end, c))
        start, end = end + 1, end + base

    for params in params_list:
        th_pool.callInThreadWithCallback(on_result, func, *params)
    th_pool.start()
    th_pool.stop()


def xs(result):
    length = len(result)
    with mysql_db.atomic():
        for i in range(0, length, 2000):
            # T_Applicant_2019.insert_many(result[i: i + 2000]).execute()
            T_Applicant_2019_20w.insert_many(result[i: i + 2000]).execute()
    print("插入{}条数据".format(length))


def all_item_range(key: str, start: int, end: int, base: int, func):
    item_counts = redis_client.llen(key)
    print("item counts is: ", item_counts)

    def on_result(f, result):
        """执行回调结果-将生成的任务队列入库"""
        if f:
            data_list = [{"applicant_cn": data} for data in result]
            return func(data_list)
        else:
            raise TypeError("get keyword.txt callback error")

    params_list = []
    while start <= item_counts:
        params_list.append((key, start, end))
        start, end = end+1, end + base
        if end > item_counts:
            end = item_counts
    th_pool = threadpool.ThreadPool()
    for params in params_list:
        th_pool.callInThreadWithCallback(on_result, redis_client.lrange, *params)
    th_pool.start()
    th_pool.stop()


def process_qxb():
    # if not T_Applicant_2019.table_exists():
    #     mysql_db.create_tables([T_Applicant_2019])
    if not T_Applicant_2019_20w.table_exists():
        mysql_db.create_tables([T_Applicant_2019_20w])

    # get_item_range(key="prov_other", start=0, counts=10001, base=5000)

    all_item_range(key="prov_other", start=0, end=10001, base=5000, func=xs)


if __name__ == '__main__':
    process_qxb()

