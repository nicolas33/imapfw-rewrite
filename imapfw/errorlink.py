# The MIT License (MIT).
# Copyright (c) 2018-2018, Nicolas Sebrecht & contributors.


from imapfw.channel import Chan


class ErrorLink(object):
    def __init__(self, backend):
        self._chan = Chan(backend)

    def __getattr__(self, name):
        return getattr(self._chan, name)

    def send(self, typ, exc):
        #TODO: improve with full string stack trace.
        self._chan.put((typ, exc.__class__, str(exc)))

    def read(self):
        """Must be run in main."""

        resp = self._chan.get()
        if resp is not None:
            typ, cls, msg = resp
            if typ == '__EXIT__':
                exit(typ, cls, msg) # Kill workers, first.
            print(msg)

