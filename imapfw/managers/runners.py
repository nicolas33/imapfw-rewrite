# The MIT License (MIT).
# Copyright (c) 2018-2018, Nicolas Sebrecht & contributors.


def loopRunner(cls, errorLink, logger, *chans):
    """Initialize the class in the worker."""

    try:
        instance = cls()
        instance.init(errorLink, *chans)
    except Exception as e:
        try:
            logger.exception(e)
        except Exception as log_e:
            errorLink.send(log_e)
        errorLink.send(e)
    instance.loop() # Run unprotected, loop must correctly handle errors.
