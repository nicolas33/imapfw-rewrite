# The MIT License (MIT).
# Copyright (c) 2018-2018, Nicolas Sebrecht & contributors.


from imapfw.channel import Chan
from imapfw.workers import MultiProcessingBackend #XXX: that sucks.


class ManagerLink(object):
    def __init__(self, backend=MultiProcessingBackend):
        self._chan = Chan(backend)

    def __getattr__(self, name):
        return getattr(self._chan, name)

    def send(self, typ, exc):
        #TODO: improve with full string stack trace.
        self._chan.put((typ, exc.__class__, str(exc)))

    def read(self):
        resp = self._chan.get_nowait()
        if resp is not None:
            typ, cls, msg = resp
            if typ == '__EXIT__':
                exit(typ, cls, msg)
            print(msg)

    def run(self):
        """Must be run in main."""

        self.read()
