# -*- coding=utf-8 -*-

import pdfkit
import requests
import os
import re
from bs4 import BeautifulSoup
import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from lxml import etree
from lxml import html
from html.parser import HTMLParser  # 导入html解析库

REALPATH = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))


class GenPdf():
    # 此方法 html 效果更好
    def deal(self, url, title, path):
        title = title.replace("|", "").replace(' ', '').replace(
            '｜', '').replace('?', '？').replace('/', '-')
        print(title)

        # 方法一
        # res = requests.get(url)
        # # data-src替换为src 有时候返回的正文被隐藏了，将hidden去掉
        # html = res.text.replace("data-src", "src").replace('style="visibility: hidden;"',"")
        # html = html.replace("font-size: 16px;font-family: 微软雅黑, sans-serif;letter-spacing: 2px;",'font-size: 20px;font-family: 微软雅黑, sans-serif;letter-spacing: 0px;')

        # 方法二
        htmlstr = self.getHTMLText(url)
        htmlstr = htmlstr.replace("data-src", "src").replace(
            'style="visibility: hidden;"', "").replace('crossorigin="anonymous"', '')
        htmlstr = re.sub(
            r'height: [0-9]{1,4}\.{0,1}[0-9]{0,17}px !important;', '', htmlstr)
        htmlstr = re.sub(
            r'width: [0-9]{1,4}\.{0,1}[0-9]{0,17}px !important;', '', htmlstr)
        htmlstr = htmlstr.replace('visibility: hidden !important;', '')

        soup = BeautifulSoup(htmlstr, features="lxml")
        # 选择正文（去除javascrapt等）
        fhtml = soup.select('div#img-content')[0]
        if title == "":
            title = soup.select('#activity-name')[0].get_text()
            # print(title)
            title = title.replace("|", "").replace("/", "-").replace(' ', '').replace(
                '｜', '').replace('?', '？').replace("\n", '').replace("\r", '')
            # print("****")
            # print(title)
            # return

        imgs = soup.select('img')
        # print(imgs)

        imgDict = {}
        for im in range(len(imgs)):
            # print(imgs[im])
            if imgs[im].get('src'):
                src = imgs[im]['src']
                # 处理成本地文件名
                newsrc = self.getLocalImg(src)
                imgDict[src] = newsrc

        # print(imgDict)

        # 获取页面样式
        # css = soup.select('head style')
        # print(len(css))
        # for cs in range(len(css)):
        #     print(len(css[cs].get_text()))

        css = self.getHtmlByXpath(htmlstr, "//style")
        # for i in range(len(css)):
        #     print(len(html.tostring(css[i])))

        # return
        fo = open("./weui.css", "r+")
        weui = fo.read()
        fo.close()

        font = '''<!DOCTYPE html>
<html lang="en">
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
        <style type="text/css">
             @font-face{font-family: "微软雅黑";src:url("‪C:\\Windows\\Fonts\\msyh.ttc")
        </style>
         <style type = "text/css">
            p { font-size:20px;font-family: "微软雅黑","Helvetica Neue", Helvetica, "Hiragino Sans GB", "Microsoft YaHei", Arial, sans-serif, cursive; margin-left: 8px;margin-right: 8px;line-height: 1.2em;}
            span{font-size: 20px;font-family: "楷体","微软雅黑", sans-serif;letter-spacing: 0px;}
        </style>
        <body>
        '''
        """

        font = font.format(title=title)+weui
        for cs in range(len(css)):
            # print(len(css[cs].get_text()))
            # print(len(html.tostring(css[cs])))
            # print(type(css[cs].get_text()))
            # font = font + "<style>" + css[cs].get_text() + "</style>"
            font = font + "<style>" + \
                HTMLParser().unescape(html.tostring(
                    css[cs]).decode()) + "</style>"
            # HTMLParser().unescape(str1.decode())

        fhtml = font + '</head><body>' + str(fhtml) + '</body></html>'
        print(title)
        # 增大较小的字体
        # html=html.replace("font-size: 14px","font-size: 18px").replace("font-size: 12px","font-size: 18px").replace("font-size: 11px","font-size: 16px").replace("font-size: 11.9px","font-size: 16px")

        fhtml = re.sub(
            r"font-size: 1[0-5]\.{0,1}[0-9]{0,1}[0-9]{0,1}px;", 'font-size: 16px;', fhtml)

        # rpath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/out/wx/' + path
        rpath = REALPATH + '/out/wx/' + path
        html_path = rpath + "/html/"
        pdf_path = rpath + "/pdf/"
        self.mkdir(html_path)
        self.mkdir(html_path+"pic/")
        self.mkdir(pdf_path)
        fo = open(html_path + title+'.html', "w+", encoding="utf-8")
        weui = fo.write(fhtml)
        fo.close()

        # html = font + str(html) + '</body></html>'

        # 选项
        # options = {
        #     'page-size': 'A4',
        #     'margin-top': '0.25in',
        #     'margin-right': '0.25in',
        #     'margin-bottom': '0.25in',
        #     'margin-left': '0.25in',
        #     'encoding': "UTF-8",
        #     'dpi':1000,
        #     # 'custom-header': headers,
        #     # 'debug-javascript': [''],
        #     'javascript-delay': 10000,
        #     # 'no-stop-slow-scripts': "",
        #     # 'load-media-error-handling': 'abort',
        #  }

        # 由 html 生成pdf
        # print(html_path +title+'.html')
        # print(pdf_path+title+'.pdf')
        ntitle = title.replace('"', '\\"')

        hfile = html_path + ntitle+'.html'
        pfile = pdf_path + ntitle+'.pdf'
        # os.system('wkhtmltopdf --dpi 300 --enable-plugins --enable-forms "{}" "{}"'.format(hfile, pfile.replace(".pdf","_wk.pdf")))
        os.system('weasyprint -q "{}" "{}"'.format(hfile, pfile))  # 目前效果最好的

        # TODO 增加功能  把html图片下载到本地并替换 保留 html 获得较好的阅读体验
        # print(imgDict)
        for k in imgDict:
            if imgDict[k] != "":
                image = requests.get(k).content
                with open(html_path+"/pic/"+imgDict[k], "wb") as fp:
                    fp.write(image)

            fhtml = fhtml.replace(k, "./pic/"+imgDict[k])

        fhtml = fhtml.replace('<body>', '<body style="margin:40px;">')
        fo = open(html_path + title+'.html', "w+", encoding="utf-8")
        weui = fo.write(fhtml)
        fo.close()

        return title

    def oldDeal(self, url, title, path):
        title = title.replace("|", "").replace(' ', '').replace(
            '｜', '').replace('?', '？').replace('/', '-')
        print(title)

        # 方法一  pdf 效果相对较好
        res = requests.get(url)
        # data-src替换为src 有时候返回的正文被隐藏了，将hidden去掉
        htmlstr = res.text.replace(
            "data-src", "src").replace('style="visibility: hidden;"', "")

        # htmlsr=self.getHTMLText(url)

        htmlstr = htmlstr.replace(
            "data-src", "src").replace('style="visibility: hidden;"', "")
        htmlstr = htmlstr.replace("font-size: 16px;font-family: 微软雅黑, sans-serif;letter-spacing: 2px;",
                                  'font-size: 20px;font-family: 微软雅黑, sans-serif;letter-spacing: 0px;')

        htmlstr = htmlstr.replace("data-src", "src").replace(
            'style="visibility: hidden;"', "").replace('crossorigin="anonymous"', '')
        htmlstr = re.sub(
            r'height: [0-9]{1,4}\.{0,1}[0-9]{0,17}px !important;', '', htmlstr)
        htmlstr = re.sub(
            r'width: [0-9]{1,4}\.{0,1}[0-9]{0,17}px !important;', '', htmlstr)

        soup = BeautifulSoup(htmlstr, features="lxml")
        # 选择正文（去除javascrapt等）
        fhtml = soup.select('div#img-content')[0]
        if title == "":
            title = soup.select('#activity-name')[0].get_text()
            # print(title)
            title = title.replace("|", "").replace("/", "-").replace(' ', '').replace(
                '｜', '').replace('?', '？').replace("\n", '').replace("\r", '')
            # print("****")
            print(title)
            # return

        imgs = soup.select('img')
        # print(imgs)

        imgDict = {}
        for im in range(len(imgs)):
            # print(imgs[im])
            if imgs[im].get('src'):
                src = imgs[im]['src']
                # 处理成本地文件名
                newsrc = self.getLocalImg(src)
                imgDict[src] = newsrc

        # print(imgDict)

        # 处理视频
        # videos = soup.select("iframe.video_iframe")
        # videoret = self.getLocalVideo(videos)


        # 获取页面样式
        css = soup.select('head style')
        # print("*****")
        # print(len(css))
        # print(type(css))
        # for cs in range(len(css)):
        #     print(css[cs].get_text())
        #     print(len(css[cs].get_text()))

        # return
        fo = open("./weui.css", "r+")
        weui = fo.read()
        fo.close()

        font = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
'''

        font = font.format(title=title)+weui
        for cs in range(len(css)):
            # print(len(css[cs].get_text()))
            # print(len(html.tostring(css[cs])))
            font = font + "<style>" + css[cs].get_text() + "</style>"

        font = font + '''
        <style>
            .avatar{width:50px;}
        </style>

        '''

        fhtml = font + '</head><body style="margin:40px;">' + \
            str(fhtml) + '</body></html>'

        # 增大较小的字体
        fhtml = re.sub(
            r"font-size: 1[0-5]\.{0,1}[0-9]{0,1}[0-9]{0,1}px;", 'font-size: 16px;', fhtml)

        # rpath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/out/wx/' + path
        rpath = REALPATH + '/out/wx/' + path
        html_path = rpath + "/html/"
        pdf_path = rpath + "/pdf/"
        self.mkdir(html_path)
        self.mkdir(html_path+"pic/")
        self.mkdir(pdf_path)
        fo = open(html_path + title+'_old.html', "w+", encoding="utf-8")
        weui = fo.write(fhtml)
        fo.close()

        # html = font + str(html) + '</body></html>'

        # 选项
        # options = {
        #     'page-size': 'A4',
        #     'margin-top': '0.25in',
        #     'margin-right': '0.25in',
        #     'margin-bottom': '0.25in',
        #     'margin-left': '0.25in',
        #     'encoding': "UTF-8",
        #     'dpi':1000,
        #     # 'custom-header': headers,
        #     # 'debug-javascript': [''],
        #     'javascript-delay': 10000,
        #     # 'no-stop-slow-scripts': "",
        #     # 'load-media-error-handling': 'abort',
        #  }

        # 由 html 生成pdf
        # print(html_path +title+'.html')
        # print(pdf_path+title+'.pdf')
        ntitle = title.replace('"', '\\"')

        hfile = html_path + ntitle+'_old.html'
        pfile = pdf_path + ntitle+'_old.pdf'
        os.system(
            'wkhtmltopdf --dpi 300 --enable-plugins --enable-forms "{}" "{}"'.format(hfile, pfile))

        # TODO 增加功能  把html图片下载到本地并替换 保留 html 获得较好的阅读体验
        # print(imgDict)
        for k in imgDict:
            if imgDict[k] != "":
                image = requests.get(k).content
                with open(html_path+"/pic/"+imgDict[k], "wb") as fp:
                    fp.write(image)

            fhtml = fhtml.replace(k, "./pic/"+imgDict[k])

        fo = open(html_path + title+'_old.html', "w+", encoding="utf-8")
        weui = fo.write(fhtml)
        fo.close()

        return title

        # pdfkit 格式不好
        # path_wkthmltopdf = r''
        # if platform.system() == "Windows":
        #     path_wkthmltopdf = r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
        # elif platform.system() == "Darwin":
        #     path_wkthmltopdf = r''

        # config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
        # rpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)) + '/../out)/wx/' + path
        # self.mkdir(rpath)
        # pdfkit.from_string(str(html), rpath+'/' +title+'.pdf', configuration=config, options=options)

    def mkdir(self, path):
        # 去除首位空格
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")
        isExists = os.path.exists(path)
        # 判断结果
        if not isExists:
            # os.makedirs(path+"/html")
            # os.makedirs(path+"/pdf")
            os.makedirs(path)
            print(path+' 创建成功')

        return True

    def getHTMLText(self, url):
        # 浏览器驱动
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        if platform.system() == "Windows":
            path_config = 'F:\\bin\\phantomjs.exe'
        elif platform.system() == "Darwin":
            path_config = '/usr/local/bin/chromedriver'
        driver = webdriver.Chrome(
            executable_path=path_config, chrome_options=chrome_options)

        # if platform.system() == "Windows":
        #     path_config = 'F:\\bin\\phantomjs.exe'
        # elif platform.system() == "Darwin":
        #     path_config = '/Users/jiachunhui/repo/phantomjs/bin/phantomjs'
        # driver = webdriver.PhantomJS(executable_path=path_config)  # phantomjs的绝对路径
        time.sleep(10)
        driver.get(url)  # 获取网页
        time.sleep(2)
        return driver.page_source

    def getHtmlByXpath(self, html_str, xpath):
        strhtml = etree.HTML(html_str)
        strResult = strhtml.xpath(xpath)
        return strResult

    def getLocalImg(self, href):
        if href.find('http') > -1:
            imgsub = "png"
            if href.find('wx_fmt=') > -1:
                imgformat = href.split('wx_fmt=')[-1]
                # print(imgformat)
                if len(imgformat) > 1:
                    imgsub = imgformat

            name = href.split('/')[-2][32:]
            return name+"."+imgsub
        return ""

    def getLocalVideo(self, video):
        if video.find('http') > -1:
            imgsub = "mp4"
            if href.find('wx_fmt=') > -1:
                imgformat = href.split('wx_fmt=')[-1]
                # print(imgformat)
                if len(imgformat) > 1:
                    imgsub = imgformat

            name = href.split('/')[-2][32:]
            return name+"."+imgsub
        return ""

    # 此方法 html 效果更好
    def dealHtml(self, url, title, path):
        title = title.replace("|", "").replace(' ', '').replace(
            '｜', '').replace('?', '？').replace('/', '-').replace('"', '')
        print(title)

        # 方法一
        # res = requests.get(url)
        # # data-src替换为src 有时候返回的正文被隐藏了，将hidden去掉
        # html = res.text.replace("data-src", "src").replace('style="visibility: hidden;"',"")
        # html = html.replace("font-size: 16px;font-family: 微软雅黑, sans-serif;letter-spacing: 2px;",'font-size: 20px;font-family: 微软雅黑, sans-serif;letter-spacing: 0px;')

        # 方法二
        htmlstr = self.getHTMLText(url)
        htmlstr = htmlstr.replace("data-src", "src").replace(
            'style="visibility: hidden;"', "").replace('crossorigin="anonymous"', '')
        htmlstr = re.sub(
            r'height: [0-9]{1,4}\.{0,1}[0-9]{0,17}px !important;', '', htmlstr)
        htmlstr = re.sub(
            r'width: [0-9]{1,4}\.{0,1}[0-9]{0,17}px !important;', '', htmlstr)

        soup = BeautifulSoup(htmlstr, features="lxml")
        # 选择正文（去除javascrapt等）
        fhtml = soup.select('div#img-content')[0]
        if title == "":
            title = soup.select('#activity-name')[0].get_text()
            # print(title)
            title = title.replace("|", "").replace("/", "-").replace(' ', '').replace(
                '｜', '').replace('?', '？').replace("\n", '').replace("\r", '')
            # print("****")
            # print(title)
            # return

        imgs = soup.select('img')
        # print(imgs)

        imgDict = {}
        for im in range(len(imgs)):
            # print(imgs[im])
            if imgs[im].get('src'):
                src = imgs[im]['src']
                # 处理成本地文件名
                newsrc = self.getLocalImg(src)
                imgDict[src] = newsrc

        # print(imgDict)

        # 获取页面样式
        # css = soup.select('head style')
        # print(len(css))
        # for cs in range(len(css)):
        #     print(len(css[cs].get_text()))

        css = self.getHtmlByXpath(htmlstr, "//style")
        # for i in range(len(css)):
        #     print(len(html.tostring(css[i])))

        # return
        fo = open("./weui.css", "r+")
        weui = fo.read()
        fo.close()

        font = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
'''

        font = font.format(title=title)+weui
        for cs in range(len(css)):
            # font = font + "<style>" + css[cs].get_text() + "</style>"
            font = font + "<style>" + \
                HTMLParser().unescape(html.tostring(
                    css[cs]).decode()) + "</style>"
            # HTMLParser().unescape(str1.decode())

        fhtml = font + '</head><body>' + str(fhtml) + '</body></html>'

        # 增大较小的字体
        fhtml = re.sub(
            r"font-size: 1[0-5]\.{0,1}[0-9]{0,1}[0-9]{0,1}px;", 'font-size: 16px;', fhtml)

        # rpath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/out/wx/' + path
        rpath = REALPATH + '/out/wx/' + path
        html_path = rpath + "/html/"
        pdf_path = rpath + "/pdf/"
        self.mkdir(html_path)
        self.mkdir(html_path+"pic/")
        self.mkdir(pdf_path)
        fo = open(html_path + title+'.html', "w+", encoding="utf-8")
        weui = fo.write(fhtml)
        fo.close()

        # html = font + str(html) + '</body></html>'

        # 选项
        # options = {
        #     'page-size': 'A4',
        #     'margin-top': '0.25in',
        #     'margin-right': '0.25in',
        #     'margin-bottom': '0.25in',
        #     'margin-left': '0.25in',
        #     'encoding': "UTF-8",
        #     'dpi':1000,
        #     # 'custom-header': headers,
        #     # 'debug-javascript': [''],
        #     'javascript-delay': 10000,
        #     # 'no-stop-slow-scripts': "",
        #     # 'load-media-error-handling': 'abort',
        #  }

        # 由 html 生成pdf
        # print(html_path +title+'.html')
        # print(pdf_path+title+'.pdf')
        ntitle = title.replace('"', '\\"')

        hfile = html_path + ntitle+'.html'
        pfile = pdf_path + ntitle+'.pdf'
        os.system(
            'wkhtmltopdf --dpi 300 --enable-plugins --enable-forms "{}" "{}"'.format(hfile, pfile))
        # os.system('weasyprint "{}" "{}"'.format(hfile, pfile))

        # TODO 增加功能  把html图片下载到本地并替换 保留 html 获得较好的阅读体验
        for k in imgDict:
            if imgDict[k] != "":
                image = requests.get(k).content
                with open(html_path+"/pic/"+imgDict[k], "wb") as fp:
                    fp.write(image)

            fhtml = fhtml.replace(k, "./pic/"+imgDict[k])

        fhtml = fhtml.replace('<body>', '<body style="margin:40px;">')
        fo = open(html_path + title+'.html', "w+", encoding="utf-8")
        weui = fo.write(fhtml)
        fo.close()

        return title
