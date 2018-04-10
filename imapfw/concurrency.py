# The MIT License (MIT).
# Copyright (c) 2015-2018, Nicolas Sebrecht & contributors.

"""

Introduction
============

The concurrency module defines a common interfaces to whatever backend is used
(multiprocessing, Python threading, etc).  "worker" is the generic term used to
define a thread (for Python threading) or a process (for multiprocessing).

Using the concurrency module
============================

The main entry point is the :func:`Concurrency` factory. The returned
backend satisfy the interface :class:`ConcurrencyInterface`.

The :func:`WorkerSafe` decorator allows to easily make any existing callable
concurrency-safe.

"""

#from imapfw import runtime
#from imapfw.constants import WRK


SimpleLock = None
"""

SimpleLock is a function defined at runtime to create locks. The real function
is set according to the command-line option.

"""


class WorkerInterface(object):
    def get_name(self):  raise NotImplementedError
    def join(self):     raise NotImplementedError
    def kill(self):     raise NotImplementedError
    def start(self):    raise NotImplementedError


class QueueInterface(object):
    def empty(self):        raise NotImplementedError
    def get(self):          raise NotImplementedError
    def get_nowait(self):   raise NotImplementedError
    def put(self):          raise NotImplementedError


class LockInterface(object):
    def acquire(self):  raise NotImplementedError
    def release(self):  raise NotImplementedError


class ConcurrencyInterface(object):
    def create_lock():          raise NotImplementedError
    def create_queue():         raise NotImplementedError
    def create_worker():        raise NotImplementedError
    def get_workerNameFunc():   raise NotImplementedError


def WorkerSafe(lock):
    """Decorator for locking any callable.

    It is usefull to forbid concurrent access to non concurrency-safe data or
    libraries. The decorated callable has to end before the next concurrent call
    can start. It is required for the decorated callable to end or your program
    might deadlock."""

    def decorate(func):
        def safeFunc(*args, **kwargs):
            with lock:
                values = func(*args, **kwargs)
            return values
        return safeFunc

    return decorate


class LockBase(LockInterface):
    def __enter__(self):
        self.lock.acquire()

    def __exit__(self, t, v, tb):
        self.lock.release()


class LocalBackend(ConcurrencyInterface):
    @staticmethod
    def create_worker(name, target, args):
        class Worker(WorkerInterface):
            def __init__(self, name, target, args):
                self._name = name
                self._target = target
                self._args = args

            def get_name(self):
                return self._name

            def kill(self):
                pass

            def start(self):
                self._target(*self._args)

            def join(self):
                pass

        return Worker(name, target, args)

    @staticmethod
    def create_lock():
        return ThreadingBackend.create_lock()

    @staticmethod
    def create_queue():
        return ThreadingBackend.create_queue()

    @staticmethod
    def get_workerNameFunc():
        return "Local callable"


class ThreadingBackend(ConcurrencyInterface):
    """
    Handling signals with threading
    ===============================

    SIGTERM
    -------

    Main thread get KeyboardInterrupt. Only daemon childs gets killed.

    SIGKILL
    -------

    Kills everything (the process is killed, so the threads).
    """

    @staticmethod
    def create_worker(name, target, args):
        from threading import Thread

        class Worker(WorkerInterface):
            def __init__(self, name, target, args):
                self._name = name

                self._thread = Thread(name=name, target=target, args=args,
                    daemon=True)

            def get_name(self):
                return self._name

            def kill(self):
                """Kill a worker.

                This is only usefull for the workers working with a failed
                worker. In daemon mode: workers get's killed when the main thread
                gets killed."""

                #runtime.ui.debugC(WRK, "%s killed"% self._name)

            def start(self):
                self._thread.start()
                #runtime.ui.debugC(WRK, "%s started"% self._name)

            def join(self):
                #runtime.ui.debugC(WRK, "%s join"% self._name)
                self._thread.join() # Block until thread is done.
                #runtime.ui.debugC(WRK, "%s joined"% self._name)

        return Worker(name, target, args)

    @staticmethod
    def create_lock():
        from threading import Lock

        class TLock(LockBase):
            def __init__(self, lock):
                self.lock = lock

            def __enter__(self):
                self.lock.acquire()

            def __exit__(self, t, v, tb):
                self.lock.release()

            def acquire(self):
                self.lock.acquire()

            def release(self):
                self.lock.release()

        return TLock(Lock())

    @staticmethod
    def create_queue():
        from queue import Queue, Empty # Thread-safe.

        class TQueue(QueueInterface):
            def __init__(self):
                self._queue = Queue()

            def empty(self):
                return self._queue.empty()

            def get(self):
                return self._queue.get()

            def get_nowait(self):
                try:
                    return self._queue.get_nowait()
                except Empty:
                    return None

            def put(self, data):
                self._queue.put(data)

        return TQueue()

    @staticmethod
    def get_workerNameFunc():
        from threading import current_thread

        def currentWorkerName():
            return current_process().name
        return currentWorkerName


