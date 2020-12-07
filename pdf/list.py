#  获取文章列表 生成指定格式数据
#  暂时写入文件

import requests
import os
from bs4 import BeautifulSoup
import json
import operator
from itertools import groupby
from db.mysqlite import simpleToolSql
from store import StoreData

'''
begin_msgid   页面最后一个
begin_itemidx  要获取的下一个 

curl --location --request GET 'https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&__biz=MzI4MzUxNjI3OA==&album_id=1506626428400877572&begin_msgid=2247484692&begin_itemidx=1&count=20&__biz=MzI4MzUxNjI3OA%3D%3D&x5=0&f=json' \
--header 'authority:  mp.weixin.qq.com' \
--header 'user-agent:  Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36' \
--header 'x-requested-with:  XMLHttpRequest' \
--header 'accept:  */*' \
--header 'sec-fetch-site:  same-origin' \
--header 'sec-fetch-mode:  cors' \
--header 'sec-fetch-dest:  empty' \
--header 'referer:  https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzI4MzUxNjI3OA==&action=getalbum&album_id=1506626428400877572&scene=173&from_msgid=2247485899&from_itemidx=1&count=3' \
--header 'accept-language:  zh-CN,zh;q=0.9'

'''

def deal(url):
    
    ret1=getFirstPage(url)
    # print(ret1)
    ret = ret1['result']
    author = ret1['author']
    title = ret1['title'].replace("#",'')
    minid = max(ret1['msgid'])
    # print(minid)
    ret2=getJsonData(url, minid)
    # print("****")
    # print(ret2)
    ret+=ret2['result']
    minid = max(ret2['msgid'])
    while len(ret2['result'])==10:
        ret2=getJsonData(url, minid)
        ret+=ret2['result']
        minid = max(ret2['msgid'])
    
    sdata=CleanResult(ret,author,title)
    # print(sdata)
    store = StoreData()
    for val in sdata:
        store.addUrl(val)
    return sdata

# 处理 url 获取参数
def dealUrl(url: str):
    ll = url.split("?")[1]
    ll1 = ll.split("#")[0]
    ldic = ll1.split("&")
    param={}
    for val in ldic:
        wdic = val.split('=')
        param[wdic[0]] = wdic[1]
    
    return param

# 获取第一页页面内容
def getFirstPage(url):
    res = requests.get(url)
    # data-src替换为src 有时候返回的正文被隐藏了，将hidden去掉
    html = res.text.replace("data-src", "src").replace('style="visibility: hidden;"',"")

    soup = BeautifulSoup(html)
    # 选择正文（去除javascrapt等）
    # html = soup.select('.album__content')[0]
    # print(html)
    # print("*********")
    # html1 = soup.select('.album__list-item')[-1]
    # print(html1)
    title = soup.select('.album__label-title')[0].string
    author = soup.select('.album__author-name')[0].string
    # print("****")
    # print(title)

    li1 = soup.select('li')
    # print(type(li1))
    # print(len(li1))
    msgid=[]
    link=[]
    for i in range(len(li1)):
        # print(li1[i]['data-msgid'])
        msgid.append(li1[i]['data-msgid'])

        # print(li1[i]['data-link'])
        # print(li1[i]['data-title'])
        # print(li1[i].find_all(class_='js_article_index')[0].string.replace(' ',''))
        turn =li1[i].find_all(class_='js_article_index')[0].string.replace(' ','')
        turn = turn.replace('\t','').replace('.','')
        # link.append({"link":li1[i]['data-link'],"title":li1[i]['data-title'],"turn":turn,"msgid":li1[i]['data-msgid']})
        link.append({"link":li1[i]['data-link'],"title":li1[i]['data-title'],"msgid":li1[i]['data-msgid']})
        # 获取最小的 msgid 提供给 json 请求使用
    return {"result":link,"msgid":msgid,"author":author,"title":title}


# 获取接口内容
def getJsonData(oldurl: str,msgid: int):
    # // 判断等于10个时继续请求 
    s = requests.Session()
    # 登录要请求的地址，
    url = "https://mp.weixin.qq.com/mp/appmsgalbum"
    # 登录所需要的get参数
    # 通过抓包的到需要传递的参数
    param = dealUrl(oldurl)
    data = {
        'action':'getalbum',
        '__biz':param['__biz'],
        'album_id':param['album_id'],
        'begin_msgid':str(msgid),
        'begin_itemidx':'1',
        'count':'10',
        'x5':'0',
        'f':'json'
    }
    # 通过抓包或chrome开发者工具分析得到登录的请求头信息,
    headers = {
        'authority': 'mp.weixin.qq.com',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': oldurl,
        'accept-language': 'zh-CN,zh;q=0.9'
    }
    # 开始登录
    r = s.get(url=url, params=data, headers=headers)
    # print(r.text)
    data = json.loads(r.text)
    # print(data)
    art =data['getalbum_resp']['article_list'] # 1 个是是dict 多个 list
    link = []
    msgid = []
    # print(type(art))
    if isinstance(art, dict):
        link.append({"link":art['url'],"title":art['title'],"msgid":art['msgid']})
        msgid.append(art['msgid'])
    elif isinstance(art, list):
        for val in art:
            link.append({"link":val['url'],"title":val['title'],"msgid":val['msgid']})
            msgid.append(val['msgid'])
    
    # print(art['title'])
    # print(art['url'])
    # print(art['msgid'])
    # print(art['itemidx'])
    # return link
    return {"result":link,"msgid":msgid}

# 处理结果
def CleanResult(data,author,title):
    # 根据 msgid 生成序号
    # print(data)
    # 去重
    data = distinct(data,"title")
    sdata = sorted(data, key=operator.itemgetter("msgid"))
    print(len(sdata))
    for i in range(len(sdata)):
        # print("******")
        # print(i)
        # print(sdata[i]['title'])
        sdata[i]['turn'] = i + 1
        sdata[i]['folder'] = author + "/" + title
    
    # print("*****")
    # print(sdata)
    # print("*****")
    # 写入数据库
    return sdata

# 数据库处理
# def StoreData(data):

#功能：list里面的每一个元素都是dict，根据dict某一个key进行去重
#函数1
def distinct(items,key):
    key = operator.itemgetter(key)
    items = sorted(items, key=key)
    return [next(v) for _, v in groupby(items, key=key)]
#函数2
#def distinct(items,key):  
#    mask = (~pd.Series(map(itemgetter(key), items)).duplicated()).tolist()


deal("https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzI4MzUxNjI3OA==&action=getalbum&album_id=1506626428400877572&scene=173&from_msgid=2247485899&from_itemidx=1&count=3#wechat_redirect")

# deal("https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MjM5NzE2NTY0Ng==&action=getalbum&album_id=1337228928003686401&scene=173&from_msgid=2650679816&from_itemidx=1&count=3#wechat_redirect")
# getJsonData("",1)