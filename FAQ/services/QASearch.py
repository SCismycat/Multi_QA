#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/1/10 14:03
# @Author  : Leslee
from elasticsearch import Elasticsearch
import jieba
class Searcher(object):
    def __init__(self,ip="127.0.0.1"):
        self._index = "complex_qa"
        self.es = Elasticsearch([ip],port=9200)
        self.doc_type = "faq"
    # 定义查询匹配
    def search_specific(self,question,key="aquestion"):

        query_body = {
            "query": {
                  "bool": {
                      "must":[
                          {
                              "match":{
                                  key : str(question)
                              }
                          }
                      ]
                  }
                }
        }
        searched = self.es.search(index=self._index,body=query_body,size=10)
        return searched["hits"]["hits"]
    # 进行问题查询
    def answer_from_es(self,question):
        answers = []
        res = self.search_specific(question,key="aquestion")
        for hit in res:
            answer_dict = {}
            answer_dict['score'] = hit['_score'] / 100
            answer_dict['sim_question'] = hit['_source']['aquestion']
            answer_dict['aanswer'] = hit['_source']['aanswer']
            answers.append(answer_dict)
        return answers

def main():
    my_search = Searcher(ip="")

    while True:
        question = input('您的问题是：')
        try:
            responses = my_search.answer_from_es(question)
            response_sorted = sorted(responses,key=lambda x:x['score'],reverse=True)
            answer = response_sorted[0]['aanswer']
            print('最佳答案：',answer)
        except:
            print(" 查询失败")

if __name__ == '__main__':
    main()
