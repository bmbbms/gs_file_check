# -*- coding:utf-8 -*-
import json
import sys
import os
import numeric_file_check
import traits_file_check
import common_function

GENOTYPE_NUM="genotype_num"
PHENOTYPE_TRAIT="phenotype_trait"
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
def check_parameter(dict, key, value_type):
    """

    检查字典中是否存在key,以及对应key的值是否是所要求的类型.
    :param dict: 字典
    :param key: 键
    :param value_type: 类型
    :return: [bool] 检查是否通过
    """
    if key not in dict.keys():
        print "Key: '" + key + "' missing."
        return False
    else:
        return True
def match_gs_file(input_file='data/task.gacfg', output_file='file_check_result.json'):
    """
    主要程序逻辑
    :param
    input_file: 输入文件名
    :param
    output_file: 输出文件名
    :return: [int]
    0 -> 检查程序无异常, 正常退出;
    (有可能检查出来有错误, 也有可能没有错误.)
    1 -> 输入参数错误;
    2 -> 被检查的文件不存在;
    3 -> 非文本文件不支持
    """


    # --- 处理输入参数 ---- #

    # DEBUG记录参数
    # logging.log(logging.DEBUG, 'argv:' + str(argv))

    # 读取json参数
    # 读取json参数
    try:
      p = json.loads(open(input_file).read(), encoding='utf-8')
    except ValueError, e:
      print 'Load Json Failed:' + e.message
      return 1

    # 从json参数中取出需要的值
    if check_parameter(p, GENOTYPE_NUM, str) and check_parameter(p, PHENOTYPE_TRAIT, str):
      numeric_file = p[GENOTYPE_NUM]
      traits_file = p[PHENOTYPE_TRAIT]
    else:
      return 1

  # --- 处理输入参数end --- #

      # 被检查的文件是否存在
    if not os.path.isfile(numeric_file):
        print "No such file : '" + str(numeric_file) + "'"
        return 2
    if not os.path.isfile(traits_file):
        print "No such file : '" + str(traits_file) + "'"
        return 2
    #   #检查是否是文本文件
    # if not common_function.isTextFile(numeric_file):
    #     print "not text file:'"+str(numeric_file)+"'"
    #     return 3
    # if not common_function.isTextFile(traits_file):
    #     print "not text file:'" + str(traits_file) + "'"
    #     return 3


      #检查numeric文件
    numeric_res=numeric_file_check.check_numeric_file(numeric_file)
    if(numeric_res[kRESULT]==False):
        res[kRESULT]=False
        res[kERROR_LIST].append(numeric_res[kERROR_LIST])
      #检查traits文件
    traits_res=traits_file_check.check_traits_file(traits_file)
    if(traits_res[kRESULT]==False):
        res[kRESULT] = False
        res[kERROR_LIST].append(traits_res[kERROR_LIST])
      #文件匹配
    numeric_file="data/form_mdp_numeric.txt"
    traits_file="data/form_mdp_traits.txt"
    numeric_title_list=numeric_file_check.title2list(numeric_file)
    traits_title_list=traits_file_check.title2list(traits_file)
    count=0
    all_gene=len(numeric_title_list)
    for name in traits_title_list:
        if name in numeric_title_list:
            count=count+1
    p=float(count)/all_gene
    if(p<0.1):
        res[kRESULT] = False
        res[kERROR_LIST].append(errors(traits_file, "文件基因匹配度不足", "文件基因型匹配必须达到10%"))
    open("file_check_result.json", "w").write(json.dumps(res, ensure_ascii=False))
    return res




if __name__=="__main__":
    match_gs_file()