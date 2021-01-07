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

    # print(toPdfList)
    # print(columns)
    # print(type(toPdfList))
    # 修改状态
    data = []
    i=0
    for val in toPdfList:
        dic = {}
        for key,name in enumerate(columns):
            dic[name] = val[key]
        genpdf(dic)
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

getPdf()

# 处理回答
def dealAnswer():
    return

# 处理文章
def dealArticle():
    return