# The MIT License (MIT).
# Copyright (c) 2018-2018, Nicolas Sebrecht & contributors.


class Reader(object):
    def __init__(self, queue):
        self._queue = queue

    def get(self):
        return self._queue.get()

    def get_nowait(self):
        return self._queue.get_nowait()


class Writer(object):
    def __init__(self, queue):
        self._queue = queue

    def put(self, data):
        self._queue.put(data)

    def put_nowait(self, data):
        self._queue.put_nowait(data)


class Chan(object):
    def __init__(self, backend):
        self.notifyDown = backend.create_queue()
        self.notifyUp = backend.create_queue()

    def create_downstreamReaderWriter(self):
        return Reader(self.notifyDown), Writer(self.notifyUp)

    def create_upstreamReaderWriter(self):
        return Reader(self.notifyUp), Writer(self.notifyDown)

    def create_downstreamReader(self):
        return Reader(self.notifyDown)

    def create_downstreamWriter(self):
        return Writer(self.notifyUp)

    def create_proxy(self):
        return Proxy(self.notifyDown, self.notifyUp)

    def create_upstreamReader(self):
        return Reader(self.notifyUp)

    def create_upstreamWriter(self):
        return Writer(self.notifyDown)

