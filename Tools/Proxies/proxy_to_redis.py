"""
读取文件将代理存入redis
"""
from proxy.db import REDISCLIENT


def proxy_to_redis(proxy):
    """
    将代理存入redis
    :param proxy:
    :return:
    """
    # 创建数据库连接对象
    db = REDISCLIENT()
    # 调用入库方法
    db.add(proxy)


# 测试代码
if __name__ == "__main__":
    with open(r'C:\Users\feng\Desktop\Tools\Proxies\proxies.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("http"):
                proxy = line[7:].strip()
                # 入库
                proxy_to_redis(proxy)
        print("入库完成")