# The MIT License (MIT).
# Copyright (c) 2018-2018, Nicolas Sebrecht & contributors.


class Repository(object):
    """The base class for all the repositories."""

    def get_className(self):
        return self.__name__
