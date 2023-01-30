#!/usr/bin/env python3
#-*-coding=utf-8 -*-

import time
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('log.txt')
handler.setLevel(logging.DEBUG)
LOG_FORMAT= "%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - line: %(lineno)d - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S %a"
LOGDIR = "./log/"
FNAME = "ciics.log"
console=logging.StreamHandler()
console.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.addHandler(console)
if os.path.exists(LOGDIR + FNAME):
    os.rename(LOGDIR + FNAME, LOGDIR + time.strftime("%H%M%S") + FNAME)
logging.basicConfig(level=logging.INFO,format=LOG_FORMAT,datefmt=DATE_FORMAT,filename= LOGDIR + FNAME)

'''
LOG_FORMAT= "%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - line: %(lineno)d - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S %a"
#FNAME = time.strftime("%Y-%m-%d %H-%M-%S",time.localtime())
FNAME = "ciics.log"
LOGDIR = "./log/"

if os.path.exists(LOGDIR + FNAME):
    os.rename(LOGDIR + FNAME, LOGDIR + time.strftime("%H%M%S") + FNAME)
    
logging.basicConfig(level=logging.INFO,format=LOG_FORMAT,datefmt=DATE_FORMAT,filename= LOGDIR + FNAME)
'''
