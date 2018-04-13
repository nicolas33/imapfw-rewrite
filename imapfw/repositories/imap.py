# The MIT License (MIT).
# Copyright (c) 2018-2018, Nicolas Sebrecht & contributors.


from .repository import Repository


class ImapRepository(Repository):
    """The base class for all the IMAP repositories."""

    def __init__(self):
        self._chan = None
        self._masterProxy = None
        self._logger = None

    def init(self, masterProxy, logger, chan, *chans):
        self._masterProxy = masterProxy
        self._logger = logger
        self._chan = chan

    def loop(self):
        self._logger.force('in ImapRepository')
