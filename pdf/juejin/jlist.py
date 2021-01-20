# -*- coding=utf-8 -*-
import requests
import json
import time
import sys
from bs4 import BeautifulSoup
# from juejin.jstore import JuejinStoreData
from juejin.jstore import JuejinStoreData
import operator
from itertools import groupby


#  获取知乎文章列表 支持个人收藏夹  文章列表

def deal(url):
    store = JuejinStoreData()
    # 根据不同的 url 关键字采用不同的方法
    # column 专栏
    # collections 某人所有收藏夹
    # collection 某个收藏夹 分为公开的和私有的 
    ret={}
    if url.find("posts") > -1:
        ret = dealList(url)
    if url.find("collection") > -1:
        ret = dealPublicFav(url) # 处理收藏夹
    # 存储链接
    store.addAblum(url, "", ret['title'])
    sdata = CleanResult(ret['result'], ret['title'])
    # print(sdata)
    # 循环数据写入 sql 
    print(ret['title'])
    if len(sdata)>0:
        for val in sdata:
            # print("*-*-*-*-*-*-*")
            # print(val)
            store.addUrl(val)
    return


# 处理某人文章
def dealList(url):
    # 从页面获取专栏名
    # title=getPageName(url) # folder archive 
    # print(title)
    user_id = url.split("/")[-2]
    api_url = "https://api.juejin.cn/content_api/v1/article/query_list"
    result=[]
    for i in range (100):
        time.sleep(1)
        offset = 10*i
        param = {"user_id": user_id, "sort_type": 2, "cursor": str(offset)}
        data = getJsonFromApi(api_url, param)
        result+=data
        if len(data)<10:
            break
    
    # print(result)
    # sys.exit(0)
    return {"title": result[0]['user'], "result":result}


def getJsonFromApi(url, param):
    s = requests.Session()
    # 通过抓包或chrome开发者工具分析得到登录的请求头信息,
    headers = {
        'authority': 'api.juejin.cn',
        'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        'content-type': 'application/json',
        'accept': '*/*',
        'origin': 'https://juejin.cn',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://juejin.cn/',
        'accept-language': 'zh-CN,zh;q=0.9',
    }
    print(url)
    # print(param)
    # 开始登录
    r = s.post(url = url, data = json.dumps(param), headers = headers)
    # print(r)
    ret=[]
    data = json.loads(r.text)
    # print(data)
    # print(type(data['data']))
    if len(data['data'])>0:
        for j in range(len(data['data'])):
            # print("*****")
            # print(data)
            # print(data['data'][j]['title'])
            ret.append({"url":"https://juejin.cn/post/"+data['data'][j]['article_info']['article_id'], 
                "title":data['data'][j]['article_info']['title'], 
                "msgid":data['data'][j]['article_info']['article_id'], 
                "user":data['data'][j]['author_user_info']['user_name'], 
                "type":data['data'][j]['category']['category_name'], 
                "created":data['data'][j]['article_info']['ctime'], 
                "updated":data['data'][j]['article_info']['mtime'] 
            })

    return ret
    # print(data)



def dealPraivateFav(url):
    
    return

# 处理收藏夹
def dealPublicFav(url):
    # 从页面获取专栏名
    # title=getPageName(url) # folder archive 
    # print(title)
    tag_id = url.split("/")[-1]
    api_url = "https://api.juejin.cn/interact_api/v1/collectionSet/get?tag_id=" + tag_id
    result=[]
    for i in range (100):
        time.sleep(1)
        offset = 10*i
        data = getFavJsonFromApi(api_url + "&cursor=" + str(offset))
        result+=data
        if len(data)<10:
            break
    
    # print(result)
    # sys.exit(0)
    return {"title": result[0]['user'], "result":result}


def getFavJsonFromApi(url):
    s = requests.Session()
    # 通过抓包或chrome开发者工具分析得到登录的请求头信息,
    headers = {
        'authority': 'api.juejin.cn',
        'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        'content-type': 'application/json',
        'accept': '*/*',
        'origin': 'https://juejin.cn',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://juejin.cn/',
        'accept-language': 'zh-CN,zh;q=0.9',
    }
    print(url)
    r = s.get(url = url, headers = headers)
    # print(r)
    ret=[]
    data = json.loads(r.text)
    # print(data)
    # print(type(data['data']['article_list']))
    if len(data['data']['article_list'])>0:
        dlist = data['data']['article_list']
        tag = data['data']['detail']['tag_name']
        tag_user = data['data']['create_user']['user_name']
        for j in range(len(dlist)):
            # print("*****")
            # print(data)
            # print(dlist[j]['title'])
            ret.append({"url":"https://juejin.cn/post/"+dlist[j]['article_info']['article_id'], 
                "title":dlist[j]['article_info']['title'], 
                "msgid":dlist[j]['article_info']['article_id'], 
                "user":dlist[j]['author_user_info']['user_name'], 
                "type":dlist[j]['category']['category_name'], 
                "created":dlist[j]['article_info']['ctime'], 
                "updated":dlist[j]['article_info']['mtime'],
                "co_folder_pre": tag_user + "-" + tag
            })

    return ret

# 处理结果
def CleanResult(data, title):
    # 根据 msgid 生成序号
    # print(data)
    # 去重
    # data = distinct(data,"title")
    # sdata = sorted(data, key=operator.itemgetter("msgid"))
    # print(data)
    for i in range(len(data)):
        if 'co_folder_pre' in data[i]:
            data[i]['folder'] = data[i]['co_folder_pre']
        else:
            data[i]['folder'] = title

        data[i]['archive'] = (data[i]['archive'] if data[i].__contains__('archive') else title)
    
    return data

def distinct(items,key):
    key = operator.itemgetter(key)
    items = sorted(items, key=key)
    return [next(v) for _, v in groupby(items, key=key)]
# dealList("https://www.zhihu.com/column/c_1284243649199472640")

# dealPublicFav("https://www.zhihu.com/collection/195406199")

# deal(sys.argv[1]) 