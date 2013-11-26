# -*-coding: UTF-8-*-
import time,re
from HotTopic import HotTopic
from Login import Login

login = Login('noucamp20@gmail.com','yiyifanfan')
login.login()

#每天的话题
''''
topic = HotTopic(login.gsid)
topic.hot_topic()

'''

#
''''''
#搜话题
topic = HotTopic(login.gsid)
for eachline in file('key.txt','r'):
    print eachline
    print type(eachline)
    topic.linkProducer(eachline.strip())
