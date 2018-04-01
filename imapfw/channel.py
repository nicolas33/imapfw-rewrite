# The MIT License (MIT).
# Copyright (c) 2018-2018, Nicolas Sebrecht & contributors.


class Chan(object):
    def __init__(self, backend):
        self.reader = backend.create_queue()
        self.writer = backend.create_queue()

    def put(self, data):
        self.writer.put(data)

    def get(self):
        return self.reader.get()

    def get_reader(self):
        return self.reader

    def get_writer(self):
        return self.writer

