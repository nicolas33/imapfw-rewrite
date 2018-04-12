# The MIT License (MIT).
# Copyright (c) 2018-2018, Nicolas Sebrecht & contributors.

from time import sleep

from imapfw.constants import SLEEP_LOOP


class LoggerProxy(object):
    def __init__(self, chan):
        self._writer = chan.create_downstream_writer()

    def enable(self, *luids):
        """Enabling logs is racy when done from workers."""

        self._writer.put_nowait(('__ENABLE__', None, luids))

    def force(self, msg, luid=None):
        self._writer.put_nowait(('__FORCE__', msg, luid))

    def debug(self, msg, luid=None):
        self._writer.put_nowait(('__DEBUG__', msg, luid))

    def exception(self, e, luid=None):
        self._writer.put_nowait(('__EXCEPTION__', str(e), luid))

    def warning(self, msg, luid=None):
        self._writer.put_nowait(('__WARNING__', msg, luid))

    def info(self, msg, luid=None):
        self._writer.put_nowait(('__INFO__', msg, luid))

    def stop_service(self, sleep_time=0):
        self._writer.put_nowait(('__STOP_SERVICE__', sleep_time, None))


class Logger(object):
    CLS_PROXY = LoggerProxy

    def __init__(self):
        self._chan = None
        self._enabled_logs = []
        self._reader = None

    def init(self, _mngrLink, _logger, chan):
        self._chan = chan
        self._reader = chan.create_downstream_reader()

    def enable(self, *luids):
        for luid in luids:
            self._enabled_logs.append(luid)

    def loop(self):
        while True:
            req = self._reader.get_nowait()
            if req is None:
                sleep(SLEEP_LOOP)
                continue
            typ, data, luid = req
            if luid in self._enabled_logs or typ == '__FORCE__':
                print(data)
            if typ == '__ENABLE__':
                self.enable(*luid)
            if typ == '__STOP_SERVICE__':
                sleep(data)
                break
