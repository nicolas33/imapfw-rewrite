# The MIT License (MIT).
# Copyright (c) 2018-2018, Nicolas Sebrecht & contributors.

from imapfw.workers.concurrency import MultiProcessingBackend
from imapfw.channel import Chan


class StopLoop(Exception):
    pass


#XXX: what happened? where? Let master take decisions.
class MasterProxy(object):
    def __init__(self, chan):
        self._reader = chan.create_downstreamReader()
        self._writer = chan.create_downstreamWriter()

    def get_nowait(self):
        return self._reader.get_nowait()

    def error(self, cls_requesterName, msg=''):
        self._writer.put(('__MASTER_ERROR__', cls_requesterName, msg))

    def stop_loop(self, cls_requesterName, msg=''):
        self._writer.put(('__MASTER_STOP_LOOP__', cls_requesterName, msg))

    def stop_application(self, cls_requesterName, msg):
        self._writer.put(('__MASTER_EXIT__', cls_requesterName, msg))


#TODO: make this singleton.
class MasterManager(object):
    """Must be run in main."""

    def __init__(self):
        self._chan = Chan(MultiProcessingBackend)
        self._reader = self._chan.create_upstreamReader()
        self._writer = self._chan.create_upstreamWriter()

    def create_proxy(self):
        return MasterProxy(self._chan)

    def on_error(self, cls_requesterName, msg):
        pass

    def _on_stopLoop(self, cls_requesterName, msg):
        pass

    def on_stop_application(self, cls_requesterName, msg):
        pass

    def run(self, *mainRunners):
        req = self._reader.get_nowait()
        if req is not None:
            typ, cls_requesterName, msg = req
            if typ == '__MASTER_STOP_LOOP__':
                self._on_stopLoop(cls_requesterName, msg)
                raise StopLoop(msg)
            if typ == '__MASTER_ERROR__':
                self.on_error(cls_requesterName, msg)
                raise StopLoop(msg)
            if typ == '__MASTER_EXIT__':
                self.on_stop_application(cls_requesterName, msg)
                msg = "{} requested exit: {}".format(cls_requesterName, msg)
                raise RuntimeError(msg)
        for func in mainRunners:
            func()

    def loop(self, *mainRunners):
        while True:
            try:
                self.run(*mainRunners)
            except StopLoop:
                break
            # Let RuntimeError bubble up.
