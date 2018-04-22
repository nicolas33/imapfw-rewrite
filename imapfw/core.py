# The MIT License (MIT).
# Copyright (c) 2018-2018, Nicolas Sebrecht & contributors.


def dispatch_req(obj, req):
    method, args, kw = req
    return getattr(obj, method)(*args, **kw)
