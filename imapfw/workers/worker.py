# The MIT License (MIT).
# Copyright (c) 2018-2018, Nicolas Sebrecht & contributors.

"""

Workers with channels.

"""

from imapfw.channel import Chan

#from .concurrency import MultiProcessingBackend, ThreadingBackend, LocalBackend


class _Worker(object):
    def __init__(self, backend, chan, name, target, args):
        self._name = name
        self._chan = Chan(backend.create_queue(), backend.create_queue())
        args = (self.chan,) + args
        self._backendWorker = backend.create_worker(name, target, args)

    def get_chan(self):
        return self._chan

    def __getattr__(self, name):
        return getattr(self._backendWorker, name)


def ProcessWorker(name, target, args):
    return _Worker(MultiProcessingBackend, name, target, args)

def ThreadWorker(name, target, args):
    return _Worker(ThreadingBackend, name, target, args)

#XXX: add param 'loop=False'?
def LocalBackend(name, target, args):
    return _Worker(LocalBackend, name, target, args)
