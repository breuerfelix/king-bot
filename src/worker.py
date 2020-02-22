#!/usr/bin/env python
# coding:utf-8

import threading

_threads = {}

class worker (threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
        if target:
            args.insert(0, self)
        super(worker, self).__init__(group, target, name, args, kwargs)
        _threads[self] = self # store thread in dict
        self._event = threading.Event() # start threading Event
        #if len(_threads) == 1:
        self._event.set() # resume the first thread

    def wait(self):
        self._event.wait() # block if paused

    def pause(self):
        for thread in _threads:
            if self.name not in thread.name:
                thread._event.clear() # pause thread

    def resume(self):
        for thread in _threads:
            if self.name not in thread.name:
                thread._event.set() # resume thread