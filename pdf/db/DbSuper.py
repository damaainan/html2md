import EasySqlite.EasySqlite

class DbSuper(object):
    dbHelper=None   #类变量，共用一个EasySqlite工具类
    
    def __init__(self):
        """
            初始化数据库
            
        """
        super().__init__()
        
    def setDb(self,  dburl): 
        """
            参数：
                dburl——数据库文件位置,str类型
        """
        DbSuper.dbHelper = EasySqlite(dburl)   
        
    
    def add(self, obj):
        """
            将实例储存到数据库，数据库中的表名应与类名一致，表中字段名与类定义的变量名一致 ，顺序也得一致
            参数：
                obj——类实例
            返回值：无    
        """
        sql = 'insert into '+type(obj).__name__+' values('  #通过type(obj).__name__获得表名
        paras = []  #sql语句的参数
        tag = True
        for attr in obj.__dict__.keys():   #获取实例对象的属性名obj.__dict__
            if tag:
                tag=False  #第一项是ID，自动生成，跳过
                continue
            sql += ',?'   #循环几次，就加几次? 生成   insert into xxxx values(,?,?,?,?)的sql语句
            para = getattr(obj, attr)    # 使用getattr函数，利用反射获得类属性实际的值
            
            if type(para)==str:    #对值进行判断，如果非str类型，应做转换，避免sql执行错误
                paras.append(para)
            else :
                paras.append(str(para))
        sql = sql.replace(',','null,', 1)    #将多余的 ， 处理一下
        sql += ')'
        #print(sql)
        #print(paras)
        DbSuper.dbHelper.execute(sql, paras)   #利用工具类执行SQL
        
    def findByProperty(self, objclass, propertyName,  propertyValueStr,strict = True,  orderby='id', pager = False, numPerPage=1, page = 1):
        """
            通过类的某一个属性查找
            参数：
                objclass——class类型，类名
                propertyName——str类型，筛选依据的属性名
                propertyValueStr——object类型，筛选依据的属性名对应的值
                strict——bool类型，文本字段是否精确匹配，非文本字段请勿改变此值
                orderby——str类型，排序的依据，默认ID排序
                pager——bool类型，查询的结果是否分页
                numPerPage——int类型，如pager=True，则此参数起作用，每页显示数据量
                page——int类型，如pager=True，则此参数起作用，页数
            返回值：objclass的list
        """
        sql = 'select * from %s where ' % objclass.__name__
        #对propertyValueStr进行判断，非str型，进行转换
        if type(propertyValueStr) != str:
            propertyValueStr = str(propertyValueStr)
            
        if strict:#默认严格匹配
            sql += '%s = ? order by %s '% (propertyName, orderby)
        else:
            sql += '%s like ? order by %s '% (propertyName, orderby)
            propertyValueStr = '%' + propertyValueStr + '%'
        if pager: #对pager进行判断，默认不进行分页处理
            sql += 'limit %d offset %d' % (numPerPage, numPerPage * (page - 1))
        retObjects = []
        
            #DbSuper.dbHelper.execute(sql, [propertyValueStr, ])执行SQL，结果返回为Dict数组
        print(sql)
        for ret in  DbSuper.dbHelper.execute(sql, [propertyValueStr, ]):
            #利用变量生成实例
            obj = objclass()
            #调用initByStr方法，将Dict解释，并赋值给对应属性，因不同类实现方式不同，故此方法由类声明时自行完成，类似接口
            obj.initByStr(ret)
            retObjects.append(obj)
        return retObjects
        
    def findByPropertyFirst(self, objclass, propertyName,  propertyValueStr, strict=True):
        """
            类似于findByProperty，做了一定简化，且只查询一个结果
            返回值：成功返回对象实例，失败返回空
        """
        sql = 'select * from %s where %s = ? limit 1' % (objclass.__name__, propertyName)
        if strict==False:
            propertyValueStr = '%' + propertyValueStr + '%'
        ret = DbSuper.dbHelper.execute(sql,  [propertyValueStr, ])
        if len(ret)>0:
            obj = objclass()
            obj.initByStr(ret[0])
            return obj 
        else:
            return None
            
    def modify(self, obj, propertyIndex='id'):
        """
            更新类，并存于数据库
            参数：
                obj——类实例
                propertyIndex——筛选依据的字段，默认ID
            返回值： 无
        """
        sql = 'update %s set ' % type(obj).__name__     #利用反射，通过实例获得类名，即表名
        params = []
        for attr in obj.__dict__.keys():        #遍历每个属性，生成update语句中的set xxx=?，注意要跳过筛选依据的属性
            if attr == propertyIndex:
                continue
            else:
                sql += ', %s=?'  % attr 
                
                #对属性值进行处理，如果不是str型，要转换
                if type(getattr(obj, attr)) == str:
                    params.append(getattr(obj, attr))
                else:
                    params.append(str(getattr(obj, attr)))
        #筛选条件语句生成
        sql += ' where %s = ?' % propertyIndex
        #加入参数
        params.append(getattr(obj, propertyIndex))
        #对生成的sql语句处理，去掉多余的，   执行SQL语句
        DbSuper.dbHelper.execute(sql .replace(',', '', 1), params)
    
    def delete(self, obj, propertyIndex='id'):
        """
            删除对象
            参数：
                obj——待删除的对象
                propertyIndex——筛选依据
                
        """
        sql = 'delete from %s where %s=?' % (type(obj).__name__, propertyIndex)
        param = getattr(obj, propertyIndex)
        if type(param) != str:
            param = str(param)
        DbSuper.dbHelper.execute(sql , [param, ])