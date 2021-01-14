from zhihu import zgetPdf
from zhihu import zlist
from wechat import getPdf
from wechat import list
import sys


# zgetPdf.getPdf()

def deal(url):
    if url.find("zhihu") > -1:
        if url.find("collection") > 1 or url.find("column") > 1:
            zlist.deal(url)
        else:
            zgetPdf.getPdf()
    elif url.find("weixin") > -1:
        if url.find('appmsgalbum') > -1:
            list.deal(url)
        else:
            getPdf.getPdf()
    return


deal(sys.argv[1])
