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
        self._writer.put(('error', cls_requesterName, msg))

    def stop_loop(self, cls_requesterName, msg=''):
        self._writer.put(('stop_loop', cls_requesterName, msg))

    def stop_app(self, cls_requesterName, msg):
        self._writer.put(('stop_app', cls_requesterName, msg))


#TODO: make this singleton.
class MasterManager(object):
    """Must be run in main."""

    def __init__(self):
        self._chan = Chan(MultiProcessingBackend)
        self._reader = self._chan.create_upstreamReader()
        self._writer = self._chan.create_upstreamWriter()
        self._loop = True
        self._mainRunners = []

    def add_mainRunners(self, *mainRunners):
        for mainRunner in mainRunners:
            self._mainRunners.append(mainRunner)

    def create_proxy(self):
        return MasterProxy(self._chan)

    def on_error(self, cls_requesterName, msg):
        pass

    def on_stop_loop(self, cls_requesterName, msg):
        pass

    def on_stop_app(self, cls_requesterName, msg):
        pass

    def stop_loop(self, cls_requesterName, msg):
        self._loop = False
        self.on_stop_loop(cls_requesterName, msg)

    def error(self, cls_requesterName, msg):
        self.on_error(cls_requesterName, msg)

    def stop_app(self, cls_requesterName, msg):
        msg = "{} requested exit: {}".format(cls_requesterName, msg)
        raise RuntimeError(msg)

    def run(self, *mainRunners):
        req = self._reader.get_nowait()
        if req is not None:
            methodName, cls_requesterName, msg = req
            getattr(self, methodName)(cls_requesterName, msg)
        for run in self._mainRunners:
            run()

    def loop(self, *mainRunners):
        while self._loop is True:
            try:
                self.run(*mainRunners)
            except StopLoop:
                break
            # Let RuntimeError bubble up.
