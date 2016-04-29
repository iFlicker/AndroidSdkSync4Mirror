# -*- coding: utf-8 -*-

import getopt
import os
import sys
import urllib
import urllib2
import json
import time

from loger import Logger
from parser import Hparser

global syncdir   #更新地址
global logdir    #日志存放地址
global checktime #检查时间间隔
global upstream  #上游源地址

global flags
flags = "null"
global timee
timee = [0]

urllist = ("/","/extras/auto/","/extras/gapid/","/extras/intel/","/sys-img/android/","/sys-img/android-tv/","/sys-img/android-wear/","/sys-img/google_apis/","/sys-img/x86/")

crlog = Logger(logdir) #实例化日志管理类
my = Hparser()   #实例化解析类


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
    my.feed(str)
    strlist = my.xs
    newdat = []

    for x in range(0, len(strlist)):
        if strlist[x].split('.')[-1] == "xml":
            newdat.append(strlist[x])
        if strlist[x].split('.')[-1] == "zip":
            newdat.append(strlist[x])
    my.xs = []
    return newdat

#urllib.urlretrieve的参数reporthook回调函数
def report(count, blockSize, totalSize):
    global timee
    #按50个块为一个计速单位
    if count%50==0:
        timee.append(time.time())
    sped =  int(( ((blockSize*50)/(timee[-1]-timee[-2])) / (1000*1000) )*1000)
    sped = str(sped) + "Kb/s"
    percent = int(count*blockSize*100/totalSize)
    view_bar(num=percent,sum=100,bar_word=":",speed=sped)

#显示下载进度,由urllib.urlretrieve的参数reporthook回调函数report()来调用
def view_bar(num=1, sum=100, bar_word=":",speed="0"):
    global flags
    global timee
    rate = float(num) / float(sum)
    rate_num = int(rate * 100)
    print '\r%d%% :' %(rate_num),
    for i in range(0, num):
        os.write(1, bar_word)
    os.write(1,speed)
    if num == sum:
        print "complete"
        flags = "complete"
        timee = [0]
    sys.stdout.flush()

#任务开始
def taskbegin():

    pass

#按时调动taskbegin
def timecycle():

    pass

#检查fileHeader_Last-Modified-Time
def checkfile(url):
    tmpres = urllib2.urlopen(url)
    lmt = tmpres.info().getheader('Last-Modified')
    # last work point ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    pass

def listanalyser(url):

    pass

#下载并写入status.list
def downandwrite(liist):
    global syncdir
    global upstream
    for x in liist:
        urllib.urlretrieve(upstream + x, syncdir+ x, reporthook=report)

    pass

#判断是不是第一次运行
def isFirstrun():

    global syncdir
    if not os.path.exists("./status.list"):
        crlog.info("first run")
        #创建文件夹
        crlog.info("create related directory")
        for x in urllist:
            os.makedirs(syncdir + x)

        # 传入list并调用downandwrite()
        pass
    else:
        crlog.info("not first, will check last sync time")
        # 调用 检查上次更新时间 函数
        pass
    pass

#默认执行顺序列表
pconfig()
for x1 in getlist(upstream+urllist[0]):
    print x1
for x2 in getlist(upstream+urllist[1]):
    print x2
for x3 in getlist(upstream+urllist[2]):
    print x3
for x4 in getlist(upstream+urllist[3]):
    print x4
for x5 in getlist(upstream+urllist[4]):
    print x5
for x6 in getlist(upstream+urllist[5]):
    print x6
for x7 in getlist(upstream+urllist[6]):
    print x7
for x8 in getlist(upstream+urllist[7]):
    print x8
for x9 in getlist(upstream+urllist[8]):
    print x9


