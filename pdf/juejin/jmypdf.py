# -*- coding=utf-8 -*-

# 知乎 pdf 文件生成

# 需要处理多种不同的文章格式内容

# question answer 回答
# zhuanlan.zhihu.com/p/341761870 专栏文章


import pdfkit
import requests
import os
import re
import json
from bs4 import BeautifulSoup
import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from lxml import etree
from lxml import html
from html.parser import HTMLParser #导入html解析库


REALPATH=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/out/juejin'


class JuejinGenPdf():
    # 此方法 html 效果更好
    def deal(self, url, title, path):
        title = title.replace("|", "").replace(' ','').replace('｜','').replace('?','？').replace('/','-')
        print(title)

        ## 方法一
        # res = requests.get(url)
        # # data-src替换为src 有时候返回的正文被隐藏了，将hidden去掉
        # html = res.text.replace("data-src", "src").replace('style="visibility: hidden;"',"")
        # html = html.replace("font-size: 16px;font-family: 微软雅黑, sans-serif;letter-spacing: 2px;",'font-size: 20px;font-family: 微软雅黑, sans-serif;letter-spacing: 0px;')

        ## 方法二
        htmlstr=self.getHTMLText(url)
        # htmlstr = htmlstr.replace("data-src", "src").replace('style="visibility: hidden;"',"").replace('crossorigin="anonymous"','')
        # htmlstr=re.sub(r'height: [0-9]{1,4}\.{0,1}[0-9]{0,17}px !important;', '', htmlstr)
        # htmlstr=re.sub(r'width: [0-9]{1,4}\.{0,1}[0-9]{0,17}px !important;', '', htmlstr)
        # htmlstr=htmlstr.replace('visibility: hidden !important;', '')
        # print(htmlstr)
        # return
        soup = BeautifulSoup(htmlstr, features="lxml")
        # 选择正文（去除javascrapt等）
        fheader = soup.select('h1.article-title')[0]
        fhtml = soup.select('div.article-content')[0]

        title_img = soup.select('.article-hero')
        title_img_str = ''
        # print(title_img)
        if len(title_img) > 0:
            # 处理下载 
            title_img_str = title_img[0]
            nsrc = self.getTitleImg(title_img_str.get("data-src"))
            title_img_str = title_img_str.decode().replace(title_img_str.get("data-src"), nsrc)
            # sys.exit(0)

        # if title == "":
        #     title = soup.select('#activity-name')[0].get_text()
        #     # print(title)
        #     title = title.replace("|", "").replace("/", "-").replace(' ','').replace('｜','').replace('?','？').replace("\n",'').replace("\r",'')
            # print("****")
            # print(title)
            # return

        imgs = soup.select('img')
        # print(imgs)

        imgDict = {}
        for im in range(len(imgs)):
            # if imgs[im].get('class') == "ztext-gif":
                # webp
            # print('-----------------')
            # print(imgs[im])
            # print(imgs[im].decode())
            # print(imgs[im].extract())
            # print(dir(imgs[im]))
            if imgs[im].get('src'):
                src=''
                if imgs[im].get('data-src'):
                    # src=imgs[im]['src']
                    src=imgs[im]['data-src']
                else:
                    # src=imgs[im]['src']
                    continue
                if src.find('raw.githubusercontent.com') > -1 or src.find('github.com') > -1  :
                    continue
                # print(imgs[im].get('class'))
                # print(src)
                # if "ztext-gif" in imgs[im].get('class'):
                #     src=src.replace('.jpg','.webp').replace('.png','.webp').replace('.jpeg','.webp')
                # print(src)

                imgDict[src]=imgs[im].decode()
        # print(imgDict)
        # return

        # 获取页面样式
        # css = soup.select('head style')
        # print(len(css))
        # for cs in range(len(css)):
        #     print(len(css[cs].get_text()))

        css_inner = self.getHtmlByXpath(htmlstr, "//style")

        css=self.getHtmlByXpath(htmlstr,"//link/@href")
        # for it in css:
        #     print(it)
        cssret =self.getLocalCss(css)
        # 集中处理 css 样式 采用公共文件夹管理

        # return
        # fo=open("./weui.css","r+")
        # weui=fo.read()
        # fo.close()

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
        '''
        """

        font=font.format(title=title)
        for cs in cssret:
            # print(len(css[cs].get_text()))
            # print(len(html.tostring(css[cs])))
            # print(type(css[cs].get_text()))
            # font = font + "<style>" + css[cs].get_text() + "</style>"
            font = font + "<link rel='stylesheet' type='text/css' href='" + cssret[cs] + "'></link>"
            # HTMLParser().unescape(str1.decode())
        
        for csi in range(len(css_inner)):
            # print(len(css[cs].get_text()))
            # print(len(html.tostring(css[cs])))
            # print(type(css[cs].get_text()))
            # font = font + "<style>" + css[cs].get_text() + "</style>"
            font = font + "<style>" + HTMLParser().unescape(html.tostring(css_inner[csi]).decode()) + "</style>"

        font = font + '''
         <style type = "text/css">
            p { font-size:20px;font-family: "微软雅黑","Helvetica Neue", Helvetica, "Hiragino Sans GB", "Microsoft YaHei", Arial, sans-serif, cursive; margin-left: 8px;margin-right: 8px;line-height: 1.2em;}
            span{letter-spacing: 0px;}
            .highlight pre{background:#e8e3e3;}
        </style>

        '''
        fhtml = font + '</head><body style="margin:20px 80px;">' + str(title_img_str) + str(fheader) + '<p><a href="'+ url +'">原文链接</a></p>' + str(fhtml) + '</body></html>'
        print(title)
        # 增大较小的字体
        # html=html.replace("font-size: 14px","font-size: 18px").replace("font-size: 12px","font-size: 18px").replace("font-size: 11px","font-size: 16px").replace("font-size: 11.9px","font-size: 16px")

        # fhtml=re.sub(r"font-size: 1[0-5]\.{0,1}[0-9]{0,1}[0-9]{0,1}px;",'font-size: 16px;',fhtml)

        svgicon=soup.select('svg.GifPlayer-icon')
        for svg in range(len(svgicon)):
            # print(svgicon[svg].decode())
            fhtml=fhtml.replace(svgicon[svg].decode(),'')


        # rpath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/' + path
        rpath = REALPATH + '/' + path
        html_path = rpath + "/html/"
        pdf_path = rpath + "/pdf/"
        self.mkdir(html_path)
        self.mkdir(html_path+"pic/")
        self.mkdir(pdf_path)
        fo=open(html_path +title+'.html',"w+",encoding="utf-8")
        fo.write(fhtml)
        fo.close()


        # html = font + str(html) + '</body></html>'

        # 由 html 生成pdf
        # print(html_path +title+'.html')
        # print(pdf_path+title+'.pdf')
        ntitle=title.replace('"','\\"')

        hfile=html_path +ntitle+'.html'
        pfile=pdf_path +ntitle+'.pdf'
        # os.system('wkhtmltopdf --dpi 300 --enable-plugins --enable-forms "{}" "{}"'.format(hfile, pfile.replace(".pdf","_wk.pdf")))
        os.system('weasyprint -q "{}" "{}"'.format(hfile, pfile)) # 目前效果最好的 


        # TODO 增加功能  把html图片下载到本地并替换 保留 html 获得较好的阅读体验
        # imgheaser={
            
        # }
        # print(imgDict)
        for src in imgDict:
            if src != "":
                # print('-*-*-*-*-*--*-*-*-*-*-')
                # print(src)
                if src.find('?') > -1:
                    imgsrc=src.split('?')[0]
                else:
                    imgsrc=src
                newsrc=self.getLocalImg(imgsrc)
                # print(imgsrc)
                image=requests.get(url=imgsrc).content
                with open(html_path+"/pic/"+newsrc,"wb") as fp:
                    fp.write(image)

                fhtml=fhtml.replace(imgDict[src],"<img style='max-width:100%;' src='./pic/"+newsrc+"'/>")

        fhtml=fhtml.replace('<body>','<body style="margin:40px;">')
        fo=open(html_path +title+'.html',"w+",encoding="utf-8")
        fo.write(fhtml)
        fo.close()

        return title
    
    def dealAns(self, url, title, path):
        title = title.replace("|", "").replace(' ','').replace('｜','').replace('?','？').replace('/','-')
        print(title)


        ## 方法二
        htmlstr=self.getHTMLText(url)

        soup = BeautifulSoup(htmlstr, features="lxml")
        # 选择正文（去除javascrapt等）
        fheader = soup.select('h1.QuestionHeader-title')[0]
        fhtml = soup.select('div.AnswerCard')[0]

        soup2 = BeautifulSoup(str(fhtml), features="lxml")
        # 选择正文（去除javascrapt等）
        zop = soup2.select('div.AnswerItem')[0]['data-zop']

        zopd = json.loads(zop)
        # {"authorName":"腾讯技术工程","itemId":1458672031,"title":"怎么学习 Golang？","type":"answer"}
        title=title+ "_" +zopd["authorName"]
        # print(zop)
        # print(type(zop))
        # return


        imgs = soup.select('img')

        imgDict = {}
        for im in range(len(imgs)):
            # print(dir(imgs[im]))
            src=''
            if imgs[im].has_attr('src'):
                if imgs[im].get('data-original'):
                    src=imgs[im]['data-original']
                    # 处理成本地文件名
                elif imgs[im].get('data-actualsrc'):
                    src=imgs[im]['data-actualsrc']
                    # imgDict[src]=imgs[im].decode()
                elif imgs[im].get('data-thumbnail'):
                    src=imgs[im]['data-thumbnail']
                # print(imgs[im].get('class'))
                # print(src)
                if imgs[im].has_attr('class'):
                    if "ztext-gif" in imgs[im].get('class'):
                        src=src.replace('.jpg','.webp').replace('.png','.webp').replace('.jpeg','.webp')
                imgDict[src]=imgs[im].decode()
        # print(imgDict)
        # return

        # 获取页面样式
        # css = soup.select('head style')
        # print(len(css))
        # for cs in range(len(css)):
        #     print(len(css[cs].get_text()))


        css=self.getHtmlByXpath(htmlstr,"//link/@href")
        # for it in css:
        #     print(it)
        cssret =self.getLocalCss(css)
        # 集中处理 css 样式 采用公共文件夹管理

        # return
        # fo=open("./weui.css","r+")
        # weui=fo.read()
        # fo.close()

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
        '''
        """

        font=font.format(title=title)
        for cs in cssret:
            # font = font + "<style>" + css[cs].get_text() + "</style>"
            font = font + "<link rel='stylesheet' type='text/css' href='" + cssret[cs] + "'></link>"
            # HTMLParser().unescape(str1.decode())

        # font = font + '''
        #  <style type = "text/css">
        #     p { font-size:20px;font-family: "微软雅黑","Helvetica Neue", Helvetica, "Hiragino Sans GB", "Microsoft YaHei", Arial, sans-serif, cursive; margin-left: 8px;margin-right: 8px;line-height: 1.2em;}
        #     span{font-size: 20px;font-family: "楷体","微软雅黑", sans-serif;letter-spacing: 0px;}
        #     .highlight pre{background:#e8e3e3;}
        # </style>

        # '''

        fhtml = font + '</head><body style="margin:20px 80px;">' + str(fheader) + str(fhtml) + '</body></html>'
        print(title)
        # 增大较小的字体
        # html=html.replace("font-size: 14px","font-size: 18px").replace("font-size: 12px","font-size: 18px").replace("font-size: 11px","font-size: 16px").replace("font-size: 11.9px","font-size: 16px")

        fhtml=re.sub(r"font-size: 1[0-5]\.{0,1}[0-9]{0,1}[0-9]{0,1}px;",'font-size: 16px;',fhtml)


        # rpath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/' + path
        rpath = REALPATH + '/' + path
        html_path = rpath + "/html/"
        pdf_path = rpath + "/pdf/"
        self.mkdir(html_path)
        self.mkdir(html_path+"pic/")
        self.mkdir(pdf_path)
        fo=open(html_path +title+'.html',"w+",encoding="utf-8")
        fo.write(fhtml)
        fo.close()


        # html = font + str(html) + '</body></html>'

        # 由 html 生成pdf
        # print(html_path +title+'.html')
        # print(pdf_path+title+'.pdf')
        ntitle=title.replace('"','\\"')

        hfile=html_path +ntitle+'.html'
        pfile=pdf_path +ntitle+'.pdf'
        # os.system('wkhtmltopdf --dpi 300 --enable-plugins --enable-forms "{}" "{}"'.format(hfile, pfile.replace(".pdf","_wk.pdf")))
        os.system('weasyprint -q "{}" "{}"'.format(hfile, pfile)) # 目前效果最好的 


        # TODO 增加功能  把html图片下载到本地并替换 保留 html 获得较好的阅读体验
        imgheaser={
            
        }
        # print(imgDict)
        for src in imgDict:
            if src != "":
                # print('-*-*-*-*-*--*-*-*-*-*-')
                # print(src)
                if src.find('?') > -1:
                    imgsrc=src.split('?')[0]
                else:
                    imgsrc=src
                newsrc=self.getLocalImg(imgsrc)
                # print(imgsrc)
                image=requests.get(url=imgsrc, headers=imgheaser).content
                with open(html_path+"/pic/"+newsrc,"wb") as fp:
                    fp.write(image)

                fhtml=fhtml.replace(imgDict[src],"<img style='max-width:100%;' src='./pic/"+newsrc+"'/>")

        # fhtml=fhtml.replace('<body>','<body style="margin:40px;">')
        fo=open(html_path +title+'.html',"w+",encoding="utf-8")
        fo.write(fhtml)
        fo.close()

        return title


    def mkdir(self, path):
        # 去除首位空格
        path=path.strip()
        # 去除尾部 \ 符号
        path=path.rstrip("\\")
        isExists=os.path.exists(path)
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
        driver = webdriver.Chrome(executable_path=path_config, chrome_options=chrome_options)
        
        # phantomjs 驱动
        # if platform.system() == "Windows":
        #     path_config = 'F:\\bin\\phantomjs.exe'
        # elif platform.system() == "Darwin":
        #     path_config = '/Users/jiachunhui/repo/phantomjs/bin/phantomjs'
        # driver = webdriver.PhantomJS(executable_path=path_config)  # phantomjs的绝对路径

        time.sleep(10)
        driver.get(url)  # 获取网页
        time.sleep(2)
        return driver.page_source

    def getHtmlByXpath(self, html_str,xpath):
        strhtml = etree.HTML(html_str)
        strResult = strhtml.xpath(xpath)
        return strResult

    def getTitleImg(self, img_str):
        # imgheaser={
            
        # }
        # pat = r'(https?://[^\s]*?(jpge|jpg|png|PNG|JPG))'
        # url = re.findall(pat, img_str.decode())
        # print(url)
        # for i in url:
        #     for j in range(len(i)):
        #         if len(i[j]) > 20:
        #             print(i[j]) 
        # print("*-*//////-*-*/////----") 
        newsrc=self.getLocalImg(img_str)
        image=requests.get(url = img_str).content
        with open(REALPATH + "/pic/"+newsrc,"wb") as fp:
            fp.write(image)
        
        return "../../pic/" + newsrc
        # print(url)

    def getLocalImg(self,href):
        if href.find('http') > -1:
            imgsub="webp"
            if href.find('?') > -1:
                href = href.split('?')[-2]
                formats = href.split('?')[-1].split('/')
                if 'webp' in formats:
                    imgsub="webp"
                elif  'gif' in formats:
                    imgsub="gif"
                elif  'png' in formats:
                    imgsub="png"

            #     imgformat=href.split('wx_fmt=')[-1]
            #     # print(imgformat)
            #     if len(imgformat)>1:
            #         imgsub=imgformat

            name=href.split('/')[-1] + "." + imgsub
            return name
        return ""

    def getLocalCss(self, css):
        # cssPath=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/css'
        cssPath=REALPATH + '/css'
        # print(css)
        ret={}
        for cs in css:
            if cs.find('css') > -1:
                cssFile=cs.split('/')[-1]
                for _, _, files in os.walk(cssPath):  
                    if len(files)>0:
                        if cssFile in files:
                            break
                            # if cssFile==cfile:
                            #     continue
                        else:
                            # 下载文件
                            image=requests.get(cs).content
                            with open(cssPath+"/"+cssFile,"wb") as fp:
                                fp.write(image)
                    else:
                        # print('8-8--8-88-8-8-8-')
                        # 下载文件
                        image=requests.get(cs).content
                        with open(cssPath+"/"+cssFile,"wb") as fp:
                            fp.write(image)
                # 替换
                ret[cs]=cssPath+"/"+cssFile
        
        return ret

    # 此方法 html 效果更好
    def dealHtml(self, url, title, path):
        title = title.replace("|", "").replace(' ','').replace('｜','').replace('?','？').replace('/','-').replace('"','')
        print(title)

        ## 方法一
        # res = requests.get(url)
        # # data-src替换为src 有时候返回的正文被隐藏了，将hidden去掉
        # html = res.text.replace("data-src", "src").replace('style="visibility: hidden;"',"")
        # html = html.replace("font-size: 16px;font-family: 微软雅黑, sans-serif;letter-spacing: 2px;",'font-size: 20px;font-family: 微软雅黑, sans-serif;letter-spacing: 0px;')

        ## 方法二
        htmlstr=self.getHTMLText(url)
        htmlstr = htmlstr.replace("data-src", "src").replace('style="visibility: hidden;"',"").replace('crossorigin="anonymous"','')
        htmlstr=re.sub(r'height: [0-9]{1,4}\.{0,1}[0-9]{0,17}px !important;', '', htmlstr)
        htmlstr=re.sub(r'width: [0-9]{1,4}\.{0,1}[0-9]{0,17}px !important;', '', htmlstr)

        soup = BeautifulSoup(htmlstr, features="lxml")
        # 选择正文（去除javascrapt等）
        fhtml = soup.select('div#img-content')[0]
        if title == "":
            title = soup.select('#activity-name')[0].get_text()
            # print(title)
            title = title.replace("|", "").replace("/", "-").replace(' ','').replace('｜','').replace('?','？').replace("\n",'').replace("\r",'')
            # print("****")
            # print(title)
            # return

        imgs = soup.select('img')
        # print(imgs)

        imgDict = {}
        for im in range(len(imgs)):
            # print(imgs[im])
            if imgs[im].get('src'):
                src=imgs[im]['src']
                # 处理成本地文件名
                newsrc=self.getLocalImg(src)
                imgDict[src]=newsrc

        # print(imgDict)

        # 获取页面样式
        # css = soup.select('head style')
        # print(len(css))
        # for cs in range(len(css)):
        #     print(len(css[cs].get_text()))


        css=self.getHtmlByXpath(htmlstr,"//style")
        # for i in range(len(css)):
        #     print(len(html.tostring(css[i])))


        # return
        fo=open("./weui.css","r+")
        weui=fo.read()
        fo.close()

        font = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
'''

        font=font.format(title=title)+weui
        for cs in range(len(css)):
            # font = font + "<style>" + css[cs].get_text() + "</style>"
            font = font + "<style>" + HTMLParser().unescape(html.tostring(css[cs]).decode()) + "</style>"
            # HTMLParser().unescape(str1.decode())

        fhtml = font + '</head><body>' + str(fhtml) + '</body></html>'

        # 增大较小的字体
        fhtml=re.sub(r"font-size: 1[0-5]\.{0,1}[0-9]{0,1}[0-9]{0,1}px;",'font-size: 16px;',fhtml)

        rpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/' + path
        html_path = rpath + "/html/"
        pdf_path = rpath + "/pdf/"
        self.mkdir(html_path)
        self.mkdir(html_path+"pic/")
        self.mkdir(pdf_path)
        fo=open(html_path +title+'.html',"w+",encoding="utf-8")
        weui=fo.write(fhtml)
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
        ntitle=title.replace('"','\\"')

        hfile=html_path +ntitle+'.html'
        pfile=pdf_path +ntitle+'.pdf'
        os.system('wkhtmltopdf --dpi 300 --enable-plugins --enable-forms "{}" "{}"'.format(hfile, pfile))
        # os.system('weasyprint "{}" "{}"'.format(hfile, pfile))


        # TODO 增加功能  把html图片下载到本地并替换 保留 html 获得较好的阅读体验
        for k in imgDict:
            if imgDict[k] != "":
                image=requests.get(k).content
                with open(html_path+"/pic/"+imgDict[k],"wb") as fp:
                    fp.write(image)

            fhtml=fhtml.replace(k,"./pic/"+imgDict[k])

        fhtml=fhtml.replace('<body>','<body style="margin:40px;">')
        fo=open(html_path +title+'.html',"w+",encoding="utf-8")
        weui=fo.write(fhtml)
        fo.close()

        return title