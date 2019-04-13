"""
此将本用于将 redis 数据库的关键字导出
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

# 获取关键字的总数
total = connect.dbsize()
# 遍历获取关键字，并写入文件
with open(r'%s' % FILE_PATH, 'a+', encoding='utf-8') as f:
    # 遍历获取关键字
    for index in range(1, total):
        keyword = connect.get(str(index)).decode('utf-8')
        # 将关键字写入文件
        f.write(keyword + "\n")
