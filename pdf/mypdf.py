import pdfkit
import requests
import os
from bs4 import BeautifulSoup

class GenPdf(object):
    def deal(self, url, title, path):
        res = requests.get(url)
        # data-src替换为src 有时候返回的正文被隐藏了，将hidden去掉
        html = res.text.replace("data-src", "src").replace('style="visibility: hidden;"',"")

        soup = BeautifulSoup(html)
        # 选择正文（去除javascrapt等）
        html = soup.select('div#img-content')[0]

        # 可以修改字体
        font = '''
        <style type="text/css">
                @font-face{font-family: "微软雅黑";src:url("‪C:\\Windows\\Fonts\\msyh.ttc")
        </style>
            <style type = "text/css">
            p { font-size:20px;font-family: "Helvetica Neue", Helvetica, "Hiragino Sans GB", "Microsoft YaHei", Arial, sans-serif, cursive; }
        </style>
        '''
        html = font + str(html)

        # 选项
        options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
        #      'custom-header': headers,
        #     'debug-javascript': [''],
            'javascript-delay': 10000,
        #     'no-stop-slow-scripts': "",
        #     'load-media-error-handling': 'abort',
            }

        path_wkthmltopdf = r''
        config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
        pdfkit.from_string(str(html), os.path.dirname(os.path.abspath(__file__)) + '/../out/' + path +title+'.pdf', configuration=config, options=options)
