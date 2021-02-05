# -*- coding=utf-8 -*-

# 知乎文章下载

from zhihu.zstore import ZhihuStoreData
import time
import sys
from zhihu.zmypdf import ZhiHuGenPdf


def getPdf():
    store = ZhihuStoreData()
    # 查数据库
    toPdfList, columns = store.getListFromParam('state=0')

    # 修改状态
    data = []
    # i=0
    for val in toPdfList:
        dic = {}
        for key, name in enumerate(columns):
            dic[name] = val[key]
        if dic["type"] == "article":
            # genpdf(dic)
            dealArticle(dic)
        elif dic["type"] == "answer":
            dealAnswer(dic)

        data.append(dic)
        # i+=1
        # if i%5==0:
        # break
    # print(data)
    return


def genpdf(data):
    store = ZhihuStoreData()
    # 传值生成pdf
    pdf = ZhiHuGenPdf()
    pdf.deal(data['url'], data['title'], data['folder'])
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
    # 接收返回完整数据
    ret = pdf.dealAns(data['url'], data['title'], data['folder'])
    # 判断 没有 id 直接写入
    if data.__contains__('id'):
        store.updateUrlState(data['id'])
    else:
        # 无数据
        store.addUrl(ret)
    return


# 处理文章
def dealArticle(data):
    store = ZhihuStoreData()
    # 传值生成pdf
    pdf = ZhiHuGenPdf()
    ret = pdf.deal(data['url'], data['title'], data['folder'])
    # 判断 没有 id 直接写入
    if data.__contains__('id'):
        store.updateUrlState(data['id'])
    else:
        # 无数据
        store.addUrl(ret)
    return


# getPdf()


def zhPdf(**kwargs):
    # print(kwargs)
    # print(kwargs['url'])
    # return
    if len(kwargs) > 0:
        print("******")
        url = kwargs['url']
        print(url)
        if url == "zhihu":
            getPdf()
        else:
            if url.find('answer') > -1:
                dealAnswer({"url":url,"title":'', 'folder':kwargs['folder']})
            else:
                dealArticle({"url":url,"title":'', 'folder':kwargs['folder']})
    else:
        getPdf()
        # print(sys.argv[0])