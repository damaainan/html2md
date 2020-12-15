# -*- coding=utf-8 -*-
from mypdf import GenPdf
from db.mysqlite import simpleToolSql


data=[{"url": "http://mp.weixin.qq.com/s?__biz=MzAxODQxMDM0Mw==&mid=2247484852&idx=1&sn=85b50b8b0470bb4897e517955f4e5002&chksm=9bd7fbbcaca072aa75e2a241064a403fde1e579d57ab846cd8537a54253ceb2c8b93cc3bf38e&scene=21#wechat_redirect", "name": "001学习算法和刷题的框架思维"}
]

# path = '***/'  || ''
# for val in data:
#     # print(val["url"])
#     # print(val["name"])
#     pdf = GenPdf()
#     title = val["name"].replace("/", "-")
#     print(title)
#     pdf.deal(val["url"], title, '')

# sql = simpleToolSql("url")
# # sql.execute("insert into wx_article (id,name,age) values (?,?,?);",[(1,'abc',15),(2,'bca',16)])
# res = sql.query("select * from wx_article;")
# print(res)
# res = sql.query("select * from wx_article where id=?;",(3,))
# print(res)
# sql.close()

# 从 db 获取需要生成的url
def getListByTitle(title:str):
    sql = simpleToolSql("url")
    res = sql.query("select * from wx_article where title="+title+";")
    print(res)
    sql.close()
    return res

# 从 db 获取需要生成的url
def getListFromSql():
    sql = simpleToolSql("url")
    # res = sql.query("select * from wx_article where state=0;")
    res = sql.query("select * from wx_article;")
    print(res)
    sql.close()
    return res

# 更新 db
def updateUrl(id:int):
    sql = simpleToolSql("url")
    res = sql.execute("update wx_article set state=1 where id = ?;",(id,)) 
    # 需要加逗号 https://blog.csdn.net/yimaoyingbi/article/details/104323701
    print(res)
    sql.close()
    return 

def addUrl():
    sql = simpleToolSql("url")
    sql.execute(
        "insert into wx_article (url,folder,title,state,turn,create_at,update_at) values (?,?,?,?,?,?);",
        [("http",'test',"01",0,1,"2020-12-03 09:38:25","2020-12-03 09:38:25")]
    )
    res = sql.query("select * from wx_article;")
    print(res)
    sql.close()
    return 

# addUrl()

updateUrl(1)
res = getListFromSql()
print(res)