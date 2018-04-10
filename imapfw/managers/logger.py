# The MIT License (MIT).
# Copyright (c) 2018-2018, Nicolas Sebrecht & contributors.


from imapfw.channel import Chan
from imapfw.logger import LoggerProxy
from .runners import loopRunner


class LoggerManager(object):
    def __init__(self):
        self._backend = None
        self._chan = None
        self._errorLink = None
        self._worker = None
        self._cls_logger = None

    def init(self, cls_logger, backend, errorLink):
        self._cls_logger = cls_logger
        self._backend = backend
        self._errorLink = errorLink
        self._chan = Chan(self._backend)

    def create_proxy(self):
        return self._cls_logger.CLS_PROXY(self._chan)

    def start(self):
        logger_proxy = self.create_proxy()
        self._worker = self._backend.create_worker(
            "logger",
            loopRunner,
            (self._cls_logger, self._errorLink, logger_proxy, self._chan),
        )
        self._worker.start()

    def stop(self, sleep_time=0):
        proxy = self.create_proxy()
        proxy.stop_service(sleep_time)
        self._worker.join()

    def kill(self):
        self._worker.kill()
        self._worker.join()
