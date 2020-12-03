#  获取文章列表 生成指定格式数据
#  暂时写入文件

import requests
import os
from bs4 import BeautifulSoup
import json
import math

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
    print(ret1)
    minid = min(ret1['msgid'])
    print(minid)
    getJsonData(url, minid)


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
        print(li1[i].find_all(class_='js_article_index')[0].string.replace(' ',''))
        turn =li1[i].find_all(class_='js_article_index')[0].string.replace(' ','')
        turn = turn.replace('\t','').replace('.','')
        link.append({"link":li1[i]['data-link'],"title":li1[i]['data-title'],"turn":turn})
        # 获取最小的 msgid 提供给 json 请求使用
    return {"result":link,"msgid":msgid}



# class GetList:
#     def getList(self):
#         return 





def getJsonData(url: str,msgid: int):
    # // 判断等于10个时继续请求 
    s = requests.Session()
    # 登录要请求的地址，
    url = "https://mp.weixin.qq.com/mp/appmsgalbum"
    # 登录所需要的get参数
    # 通过抓包的到需要传递的参数
    data = {
        'action':'getalbum',
        '__biz':'MzI4MzUxNjI3OA==',
        'album_id':'1506626428400877572',
        'begin_msgid':'2247484692',
        'begin_itemidx':'1',
        'count':'50',
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
        'referer': 'https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzI4MzUxNjI3OA==&action=getalbum&album_id=1506626428400877572&scene=173&from_msgid=2247485899&from_itemidx=1&count=3',
        'accept-language': 'zh-CN,zh;q=0.9'
    }
    # 开始登录
    r = s.get(url=url, params=data, headers=headers)
    # print(r.text)
    data = json.loads(r.text)
    art =data['getalbum_resp']['article_list']
    print(type(art))

    print(art['title'])
    print(art['url'])
    print(art['msgid'])
    print(art['itemidx'])


# getFirstPage("https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzI4MzUxNjI3OA==&action=getalbum&album_id=1506626428400877572&scene=173&from_msgid=2247485899&from_itemidx=1&count=3#wechat_redirect")
deal("https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzI4MzUxNjI3OA==&action=getalbum&album_id=1506626428400877572&scene=173&from_msgid=2247485899&from_itemidx=1&count=3#wechat_redirect")

# getJsonData("",1)