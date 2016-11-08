# -*- coding:utf-8 -*-

import re
import json
import common_function

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
    list_line = line.replace("\"", "").replace("'", "").strip()
    str_line = "\t".join(re.split("[\s\,]+", list_line))
    return str_line
def format_file(file_name):
    f=open(file_name,"r")
    fw=open("data/form_mdp_traits.txt","w")
    headline = f.readline()
    head = headline.replace("\"", "").replace("'", "").strip()
    list_head = re.split("[\s\,]+", head)
    if (list_head[0] != "1"):
        str_head="\t".join(list_head[0:2])
        fw.writelines(str_head)
        fw.writelines("\n")
        for line in f.readlines():
            str_line=format_line(line)
            list_line=re.split("\t",str_line)[0:2]
            if(list_line[1].lower=="na" or list_line[1].lower()=="nan"):
                list_line[1]="NA"
            cut_str_line="\t".join(list_line)
            fw.writelines(cut_str_line)
            fw.writelines("\n")
    elif(list_head[0]=="1"):
        str_head = "\t".join(list_head[1:3])
        fw.writelines(str_head)
        fw.writelines("\t")
        for line in f.readlines():
            form_line = line.replace("\"", "").replace("'", "").strip()
            list_line=re.split("[\s\,]+",form_line)[1:3]
            if (list_line[1].lower == "na" or list_line[1].lower()=="nan"):
                list_line[1] = "NA"
            str_line = "\t".join(list_line)
            fw.writelines(str_line)
            fw.writelines("\n")
    else:
        res[kRESULT]=False
        res[kERROR_LIST].append(errors(file_name, "文件第" + str(1) + "行数据错误", "文件必须有行标题"))

    f.close()
    fw.close()
def check_lin_title(file_name):
    num=0
    for line in open(file_name):
        num=num+1
        title=line.strip().split("\t")[0]
        if len(title)<2:
            res[kRESULT] = False
            res[kERROR_LIST].append(errors(file_name, "文件第"+str(num)+"行缺少标题", "文件第一列必须为标题"))
            if (len(res[kERROR_LIST]) >= 10):
                break
            continue
def check_form_data(file_name):
    num=1
    f=open(file_name,"r")
    headline=f.readline()
    for line in f.readlines():
        num=num+1
        list_line=line.strip().split("\t")

        if(re.match("^[0-9]*\.?[0-9]+$",list_line[1]) or list_line[1]=="NA"):#匹配浮点数或者NA
            continue
        else:
            res[kRESULT] = False
            res[kERROR_LIST].append(errors(file_name, "文件第" + str(num) + "行数据错误", "第二列数据必须为数值或NA"))
            if (len(res[kERROR_LIST]) >= 10):
                break
        if (len(res[kERROR_LIST]) >= 10):
            break
    f.close()
def title2list(file_name):
    list_title=[]
    f=open(file_name,"r")
    headline = f.readline()
    for line in f.readlines():
        title=line.strip().split('\t')[0]
        list_title.append(title)
    f.close()
    return list_title

def check_traits_file(file_name):
    if not common_function.isTextFile(file_name):
        res[kRESULT] = False
        res[kERROR_LIST].append(errors(file_name, "文件不是text文件", "计算所需文件为text格式文本文件"))
    else:

        #格式化文件（去掉，“ 空格 首列可能为行号的可能，并以\t 分隔数据）
        format_file(file_name)
        file_name="data/form_mdp_traits.txt"
        #标题检查
        check_lin_title(file_name)
        #数据检查
        check_form_data(file_name)
        return res
  #  open("file_check_result.json", "w").write(json.dumps(res, ensure_ascii=False))

    #文件格式检查
if __name__ == "__main__":
    # 调用主函数
    dict_res= check_traits_file("data/mdp_traits.txt")
    open("file_check_result.json", "w").write(json.dumps(dict_res, ensure_ascii=False))
