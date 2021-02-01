# 遍历所有文件夹 获取文件中的可下载文件链接 下载到当前目录 并替换
import sys
import os
import re
import requests
from bs4 import BeautifulSoup


def deal(path):
    # ipp = 0
    for root, dirs, files in os.walk(path):
        for name in files:
            # print(os.path.join(root, name))
            # for name in dirs:
            #     print(os.path.join(root, name))
            realp = os.path.join(root, name)
            if realp.find(".html") > -1:
                print(realp)
                print("*-*-*-*-")
                fo = open(realp, "r+")
                htmlstr = fo.read()
                fo.close()

                pat = '(https?://[^\s]*?\.(jpge|jpg|png|PNG|JPG|css|js|webp|bmp))'
                url = re.findall(pat, htmlstr)
                # if realp == '/Users/jiachunhui/work/draveness.me/golang/index.html':
                #     print(url)
                for i in url:
                    for j in range(len(i)):
                        rurl = i[j]
                        if len(rurl) < 5 or rurl.find('window,document') > -1:
                            continue
                        if rurl == "https://cdn.webp" or rurl == 'https://www.js':
                            continue
                        print(rurl)
                        if rurl.find('http') == -1:
                            rurl = "https://" + rurl
                        # 处理文件 下载至相应文件夹
                        lpath = getLocalFile(rurl)
                        # 计算相对路径 进行替换
                        rel_path = os.path.relpath(lpath, realp)
                        # 相对路径 包含 头部  ..  需要替换
                        if rel_path.find("../../download") > -1:
                            rel_path = rel_path.replace("../../download", '../download')
                        else:
                            rel_path = rel_path.replace("../download", './download')
                        # rel_path = rel_path.replace('../download', './download').replace("../../download", '../download')
                        # print("******------*****")
                        # print(lpath)
                        # print(realp)
                        # print(rel_path)
                        htmlstr = htmlstr.replace(rurl, rel_path)

                # print(htmlstr)

                fo = open(realp, "w+", encoding="utf-8")
                fo.write(htmlstr)
                fo.close()

                break
        # ipp += 1
        # if ipp == 20:
        #     break

    return


def getLocalFile(url):
    real_path = url.split("//")[1]
    # print(real_path)
    # 再次分割 目录对应
    ret = dealPath(real_path)
    # rpath = "/Users/jiachunhui/work/draveness.me/download"
    rpath = "/Users/jiachunhui/work/golang.design/download"
    path = rpath + '/' + ret['path']
    mkdir(path)
    # print('*/*/*/*/*/*')
    # print(ret)

    # 判断文件是否已存在
    for _, _, files in os.walk(path):
        if len(files) > 0:
            if ret['name'] in files:
                return path + "/" + ret['name']
    requests.DEFAULT_RETRIES = 5
    s = requests.Session()
    s.keep_alive = False
    # proxy={
    #     'http':'102.129.249.120:3128'
    # }
    # 通过抓包或chrome开发者工具分析得到登录的请求头信息,
    headers = {
        # 'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'

        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
        # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        # 'cookie': '__cfduid=d2eeacb432670ad3b47e60c973d12555c1612162897; __cf_bm=822222bb7e7ec8c5017f259dfa2a21f18967ac37-1612162902-1800-AXyGzcTD6or4Tlzn9/WHYuncIUJSVEzzgjkinKYZEOfn4cibbsxtyIluu8hp2xfq6b2uvDldjdyJ7JbOsz/XofE=',
        # 'authority': 'ajax.cloudflare.com'
        'authority': 'static.cloudflareinsights.com',
        'cookie': '__cfduid=dcd8b88549ed2f28b2f4a4fec0d019bd01612165337'
    }
    image = s.get(url=url, headers=headers, allow_redirects=False).content
    # image = s.get(url=url, headers=headers, allow_redirects=False, proxies = proxy).content
    # print('*/*/*/*/*/*------------')
    # print(ret['name'])
    # print(path + "/" + ret['name'])
    # sys.exit(0)

    # image = requests.get(url).content
    with open(path + "/" + ret['name'], "wb") as fp:
        fp.write(image)

    return path + "/" + ret['name']


def dealPath(str):
    paths = str.split('/')
    # if str.find('/') > -1:
    name = paths[-1]
    path = '/'.join(paths[1:-1])

    # print('[][][][][][]][][][][[]][][[]')
    # print(path)
    # print(name)
    return {"path": path, "name": name}
    # else:


def mkdir(path):
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
        print(path + ' 创建成功')

    return True

# 参数为要扫描的路径
deal(sys.argv[1])