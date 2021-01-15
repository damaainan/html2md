import time
from zhihu import zgetPdf
from zhihu import zlist
from zhihu import zstore
from wechat import getPdf
from wechat import store
from wechat import list as wList
import sys


# zgetPdf.getPdf()

def dealAll(url):
    # url=args[0]
    if url.find("zhihu") > -1:
        if url.find("collection") > 1 or url.find("column") > 1:
            zlist.deal(url)
        else:
            zgetPdf.zhPdf(url=url)
    elif url.find("weixin") > -1:
        if url.find('appmsgalbum') > -1:
            wList.deal(url)
        else:
            getPdf.wxPdf(url=url)
    return


if len(sys.argv) > 1:
    dealAll(sys.argv[1]) 
else:
    print(sys.argv)
    # 查询已有list 更新 url 微信 知乎
    store = store.StoreData()
    li = store.getAblums()
    for i in li:
        print(i[2])
        wList.deal(i[1])
        time.sleep(2)

    zStore = zstore.ZhihuStoreData()
    li = zStore.getAblums()
    for i in li:
        print(i[2])
        zlist.deal(i[1])
        time.sleep(2)
