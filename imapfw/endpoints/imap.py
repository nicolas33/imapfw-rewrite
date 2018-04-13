# The MIT License (MIT).
# Copyright (c) 2018-2018, Nicolas Sebrecht & contributors.


class ImapEndpoint(object):
    def __init__(self):
        self._chan = None
        self._masterProxy = None
        self._logger = None

    def init(self, masterProxy, logger, chan):
        self._masterProxy = masterProxy
        self._logger = logger
        self._chan = chan

    def loop(self):
        self._logger.force("in ImapEndpoint")
