# The MIT License (MIT).
# Copyright (c) 2018-2018, Nicolas Sebrecht & contributors.


from imapfw.channel import Chan
from .runners import loopRunner


class LoggerProxy(object):
    def __init__(self, chan):
        self._chan = chan

    def exception(self, luid, e):
        self._chan.put((luid, '__EXCEPTION__', str(e)) #TODO: improve this.

    def info(self, luid, msg):
        self._chan.put((luid, '__INFO__', str(e)) #TODO: improve this.

    def warning(self, luid, msg):
        self._chan.put((luid, '__WARNING__', str(e)) #TODO: improve this.


class LoggerManager(object):
    def __init__(self):
        self._backend = None
        self._chan = None
        self._errorLink = None
        self._proxy = None
        self._worker = None
        self._logger = None

    def init(self, logger, backend, errorLink):
        self._logger = logger
        self._backend = backend
        self._errorLink = errorLink
        self._chan = Chan(self._backend)
        self._proxy = LoggerProxy(self._chan)

    def get_proxy(self):
        return self._proxy

    def start(self):
        self._worker = self._backend.create_worker(
            "logger",
            loopRunner,
            (self._logger, self._errorLink, self._proxy),
        )
        self._worker.start()

    def stop(self):
        pass

    def kill(self):
        pass


