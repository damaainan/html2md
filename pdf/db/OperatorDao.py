# import DbSuper.DbSuper
import DbEntity

class OperatorDao(DbSuper):
    
    def __init__(self):
        super().__init__()
    
    def findById(self, id):
        """
            根据ID查找类
            返回类，如未找到返回空
        """
        return super().findByPropertyFirst(DbEntity.Operators, 'id', id)
            

    def findByLoginname(self, loginname):
        """
            根据登录名查找类
            返回类，如未找到返回空
        """
        return super().findByPropertyFirst(DbEntity.Operators, 'loginName', loginname)
        #return super().findByProperty(Operators, 'loginName', loginname)
        #return super().findByProperty(Operators, 'loginName', loginname,strict=False)
        #return super().findByProperty(Operators, 'loginName', loginname, pager = True, numPerPage=5, page = 1)
    
    def addOper(self, oper):
        #可以对实例进一步处理，比如MD5加密 oper.loginPass = MDUtils.md5Text(oper.loginPass)
        return super().add(oper)
    
    def modiOper(self, oper):
        return super().modify(oper)
    
    def delOper(self, oper):
        return super().delete(oper)


    
if __name__ == '__main__':
    operatorDao = OperatorDao()
    operatorDao.setDb('url.db')
    oper = operatorDao.findByLoginname('test')
    for op in oper:
        print(op)