# The MIT License (MIT).
# Copyright (c) 2018-2018, Nicolas Sebrecht & contributors.


__logger = None

def set_logger(logger):
    global __logger
    __logger = logger

def get_logger():
    global __logger
    return __logger

