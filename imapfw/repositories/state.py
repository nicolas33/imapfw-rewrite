# The MIT License (MIT).
# Copyright (c) 2018-2018, Nicolas Sebrecht & contributors.


from .repository import Repository


class StateRepository(Repository):
    """The base class for all the State repositories."""

    def __init__(self):
        self._chan = None
        self._mngrLink = None
        self._logger = None

    def init(self, mngrLink, logger, chan, *chans):
        self._mngrLink = mngrLink
        self._logger = logger
        self._chan = chan

    def loop(self):
        self._logger.force('in ImapRepository')
