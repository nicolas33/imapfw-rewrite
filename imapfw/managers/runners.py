# The MIT License (MIT).
# Copyright (c) 2018-2018, Nicolas Sebrecht & contributors.


def oneshotRunner(cls, errorLink, logger, *chans):
    """Initialize and run the class in the worker."""

    try:
        instance = cls()
        instance.init(errorLink, logger, *chans)
    except Exception as e:
        try:
            logger.exception('OR001', e)
        except Exception as log_e:
            errorLink.send('__EXCEPTION__', log_e)
        errorLink.send('__EXCEPTION__', e)
    instance.run() # Run unprotected, must correctly handle errors.


def loopRunner(cls, errorLink, logger, *chans):
    """Initialize and run the class in the worker."""

    try:
        instance = cls()
        instance.init(errorLink, logger, *chans)
    except Exception as e:
        try:
            logger.exception('OR002', e)
        except Exception as log_e:
            errorLink.send('__EXCEPTION__', log_e)
        errorLink.send('__EXCEPTION__', e)
    instance.loop() # Run unprotected, must correctly handle errors.
