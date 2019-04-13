"""
此脚本用于将单列多行的 csv 转换为多行的 txt 文件
"""

import xlrd

# 要转换的csv文件路径
data = xlrd.open_workbook(r'G:\工作\工作计划\腾讯调研--超100件的企业.xlsx')
# 这个一定得先重新命名sheet----->
sh = data.sheet_by_name('tencent')
# 总行数/列数
print(sh.nrows)
print(sh.ncols)
# 将数据重新写入文件之中
with open(r'G:\工作\工作计划\Boss_tencent.txt', 'w+', encoding='utf-8') as f:
    for i in range(sh.nrows):
        text = sh.cell_value(i, 0)
        print(text)
        f.write(text)
        f.write("\n")
