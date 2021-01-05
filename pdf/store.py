# -*- coding=utf-8 -*-
from db.mysqlite import simpleToolSql
import time
import datetime


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
    # 更新 db
    def updateUrlStateByMsg(self):
        sql = simpleToolSql("url")
        res = sql.execute("update wx_article set state=1 where msgid = ?;",(0,))
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
            [(data['link'],data['folder'].replace(' ',''),data['title'],0,data['msgid'],data['turn'],time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))]
        )
        print(res)
        sql.close()
        return

    def getAblumListFromSql(self, url):
        sql = simpleToolSql("url")
        # res = sql.query("select * from wx_article where state=0;")
        res = sql.query("select * from wx_ablum where url='{u}' and update_at<'{t}';".format(u=url,t=(datetime.datetime.now()-datetime.timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")))
        # print(res)
        sql.close()
        return res

    def getAblumListFromAuthorAndTitle(self, author, title):
        sql = simpleToolSql("url")
        # res = sql.query("select * from wx_article where state=0;")
        res = sql.query("select * from wx_ablum where author='{a}' and title='{ti}' and update_at<'{t}';".format(a=author,ti=title,t=(datetime.datetime.now()-datetime.timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")))
        # print(res)
        sql.close()
        return res
    def updateAblum(self, id):
        sql = simpleToolSql("url")
        # res = sql.query("select * from wx_article where state=0;")
        # print("-*-*-*-*")
        res = sql.execute("update wx_ablum set update_at='{t}' where id={id};".format(t=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),id=id))
        print("更新===",res)
        sql.close()
        return res
    def addAblum(self, url, author, title):
        sql = simpleToolSql("url")
        res = self.getAblumListFromAuthorAndTitle(author, title)
        print(res)
        # return
        if len(res)>0:
            self.updateAblum(res[0][0])
            print(res[0][0])
            return

        res=sql.execute(
            "insert into wx_ablum (url,author,title,create_at,update_at) values (?,?,?,?,?);",
            [(url,author,title,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))]
        )
        print(res)
        sql.close()
        return

    def getAblums(self):
        sql = simpleToolSql("url")
        res = sql.query("select * from wx_ablum where update_at<'{t}';".format(t=(datetime.datetime.now()-datetime.timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")))
        # print(res)
        sql.close()
        return res
