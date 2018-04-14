# The MIT License (MIT).
# Copyright (c) 2018-2018, Nicolas Sebrecht & contributors.

from time import sleep

from imapfw.constants import SLEEP_LOOP


def dispatch_req(obj, req):
    method, args, kw = req
    return getattr(obj, method)(*args, **kw)


class ImapEndpoint(object):
    """Controllers and R/W drivers for IMAP.

    Obeys to the ImapRepository worker."""

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

    def init(self, masterProxy, logger, chan):
        self._masterProxy = masterProxy
        self._logger = logger
        self._chan = chan
        self._reader = chan.create_downstreamReader()
        self._writer = chan.create_upstreamWriter()

    def instanciate_driver(self, cls_driver, cls_controllers):
        driver = cls_driver()
        for cls_controller in reversed(cls_controllers):
            driver = cls_controller(driver)
        self._driver = driver

    def run(self):
        req = self._reader.get()
        if req is None:
            return None
        return self.dispatch_req(req)

    def loop(self):
        self._logger.force("in ImapEndpoint")
        while True:
            m_req = self._masterProxy.get_nowait()
            if req is not None:
                self.dispatch_req(req)
            req = self._reader.get_nowait()
            if req is None:
                sleep(SLEEP_LOOP)
