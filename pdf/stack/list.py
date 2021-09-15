# -*- coding=utf-8 -*-

#  获取文章列表 生成指定格式数据
#  暂时写入文件

import requests
from bs4 import BeautifulSoup
import json
import sys
import os
import operator
from itertools import groupby
from termcolor import colored, cprint
from lxml import etree
from lxml import html
from html.parser import HTMLParser  # 导入html解析库

REALPATH = os.path.dirname(
    os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))) + '/out/stack'


def deal(url):

    # 获取列表
    html = getJsonData(url, '')

    ret = getFirstPage(html)
    # print(ret)
    # exit(0)
    # sys.exit(0)
    # print('][][][][][[][[][][]')
    # ret = ret1['result']
    # flag = ret1['flag']
    # author = ret1['author']
    title = ret['title']
    template = ret['html']
    # 循环请求内容

    for data in ret['result']:
        print(data)
        # data = json.loads(datai)
        url = 'https://www.bookstack.cn/' + data['link']
        cont = html = getJsonData(url, 'json')
        # 图片文件 替换为本地
        imghtml = dealImg(cont)

        # 替换核心内容
        template = template.replace('######核心内容######', imghtml)
        # 内容写入文件
        if not os.path.exists("./" + title):
            os.mkdir("./" + title)
        with open("./" + title + "/" + data['title'] + '.html', "w") as fp:
            fp.write(template)
        # exit(0)
    # while len(ret2['result']) == 10:
    # while ret2['continue'] == "1":
    #     ret2 = getJsonData(url, minid)
    #     if len(ret2['result']) == 0:
    #         continue
    #     ret += ret2['result']
    #     print(colored("==============================","cyan"))

    #     minid = ret2['msgid'][-1]

    # return sdata


# 处理图片
def dealImg(html):
    soup = BeautifulSoup(html, features="lxml")
    imgs = soup.select('img')
    # print(imgs)

    imgDict = {}
    for im in range(len(imgs)):
        # print(imgs[im])
        if imgs[im].get('src'):
            src = imgs[im]['src']
            # 处理成本地文件名
            newsrc = getLocalImg(src)
            imgDict[src] = newsrc

    for k in imgDict:
        if imgDict[k] != "":
            image = requests.get(k).content
            with open("./pic/"+imgDict[k], "wb") as fp:
                fp.write(image)

        html = html.replace(k, "./pic/"+imgDict[k])

    return html


def getLocalImg(href):
    # if href.find('http') > -1:
    name = href.split('/')[-1]
    return name
    # return ""


# 获取第一页页面内容
def getFirstPage(ohtml):
    soup = BeautifulSoup(ohtml, features="lxml")
    # 判断是否完整列表
    # liarticle=soup.select('#appmsgList')
    # msgid = []
    link = []
    # 获取书名  公共 样式 写入文件夹

    css_inner = getHtmlByXpath(ohtml, "//style")

    css = getHtmlByXpath(ohtml, "//link/@href")
    # for it in css:
    #     print(it)
    cssret = getLocalCss(css)
    # 集中处理 css 样式 采用公共文件夹管理

    title = soup.select('.book-title')[0].string

    # 拼装公共部分
    head = '''
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
'''
    """
    # 可以修改字体
    font = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
    </head>
    '''
    """

    head = head.format(title=title)
    for cs in cssret:
        # print(len(css[cs].get_text()))
        # print(len(html.tostring(css[cs])))
        # print(type(css[cs].get_text()))
        # font = font + "<style>" + css[cs].get_text() + "</style>"
        head = head + "<link rel='stylesheet' type='text/css' href='" + cssret[
            cs] + "'></link>"
        # HTMLParser().unescape(str1.decode())

    for csi in range(len(css_inner)):
        # print(len(css[cs].get_text()))
        # print(len(html.tostring(css[cs])))
        # print(type(css[cs].get_text()))
        # font = font + "<style>" + css[cs].get_text() + "</style>"
        head = head + "<style>" + HTMLParser().unescape(
            html.tostring(css_inner[csi]).decode()) + "</style></head>"

    # head 替换
    ohead = soup.head
    # print(type(ohead))
    # print(dir(ohead))
    # print(ohead.getText())
    # print(ohead.decode_contents())
    # sys.exit(0)
    ohtml = ohtml.replace(ohead.decode_contents(), head)

    # 标记内容
    page = soup.select('#page-content')[0].get_text()
    ohtml = ohtml.replace(page, '######核心内容######')

    # 返回新的 html 和所有链接

    li1 = soup.select('.article-menu-detail li')

    for i in range(len(li1)):
        url = li1[i].find('a').get('href')
        title = li1[i].find('a').get('title')
        link.append({"link": url, "title": title})

    title = title.replace(' ', '')
    # print(link)
    return {"result": link, 'html': ohtml, 'title': title}


