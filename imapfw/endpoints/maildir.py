# The MIT License (MIT).
# Copyright (c) 2018-2018, Nicolas Sebrecht & contributors.


class MaildirEndpoint(object):
    """Controllers and R/W drivers for the state.

    Obeys to the MaildirRepository worker."""

    def __init__(self):
        self._chan = None
        self._driver = None
        self._masterProxy = None
        self._logger = None
        self._reader = None
        self._writer = None

    def init(self, masterProxy, logger, chan):
        self._masterProxy = masterProxy
        self._logger = logger
        self._chan = chan
        self._reader = chan.create_downstreamReader()
        self._writer = chan.create_upstreamWriter()

    def loop(self):
        self._logger.force("in MaildirEndpoint")
