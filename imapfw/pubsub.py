# The MIT License (MIT).
# Copyright (c) 2018-2018, Nicolas Sebrecht & contributors.


class _Route(object):
    def __init__(self, name, reader):
        self.reader = reader
        self.writers = []

    def subscribe(self, writer):
        self.writers.append(writer)

    def flush(self):
        while True:
            msg = self.reader.get()
            if msg is None:
                break
            for writer in self.writers:
                writer.put(msg)


class PubSub(object):
    def __init__(self):
        self.routes = {}

    def declare(self, name, chan):
        if name in self.routes:
            raise Exception("name already taken")
        self.routes[name] = _Route(chan.get_reader())

    def subscribe(self, upstream, chan):
        if name not in self.routes:
            raise Exception("name does not exists")
        self.routes[name].subscribe(chan.get_writer())

    def flush(self):
        for route in self.routes.values():
            route.flush()
