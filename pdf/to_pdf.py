import time
from zhihu import zgetPdf
from zhihu import zlist
from zhihu import zstore
from wechat import getPdf
from wechat import store
from wechat import list as wList
from bili import list as bList
from juejin import jgetPdf
from juejin import jlist
from juejin import jstore
import sys

# zgetPdf.getPdf()


def dealAll(**kwargs):
    url = kwargs['url']
    if url.find("zhihu") > -1:
        if url.find("collection") > 1 or url.find("column") > 1:
            zlist.deal(url)
        else:
            # zgetPdf.zhPdf(url=url)
            if len(kwargs) > 1:
                folder = kwargs['folder']
                zgetPdf.zhPdf(url=url, folder=folder)
            else:
                zgetPdf.zhPdf(url=url)
    elif url.find("weixin") > -1:
        if url.find('appmsgalbum') > -1 or url.find("homepage") > -1:
            wList.deal(url)
        else:
            # getPdf.wxPdf(url=url)
            if len(kwargs) > 1:
                folder = kwargs['folder']
                getPdf.wxPdf(url=url, folder=folder)
            else:
                getPdf.wxPdf(url=url)
                # zgetPdf.zhPdf(url=url)
    elif url.find("bilibili") > -1:
        bList.deal(url)

    elif url.find("juejin") > -1:
        if url.find("collection") > 1 or url.find('posts') > -1:
            jlist.deal(url)
        else:
            # jgetPdf.jjPdf(url=url)
            if len(kwargs) > 1:
                folder = kwargs['folder']
                jgetPdf.jjPdf(url=url, folder=folder)
            else:
                jgetPdf.jjPdf(url=url)
    return


if len(sys.argv) > 1:
    if len(sys.argv) == 3:
        dealAll(url=sys.argv[1], folder=sys.argv[2])
    elif len(sys.argv) == 2:
        dealAll(url=sys.argv[1])
    # else:
    #     dealAll(url=sys.argv[1], folder=sys.argv[2], title=sys.argv[3])
else:
    print(sys.argv)
    # 查询已有list 更新 url 微信 知乎
    store = store.StoreData()
    li = store.getAblums()
    for i in li:
        print(i[0], "===", i[2])
        wList.deal(i[1])
        time.sleep(2)

    zStore = zstore.ZhihuStoreData()
    li = zStore.getAblums()
    for i in li:
        print(i[2])
        zlist.deal(i[1])
        time.sleep(2)

    jStore = jstore.JuejinStoreData()
    li = jStore.getAblums()
    for i in li:
        print(i[2])
        jlist.deal(i[1])
        time.sleep(2)