# 获取接口内容
def getJsonData(oldurl: str, types: str):
    # // 判断等于10个时继续请求
    s = requests.Session()
    # 登录要请求的地址，
    url = oldurl
    # 登录所需要的get参数
    # 通过抓包的到需要传递的参数
    # param = dealUrl(oldurl)
    data = {
    }
    # 通过抓包或chrome开发者工具分析得到登录的请求头信息,
    headers = {
        'authority': 'www.bookstack.cn',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': 'iamadmin=true; UM_distinctid=17a378c84732de-09e3b3527d25e2-6518267c-384000-17a378c84747d5; _ga=GA1.2.592178964.1624429595; __gads=ID=8777fc5a889ffd21-22f7815e75ca000b:T=1626861104:RT=1626861104:S=ALNI_MbH1cPeaRsscUHK8cFukC1XGrodAQ; Hm_lvt_227e05b01b8f7eefb29a75df28f53840=1626861102; login=P_-JAwEBDkNvb2tpZVJlbWVtYmVyAf-KAAEDAQhNZW1iZXJJZAEEAAEHQWNjb3VudAEMAAEEVGltZQH_hgAAABD_hQUBAQRUaW1lAf-GAAAAJP-KAf5cFAEKanVueXVhbjgwMgEPAQAAAA7YjWuMNe64aQHgAA==|1627092108904881694|29dde1e81ca110606234102faec518cfa47b5020; bookstack=9ce8490b9cb5cce3c7c5a47a1e2d2aa8; CNZZDATA1277690469=1877497362-1624426087-https%253A%252F%252Fwww.baidu.com%252F%7C1629164652; _gid=GA1.2.1948366462.1629168706; _gat_gtag_UA_166942584_1=1; Hm_lpvt_227e05b01b8f7eefb29a75df28f53840=1629168754',
    }
    # 开始登录
    print(types)
    if types == 'json':
        url = url + '?fr=bookstack'
        headers['x-requested-with'] = 'XMLHttpRequest'

    r = s.get(url=url, params=data, headers=headers)
    # print(url)
    print(r.text)
    # 两种情况 获取 json 和 html
    if types == 'json':
        # 作为 html 解析
        data = json.loads(r.text)
        return data['data']['body']
    else:
        return r.text


def getHtmlByXpath(html_str, xpath):
    strhtml = etree.HTML(html_str)
    strResult = strhtml.xpath(xpath)
    return strResult


def getLocalCss(css):
    # cssPath=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/css'
    cssPath = REALPATH + '/css'
    # print(css)
    ret = {}
    for cs in css:
        if cs.find('css') > -1:
            cssFile = cs.split('/')[-1]
            for _, _, files in os.walk(cssPath):
                if len(files) > 0:
                    if cssFile in files:
                        break
                        # if cssFile==cfile:
                        #     continue
                    else:
                        # 下载文件
                        image = requests.get(cs).content
                        with open(cssPath + "/" + cssFile, "wb") as fp:
                            fp.write(image)
                else:
                    # print('8-8--8-88-8-8-8-')
                    # 下载文件
                    image = requests.get(cs).content
                    with open(cssPath + "/" + cssFile, "wb") as fp:
                        fp.write(image)
            # 替换
            ret[cs] = cssPath + "/" + cssFile

    return ret


deal(sys.argv[1])
