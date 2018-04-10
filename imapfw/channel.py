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
        self.upstream = backend.create_queue()
        self.downstream = backend.create_queue()

    def create_downstream_reader(self):
        return Reader(self.downstream)

    def create_downstream_writer(self):
        return Writer(self.downstream)

    def create_upstream_reader(self):
        return Reader(self.upstream)

    def create_upstream_writer(self):
        return Writer(self.upstream)

