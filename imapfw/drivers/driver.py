# The MIT License (MIT).
# Copyright (c) 2018-2018, Nicolas Sebrecht & contributors.


class Driver(object):
    """The Driver base class.

    This is the low-level driver:
    - this is the base class for all the drivers (e.g. Maildir, Imap, etc).
    - does not enable controllers machinery at this point.

    This interface is the API for the controllers.
    """

    def getClassName(self) -> str:
        return self.__class__.__name__
