# -*- coding=utf-8 -*-

from wechat.store import StoreData
import sys
from wechat.mypdf import GenPdf


def getPdf():
    mystore = StoreData()
    # 查数据库
    toPdfList, columns = mystore.getListFromParam('state=0')

    # print(toPdfList)
    # print(columns)
    # print(type(toPdfList))
    # 修改状态
    data = []
    i = 0
    for val in toPdfList:
        dic = {}
        for key, name in enumerate(columns):
            # print(key)
            # print(name)
            # print(val[key])
            dic[name] = val[key]
        genpdf(dic)
        data.append(dic)
        i += 1
        if i == 100:
            break
    # print(data)
    return


def genpdf(data):
    mystore = StoreData()
    # 传值生成pdf
    mypdf = GenPdf()
    mypdf.dealHtml(data['url'], str(data['turn']) + '-' + data['title'], data['folder'])
    mystore.updateUrlState(data['id'])
    return


if len(sys.argv) > 1:
    print("******")
    url = sys.argv[1]
    print(url)
    folder = "面试精选"
    if len(sys.argv) == 3:
        folder = sys.argv[2]
    # 传值生成pdf
    pdf = GenPdf()
    title = pdf.dealHtml(url, "", folder)
    store = StoreData()
    store.addUrl({'link': url, 'folder': folder, 'title': title, 'msgid': '0', 'turn': 0})
    store.updateUrlStateByMsg()
else:
    getPdf()
    # print(sys.argv[0])
