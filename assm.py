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

global downflag
downflag = False
global flags
flags = "null"
global timee
timee = [0]
global urllist
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


#tools->获取下载列表
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

#tools->分别获取所有目录下的文件,挑出xml单独放入
def supergetlist(url):
    global urllist
    allist = [[] for i in range(10)]

    allist[0] = getlist(url + urllist[0])
    allist[1] = getlist(url + urllist[1])
    allist[2] = getlist(url + urllist[2])
    allist[3] = getlist(url + urllist[3])
    allist[4] = getlist(url + urllist[4])
    allist[5] = getlist(url + urllist[5])
    allist[6] = getlist(url + urllist[6])
    allist[7] = getlist(url + urllist[7])
    allist[8] = getlist(url + urllist[8])

    delallist = [[] for i in range(9)]
    #将xml元素存入allist[9],并标记入delallist
    for num in range(0,9):
        for strr in allist[num]:
            if "xml" in strr:
                allist[9].append(urllist[num] + strr)
                delallist[num].append(strr)  #将xml元素下标存入delallist
    # 删除xml元素
    for s in range(0,9):
        for sx in delallist[s]:
            allist[s].remove(sx)
    return allist

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

# tools->将unicode对象转为string对象
def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

# 检查本地status.list xml文件列表的lmt与上游源是否一致   未完成(调用休眠)
# 参数为 supergetlist的allist[9]
def checkxml(liist):
    global urllist
    global upstream
    filejs = open("status.list", "r")
    decoded = json.loads(filejs.read())
    filejs.close()
    decoded = byteify(decoded)
    nliist = {}
    for i in liist:
        nliist[i] = getlmt(upstream + i)
    for s in decoded["xml"]:
        if decoded["xml"][s] != nliist[s]:
            # 本地status.list xml和上游源的lmt不同,需要更新
            syncxml(liist,nliist)
            return 0
        else:
            continue

    # 没有return ,本地status.list xml和上游源的lmt相同,需要休眠
    # ***************************************************************
    #这儿调用休眠函数

# 更新下载xml文件 参数为 supergetlist的allist[9] ,存入xml
def syncxml(liist, nliist):
    global upstream
    global syncdir
    for s in liist:
        x = s.split("/")
        ss = s.replace(x[-1], "")
        crlog.info("download " + s)
        urllib.urlretrieve(upstream + s,syncdir + ss , reporthook=report)
    # 将新lmt和文件名写入status.list
    filejs = open("status.list", "r")
    decoded = json.loads(filejs.read())
    filejs.close()
    decoded = byteify(decoded)
    for k in nliist:
        decoded["xml"][k] = nliist[k]

    filejss = open("status.list", "w")
    filejss.truncate()
    filejss.write(json.dumps(decoded))
    filejss.close()
    return 0

# 第一次运行时 更新下载xml文件        (未完成)
def syncxml_first(liist):

    pass



# tools->返回url的Last-Modified time
def getlmt(url):
    tmpres = urllib2.urlopen(url)
    lmt = tmpres.info().getheader('Last-Modified')
    return lmt


# tools->下载
# 参数为 supergetlist()返回的list
def downandwrite(liist):
    global downflag
    global urllist
    global syncdir
    global upstream
    for i in range(0,9):
        for x in i:
            # 检查文件是否存在,存在就跳过,不存在就下载
            if os.path.exists(syncdir + urllist[i] + x):
                continue
            else:
                try:
                    urllib.urlretrieve(upstream + urllist[i] + x, syncdir + urllist[i] + x, reporthook=report)
                except Exception,arg:
                    crlog.error(arg)
                    if arg == "timed out" and os.path.exists(syncdir + urllist[i] + x):
                        try:
                            os.remove(syncdir + urllist[i] + x)
                        except Exception:
                            crlog.error("delete Failed file failed...,pls check file permission!")
                    sys.exit(1)
            # 抛出异常,如果网络错误则删除current文件
    # 如果下载完毕,修改downflag为True, 表示下载完成
    downflag = True


#判断是不是第一次运行   (未完成)
def isFirstrun():

    global syncdir
    if not os.path.exists("./status.list"):  # status.list不存在, 然后初始化
        crlog.info("first run")
        #创建文件夹
        crlog.info("create related directory")
        for x in urllist:
            os.makedirs(syncdir + x)
        # 先下载更新xml

        # 再创建status.list
        # 传入list并调用downandwrite()
        pass
    else:                                    # status.list存在,
        crlog.info("not first, will check last sync time")
        # 调用 检查上次更新时间 函数
        pass
    pass


#任务开始      未完成(休眠)
def taskbegin():
    global downflag
    global syncdir
    global logdir
    global checktime
    global upstream
    global urllist
    # 获取所有文件信息
    all_list = supergetlist(upstream)
    # 检查上游源xml的lmt和本地status.list记录的是否相同
    # 如果相同则休眠,如果不同则更新xml文件并将新的lmt写进status.list
    checkxml(all_list[9])
    # 然后调用 downandwrite 下载文件
    downandwrite(all_list)
    # 判断 downflag
    if downflag:
        # 下载完成,任务结束进入休眠********************************
        pass
    #






#默认执行顺序列表
pconfig()



