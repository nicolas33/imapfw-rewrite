# The MIT License (MIT).
# Copyright (c) 2018-2018, Nicolas Sebrecht & contributors.


from .runners import oneshotRunner


class Engine(object):
    def __init__(self):
        self._backend = None
        self._chans = None
        self._cls_engine = None
        self._errorLink = None
        self._logger = None
        self._worker = None

    def init(self, cls_engine, errorLink, logger, *chans):
        self._cls_engine = cls_engine
        self._errorLink = errorLink
        self._logger = logger
        self._chans = chans

    def set_backend(self, backend):
        self._backend = backend

    def start(self):
        self._worker = self._backend.create_worker(
            self._cls_engine.__name__,
            oneshotRunner,
            (self._cls_engine, self._errorLink, self._logger, *self._chans),
        )
        self._worker.start()

    def join(self):
        self._worker.join()
