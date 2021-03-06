#!/usr/bin/python3
"""

This command is run by:

```sh
> imapfw myapp sync
```

Apps can be fully written by users or provided by imapfw.

The three most important namespaces are:

- imapfw.api -> access the (default) imapfw objects.
- myapp -> the objects defined for this app.
- imapfw.<pkg_name> -> access the core imapfw objects not exposed in the api
  (discouraged).

"""

import time

start = time.time()

import sys

from imapfw.api.engines import ConvertEngine
from imapfw.api.workers import (
    LocalBackend as LBackend,
    ThreadingBackend as TBackend,
    MultiProcessingBackend as PBackend,
)
from imapfw.api.repositories import (
    ImapRepository,
    MaildirRepository,
    StateRepository,
)
from imapfw.api.managers import (
    EngineManager,
    LoggerManager,
    MasterManager,
    RepositoryManager,
)
from imapfw.api.endpoints import ImapEndpoint, MaildirEndpoint, StateEndpoint
from imapfw.api.loggers import Logger
# Usual apps should have helpers from imapfw.apps, e.g.
# classic remote/local/state repositories.


#from myapp.repositories.home import HomeImap, HomeMaildir, HomeState


# __init__: attributes only: instanciate without issues
# init: initialize

# Workers:
# - start: before loop/run
# - loop: loop

# 2 models:
# a. override methods
# b. hooks


def chans_from(*classes):
    d = tuple(cls.get_repoChan() for cls in classes)
    return d


exitCode = 254

try:
    masterManager = MasterManager()
    masterProxy = masterManager.create_proxy()

    # Enable logging.
    loggerManager = LoggerManager()
    loggerManager.init(Logger, PBackend, masterProxy)
    loggerManager.start()
    logger = loggerManager.create_proxy()
    logger.enable('M001')
    logger.info("starting", 'M001')

    ## Setup the defaults (fallbacks).
    #runtime.set_backend(PBackend)

    # Setup the app. At the end of the setup, the app is ready to go.
    imapManager = RepositoryManager()
    #maildirManager = RepositoryManager()
    #stateManager = RepositoryManager()
    engineManager = EngineManager()

    imapManager.set_backends(PBackend, PBackend)
    #maildirManager.set_backends(PBackend, PBackend)
    #stateManager.set_backends(PBackend, PBackend)
    engineManager.set_backend(PBackend)

    imapManager.init(ImapRepository, ImapEndpoint, masterProxy, logger)
    #maildirManager.init(MaildirRepository, MaildirEndpoint, masterProxy, logger)
    #stateManager.init(StateRepository, StateEndpoint, masterProxy, logger)

    #chans = chans_from(imapManager, maildirManager, stateManager)
    chans = chans_from(imapManager)
    engineManager.init(ConvertEngine, masterProxy, logger, *chans)

    imapManager.set_maxEndpoints(1)
    #maildirManager.set_maxEndpoints(1)
    #stateManager.set_maxEndpoints(1)
    # Setup end.

    # Start here #
    imapManager.start() #BUG?
    #maildirManager.start()
    #stateManager.start()
    engineManager.start()

    masterManager.loop()

    imapManager.stop()
    #maildirManager.stop()
    #stateManager.stop()

    exitCode = 0

except KeyboardInterrupt:
    exitCode = 253
    try:
        for manager in [engineManager, imapManager, maildirManager, stateManager]:
            try:
                manager.stop()
            except:
                pass
    except:
        pass
except Exception:
    raise
    for manager in [engineManager, imapManager, maildirManager, stateManager]:
        try:
            manager.kill()
        except:
            pass
finally:
    loggerManager.stop()

end = time.time(); print("elapsed time: {}".format(end - start))
sys.exit(exitCode)
