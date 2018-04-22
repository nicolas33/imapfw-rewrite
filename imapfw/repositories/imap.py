# The MIT License (MIT).
# Copyright (c) 2018-2018, Nicolas Sebrecht & contributors.

from time import sleep

from imapfw.endpoints.imap import ImapEndpoint
from imapfw.constants import SLEEP_LOOP
from imapfw.core import dispatch_req
from .repository import Repository


class ImapRepositoryProxy(object):
    def __init__(self, logger, chan):
        self._logger = logger
        self._chan = chan
        self._reader = chan.create_upstreamReader()
        self._writer = chan.create_upstreamWriter()

    def stop_loop(self):
        self._writer.put(('stop_loop', (), {}))


class ImapRepository(Repository):
    """The base class for all the IMAP repositories."""

    cls_endpoint = ImapEndpoint
    cls_proxy = ImapRepositoryProxy
    dispatch_req = dispatch_req

    def __init__(self):
        self._chan = None
        self._chans = None
        self._endpointProxies = []
        self._masterProxy = None
        self._logger = None
        self._loop = True
        self._reader = None
        self._writer = None

    def init(self, masterProxy, logger, chan, *chans):
        self._masterProxy = masterProxy
        self._logger = logger
        self._chan = chan
        self._chans = chans
        self._reader = chan.create_downstreamReader()
        self._writer = chan.create_downstreamWriter()
        for chan in self._chans:
            proxy = self.cls_endpoint.cls_proxy(self._logger, self._chan)
            proxy.init()
            proxy.build_driver()
            self._endpointProxies.append(proxy)
        self.on_init()

    def on_init(self):
        pass

    def on_loop(self):
        pass

    def stop_loop(self):
        self._loop = False

    def run(self):
        got_request = False
        m_req = self._masterProxy.get_nowait()
        if m_req is not None:
            got_request = True
            self.dispatch_req(m_req)
        req = self._reader.get_nowait()
        if req is not None:
            got_request = True
            self.dispatch_req(req)
        return got_request

    def loop(self):
        self._logger.force('in ImapRepository')
        self.on_loop()
        try:
            while self._loop is True:
                if self.run() is True:
                    sleep(SLEEP_LOOP)
        except Exception as e:
            # send failure to repository manager.
            self._logger.force('Oops: {}'.format(e))
        self._logger.force('out ImapRepository')
