"""
此脚本用于将 txt 文本的关键字导入到 redis 数据库
"""
import redis

# redis 数据库配置信息
REDIS_HOST = '40.73.39.166'
REDIS_PORT = 6379   # 注意为 int 类型
REDIS_DB = 0    # 默认为 0 ，需要其他的写自己的数据库  int 类型
REDIS_PASSWORD = None   # 默认为 None，如果有写入你的密码，str 类型
FILE_PATH = 'your_file_path'    # 文件的路径

# 使用 redis 连接池
pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD)
connect = redis.Redis(connection_pool=pool)

with open(r'%s' % FILE_PATH, 'r+', encoding='utf-8') as f:
    lines = f.readlines()
    for index in range(len(lines)):
        connect.set(index, lines[index].strip())
    print("数据导入完成")
