# -*- coding=utf-8 -*-

# 知乎文章下载

from juejin.jmypdf import JuejinGenPdf
from juejin.jstore import JuejinStoreData


def getPdf():
    store = JuejinStoreData()
    # 查数据库
    toPdfList, columns = store.getListFromParam('state=0')

    # 修改状态
    data = []
    # i=0
    for val in toPdfList:
        dic = {}
        for key, name in enumerate(columns):
            dic[name] = val[key]

        genpdf(dic)
        data.append(dic)
        # i+=1
        # if i%5==0:
        #     break
    # print(data)
    return


def genpdf(data):
    store = JuejinStoreData()
    # 传值生成pdf
    pdf = JuejinGenPdf()
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

# getPdf()


def jjPdf(**kwargs):
    # print(kwargs)
    # print(kwargs['url'])
    # return
    if len(kwargs) > 0:
        print("******")
        url = kwargs['url']
        print(url)
        if url == "juejin":
            getPdf()
        else:
            #     print(url)
            folder = "面试精选"
            if len(kwargs) == 2:
                folder = kwargs['folder']
            # 传值生成pdf
            pdf = JuejinGenPdf()
            title = pdf.deal(url, "", folder)
            store = JuejinStoreData()
            store.addUrl({
                'url': url,
                'folder': folder,
                'title': title,
                'msgid': '0',
                'archive': folder,
                "type": '单篇文章',
                'created':0,
                'updated':0
            })
            store.updateUrlStateByMsg()
    else:
        getPdf()
        # print(sys.argv[0])
