#!/usr/bin/env python3
#-*-coding=utf-8 -*-

import time
import os
import logging


LOG_FORMAT= "%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - line: %(lineno)d - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S %a"
#FNAME = time.strftime("%Y-%m-%d %H-%M-%S",time.localtime())
FNAME = "casjc.log"
LOGDIR = "../../GKJY-TEST/static/log/"

#if os.path.exists(LOGDIR + FNAME):
#    os.rename(LOGDIR + FNAME, LOGDIR + FNAME + time.strftime("%H%M%S"))
    
logging.basicConfig(level=logging.INFO,format=LOG_FORMAT,datefmt=DATE_FORMAT,filename= LOGDIR + FNAME)
