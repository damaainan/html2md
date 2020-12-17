# -*- coding=utf-8 -*-

import pdfkit
import requests
import os
from bs4 import BeautifulSoup
import platform

class GenPdf():
    def deal(self, url, title, path):
        title = title.replace("|", "").replace(' ','').replace('｜','').replace('?','？')
        print(title)
        res = requests.get(url)
        # data-src替换为src 有时候返回的正文被隐藏了，将hidden去掉
        html = res.text.replace("data-src", "src").replace('style="visibility: hidden;"',"")
        # html = html.replace("font-size: 16px;font-family: 微软雅黑, sans-serif;letter-spacing: 2px;",'font-size: 20px;font-family: 微软雅黑, sans-serif;letter-spacing: 0px;')

        soup = BeautifulSoup(html, features="lxml")
        # 选择正文（去除javascrapt等）
        html = soup.select('div#img-content')[0]
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
        css = soup.select('head style')
        # print(type(css))
        fo=open("./weui.css","r+")
        weui=fo.read()
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

        font=font.format(title=title)+weui
        for cs in range(len(css)):
            # print(type(css[cs].get_text()))
            font = font + "<style>" + css[cs].get_text() + "</style>"

        html = font + "</head><body>" + str(html) + '</body></html>'

        # 增大较小的字体
        html=html.replace("font-size: 14px","font-size: 18px").replace("font-size: 12px","font-size: 18px").replace("font-size: 11px","font-size: 16px")


        rpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/out/wx/' + path
        html_path = rpath + "/html/"
        pdf_path = rpath + "/pdf/"
        self.mkdir(html_path)
        self.mkdir(html_path+"/pic/")
        self.mkdir(pdf_path)
        fo=open(html_path +title+'.html',"w+",encoding="utf-8")
        weui=fo.write(html)
        fo.close()


        # html = font + str(html) + '</body></html>'

        # 选项
        options = {
            'page-size': 'A4',
            'margin-top': '0.25in',
            'margin-right': '0.25in',
            'margin-bottom': '0.25in',
            'margin-left': '0.25in',
            'encoding': "UTF-8",
            'dpi':1000,
            # 'custom-header': headers,
            # 'debug-javascript': [''],
            'javascript-delay': 10000,
            # 'no-stop-slow-scripts': "",
            # 'load-media-error-handling': 'abort',
         }

        # 由 html 生成pdf
        # print(html_path +title+'.html')
        # print(pdf_path+title+'.pdf')
        ntitle=title.replace('"','\\"')

        hfile=html_path +ntitle+'.html'
        pfile=pdf_path +ntitle+'.pdf'
        os.system('wkhtmltopdf --dpi 300 --enable-local-file-access --enable-plugins --enable-forms "file://{}" "{}"'.format(hfile, pfile))

        # TODO 增加功能  把html图片下载到本地并替换 保留 html 获得较好的阅读体验
        for k in imgDict:
            if imgDict[k] != "":
                image=requests.get(k).content
                with open(html_path+"/pic/"+imgDict[k],"wb") as fp:
                    fp.write(image)

            html=html.replace(k,"./pic/"+imgDict[k])

        fo=open(html_path +title+'.html',"w+",encoding="utf-8")
        weui=fo.write(html)
        fo.close()

        return title

        # pdfkit 格式不好
        # path_wkthmltopdf = r''
        # if platform.system() == "Windows":
        #     path_wkthmltopdf = r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
        # elif platform.system() == "Darwin":
        #     path_wkthmltopdf = r''

        # config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
        # rpath = os.path.dirname(os.path.abspath(__file__)) + '/../out/wx/' + path
        # self.mkdir(rpath)
        # pdfkit.from_string(str(html), rpath+'/' +title+'.pdf', configuration=config, options=options)

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

    def getLocalImg(self,href):
        if href.find('http') > -1:
            name=href.split('/')[-2][32:]
            return name+".png"
        return ""