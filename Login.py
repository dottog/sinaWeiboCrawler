# -*-coding: UTF-8-*-

import re,StringIO ,time ,os,shutil ,urllib,urllib2,string,cookielib,urllib,datetime
import hashlib ,binascii,locale,codecs,threading,socket
import gsid.gsid as Gsid
import cPickle as pickle



class Login():
    def __init__(self,email,passwd):
        self.email = email
        self.pwd = passwd
        self.gsid = ''
    def login(self):
        print 'now login.....'
        self.url = "http://3g.sina.com.cn/prog/wapsite/sso/login.php" #登录地址,手机新浪网
        gsid = []
        cj = cookielib.LWPCookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        gsid = Gsid.Get_Post_Gsid(self.opener,self.email,self.pwd,self.url)
        print 'login successfully!'
        self.gsid = gsid[0]
    def OpenPage(self,aim): 
        request = urllib2.Request(aim)
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.1.14) Gecko/20080404 (FoxPlus) Firefox/2.0.0.14')
        socket.setdefaulttimeout(10)
        try:
            PageContent =  self.opener.open(request).read()#请求网页的html
            return PageContent
        except Exception,data:
            print data
