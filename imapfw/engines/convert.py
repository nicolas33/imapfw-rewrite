# The MIT License (MIT).
# Copyright (c) 2018-2018, Nicolas Sebrecht & contributors.

from .engine import Engine


class ConvertEngine(Engine):
    """Convert the first side into the second side (ASSUMED EMPTY)."""

    def __init__(self):
        self._mngrLink = None
        self._logger = None
        self._chans = None

    def init(self, mngrLink, logger, *chans):
        self._mngrLink = mngrLink
        self._logger = logger
        self._chans = chans

    def run(self):
        self._logger.force('in ConvertEngine')
