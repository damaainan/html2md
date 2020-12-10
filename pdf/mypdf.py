import pdfkit
import requests
import os
from bs4 import BeautifulSoup
import platform

class GenPdf():
    def deal(self, url, title, path):
        res = requests.get(url)
        # data-src替换为src 有时候返回的正文被隐藏了，将hidden去掉
        html = res.text.replace("data-src", "src").replace('style="visibility: hidden;"',"")
        html = html.replace("font-size: 16px;font-family: 微软雅黑, sans-serif;letter-spacing: 2px;",'font-size: 20px;font-family: 微软雅黑, sans-serif;letter-spacing: 0px;')

        soup = BeautifulSoup(html)
        # 选择正文（去除javascrapt等）
        html = soup.select('div#img-content')[0]

        # 可以修改字体
        font = '''
        <style type="text/css">
            @font-face{font-family: "微软雅黑";src:url("‪C:\\Windows\\Fonts\\msyh.ttc")
        </style>
        <style type = "text/css">
            p { font-size:20px;font-family: "微软雅黑","Helvetica Neue", Helvetica, "Hiragino Sans GB", "Microsoft YaHei", Arial, sans-serif, cursive; margin-left: 8px;margin-right: 8px;line-height: 1.2em;}
            span{font-size: 20px;font-family: "微软雅黑", sans-serif;letter-spacing: 2px;}
        </style>
        '''
        html = font + str(html)

        # 选项
        options = {
            'page-size': 'A4',
            'margin-top': '0.25in',
            'margin-right': '0.25in',
            'margin-bottom': '0.25in',
            'margin-left': '0.25in',
            'encoding': "UTF-8",
            'dpi':300,
        #      'custom-header': headers,
        #     'debug-javascript': [''],
            'javascript-delay': 10000,
        #     'no-stop-slow-scripts': "",
        #     'load-media-error-handling': 'abort',
        }

        # path_wkthmltopdf = r''
        if platform.system() == "Windows":
            path_wkthmltopdf = r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
        elif platform.system() == "Darwin":
            path_wkthmltopdf = r''
        
        config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
        rpath = os.path.dirname(os.path.abspath(__file__)) + '/../out/wx/' + path
        self.mkdir(rpath)
        pdfkit.from_string(str(html), rpath+'/' +title+'.pdf', configuration=config, options=options)

    def mkdir(self, path):
        # 去除首位空格
        path=path.strip()
        # 去除尾部 \ 符号
        path=path.rstrip("\\")
        isExists=os.path.exists(path)
        # 判断结果
        if not isExists:
            os.makedirs(path) 
            print(path+' 创建成功')
        
        return True