# The MIT License (MIT).
# Copyright (c) 2018-2018, Nicolas Sebrecht & contributors.


from .runners import oneshotRunner


class Engine(object):
    def __init__(self):
        self._backend = None
        self._chans = None
        self._cls_engine = None
        self._mngrLink = None
        self._logger = None
        self._worker = None

    def init(self, cls_engine, mngrLink, logger, *chans):
        self._cls_engine = cls_engine
        self._mngrLink = mngrLink
        self._logger = logger
        self._chans = chans

    def set_backend(self, backend):
        self._backend = backend

    def start(self):
        self._worker = self._backend.create_worker(
            self._cls_engine.__name__,
            oneshotRunner,
            (self._cls_engine, self._mngrLink, self._logger, *self._chans),
        )
        self._worker.start()

    def join(self):
        self._worker.join()


class EngineManager(object):
    def __init__(self):
        self._backend = None
        self._chans = None
        self._cls_engine = None
        self._mngrLink = None
        self._logger = None
        self._worker = None
        self._exitCode = 254

    def init(self, cls_engine, mngrLink, logger, *chans):
        self._cls_engine = cls_engine
        self._mngrLink = mngrLink
        self._logger = logger
        self._chans = chans

    def set_backend(self, backend):
        self._backend = backend

    def start(self):
        self._worker = self._backend.create_worker(
            self._cls_engine.__name__,
            oneshotRunner,
            (self._cls_engine, self._mngrLink, self._logger, *self._chans),
        )
        self._worker.start()

    def join(self):
        self._worker.join()

    def kill(self):
        self._worker.kill()
