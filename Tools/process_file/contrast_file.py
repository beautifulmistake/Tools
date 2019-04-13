"""
此脚本用于对比两个文件，找出两个文件的不同的数据
常用于处理 txt 类型的关键字文件
"""
import re


BASE_FILE = 'your file path'    # str 类型，数据较多的文件
CONTRAST_FILE = 'contrast file path'    # str 类型，要对比的文件
RESULT_FILE = 'save result file path'   # str 类型，存储结果的文件

# 集合去重
base_set = set()
contrast_set = set()


with open(r'%s' % BASE_FILE, 'r+', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()
    for line in lines:
        # 此处可以根据不同情况做数据的清洗，比如包含其他字符，都可先使用 re 清洗后存入
        # word = re.compile('"(.*)"').findall(line)[0]
        base_set.add(line.strip())

with open(r'%s' % CONTRAST_FILE, 'r+', encoding='utf-8', errors='ignore') as f2:
    contrast_lines = f2.readlines()
    for line in contrast_lines:
        try:
            # word = re.compile(r'(.*?)ÿ.*').findall(line)[0]
            contrast_set.add(line.strip())
        except IndexError:
            print('wrong line : ', contrast_lines.index(line))


different_set = base_set - contrast_set
print("共有%s条数据不同，对比结果如下：\n%s" % (len(different_set), different_set))

with open(r'%s' % CONTRAST_FILE, 'w+', encoding='utf-8', errors='ignore') as f3:
    for key in different_set:
        f3.write('%s' % key + '\n')
    print('数据对比/写入文件完成')
