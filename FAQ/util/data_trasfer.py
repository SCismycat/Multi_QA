#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/1/9 12:14
# @Author  : Leslee
"""
数据转换为json数据格式
"""
import csv
import json
import random
import string

def read_file(filename):
    qa_pairs = []
    with open(filename,'r',encoding='utf-8') as csv_file:
        fieldNames = ("title","question","reply")
        reader = csv.DictReader(csv_file,fieldNames)
        for row in reader:
            if row['title'] == 'title':
                del row['title']
                continue
            # yield (row['title']+row['reply'])
            qa_pairs.append((row['title'],row['reply']))
    return qa_pairs

def gen_random_ids():
    random_id = "".join(random.sample(string.ascii_letters+string.digits,8))
    return random_id

def trans_to_json(tup_data,category):
    result_dict_list = []
    for data in tup_data:
        result = {}
        result['id'] = gen_random_ids()
        result['aQuestion'] = data[0]
        result['aQtopic'] = []
        result['aQkeywords'] = []
        result['aAnswer'] = data[1]
        result['aAtopic'] = []
        result['aAkeywords'] = []
        result['category'] = category
        result['subCategory'] = ""
        result_dict_list.append(json.dumps(result,ensure_ascii=False))
    return result_dict_list

def json_trans_myjson(filename,category):
    result_data = []
    with open(filename,'r',encoding='utf-8') as jfile:
        for line in jfile.readlines():
            li_dict = json.loads(line)
            result = {}
            result['id'] = gen_random_ids()
            result['aQuestion'] = li_dict['question']
            result['aQtopic'] = []
            result['aQkeywords'] = []
            result['aAnswer'] = li_dict['answers']
            result['aAtopic'] = []
            result['aAkeywords'] = []
            result['category'] = category
            result['subCategory'] = li_dict['category']
            result_data.append(json.dumps(result,ensure_ascii=False))
    return result_data

def writer_to_json(filename,result):
    with open(filename,'w',encoding='utf-8') as writer:
        for res in result:
            writer.write(res+"\n")

if __name__ == '__main__':
    # fileName = "F:/学习资料/对话系统/问答语料库/anhuidianxinzhidao_filter.csv"
    #     fileName1 = "F:/学习资料/对话系统/问答语料库/nonghangzhidao_filter.csv"
    # fileName = "F:/学习资料/对话系统/问答语料库/financezhidao_filter.csv"
    #
    # qa_pairs = read_file(fileName)
    category = "法律知识"
    # result = trans_to_json(qa_pairs,category=category)
    w_name = "./law.json"
    # writer_to_json(w_name,result)
    name = "./qa_corpus.json"
    ans = json_trans_myjson(name,category)
    writer_to_json(w_name,ans)