# -*- coding: utf-8 -*-
# encoding:utf-8

import sys
import logging
import time

#__metaclass__ = type

class Logger(object):
    def __init__(self):
        filename = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        logging.basicConfig(level = logging.DEBUG,
                            format = '%(asctime)s [%(levelname)s] %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename = filename + ".log",
                            filemode = 'a'
        )

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