class MultiProcessingBackend(ConcurrencyInterface):
    """
    Handling signals with multiprocessing
    =====================================

    SIGTERM
    -------

    Signal is sent to all workers by multiprocessing.

    SIGKILL
    -------

    Current process is killed. Other processes continue (orphaned if main
    process was killed).
    """

    @staticmethod
    def create_worker(name, target, args):
        from multiprocessing import Process

        class Worker(WorkerInterface):
            def __init__(self, name, target, args):
                self._name = name

                self._process = Process(name=name, target=target, args=args)

            def get_name(self):
                return self._name

            def kill(self):
                """Kill a worker.

                This is only usefull for the workers working with a failed
                worker. KeyboardInterrupt is natively sent to all workers by
                multiprocessing."""

                self._process.terminate() # Send SIGTERM.
                self.join(verbose=False)
                #runtime.ui.debugC(WRK, "%s killed"% self._name)

            def start(self):
                self._process.start()
                #runtime.ui.debugC(WRK, "%s started"% self._name)

            def join(self, verbose=True):
                # if verbose is True:
                    #runtime.ui.debugC(WRK, "%s join"% self._name)
                self._process.join() # Block until process is done.
                # if verbose is True:
                    #runtime.ui.debugC(WRK, "%s joined"% self._name)

        return Worker(name, target, args)

    @staticmethod
    def create_lock():
        from multiprocessing import Lock

        class MLock(LockBase):
            def __init__(self, lock):
                self.lock = lock

            def acquire(self):
                self.lock.acquire()

            def release(self):
                self.lock.release()

        return MLock(Lock())

    @staticmethod
    def create_queue():
        from multiprocessing import Queue
        import queue

        class MQueue(QueueInterface):
            def __init__(self):
                self._queue = Queue()

            def empty(self):
                return self._queue.empty()

            def get(self):
                return self._queue.get()

            def get_nowait(self):
                try:
                    return self._queue.get_nowait()
                except queue.Empty:
                    return None

            def put(self, data):
                self._queue.put(data)

            def put_nowait(self, data):
                self._queue.put_nowait(data)

        return MQueue()

    @staticmethod
    def get_workerNameFunc():
        from multiprocessing import current_process

        def currentWorkerName():
            return current_process().name
        return currentWorkerName



ConcurrencyBackends = {
    'multiprocessing': MultiProcessingBackend,
    'threading': ThreadingBackend,
    'local': LocalBackend,
}

def Concurrency(backendName):
    """Get the concurrency backend for the requested backend name.

    backendName: currently 'multiprocessing', 'threading' or 'local'."""

    global SimpleLock
    try:
        concurrency = ConcurrencyBackends[backendName]()
        if SimpleLock is None:
            SimpleLock = concurrency.create_lock
        return concurrency
    except KeyError:
        raise Exception("unkown backend: %s"% backendName)
