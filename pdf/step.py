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

sql = simpleToolSql("url")
# f = sql.execute("create table test (id int not null,name text not null,age int);")
# print("ok")
# sql.execute("insert into test (id,name,age) values (?,?,?);",[(1,'abc',15),(2,'bca',16)])
res = sql.query("select * from test;")
print(res)
res = sql.query("select * from test where id=?;",(3,))
print(res)
sql.close()

# 从 db 获取需要生成的url
def getListFromSql():
    sql = simpleToolSql("url")
    res = sql.query("select * from test;")
    print(res)
    sql.close()
    return res

# 更新 db
def updateUrl():
    sql = simpleToolSql("url")
    res = sql.query("update test set satte=1 where id in (" + ");")
    print(res)
    sql.close()
    return 

def addUrl():    
    return 

