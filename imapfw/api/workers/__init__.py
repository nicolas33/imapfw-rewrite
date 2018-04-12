"""

The public API.

Import the objects made public from the real objects defined in their
uncorrelated path. This allows more fine-grained control of what is made public
and how to structure the underlying code.

"""

__all__ = [
    'LocalBackend',
    'MultiProcessingBackend',
    'ThreadingBackend',

    'SimpleLock',
    'WorkerSafe',
]


from imapfw.workers.concurrency import SimpleLock, WorkerSafe
from imapfw.workers.worker import (
    MultiProcessingBackend,
    ThreadingBackend,
    LocalBackend,
)
