# -*- coding: utf-8 -*-
# encoding:utf-8

import sys
import logging
import time

#__metaclass__ = type

class Logger(object):
    # 构造函数初始化日志类的相关配置
    def __init__(self,logdir):
        filename = time.strftime('%Y-%m-%d',time.localtime(time.time())) # 获取当前时间
        logging.basicConfig(level = logging.DEBUG,
                            format = '%(asctime)s [%(levelname)s] %(message)s',
                            datefmt ='%Y-%m-%d %H:%M:%S',
                            filename = logdir + "assm " + filename + ".log",
                            filemode = 'a'
        )
        # 日志输出到控制台
        tlog = logging.StreamHandler()
        tlog.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        tlog.setFormatter(formatter)
        logging.getLogger("").addHandler(tlog)

    def debug(self,msg):
        logging.debug(str(msg))

    def info(self, msg):
        logging.info(str(msg))

    def warning(self, msg):
        logging.warning(str(msg))

    def error(self, msg):
        logging.error(str(msg))

    def critical(self, msg):
        logging.critical(str(msg))