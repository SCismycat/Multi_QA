# Multi_QA
This projct contains FAQ/KBQA/reading comprehension..etc..,and Experiment with filters and reRakning methods and weight controller combinations.   

## FAQ
### 思路:(不完备)
使用elasticSearch存储标准问答对，搭建问答服务，对输入进行匹配。
首先搭建基础服务（数据导入、查询服务等），然后从以下三个方面优化：  
1. 输入匹配问题；在es上进一步优化文本匹配，训练深度语义匹配模型；
2. 数据结构设计；考虑标准问答库中很多文本信息可以作为相似度比对标准。因此，考虑设计
对应字段，增加匹配能力和精度。例如：获取并存储标准Q-A对的主题以及core words。
3. 结果reRanking：问题与问题，问题与答案，答案与答案；考虑精排的reRanking，怎么精排？怎么二次排序？
4. 其他trick
### Version 0.0.1
1. 搭建es分布式集群
2. 学习使用Python的es client，抽象数据结构，封装数据导入接口、查询接口等。
3. 导入数据集，完成基本检索过程。
完成基本检索功能。
### Version 0.0.2
直接通过es的查询和字段控制对结果进行reRanking一定可以提高检索效果。es工程向的东西慢慢优化。
1. 提取aQ和aA的关键词和主题，在匹配时，考虑主题匹配和关键词相似度来共同加权。
2. 进一步，研究深度短文本匹配方法。
3. 字段预定义Category和SubCategory，学习一下聚合查询，完成选定领域的QA。(此法可扩展至文本分类确定category)

## KBQA
待补充..
## RC
待补充..
# Reference
待添加