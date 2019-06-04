"""
使用redis list 类型实现一个简单的任务队列
"""
import redis


class RedisQueue(object):
    def __init__(self, name, namespace='queue', **redis_kwargs):
        """
        初始化一些参数，redis 的默认参数为：host='localhost',port=6379,db=0
        :param name:
        :param namespace:
        :param redis_kwargs:
        """
        # 获取数据库连接对象
        self.__db = redis.Redis(**redis_kwargs)
        # 存取值的键
        self.key = '%s: %s' % (namespace, name)

    def qsize(self):
        """
        返回任务队列里的数量
        :return:
        """
        return self.__db.llen(self.key)

    def put(self, item):
        """
        向任务队列的最右方添加元素
        :param item:
        :return:
        """
        self.__db.rpush(self.key, item)

    def get_wait(self, timeout=None):
        """
        返回队列里的第一个元素，如果为空则等待至有元素被加入队列
        超时时间的阈值为timeout，如果为None，则一直等待
        :param timeout:
        :return:
        """
        item = self.__db.blpop(self.key, timeout=timeout)
        return item

    def get_nowait(self):
        """
        直接返回任务队列第一个元素，如果队列为空则返回的是None
        :return:
        """
        item = self.__db.lpop(self.key)
        return item
