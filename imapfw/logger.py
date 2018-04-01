# The MIT License (MIT).
# Copyright (c) 2018-2018, Nicolas Sebrecht & contributors.


class Logger(object):
    def __init__(self):
        self._chan = None
        self._enabled_logs = []

    def init(self, chan):
        self._chan = chan

    def enable(self, *luids):
        for luid in luids:
            self._enabled_logs.append(luid)

    def loop(self):
        while True:
            req = self._chan.get()
            if req is None:
                break
            luid, typ, data = req
            if luid in self._enabled_logs:
                print(data)
