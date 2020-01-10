#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/1/9 22:06
# @Author  : Leslee
import os
import time
import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

class ProcessEs(object):

    def __init__(self,ip="127.0.0.1",port=9200,index="complex_qa",doc_type="",datapath=""):
        self._index = index # es创建index相当于创建数据库

        self.es = Elasticsearch([ip], port=port)
        # 用户密码
        # self.es = Elasticsearch([ip], http_auth=('admin', '123456'), port=9200)
        self.doc_type = doc_type
        self.my_file = datapath

    # 创建es索引，确定分词类型。索引用max_word，搜索时用ik_smart

    def create_idx_mapping(self):
        node_mappings = {
            "mappings": {
                self.doc_type: {  # type
                    "properties": {
                        "aquestion": {  # field: 问题
                            "type": "text",  # lxw NOTE: cannot be string
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_smart",
                            "index": "true"  # The index option controls whether field values are indexed.
                        },
                        "category": {  # field: 大类别
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_smart",
                            "index": "true"
                        },
                        "subcategory": {  # field: 子类别
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_smart",
                            "index": "true"
                        },
                        "aanswer": {  # field: 答案
                            "type": "text",  # lxw NOTE: cannot be string
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_smart",
                            "index": "true"  # The index option controls whether field values are indexed.
                        },
                        "aqtopic": {  # field: 问题的主题类型
                            "type": "text",  # lxw NOTE: cannot be string
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_smart",
                            "index": "true"  # The index option controls whether field values are indexed.
                        },
                        "aqkeywords": {  # field: 问题的关键词
                            "type": "text",  # lxw NOTE: cannot be string
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_smart",
                            "index": "true"  # The index option controls whether field values are indexed.
                        },
                        "aatopic": {  # field: 答案的主题
                            "type": "text",  # lxw NOTE: cannot be string
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_smart",
                            "index": "true"  # The index option controls whether field values are indexed.
                        },
                        "aakeywords": {  # field: 答案的关键词
                            "type": "text",  # lxw NOTE: cannot be string
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_smart",
                            "index": "true"  # The index option controls whether field values are indexed.
                        },
                    }
                }
            }
        }
        if not self.es.indices.exists(index=self._index):
            self.es.indices.create(index=self._index, body=node_mappings, ignore=[400, 409])
            print("Create {} mapping successfully.".format(self._index))
        else:
            print("index({}) already exists.".format(self._index))
    # 批量插入数据
    def insert_batch_data(self,data_list):
        success,_ = bulk(self.es,data_list,index=self._index,raise_on_error=True)
        print("Performed {0} actions. _: {1}".format(success, _))

# 初始化es，并且把数据插入到es中
def InitAndInsert(ip,port,index,type,data_path,bulk_count):

    pre_es = ProcessEs(ip=ip,port=port,index=index,doc_type=type,datapath=data_path)
    # 创建index
    pre_es.create_idx_mapping()
    start_time = time.time()
    index = 0
    count = 0
    action_list = []
    BULK_COUNT = bulk_count # batch_size

    for line in open(pre_es.my_file,'r',encoding='utf-8'):
        if not line:
            continue
        item = json.loads(line)
        index += 1

        action = {
            "_index":pre_es._index,
            "_type": pre_es.doc_type,
            "_source":{
                "aquestion":item['aQuestion'],
                "category": item['category'],
                "subcategory":item['subCategory'],
                "aanswer": item['aAnswer'],
                "aqtopic": item['aQtopic'],
                "aqkeywords":item['aQkeywords'],
                "aatopic":item['aAtopic'],
                "aakeywords":item['aAkeywords'],
            }
        }
        action_list.append(action)
        if index > BULK_COUNT:
            pre_es.insert_batch_data(data_list=action_list)
            index = 0
            count += 1
            print("bulk {} writted finished!".format(count))
            action_list = []
    endtime = time.time()
    print("time slep:{0}".format(endtime-start_time))

if __name__ == '__main__':
    ip = ""
    port = 0000
    index = "complex_qa"
    type = "faq"
    data_path = "./qa_corpus.json"
    bulk_count = 1000
    InitAndInsert(ip,port,index,type=type,data_path=data_path,bulk_count=bulk_count)

