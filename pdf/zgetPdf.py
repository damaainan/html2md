# -*- coding=utf-8 -*-

# 知乎文章下载

from zstore import ZhihuStoreData
import time
import sys
from zmypdf import ZhiHuGenPdf

def getPdf():
    store = ZhihuStoreData()
    # 查数据库
    toPdfList, columns = store.getListFromParam('state=0')

    # 修改状态
    data = []
    i=0
    for val in toPdfList:
        dic = {}
        for key,name in enumerate(columns):
            dic[name] = val[key]
        if dic["type"] == "article":
            # genpdf(dic)
            dealArticle(dic)
        elif dic["type"] == "answer":
            dealAnswer(dic)

        data.append(dic)
        i+=1
        if i%2==0:
            break
    # print(data)
    return

def genpdf(data):
    store = ZhihuStoreData()
    # 传值生成pdf
    pdf = ZhiHuGenPdf()
    pdf.deal(data['url'],data['title'],data['folder'])
    store.updateUrlState(data['id'])
    return

# if len(sys.argv)>1:
#     print("******")
#     url=sys.argv[1]
#     print(url)
#     folder="面试精选"
#     if len(sys.argv) == 3:
#         folder=sys.argv[2]
#     # 传值生成pdf
#     pdf = GenPdf()
#     title=pdf.deal(url,"",folder)
#     store = StoreData()
#     store.addUrl({'link':url,'folder':folder,'title':title,'msgid':'0','turn':0})
#     store.updateUrlStateByMsg()
# else:
#     getPdf()
    # print(sys.argv[0])



# 处理回答
def dealAnswer(data):
    store = ZhihuStoreData()
    # 传值生成pdf
    pdf = ZhiHuGenPdf()
    pdf.dealAns(data['url'],data['title'],data['folder'])
    store.updateUrlState(data['id'])
    return

# 处理文章
def dealArticle(data):
    store = ZhihuStoreData()
    # 传值生成pdf
    pdf = ZhiHuGenPdf()
    pdf.deal(data['url'],data['title'],data['folder'])
    store.updateUrlState(data['id'])
    return

getPdf()    