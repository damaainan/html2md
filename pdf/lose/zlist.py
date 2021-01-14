# -*- coding=utf-8 -*-
import requests
import json
import time
import sys
from bs4 import BeautifulSoup
from zstore import ZhihuStoreData
import operator
from itertools import groupby


#  获取知乎文章列表 支持个人收藏夹  文章列表

def deal(url):
    store = ZhihuStoreData()
    # 根据不同的 url 关键字采用不同的方法
    # column 专栏
    # collections 某人所有收藏夹
    # collection 某个收藏夹 分为公开的和私有的 
    if url.find("column") > -1:
        ret = dealList(url)
    if url.find("collection") > -1:
        ret = dealPublicFav(url)
    # 存储链接
    store.addAblum(url, "", ret['title'])
    sdata = CleanResult(ret['result'], ret['title'])
    # 循环数据写入 sql 
    print(ret['title'])
    if len(sdata)>0:
        for val in sdata:
            print("*-*-*-*-*-*-*")
            print(val)
            store.addUrl(val)
    return


# 处理专栏
def dealList(url):
    # 从页面获取专栏名
    title=getPageName(url) # folder archive 
    # print(title)
    flag=url.split("/")[-1]
    api_url="https://www.zhihu.com/api/v4/columns/"+flag+"/items?limit=10"
    result=[]
    for i in range (100):
        time.sleep(1)
        offset = 10*i
        nurl=api_url+"&offset="+str(offset)
        data=getJsonFromApi(nurl)
        result+=data
        if len(data)<10:
            break
    
    # print(result)
    return {"title":title,"result":result}

# 获取第一页页面内容
def getPageName(url):
    headers={
        'authority': 'www.zhihu.com' ,
        'cache-control': 'max-age=0' ,
        'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"' ,
        'sec-ch-ua-mobile': '?0' ,
        'upgrade-insecure-requests': '1' ,
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36' ,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' ,
        'sec-fetch-site': 'none' ,
        'sec-fetch-mode': 'navigate' ,
        'sec-fetch-user': '?1' ,
        'sec-fetch-dest': 'document' ,
        'accept-language': 'zh-CN,zh;q=0.9' ,

    }

    res = requests.get(url=url, headers=headers)
    # # data-src替换为src 有时候返回的正文被隐藏了，将hidden去掉
    html = res.text

    # pdf = GenPdf()
    # htmlstr=pdf.getHTMLText(url)
    # html = htmlstr.replace("data-src", "src").replace('style="visibility: hidden;"',"")
    # print(html) 
    soup = BeautifulSoup(html, features="lxml")
    # 判断是否完整列表
    title=soup.select('.ColumnPageHeader-TitleColumn')[0].string
    # print(title)
    return title

def getJsonFromApi(url):
    s = requests.Session()
    # 通过抓包或chrome开发者工具分析得到登录的请求头信息,
    headers = {
        'authority': 'www.zhihu.com',
        'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'zh-CN,zh;q=0.9',
    }
    print(url)
    # 开始登录
    r = s.get(url=url, headers=headers)
    # print(r)
    ret=[]
    data = json.loads(r.text)
    if len(data['data'])>0:
        for j in range(len(data['data'])):
            # print("*****")
            # print(data['data'][j]['url'])
            # print(data['data'][j]['title'])
            ret.append({"url":data['data'][j]['url'], 
                "title":data['data'][j]['title'], 
                "type":data['data'][j]['type'], 
                "msgid":data['data'][j]['id'], 
                "created":data['data'][j]['created'], 
                "updated":data['data'][j]['updated'] 
            })

    return ret
    # print(data)



def dealPraivateFav(url):
    
    return

