# -*- coding: utf-8 -*-

import getopt
import sys
import urllib2

from loger import Logger
import json
from parser import HParser

global syncdir   #更新地址
global logdir    #日志存放地址
global checktime #检查时间间隔
global upstream  #上游源地址

urllist = ["/","/extras/auto/","/extras/gapid/","/extras/intel/"]

crlog = Logger()

# 程序入口,参数操作
option,args = getopt.getopt(sys.argv[1:],"Vhs:",["version","help","start","stop","status"])
for key,value in option:
    if key in ("-V","--version"):
        print "current version" #待定
    if key in ("-h","--help"):
        print "args list"       #待定
    if key == ("-s"):
        if value == "start":
            print "start task"  #待定
            break
        elif value == "stop":
            print "stop task"   #待定
            break
        elif value == "status":
            print "return current status"  #待定
            break
    if key in ("--start"):
        print "start task"      #待定  value为配置脚本路径
        #crlog.info("啦啦")
        #crlog.info("fdssfdfdsfs")    #日志测试
        #crlog.debug("sdssssssssssssssssssssssss")
    if key in ("--stop"):
        print "stop task"       #待定
    if key in ("--status"):
        print "return current status"      #待定


# 检测并加载配置文件
def pconfig():
    global syncdir
    global logdir
    global checktime
    global upstream
    filejs = open("assm.conf", "r")
    decoded = json.loads(filejs.read())
    filejs.close()
    syncdir = decoded["syncdir"]
    logdir = decoded["logdir"]
    checktime = decoded["checktime"]
    upstream = decoded["upstream"]



#获取下载列表
def getlist(url):
    #url = "http://mirrors.opencas.cn/android/repository/"
    str = urllib2.urlopen(url, timeout=10).read()
    my = HParser()
    my.feed(str)
    strlist = my.xs
    newdat = []

    for x in range(0, len(strlist)):
        if strlist[x].split('.')[-1] == "xml":
            newdat.append(strlist[x])
        if strlist[x].split('.')[-1] == "zip":
            newdat.append(strlist[x])
    for x in newdat:
        print url+x
    #return newdat



pconfig()
getlist(upstream+urllist[0])
getlist(upstream+urllist[1])
getlist(upstream+urllist[2])
getlist(upstream+urllist[3])
