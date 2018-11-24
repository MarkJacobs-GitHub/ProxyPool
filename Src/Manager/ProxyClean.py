# -*- coding: utf-8 -*-
# !/usr/bin/env python

import sys
sys.path.append("Src")
import time
import threading

from Manager.ProxyManager import ProxyManager
from Log.LogManager import log
from Config.ConfigManager import config

try:
    from Queue import Queue  # py3
except:
    from queue import Queue  # py2

# 这样的实现多线程有问题, 后期无法扩展到独立的进程.
# must call classmethod initQueue before when thread start
class ProxyClean(threading.Thread):
    def __init__(self, **kwargs):
        super(ProxyClean, self).__init__(**kwargs)
        self.proxy_manager = ProxyManager()

class ProxyCleanUseful(ProxyClean):

    def run(self):
        hold_number = config.BASE.hold_useful_proxy_number
        clean_number = self.proxy_manager.cleanUsefulProxy(hold_number=hold_number)
        total_number = self.proxy_manager.getUsefulProxyNumber()

        log.info("clean useful, total_number:{total_number}, clean_number:{clean_number}, hold_number:{hold_number}".format(total_number=total_number, clean_number=clean_number, hold_number=hold_number))

class ProxyCleanRaw(ProxyClean):

    def run(self):
        hold_number = config.BASE.hold_raw_proxy_number
        clean_number = self.proxy_manager.cleanRawProxy(hold_number=hold_number)
        total_number = self.proxy_manager.getRawProxyNumber()

        log.info("clean raw_proxy, total_number:{total_number}, clean_number:{clean_number}, hold_number:{hold_number}".format(total_number=total_number, clean_number=clean_number, hold_number=hold_number))

if __name__ == "__main__":
    t1 = ProxyCleanUseful()
    t1.daemon = True
    t1.start()

    t2 = ProxyCleanRaw()
    t2.daemon = True
    t2.start()

    t1.join()
    t2.join()