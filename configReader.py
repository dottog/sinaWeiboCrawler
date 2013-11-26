# -*- coding: utf8 -*-
import MySQLdb
import ConfigParser  
        
def dbCursorInit(configFilePath):
    try:
        cf = ConfigParser.ConfigParser() 
        cf.read(configFilePath)
        db_host = cf.get("baseconf", "host")  
        db_user = cf.get("baseconf", "user")  
        db_pwd = cf.get("baseconf", "password") 
        db_name = cf.get("baseconf", "db_name") 
        db_port = cf.getint("baseconf", "port")  

        conn = MySQLdb.connect(host="%s" %db_host,
                user="%s" %db_user ,passwd="%s" %db_pwd,
                db="%s" %db_name, charset="utf8")  
        return  conn   
    except Exception,e:
        print e


