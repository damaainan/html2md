# -*- coding=utf-8 -*-

#  获取文章列表 生成指定格式数据
#  暂时写入文件

import requests
from bs4 import BeautifulSoup
import json
import operator
from itertools import groupby
from termcolor import colored, cprint

def deal(url):
    # 如果 homepage 采用另外的方法
    if url.find("space") > -1:
        ret1 = dealHome(url)
    else:
        ret1 = getJsonData(url)
    
    # print(ret1)
    # print(ret1['result'])
    writeScript(ret1['result'])
    # 生成文件
    return ret1['result']

def dealHome(url):
    if url.find("channel") > -1:
        return dealChannel(url)
    ret2 = getHomeJsonData(url, 1)
    print("****")
    # print(ret2)
    ret = []
    if len(ret2['result']) > 0:
        ret = ret2['result']

    page = 2
    while len(ret2['result']) == 30:
        ret2 = getHomeJsonData(url, page)
        if len(ret2['result']) == 0:
            continue
        ret += ret2['result']
        page=page+1

    # print(ret)
    return {"result": ret}

# 获取接口内容
def getHomeJsonData(oldurl: str, page: int):
    # // 判断等于10个时继续请求
    s = requests.Session()
    # 登录要请求的地址，
    url = "https://api.bilibili.com/x/space/arc/search"
    # 登录所需要的get参数
    # 通过抓包的到需要传递的参数
    param = dealUrl(oldurl)
    data = {
        'mid':param['mid'],
        'ps':30,
        'tid':param['tid'],
        'pn':page,
        'order':'pubdate',
        'jsonp':'jsonp',
    }
    # 通过抓包或chrome开发者工具分析得到登录的请求头信息,
    headers = {
        'authority': 'api.bilibili.com' ,
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"' ,
        'accept': 'application/json, text/plain, */*' ,
        'sec-ch-ua-mobile': '?0' ,
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36' ,
        'origin': 'https://space.bilibili.com' ,
        'sec-fetch-site': 'same-site' ,
        'sec-fetch-mode': 'cors' ,
        'sec-fetch-dest': 'empty' ,
        'referer': 'https://space.bilibili.com/567195437/video?tid=0&page=2&keyword=&order=pubdate' ,
        'accept-language': 'zh-CN,zh;q=0.9' 
    }
    # 开始登录
    r = s.get(url=url, params=data, headers=headers)
    # print(data)
    # print(r.text)
    data = json.loads(r.text)
    link = []
    if "list" in data['data'].keys():
        art = data['data']['list']['vlist']  # 1 个是是dict 多个 list

        for val in art:
            link.append(
                {"link": 'https://www.bilibili.com/video/' + val['bvid'], "title": val['title']})

    return {"result": link}


def dealChannel(url):
    ret2 = getChannelJsonData(url, 1)
    print("****")
    # print(ret2)
    ret = []
    if len(ret2['result']) > 0:
        ret = ret2['result']

    page = 2
    while len(ret2['result']) == 30:
        ret2 = getChannelJsonData(url, page)
        if len(ret2['result']) == 0:
            continue
        ret += ret2['result']
        page=page+1

    # print(ret)
    return {"result": ret}
# https://api.bilibili.com/x/space/channel/video?mid=326749661&cid=61588&pn=4&ps=30&order=0&ctype=0&jsonp=jsonp&callback=__jp9



