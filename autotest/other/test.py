#!/usr/bin/env python3

from multiprocessing import Process
import time, sys, queue, os
from multiprocessing.managers import BaseManager
import userInfo
import threading

'''
print("Global pid %s "%os.getpid())
print('worker exit.')
'''
class a():
    def __init__(self):
        self.object = "abc"
    def bb(self):
        print(self.object)
ll = a()
ll.bb()
