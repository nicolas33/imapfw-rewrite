# The MIT License (MIT).
# Copyright (c) 2018-2018, Nicolas Sebrecht & contributors.


from imapfw.channel import Chan
from .runners import loopRunner


class Repository(object):
    def loop(self):
        # Dispatch requests to endpoints.
        # Return responses (in order?).
        pass


class RepositoryManager(object):
    """Handle the repository and endpoints workers. Runs in main.

    - start endpoints dynamically on Repository request?
    - create "Endpoint" class?
    """

    def __init__(self):
        self._cls_repoBackend = None
        self._cls_endpointBackend = None
        self._cls_repo = None
        self._cls_endpoint = None
        self._endpoints = [] # Tuples: (worker, chan)
        self._endpointsChans = []
        self._errorLink = None
        self._logger = None
        self._maxEndpoints = 1
        self._repoChan = None
        self._repositoryWorker = None

    def _initEndpointChannels(self):
        for number in range(self._maxEndpoints):
            chan = Chan(self._cls_endpointBackend)
            self._endpointsChans.append(chan)

    def get_className(self):
        return self.__class__.__name__

    def init(self, cls_repo, cls_endpoint, errorLink, logger):
        self._cls_repo = cls_repo
        self._cls_endpoint = cls_endpoint
        self._errorLink = errorLink
        self._logger = logger

    def get_repoChan(self):
        return self._repoChan

    def run(self):
        #TODO: read errorLink and apply error requests.
        pass

    def set_maxEndpoints(self, number):
        self._maxEndpoints = number

    def set_backends(self, cls_endpointBackend, cls_repoBackend):
        self._cls_endpointBackend = cls_endpointBackend
        self._cls_repoBackend = cls_repoBackend

    def start_endpointWorkers(self):
        for number in range(self._maxEndpoints):
            chan = self._endpointsChans.pop()
            name = "{}.{}".format(self._cls_endpoint.__name__, number)

            worker = self._cls_repoBackend.create_worker(
                name,
                loopRunner,
                (self._cls_endpoint, self._errorLink, self._logger, chan),
            )
            worker.start()
            self._endpoints.append((worker, chan))

    def start_repositoryWorker(self):
        self._repoChan = Chan(self._cls_repoBackend)
        chans = tuple(chan for _, chan in self._endpoints)

        self._repositoryWorker = self._cls_repoBackend.create_worker(
            self._cls_repo.__name__,
            loopRunner,
            (self._cls_repo, self._errorLink, self._logger, self._repoChan) + chans,
        )
        self._repositoryWorker.start()


    def start(self):
        self._initEndpointChannels()
        self.start_endpointWorkers()
        self.start_repositoryWorker()

    def stop(self):
        pass # Send stop message to workers and join.
