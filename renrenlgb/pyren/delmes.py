# -*- coding: utf-8 -*-
import urllib2, cookielib, urllib, time

userName = '13613112728'#你的账户
passWord = '075100'#你的密码
myUserId = '256593238'#你的ID
destUserId = '278877089'#想删除的美眉的ID
loginAddr = 'http://www.renren.com/PLogin.do'
getMsgAddr = 'http://gossip.renren.com/getconversation.do'
delMsgAddr = 'http://gossip.renren.com/delgossip.do'
#headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5'}
headers = {'User-Agent':' Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0'}
#headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:7.0.1) Gecko/20100101 Firefox/7.0.1'}
#headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
class MsgStruct(object):
    def __init__(self, id_p, owner_id):
        self.id = id_p
        self.owner = owner_id
class RenrenProcessor(object):
    def __init__(self):
        self.msgList = []
        self.cj = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
        self.opener = urllib2.build_opener(self.cj, urllib2.HTTPHandler)
        urllib2.install_opener(self.opener)
    def loginRenren(self):
        params = {"email":userName, "password":passWord}
        params = urllib.urlencode(params)
        params = params.encode('utf-8')
        req = urllib2.Request(url = loginAddr, data = params, headers = headers)
        response = urllib2.urlopen(req) 
        f = open("renren.html", "wb")
        f.write(response.read())
    def getId(self, text, startIndex):
        startI = text.find('"', startIndex)
        endI = text.find('"', startI + 1)
        return text[startI+1: endI]
    def dealMsgText(self, text):
        del self.msgList[:]
        num1 = 0
        num2 = 0
        while True:
            num1 = text.find('id', num1+1)
            num2 = text.find('owner', num2+1)
            if num1 == -1:
                break
            self.msgList.append(MsgStruct(self.getId(text, num1+4), self.getId(text, num2+7)))
        return len(self.msgList)
    def getMsgList(self):
        params = {'guest':destUserId, 'curpage':'0', 'destpage':'0', 'hostBeginId':'', 'hostEndId':'','guestBeginId':'', 'guestEndId':'', 'page':'undefined', 'id':destUserId, 'resource':'0','search':'0', 'boundary':'0', 'gossipCount':'0', 'requestToken':'-134632329','_rtk':'c3baaad1'}
    #该处的requestToken与_rtk截取下数据可以得到，或者用这个可能也可以，可以尝试下。
        params = urllib.urlencode(params)
        params = params.encode('utf-8')
        req = urllib2.Request(url = getMsgAddr, data = params, headers = headers)

        tmp = open("req.html","wb")
        tmp.write(rep.read())
        response = urllib2.urlopen(req)
        f = open("msg.html", "wb")
        f.write(response.read())
        return self.dealMsgText(response.read())

    def delMsg(self, curMsgIndex):
        msgcount = 1
        for item in self.msgList:
            params = {'id':item.id, 'owner':item.owner, 'age':'recent', 'requestToken':'-134632329','_rtk':'c3baaad1'}
            params = urllib.urlencode(params)
            params = params.encode('utf-8')
            req = urllib2.Request(url = delMsgAddr, data = params, headers = headers)
            response = urllib2.urlopen(req)
            print 'deleting the msg id: %s, msg owner: %s' % (item.id, item.owner)
            msgcount = msgcount + 1
            time.sleep(1.5)#太快了好像会卡住

msgNum = 0
instance = RenrenProcessor()
print 'start to login renren'
instance.loginRenren()
while True:
    print 'calc message num'
    curMsgNum = instance.getMsgList()
    print "we have %d message need to delete" % curMsgNum
    if curMsgNum == 0 :
        break
    instance.delMsg(msgNum)
    msgNum = msgNum + curMsgNum 


print 'delete the all message(%d)' % msgNum#统计下你和MM一共发了多少～～
