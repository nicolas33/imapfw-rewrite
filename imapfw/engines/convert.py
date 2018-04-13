# The MIT License (MIT).
# Copyright (c) 2018-2018, Nicolas Sebrecht & contributors.

from .engine import Engine


class ConvertEngine(Engine):
    """Convert the first side into the second side (ASSUMED EMPTY)."""

    def __init__(self):
        self._masterProxy = None
        self._logger = None
        self._chans = None

    def init(self, masterProxy, logger, *chans):
        self._masterProxy = masterProxy
        self._logger = logger
        self._chans = chans

    def get_className(self):
        return self.__class__.__name__

    def run(self):
        self._logger.force('in ConvertEngine')
        self._masterProxy.stop_loop(self.get_className())
