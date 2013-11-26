# -*-coding: UTF-8-*-
import re,StringIO ,time ,os,shutil ,urllib,urllib2,string,cookielib,urllib,datetime
import hashlib ,binascii,locale,codecs,threading,socket
import gsid.gsid as Gsid
import cPickle as pickle
import MySQLdb
from Login import Login
from configReader import dbCursorInit

class HotTopic():

    def __init__(self, gsid):
        self.gsid = gsid
        self.conn = dbCursorInit("dbConfig.ini")
        self.cursor = self.conn.cursor()


    def getPageContent(self, url):
            print ""
            print ""
            print url
            print ""
            print ""
            request = urllib2.Request(url)
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.1.14) Gecko/20080404 (FoxPlus) Firefox/2.0.0.14')
            socket.setdefaulttimeout(10)
            try:
                cj = cookielib.LWPCookieJar()
                self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
                pageContentString =  self.opener.open(request).read()
                #print pageContentString
                return pageContentString
            except Exception,data:
                print data



    def getWeiboTime(self, weiboRawString):
        weiboRawString = weiboRawString.decode('utf-8')
        regx_time = '<span\sclass="ct">(.*?)&nbsp'.decode('utf-8')
        regx_id = 'id=".*?">'.decode('utf-8')
        weiboContent = re.sub(regx_id,'',weiboRawString)
        time = re.findall(regx_time,weiboContent)
        if len(time) > 0:
            time = time[0]
        else:
            time = ''
            print '!'
        if '分'.decode('utf-8') in time:
            time = re.findall(r'([0-9]{1,2})',time)
            if len(time):
                time_value = int(time[0])
                time = (datetime.datetime.now()-datetime.timedelta(minutes = time_value)).strftime('%Y-%m-%d %H:%M')
        if '今天'.decode('utf-8') in time:
            time = time.split(' ')[1]
            time = datetime.datetime.now().strftime('%Y-%m-%d')+' '+time
        if '月'.decode('utf-8') in time:
            time = time.replace('月'.decode('utf-8'),'-').replace('日'.decode('utf-8'),'')
            time = datetime.datetime.now().strftime('%Y')+'-'+time
        return time
   
    def mainCrawler(self,link, keyword):

        page = 1
        #regCount = '共(.*?)条'.decode('utf-8')
        regCount = '共(.*?)条'
        regNickRawString = 'class="nk" herf=(.*?)</a>'
        regNickRawString = 'class="nk" href=(.*?)</a>'.decode('utf-8')
        regNick = '>.*'.decode('utf-8')
        regTransmit = '"ctt">(.*?)</div>'.decode('utf-8')
        regTransmittedOriginal = '转发理由(.*?)赞'

        while(True):
            flag = 0
            print 'Page -->',page
            pageUrl = link + '&page='+str(page)+'&gsid='+str(self.gsid)#+'&st=1ac0'
            content = self.getPageContent(pageUrl)
            print  "-------------------------------------------------------------------------------------------------------------------"
            print  "-------------------------------------------------------------------------------------------------------------------"
            print  "-------------------------------------------------------------------------------------------------------------------"
            if content == None:
                print 'failed to find any content'
                break
            else:
                weiboCount = re.findall(regCount, content)
                if len(weiboCount):
                    print "weiboCount this page: ",weiboCount[0]
                else:
                    print "could not find any content by ", regCount

                regx_weibo = '<div\sclass="c"(.*?)<div\sclass="s">'
                weiboStringList = re.findall(regx_weibo,content)
                if len(weiboStringList) == 0:
                    break
                for weiboRawString in weiboStringList:
                    #weiboRawString
                    print ""
                    print "-----------------NEW WEIBO GOT----------------"
                    print ""
                    authorNick = ""
                    authorNickRawString = re.findall(regNickRawString, weiboRawString)
                    if authorNickRawString:
                        authorNick = re.findall(regNick,authorNickRawString[0])
                        if authorNick:
                            authorNick = authorNick[0][1:]
                            
                    weibo_time = self.getWeiboTime(weiboRawString)
                    print "authorNick: ", authorNick
                    print "weiboTime: ", weibo_time
                    transmitContent = ""
                    originalContent = ""

                    weiboTransmit = re.findall(regTransmit, weiboRawString)
                    if(weiboTransmit):
                        #print '内容: ',  weiboTransmit[0].replace('<span class="kt">', "").replace('</span>', '')
                        transmitContent = self.contentExtractor(weiboTransmit[0])
                        print "transmitContent:  ", transmitContent

                    if '转发了' in weiboRawString:
                        weiboTransmittedOriginalRawString = re.findall(regTransmittedOriginal, weiboRawString)
                        if(weiboTransmittedOriginalRawString):
                            #print "原始微博内容： ", weiboTransmittedOriginalRawString[0]
                            originalContent = self.contentExtractor(weiboTransmittedOriginalRawString[0])
                            print "originalContent: ", originalContent
                    self.dbWriter(keyword, authorNick, weibo_time, originalContent, transmitContent)


            page += 1
            time.sleep(7)
   
    def contentExtractor(self, rawString):
        result = rawString.replace('<span class="kt">', "").replace('</span>', '').replace('[a-z]', '')
        result = re.sub(r'[a-z]|[A-Z]','',result)
        result = re.sub(r'赞|收藏|转发|评论|来自|客户端|原文|点击查看|组图|显示地图','',result)
        result = re.sub(r'<|>|[|]|\\|\/|/\|//|%|;|&|:|=','',result)
        result = re.sub(r'"(.*?)"','',result)
        result = re.sub(r'----.*|\[[0-9]*\]','',result)
        return result

    def dbWriter(self, keyword, authorNick, weiboTime, originalContent, transmitContent):
        '''
        print keyword
        print authorNick
        print weiboTime
        print originalContent
        print transmitContent
        print type(keyword)
        '''
        sql = "insert into weibo_info (keyword, author_nick, weibo_time, original_content, transmit_content) values ('%s','%s','%s','%s','%s')" %(keyword, authorNick, str(weiboTime), originalContent, transmitContent)
   

        print sql
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            print "insert successfully"
        except Exception, e:
            print e

                    
    def linkProducer(self, keyword, startTime = '20130420', endTime = '20130510'):
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        link = 'http://weibo.cn/search/mblog?hideSearchFrame=&keyword=' + keyword + '&advancedfilter=1&' + 'starttime=' + startTime + '&endtime=' + endTime + '&sort=time'

        print ""
        print ""
        print link
        print ""
        print ""
        self.mainCrawler(link, keyword)
        #'&page=1&gsid=4uuS2ba21GAAPA0z6ssogeVFI7d&st=cec9'


