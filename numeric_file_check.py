# -*- coding:utf-8 -*-
import json
import os
import common_function
import re

kRESULT = 'result'
kERROR_LIST = 'error_list'
kTITLE = 'title'
kMSG = 'msg'
kINFO = 'info'
res = {kRESULT: True, kERROR_LIST: []}


def errors(title, msg, info):
    """

    构造一个错误字典
    :param title: 错误标题
    :param msg: 错误信息
    :param info: 错误的具体描述
    :return: [dict] 错误字典
    """
    return {kTITLE: title, kMSG: msg, kINFO: info}


def format_line(line):
    """

    :param line:
    :return:
    """
    list_line = line.replace("\"", "").replace("'", "").strip()
    str_line = "\t".join(re.split("[\s\,]+", list_line))
    return str_line


def format_file(file_name):
    f = open(file_name, "r")
    fw = open("data/form_mdp_numeric.txt", "w")
    headline = f.readline()
    head = headline.replace("\"", "").replace("'", "").strip()
    list_head = re.split("[\s\,]+", head)
    if (list_head[0] == "1"):
        if (list_head[1] != "0" and list_head[1] != "1" and list_head[1] != "2"):
            if (list_head[2] != "0" and list_head[2] != "1" and list_head[2] != "2"):  # 有行标题并且前面有行号
                for line in f.readlines():
                    list_line = line.replace("\"", "").replace("'", "").strip()
                    str_line = "\t".join(re.split("[\s\,]+", list_line)[1:])
                    fw.writelines(str_line)
                    fw.writelines("\n")
            else:  # 没有行标题 但有序号
                list_line = headline.replace("\"", "").replace("'", "").strip()
                str_line = "\t".join(re.split("[\s\,]+", list_line)[1:])
                fw.writelines(str_line)
                fw.writelines("\n")
                for line in f.readlines():
                    list_line = line.replace("\"", "").replace("'", "").strip()
                    str_line = "\t".join(re.split("[\s\,]+", list_line)[1:])
                    fw.writelines(str_line)
                    fw.writelines("\n")
    else:
        if (list_head[0] != "0" and list_head[0] != "1" and list_head[0] != "2"):
            if (list_head[1] != "0" and list_head[1] != "1" and list_head[1] != "2"):  # 有行标题并且前面没有行号
                for line in f.readlines():
                    list_line = line.replace("\"", "").replace("'", "").strip()
                    str_line = "\t".join(re.split("[\s\,]+", list_line))
                    fw.writelines(str_line)
                    fw.writelines("\n")
            else:
                str_line = format_line(headline)
                fw.writelines(str_line)
                fw.writelines("\n")
                for line in f.readlines():
                    str_line = format_line(line)
                    fw.writelines(str_line)
                    fw.writelines("\n")
    f.close()
    fw.close()


def check_title(file_name):
    num = 0
    for line in open(file_name):
        num = num + 1
        title = line.strip().split("\t")[0]
        if len(title) < 2:
            # if title.isdigit():
            res[kRESULT] = False
            res[kERROR_LIST].append(errors(file_name, "文件第" + str(num) + "行缺少标题", "文件第一列必须为标题"))
            if (len(res[kERROR_LIST]) >= 10):
                break
            continue


def check_line_data_num(file_name):
    num = 1
    f = open(file_name, "r")
    head_line = f.readline()
    list_head = head_line.split("\t")
    data_line_num = len(list_head)
    for line in f.readlines():
        num = num + 1
        list_line = line.strip().split("\t")
        if (data_line_num != len(list_line)):
            res[kRESULT] = False
            res[kERROR_LIST].append(errors(file_name, "文件第" + str(num) + "行数据缺失或冗余", "文件每行数据的列数应该相同"))
            if (len(res[kERROR_LIST]) >= 10):
                break
            continue


def check_data(file_name):
    num = 0
    for line in open(file_name):
        num = num + 1
        content_data = line.strip().split("\t")[1:]
        for data in content_data:
            if (data == "0" or data == "1" or data == "2"):
                continue
            else:
                res[kRESULT] = False
                res[kERROR_LIST].append(errors(file_name, "文件第" + str(num) + "行数据错误", "文件数据必须为0，1,2"))
                if (len(res[kERROR_LIST]) >= 10):
                    break
                continue
        if (len(res[kERROR_LIST]) >= 10):
            break


def title2list(file_name):
    list_title = []
    f = open(file_name, "r")
    for line in f.readlines():
        title = line.strip().split('\t')[0]
        list_title.append(title)
    f.close()
    return list_title


def check_numeric_file(numeric_file):
    # 定义检查结果


    # --- 检查文件 --- #


    # 是否是文本文件

    # 被检查的文件是否是文本文件
    if not common_function.isTextFile(numeric_file):
        res[kRESULT] = False
        res[kERROR_LIST].append(errors(numeric_file, "文件不是text文件", "计算所需文件为text格式文本文件"))
    else:
        # 格式化文件
        format_file(numeric_file)
        numeric_file = "data/form_mdp_numeric.txt"

        # 检查文件第一列是否为标题
        check_title(numeric_file)

        # 检查行数据格式是否相同
        check_line_data_num(numeric_file)
        # 检查数据是否都是0,1,2
        check_data(numeric_file)
        # 返回res 字典
        return res


# 命令行入口
if __name__ == "__main__":
    # 调用主函数
    dict_res = check_numeric_file("test/mdp_numeric.txt")
    open("test/numeric_check_result.json", "w").write(json.dumps(dict_res, ensure_ascii=False))
    # dict_res1 = check_numeric_file("test/mdp_numeric_linenum.txt")
    # open("test/numeric_check_line_result.json", "w").write(json.dumps(dict_res1, ensure_ascii=False))
