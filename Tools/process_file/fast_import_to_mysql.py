"""
此脚本用于处理批量的文件数据，如果在使用 python 连接 mysql 进行存储比较慢的时候可以考虑将数据整理成如下的数据结构：
例如如下举例：
title-----------> search_key    company_name    company_type    company_size    is_listed
field----------->field_value    field_value     field_value     field_value     field_value
然后在 MySQL 中创建一张跟目标字段一样的表结构，用数据导入的方式进行导入即可
"""
import json

# 配置文件路径
RAW_FILE = '源文件路径'  # C:\Users\feng\Desktop\腾讯数据\APP全站数据\历趣\result.json
NEW_FILE = '新文件路径'  # C:\Users\feng\Desktop\腾讯数据\APP全站数据\LiQu.txt
WRONG_FILE = '记录错误文件路径'     # C:\Users\feng\Desktop\腾讯数据\APP全站数据\wrong.json
TARGET_FIELD = '%s\t%s\t%s\t%s\t%s\t%s\n' % ()  # write your field


# 文件对象
raw_file = open(r'%s' % RAW_FILE, 'r', encoding='utf-8')
new_file = open(r'%s' % NEW_FILE, 'w+', encoding='utf-8')
wrong_file = open(r'%s' % WRONG_FILE, 'w+', encoding='utf-8')

# 写入标题行----->注意最后的换行符
new_file.write('app_name\tapp_info\n')

while True:
    # 每次处理固定的数据
    lines = raw_file.readlines(4 * 4096)
    if not lines:
        break
    for line in lines:
        try:
            """
            这里根据自己的文件类型不同，根据想要字段编写自己的处理逻辑
            这里有几个处理过的样本供参考
            """
            # 是json,转换为字典形式  [i.strip() for i in data.get('app_info') if i != "\n"]
            # data = json.loads(line)
            # app_name = data.get('app_name').strip() if data.get('app_name') else "暂无"
            # app_info_ = data.get('app_info')
            # app_info = list()
            # for k, v in app_info_.items():
            #     s = k + v
            #     app_info.append(s)
            # app_info = " ".join(app_info)
            # new_file.write('%s\t%s\n' % (app_name, app_info))

            # 获取每一个值 " ".join(data.get('app_desc')) if data.get('app_info') else "暂无"
            # " ".join(data.get('app_info')) if data.get('app_info') else "暂无"
            # app_name = data.get('app_name').strip() if data.get('app_name') else "暂无"
            # app_desc_ = [i.strip() for i in data.get('app_desc') if i]
            # app_desc = " ".join(app_desc_) if app_desc_ else "暂无"
            # app_info_ = [i.strip() for i in data.get('app_info') if i != "\n"]
            # app_info = " ".join(app_info_) if app_info_ else "暂无"
            # app_downloads = data.get('app_downloads').strip() if data.get('app_downloads') else "暂无"
            # cate_name = data.get('cate_name').strip() if data.get('cate_name') else "暂无"
            # category_name = data.get('category_name').strip() if data.get('category_name') else "暂无"
            # new_file.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (app_name, app_desc, app_info,
            #                                              app_downloads, cate_name, category_name))
            # # 获取每一个值
            # app_name = data.get('app_name').strip() if data.get('app_name') else "暂无"
            # app_desc = data.get('app_desc').strip() if data.get('app_desc') else "暂无"
            # app_info = " ".join(data.get('app_info')) if data.get('app_info') else "暂无"
            # cate_name = data.get('cate_name').strip() if data.get('cate_name') else "暂无"
            # category_name = data.get('category_name').strip() if data.get('category_name') else "暂无"
            # new_file.write('%s\t%s\t%s\t%s\t%s\n' % (app_name, app_desc, app_info, cate_name, category_name))
        except Exception as e:
            print(e)
            wrong_file.write(line)
