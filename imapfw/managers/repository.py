# The MIT License (MIT).
# Copyright (c) 2018-2018, Nicolas Sebrecht & contributors.


from imapfw.channel import Chan


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

    def __init__(self, repoBackend, endpointsBackend):
        self._cls_repoBackend = repoBackend
        self._cls_endpointBackend = endpointsBackend
        self._cls_repo = None
        self._cls_endpoint = None
        self._endpoints = [] # Tuples: (worker, chan)
        self._errorLink = None
        self._repoChan = None
        self._repositoryWorker = None

    def get_className(self):
        return self.__class__.__name__

    def init(self, cls_repo, cls_endpoint, errorLink):
        self._cls_repo = cls_repo
        self._cls_endpoint = cls_endpoint
        self._errorLink = errorLink

    def get_repoChan(self):
        return self._repoChan

    def loop(self):
        #TODO: read errorLink and apply error requests.
        pass

    def start_endpointWorkers(self):
        for number in range(3):
            chan = Chan(self._cls_endpointBackend)
            name = "{}.{}".format(self._cls_endpoint.__name__, number)

            worker = self._cls_backend.create_worker(
                name,
                loopRunner,
                (self._cls_endpoint, self._errorLink, chan),
            )
            worker.start()
            self._endpoints.append(worker, chan)

    def start_repositoryWorker(self):
        chans = []
        for endpoint in self._endpoints:
            chans = endpoint[1]
        self._repoChan = Chan(self._cls_repoBackend)

        self._repositoryWorker = self._cls_repoBackend.create_worker(
            self._cls_repo.__name__,
            loopRunner,
            (self._cls_repo, self._errorLink, self._repoChan) + chans,
        )
        self._repositoryWorker.start()


    def start(self):
        self.start_endpointWorker() #XXX: start on request?.
        self.start_repositoryWorker()

    def set_backends(self, cls_endpointBackend, cls_repoBackend):
        self._cls_endpointBackend = cls_endpointBackend
        self._cls_repoBackend = cls_repoBackend
