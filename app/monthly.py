import urllib
import urllib3
import urllib.request
import re

class Spider:

    def __init__(self):
        self.siteURL = 'http://mysql.taobao.org/monthly/'

    def getPage(self,pageIndex):
        url = self.siteURL
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        # print(response.read().decode('utf-8'))
        return response.read().decode('utf-8')

    def getContents(self,pageIndex):
        page = self.getPage(pageIndex)
        # pattern = re.compile('<div class="list-item".*?pic-word.*?<a href="(.*?)".*?![]((.*?))(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>',re.S)
        pattern = re.compile('<li><h3><a target="_top" class="main" href="(.*?)">',re.S)
        # <li><h3><a target="_top" class="main" href="/monthly/2020/06">
        #       数据库内核月报 － 2020/06
        #     </a></h3></li>
        items = re.findall(pattern,page)
        # print(items)
        # for item in items:
        #     print(item)

        return items

    def getContents2(self,pageIndex):
        items = self.getContents(pageIndex)
        for item in items:
            url = "http://mysql.taobao.org" + item + "/"
            # print(url)

            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            page = response.read().decode('utf-8')
            # print(page)
            pattern = re.compile('<li>.*?<h3>.*?<small class="datetime muted" data-time=".*?</small>.*?<a href="(.*?)" target="_blank">',re.S)
            
            nitems = re.findall(pattern,page)
            # print(nitems)
            for nitem in nitems:
                print("http://mysql.taobao.org" + nitem)

# <li>
#   <h3>
#     <small class="datetime muted" data-time="2019-07-08 00:00:00 +0800"># 08 </small>
#     <a href="/monthly/2019/07/08/" target="_blank">

spider = Spider()
spider.getContents2(1)