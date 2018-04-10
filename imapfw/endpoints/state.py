# The MIT License (MIT).
# Copyright (c) 2018-2018, Nicolas Sebrecht & contributors.


class StateEndpoint(object):
    def __init__(self):
        self._chan = None
        self._errorLink = None
        self._logger = None

    def init(self, errorLink, logger, chan):
        self._errorLink = errorLink
        self._logger = logger
        self._chan = chan

    def loop(self):
        self._logger.force("in ImapEndpoint")