# 获取接口内容
def getChannelJsonData(oldurl: str, page: int):
    # // 判断等于10个时继续请求
    s = requests.Session()
    # 登录要请求的地址，
    url = "https://api.bilibili.com/x/space/channel/video"
    # 登录所需要的get参数
    # 通过抓包的到需要传递的参数
    param = dealUrl(oldurl)
    data = {
        'mid': param['mid'],
        'cid': param['cid'],
        'pn': page,
        'ps': 30,
        'order': param['order'],
        'ctype': param['ctype'],
        'jsonp': param['jsonp'],
        'callback': param['callback'],
    }
    # 通过抓包或chrome开发者工具分析得到登录的请求头信息,
    headers = {
        'authority': 'api.bilibili.com' ,
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"' ,
        'accept': 'application/json, text/plain, */*' ,
        'sec-ch-ua-mobile': '?0' ,
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36' ,
        'sec-fetch-site': 'same-site' ,
        'sec-fetch-mode': 'cors' ,
        'sec-fetch-dest': 'empty' ,
        'referer': 'https://space.bilibili.com/326749661/channel/detail?cid=61588&ctype=0' ,
        'accept-language': 'zh-CN,zh;q=0.9' 
    }
    # 开始登录
    r = s.get(url=url, params=data, headers=headers)
    # print(data)
    # print(r.text)
    data = json.loads(r.text)
    link = []
    if "list" in data['data'].keys():
        art = data['data']['list']['archives']  # 1 个是是dict 多个 list

        for val in art:
            link.append(
                {"link": 'https://www.bilibili.com/video/' + val['bvid'], "title": val['title']})

    return {"result": link}




# 获取接口内容
def getJsonData(oldurl: str):
    # // 判断等于10个时继续请求
    s = requests.Session()
    # 登录要请求的地址，
    url = "https://api.bilibili.com/x/player/pagelist"
    # 登录所需要的get参数
    # 通过抓包的到需要传递的参数
    data = {
        'bvid':oldurl.split("/")[-1],
        'jsonp':'jsonp',
    }
    # 通过抓包或chrome开发者工具分析得到登录的请求头信息,
    headers = {
        'authority': 'api.bilibili.com' ,
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"' ,
        'accept': 'application/json, text/plain, */*' ,
        'sec-ch-ua-mobile': '?0' ,
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36' ,
        'origin': 'https://www.bilibili.com' ,
        'sec-fetch-site': 'same-site' ,
        'sec-fetch-mode': 'cors' ,
        'sec-fetch-dest': 'empty' ,
        'referer': oldurl ,
        'accept-language': 'zh-CN,zh;q=0.9' 
    }
    # 开始登录
    r = s.get(url=url, params=data, headers=headers)
    # print(url)
    # print(data)
    # print(r.text)
    data = json.loads(r.text)
    link = []
    # print(data)
    art = data['data']  # 1 个是是dict 多个 list
    if isinstance(art, dict):
        link.append(
            {"link": oldurl + '?p=' + str(art['page']), "title": art['part']})
    elif isinstance(art, list):
        for val in art:
            link.append(
                {"link": oldurl + '?p=' + str(val['page']), "title": val['part']})

    return {"result": link}

# 功能：list里面的每一个元素都是dict，根据dict某一个key进行去重
# 函数1

def distinct(items, key):
    key = operator.itemgetter(key)
    items = sorted(items, key=key)
    return [next(v) for _, v in groupby(items, key=key)]

# 处理 url 获取参数
def dealUrl(url: str):
    ll = url.split("?")[1]
    ll1 = ll.split("#")[0]
    ldic = ll1.split("&")
    param = {}
    for val in ldic:
        wdic = val.split('=')
        # print("-*-*-*-")
        # print(wdic[1:])
        wdic_ = map(lambda x: [x, '='][x == ''], wdic[1:])
        param[wdic[0]] = ''.join(wdic_)

    return param

def writeScript(data):
    str1 = ""
    str2 = ""
    for val in data:
        title=val['title']
        print(title)
        title = title.replace('?', '？').replace(' ', '').replace(':', '：').replace('*', '＊').replace('amp;', '').replace('/','')
        print(colored(title, "cyan"))
        str1 = str1 + 'you-get --format=dash-flv720 -O "' + title + '" "' + val['link'] + '"\n'
        str2 = str2 + 'F:/bin/ffmpeg/bin/ffmpeg.exe -i "' + title + '[00].mp4" -i "' + title + '[01].mp4" -vcodec copy -acodec copy "' + title + '.mp4"' + "\n"
    with open('./bi.sh', mode='a') as filename:
        filename.write(str1)
        filename.write('\n\n') # 换行
        filename.write(str2)
        filename.write('\n\n') # 换行
        filename.write('# *=*=**=*=**=*=**==*=*=**=*==*\n\n\n') # 换行
