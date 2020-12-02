# -*- coding=utf-8 -*-
from enum import Enum
import abc

class Levels(Enum):
    """
        枚举类，标明权限类型
    """
    DATA_INPUTER='查询数据,录入数据,修改数据'
    USER_MANAGER='增加用户,修改用户基本信息'
    POWER_MANAGER='增加用户,修改用户基本信息,修改用户权限'

class DbEntity(object):
    
    @abc.abstractmethod 
    def initByStr(self, attrDict):
        pass


class Operators(DbEntity):    
    """
        用户类
    """
    def __init__(self):
        super().__init__()
        self.id=0
        self.loginName=''
        self.loginPass=''
        self.showName=''
        self.level=Levels.DATA_INPUTER

    def initByStr(self, attrDict):
        if len(attrDict)==5:
            self.id = int(attrDict['id'])
            self.loginName = attrDict['loginname']
            self.loginPass = attrDict['loginpass']
            self.showName = attrDict['showname']
            self.level = Levels(attrDict['level'])