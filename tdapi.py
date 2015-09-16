# encoding: UTF-8

import sys
import os
from PyQt4 import QtGui
from time import sleep

from vnctptd import *
from eventdriven import *


class TestTdApi(TdApi):

    def __init__(self):
        super(TestTdApi, self).__init__()
        self.__reqid = 0
        self.__engine = None

        self.__userid = ''
        self.__passwd = ''
        self.__address = ''
        self.__brokerid = ''

        self.createFtdcTraderApi(os.getcwd() + '/tdconnection/')


    def registerEngine(self, engine):
        self.__engine = engine

    def onFrontConnected(self):
        print u'td服务器连接'

    def onFrontDisConnected(self, n):
        print u'td服务器断开'

    def onRspError(self, error, n, last):   # debug
        print(error)

    def onRspUserLogin(self, data, error, n, last):
        state = {'n' : n, 'last' : last}
        event = Event(EVENT_TD_LOGIN, data, error, state)
        self.__engine.put(event)
        print(data)
        print(error['ErrorMsg'])
        #print u'用户登录'

    def onRspQrySettlementInfo(self, data, error, n, last):
        for key, value in data.items():
            print(str(key).decode('gbk') + ':' + str(value).decode('gbk'))
        for key, value in error.items():
            print(str(key).decode('gbk') + ':' + str(value).decode('gbk'))
        state = {'n' : n, 'last' : last}
        event = Event(EVENT_TD_SETTLEINFO, data, error, state)
        self.__engine.put(event)

    def onRspSettlementInfoConfirm(self, data, error, n, last):
        for key, value in data.items():
            print(str(key).decode('gbk') + ':' + str(value).decode('gbk'))
        for key, value in error.items():
            print(str(key).decode('gbk') + ':' + str(value).decode('gbk'))
        state = {'n' : n, 'last' : last}
        event = Event(EVENT_TD_SETTLECONFIRM, data, error, state)
        self.__engine.put(event)

    def onRspOrderInsert(self, data, error, n, last):
        print(u'报单错误')
        print('ErrorID' + error['ErrorID'] + ' ' + 'ErrorMsg' + error['ErrorMsg'].decode('gbk'))

    def onRspOrderAction(self, data, error, n, last):
        print(u'撤单错误')
        print('ErrorID' + error['ErrorID'] + ' ' + 'ErrorMsg' + error['ErrorMsg'].decode('gbk'))

    def onRspQryInvestor(self, data, error, n, last):
        print(u'投资者回报')
        if error['ErrorID'] == 0:
            for key, value in data.items():
                print(str(key).decode('gbk') + ':' + str(value).decode('gbk'))
        else:
            print('ErrorID' + error['ErrorID'] + 'ErrorMsg' + error['ErrorMsg'])

    def onRspQryInvestorPosition(self, data, error, n, last):
        print(u'持仓回报')
        if error['ErrorID'] == 0:
            for key, value in data.items():
                print(str(key).decode('gbk') + ':' + str(value).decode('gbk'))
        else:
            print('ErrorID' + error['ErrorID'] + 'ErrorMsg' + error['ErrorMsg'])

    def onRspQryTradingAccount(self, data, error, n, last):
        print(u'账户查询回报')
        for key, value in data.items():
            print(str(key).decode('gbk') + ':' + str(value).decode('gbk'))
        for key, value in error.items():
            print(str(key).decode('gbk') + ':' + str(value).decode('gbk'))


    #def onRtnOrder(self, data):


    # 以下为主动函数
    def login(self, userid, passwd, address, brokerid):

        self.__address = address
        self.registerFront(address)
        self.init()
        sleep(0.5)

        self.subscribePrivateTopic(0)   # 数据重传模式设为从本日开始
        self.subscribePublicTopic(0)

        loginReq = {}
        loginReq['UserID'] = self.__userid = userid
        loginReq['Password'] = self.__passwd = passwd
        loginReq['BrokerID'] = self.__brokerid = brokerid
        self.__reqid += 1
        self.reqUserLogin(loginReq, self.__reqid)


    def qrySettlementInfo(self):
        # 在查询过后自动进行confirm

        req = {}
        req['BrokerID'] = self.__brokerid
        req['InvestorID'] = self.__userid

        self.__reqid += 1
        self.reqQrySettlementInfo(req, self.__reqid)

        self.__reqid += 1
        self.reqSettlementInfoConfirm(req, self.__reqid)

    def qryAccount(self):
        self.__reqid += 1
        loginReq = {}
        loginReq['UserID'] = self.__userid
        loginReq['Password'] = self.__passwd
        loginReq['BrokerID'] = self.__brokerid
        self.reqQryTradingAccount(loginReq, self.__reqid)

    def qryInvestor(self):
        self.__reqid += 1
        self.reqQryInvestor({}, self.__reqid)




def main():

    reqid = 0

    engine = EventDispatcher()
    engine.start()
    app = QtGui.QApplication(sys.argv)

    td = TestTdApi()
    td.registerEngine(engine)
    td.login('020956', '18936803910', 'tcp://180.168.146.187:10000', '9999')

    td.subscribePrivateTopic(1)
    td.subscribePublicTopic(1)
    
    #td.createFtdcTraderApi('')

    #td.registerFront("tcp://180.168.146.187:10000")

    #td.init()

    #td.qrySettlementInfo()

    #td.qryInvestor()
    #td.qryAccount()

    exit(app.exec_())


if __name__ == '__main__':
    main()

