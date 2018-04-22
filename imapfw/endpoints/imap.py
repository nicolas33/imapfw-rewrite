# The MIT License (MIT).
# Copyright (c) 2018-2018, Nicolas Sebrecht & contributors.

from time import sleep

from imapfw.constants import SLEEP_LOOP
from imapfw.core import dispatch_req


class ImapEndpointProxy(object):
    def __init__(self, logger, chan):
        self._logger = logger
        self._chan = chan
        self._reader = None
        self._writer = None

    def init(self):
        self._reader = self._chan.create_upstreamReader()
        self._writer = self._chan.create_upstreamWriter()


class ImapEndpoint(object):
    """Controllers and R/W drivers for IMAP.

    Obeys to the ImapRepository worker."""

    cls_proxy = ImapEndpointProxy
    drivers = [] # Usually one (R/W) driver.
    controllers = [] # Chain of controllers.
    dispatch_req = dispatch_req

    def __init__(self):
        self._chan = None
        self._driver = None
        self._masterProxy = None
        self._logger = None
        self._reader = None
        self._writer = None
        self._loop = True

    def init(self, masterProxy, logger, chan):
        self._masterProxy = masterProxy
        self._logger = logger
        self._chan = chan
        self._reader = chan.create_downstreamReader()
        self._writer = chan.create_downstreamWriter()

    def build_driver(self, cls_driver, cls_controllers):
        self._logger.force('in build_driver')
        return
        driver = cls_driver()
        for cls_controller in reversed(cls_controllers):
            driver = cls_controller(driver)
        self._driver = driver

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
        self._logger.force("in ImapEndpoint")
        try:
            while self._loop is True:
                if self.run() is not True:
                    sleep(SLEEP_LOOP)
        except Exception as e:
            # send failure to repository worker.
            self._logger.force('Oops: {}'.format(e))
        self._logger.force("out ImapEndpoint")