# 处理收藏夹
def dealPublicFav(url):
    # 从页面获取专栏名
    title=getFavPageName(url)
    # print("my_"+title)
    flag=url.split("/")[-1]
    api_url="https://www.zhihu.com/api/v4/collections/"+flag+"/items?limit=20"
    result=[]
    # p=1
    for i in range (100):
        time.sleep(1)
        offset = 20*i
        nurl=api_url+"&offset="+str(offset)
        data=getFavJsonFromApi(nurl)
        result+=data
        # if p==2:
        #     break
        # p+=1
        # break
        # if len(data)<20:
        #     break
    
    # print(result)
    return {"title":"my"+title,"result":result}

# 获取第一页页面内容
def getFavPageName(url):
    headers={
        'authority': 'www.zhihu.com' ,
        'cache-control': 'max-age=0' ,
        'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"' ,
        'sec-ch-ua-mobile': '?0' ,
        'upgrade-insecure-requests': '1' ,
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36' ,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' ,
        'sec-fetch-site': 'none' ,
        'sec-fetch-mode': 'navigate' ,
        'sec-fetch-user': '?1' ,
        'sec-fetch-dest': 'document' ,
        'accept-language': 'zh-CN,zh;q=0.9' ,

    }

    res = requests.get(url=url, headers=headers)
    # # data-src替换为src 有时候返回的正文被隐藏了，将hidden去掉
    html = res.text

    # pdf = GenPdf()
    # htmlstr=pdf.getHTMLText(url)
    # html = htmlstr.replace("data-src", "src").replace('style="visibility: hidden;"',"")
    # print(html) 
    soup = BeautifulSoup(html, features="lxml")
    # 判断是否完整列表
    title=soup.select('.CollectionDetailPageHeader-title')[0].string
    # print(title)
    return title

def getFavJsonFromApi(url):
    s = requests.Session()
    # 通过抓包或chrome开发者工具分析得到登录的请求头信息,
    headers = {
        'authority': 'www.zhihu.com',
        'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'zh-CN,zh;q=0.9',
    }
    print(url)
    # 开始登录
    r = s.get(url=url, headers=headers)
    # print(r)
    ret=[]
    data = json.loads(r.text)
    if len(data['data'])>0:
        for j in range(len(data['data'])):
            # 获取 archive
            if data['data'][j]['content'].__contains__('column'):
                archive=data['data'][j]['content']['column']['title']  # TODO 乱码问题
            elif data['data'][j]['content'].__contains__('question'):
                archive=data['data'][j]['content']['question']['title']
            else:
                archive="单文章"

            if data['data'][j]['content']['title'] == "":
                title=archive
            else:
                title=data['data'][j]['content']['title']
            # print("*****")
            # print(data['data'][j]['url'])
            # print(data['data'][j]['title'])
            ret.append({"url":data['data'][j]['content']['url'], 
                "title":title, 
                "msgid":data['data'][j]['content']['id'], 
                "type":data['data'][j]['content']['type'], 
                "created":(data['data'][j]['content']['created'] if data['data'][j]['content'].__contains__('created') else data['data'][j]['content']['created_time']), 
                "updated":(data['data'][j]['content']['updated'] if data['data'][j]['content'].__contains__('updated') else data['data'][j]['content']['updated_time']),  
                "archive":archive
            })

    return ret
    # print(data)

# 处理结果
def CleanResult(data, title):
    # 根据 msgid 生成序号
    # print(data)
    # 去重
    # data = distinct(data,"title")
    # sdata = sorted(data, key=operator.itemgetter("msgid"))
    # print(len(data))
    for i in range(len(data)):
        data[i]['folder'] = title
        data[i]['archive'] = (data[i]['archive'] if data[i].__contains__('archive') else title)
    
    return data

def distinct(items,key):
    key = operator.itemgetter(key)
    items = sorted(items, key=key)
    return [next(v) for _, v in groupby(items, key=key)]
# dealList("https://www.zhihu.com/column/c_1284243649199472640")

# dealPublicFav("https://www.zhihu.com/collection/195406199")

deal(sys.argv[1]) 