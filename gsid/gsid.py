# -*-coding: UTF-8-*-
import re,urllib2,urllib

def Get_Post_Gsid(opener,email,pwd,url):
    pattern_post = re.compile(r'''<input .+"(.*?)".+"(.*?)".+"(.*?)"''')
    post_list = []

    while True:
        login_1 = urllib2.Request(url)
        login_1.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.1.14) Gecko/20080404 (FoxPlus) Firefox/2.0.0.14')    
        login_html = opener.open(login_1).read()
        post_get = re.findall(pattern_post,login_html)
        #raw_input(post_get)
        for elem in post_get:
            if elem[0] == "mobile":
                post_list.append("mobile="+email)
                continue
            elif "password" in elem[0]:
                post_list.append(elem[0]+"="+pwd)
                continue
            elif elem[0] == "checkbox":
                post_list.append("remember=on")
                continue
            elif elem[0] == "hidden":
                post_list.append(elem[1]+'='+urllib.quote(elem[2]))
                continue
            elif elem[0] == "submit":
                post_list.append(elem[1]+"="+elem[2])
                continue
        if not '=' in post_list:
            post_data = '&'.join(post_list)
            #raw_input(post_data)
            print post_data
            break
        else:
            print "failed to get the post data and try to get again"

    while True:
        gsid = []
        req = urllib2.Request(url,post_data)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.1.14) Gecko/20080404 (FoxPlus) Firefox/2.0.0.14')
        try:
            res = opener.open(req).read()
            #print res
            #print res.decode('utf-8').encode('gb2312')
            pattern = re.compile('''gsid=(.*?)&''')#提取gsid
            gsid = re.findall(pattern, res)
            print gsid
            if gsid != []:
                print "sucessed and begin to crawl..."
                break
        except Exception,data:
            print "login1 failes and login1 again"
            print data
            break
    return gsid
