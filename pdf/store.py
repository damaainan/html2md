import sqlite_utils
from db.mysqlite import simpleToolSql
import time


class StoreData():
    # 从 db 获取需要生成的url
    def getListByTitle(self, title:str):
        sql = simpleToolSql("url")
        res = sql.query("select * from wx_article where title="+title+";")
        print(res)
        sql.close()
        return res

    # 从 db 获取需要生成的url
    def getListFromSql(self, title):
        sql = simpleToolSql("url")
        # res = sql.query("select * from wx_article where state=0;")
        res = sql.query("select * from wx_article where title='" + title + "';")
        # print(res)
        sql.close()
        return res

    # 从 db 获取需要生成的url
    def getListFromParam(self, paramsql):
        sql = simpleToolSql("url")
        # res = sql.query("select * from wx_article where state=0;")
        res, res_name = sql.queryall("select * from wx_article where " + paramsql + ";")
        # print(res)
        sql.close()
        return res, res_name

    # 更新 db
    def updateUrlState(self, id:int):
        sql = simpleToolSql("url")
        res = sql.execute("update wx_article set state=1 where id = ?;",(id,)) 
        # 需要加逗号 https://blog.csdn.net/yimaoyingbi/article/details/104323701
        print(res)
        sql.close()
        return 

    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def addUrl(self, data):
        sql = simpleToolSql("url")
        res = self.getListFromSql(data['title'])
        if len(res)>0:
            return
        # print(res)
        # return
        
        res=sql.execute(
            "insert into wx_article (url,folder,title,state,msgid,turn,create_at,update_at) values (?,?,?,?,?,?,?,?);",
            [(data['link'],data['folder'],data['title'],0,data['msgid'],data['turn'],time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))]
        )
        print(res)
        sql.close()
        return 

    def addAblum(self, url, author, title):
        sql = simpleToolSql("url")
        res = self.getListFromSql(title)
        if len(res)>0:
            return
        
        res=sql.execute(
            "insert into wx_ablum (url,author,title,create_at,update_at) values (?,?,?,?,?);",
            [(url,author,title,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))]
        )
        print(res)
        sql.close()
        return 
