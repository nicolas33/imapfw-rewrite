# The MIT License (MIT).
# Copyright (c) 2018-2018, Nicolas Sebrecht & contributors.

"""

The public API.

Import the objects made public from the real objects defined in their
uncorrelated path. This allows more fine-grained control of what is made public
and how to structure the underlying code.

"""


from imapfw.managers import (
    EngineManager,
    LoggerManager,
    MasterManager,
    RepositoryManager,
)


__all__ = [
    'EngineManager',
    'LoggerManager',
    'MasterManager',
    'RepositoryManager',
]
