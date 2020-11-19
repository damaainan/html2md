import pdfkit
import requests
from bs4 import BeautifulSoup

def deal(url, title):
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

    pdfkit.from_string(str(html), './labuladong/'+title+'.pdf', configuration=config, options=options)


data=[{"url": "http://mp.weixin.qq.com/s?__biz=MzAxODQxMDM0Mw==&mid=2247484852&idx=1&sn=85b50b8b0470bb4897e517955f4e5002&chksm=9bd7fbbcaca072aa75e2a241064a403fde1e579d57ab846cd8537a54253ceb2c8b93cc3bf38e&scene=21#wechat_redirect", "name": "001学习算法和刷题的框架思维"},
{"url": "http://mp.weixin.qq.com/s?__biz=MzAxODQxMDM0Mw==&mid=2247484731&idx=1&sn=f1db6dee2c8e70c42240aead9fd224e6&chksm=9bd7fb33aca07225bee0b23a911c30295e0b90f393af75eca377caa4598ffb203549e1768336&scene=21#wechat_redirect", "name": "002动态规划解题套路框架"},
{"url": "http://mp.weixin.qq.com/s?__biz=MzAxODQxMDM0Mw==&mid=2247484709&idx=1&sn=1c24a5c41a5a255000532e83f38f2ce4&chksm=9bd7fb2daca0723be888b30345e2c5e64649fc31a00b05c27a0843f349e2dd9363338d0dac61&scene=21#wechat_redirect", "name": "003回溯算法解题套路框架"},
{"url": "http://mp.weixin.qq.com/s?__biz=MzAxODQxMDM0Mw==&mid=2247485134&idx=1&sn=fd345f8a93dc4444bcc65c57bb46fc35&chksm=9bd7f8c6aca071d04c4d383f96f2b567ad44dc3e67d1c3926ec92d6a3bcc3273de138b36a0d9&scene=21#wechat_redirect", "name": "004BFS 算法解题套路框架"},
{"url": "http://mp.weixin.qq.com/s?__biz=MzAxODQxMDM0Mw==&mid=2247485044&idx=1&sn=e6b95782141c17abe206bfe2323a4226&chksm=9bd7f87caca0716aa5add0ddddce0bfe06f1f878aafb35113644ebf0cf0bfe51659da1c1b733&scene=21#wechat_redirect", "name": "005我写了首诗，让你闭着眼睛也能写对二分搜索"},
{"url": "http://mp.weixin.qq.com/s?__biz=MzAxODQxMDM0Mw==&mid=2247485141&idx=1&sn=0e4583ad935e76e9a3f6793792e60734&chksm=9bd7f8ddaca071cbb7570b2433290e5e2628d20473022a5517271de6d6e50783961bebc3dd3b&scene=21#wechat_redirect", "name": "006我写了首诗，把滑动窗口算法算法变成了默写题"}
]



for val in data:
    # print(val["url"])
    # print(val["name"])
    title = val["name"].replace("/", "-")
    print(title)
    deal(val["url"], title)


