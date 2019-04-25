# -*- coding: UTF-8 -*-
# 2019.4.26 by astraywu
# 给组里使用的CSV文件进行格式化
# eg: input_full_range = 1 #, 0, 0, 1, 0, 0, ,,0:limited range 1:full range, , (DCIParam)stDCIPara.s32InputFRange
# python format_csv.py test.csv output.csv

import sys
import csv

def getlen(data):
    # 获取字符串长度，中文按2个，英文按1个
    count = len(data)
    for s in data:
        if ord(s) > 127:
            count += 1
    return count

def getchineselen(data):
    # 获取中文字符的个数
    count = 0
    for s in data:
        if ord(s) > 127:
            count += 1
    return count
    # print('####')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        exit()
    in_filename = sys.argv[1]
    out_filename = sys.argv[2]
    with open(in_filename, 'r', encoding='utf-8', newline='') as fin:
        reader = csv.reader(fin)
        reader2 = []
        reader_strip = [] # 除去第一列剩余部分的csv内容
        f0 = []
        f1 = []
        for row in reader:
            reader2.append(row)
            if (len(row) != 11 or row[0] == '#' or row[0].find('#') == -1):
                continue
            # 第一列包含了等号和#号，需要额外对齐
            f0.append(row[0].split('=')[0].strip())
            f1.append(row[0].split('=')[1].strip('# '))
            row = [item.strip() for item in row ]
            reader_strip.append(row)
        # 直接用列表推导式完成二维矩阵的长度计算，使用getlen获取包括中文的长度（中文占两个字符宽度）
        widths = [max(getlen(row[i]) for row in reader_strip) for i in range(len(reader_strip[0]))] 
        w0 = max(len(row) for row in f0)
        w1 = max(len(row) for row in f1)
        with open(out_filename, 'w', encoding='utf-8', newline='') as fout:
            writer = csv.writer(fout)
            for row in reader2:
                # print('##################')
                if (len(row) != 11 or row[0] == '#' or row[0].find('#') == -1):
                    writer.writerow(row)
                    # print(row)
                    continue
                row_formatted = []

                f00 = row[0].split('=')[0].strip()
                f11 = row[0].split('=')[1].strip('# ')
                row = [item.strip() for item in row]
                row_formatted.append(f00.ljust(w0) + ' = ' + f11.ljust(w1) + ' #')
                for i in range(1, len(row)):
                    item = row[i].ljust(widths[i], '#')
                    row_formatted.append(row[i].ljust(widths[i] - getchineselen(row[i]), ' '))
                writer.writerow(row_formatted)
                # print(row_formatted)
