import json

import redis


def write_to_file(file_name, file_type):
    """
    将数据写入文件
    :param file_name: 文件的名称
    :param file_type: 文件的类型  txt/json
    :return:
    """
    return open('%s.%s' % (file_name, file_type), 'w+', encoding='utf-8')


def conn_to_redis(redis_host, redis_port, redis_db, password):
    """
    获取redis 数据库连接
    :param redis_host: host
    :param redis_port: port
    :param redis_db: 连接的数据库（0 ~ 16)
    :param password: 密码
    :return:
    """
    pool = redis.ConnectionPool(host=redis_host, port=redis_port, db=redis_db, password=password)

    return redis.Redis(connection_pool=pool)


def all_data(redis_host, redis_port, redis_db, password, redis_key, file_name, file_type):
    """
    直接传参调用此方法即可
    :param redis_host: host
    :param redis_port: port
    :param redis_db: db
    :param password: 密码
    :param redis_key: 存储数据的 key
    :param file_name: 文件名称
    :param file_type: 文件类型 txt/json
    :return:
    """
    # 获取数据库连接
    conn = conn_to_redis(redis_host, redis_port, redis_db, password)
    # 数据总数
    list_len = conn.llen(redis_key)
    # 文件对象
    file = write_to_file(file_name, file_type)
    # 遍历每一条数据
    for index in range(list_len):
        word = json.loads(conn.lindex(redis_key, index).decode('utf-8'))
        # 写入文件
        file.write(json.dumps(word, ensure_ascii=False) + '\n')
    # 关闭文件
    file.close()
    print("数据导出完成")


# 测试代码
if __name__ == "__main__":
    # 导出数据
    # all_data('host', 6379, 0, 'password', 'redis_key', 'file_name', 'file_type')
