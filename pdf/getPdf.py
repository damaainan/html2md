# -*- coding=utf-8 -*-

from store import StoreData
import time
from mypdf import GenPdf

def getPdf():
    store = StoreData()
    # 查数据库
    toPdfList, columns = store.getListFromParam('state=0')

    # print(toPdfList)
    # print(columns)
    # print(type(toPdfList))
    # 修改状态
    data = []
    i=1
    for val in toPdfList:
        dic = {}
        for key,name in enumerate(columns):
            # print(key)
            # print(name)
            # print(val[key])
            dic[name] = val[key]
        genpdf(dic)
        data.append(dic)
        i+=1
        if i==20:
            break
    # print(data)
    return

def genpdf(data):
    store = StoreData()
    # 传值生成pdf
    pdf = GenPdf()
    pdf.deal(data['url'],str(data['turn']) + '-' + data['title'],data['folder'])
    store.updateUrlState(data['id'])
    return


getPdf()