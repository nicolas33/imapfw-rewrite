# The MIT License (MIT).
# Copyright (c) 2018-2018, Nicolas Sebrecht & contributors.


def oneshotRunner(cls, masterProxy, logger, *chans):
    """Initialize and run the class in the worker."""

    try:
        instance = cls()
        instance.init(masterProxy, logger, *chans)
    except Exception as e:
        try:
            logger.exception('OR001', e)
        except Exception as log_e:
            masterProxy.error(logger.get_className(), str(log_e))
        masterProxy.error(cls.__name__, str(e))
    instance.run() # Run unprotected, must correctly handle errors.


def loopRunner(cls, masterProxy, logger, *chans):
    """Initialize and run the class in the worker."""

    try:
        instance = cls()
        instance.init(masterProxy, logger, *chans)
    except Exception as e:
        try:
            logger.exception('OR002', e)
        except Exception as log_e:
            masterProxy.error(logger.get_className(), str(log_e))
        masterProxy.error(cls.__name__, str(e))
    instance.loop() # Run unprotected, must correctly handle errors.
