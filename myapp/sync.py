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
from imapfw.api.concurrency import (
    LocalBackend,
    ThreadingBackend,
    MultiProcessingBackend as PBackend,
)
from imapfw.api.repositories import (
    ImapRepository,
    MaildirRepository,
    StateRepository,
)
from imapfw.api.endpoints import ImapEndpoint, MaildirEndpoint, StateEndpoint

from imapfw.api.managers import RepositoryManager, EngineManager, LoggerManager
from imapfw.api.loggers import Logger
from imapfw.errorlink import ErrorLink #FIXME
# Usual apps should have helpers from imapfw.apps, e.g.
# classic remote/local/state repositories.


#from myapp.repositories.home import HomeImap, HomeMaildir, HomeState


exitCode = 254

#XXX: both the engine and the logger shouldn't run in the same process.
try:
    errorLink = ErrorLink(PBackend)

    # Enable logging.
    loggerManager = LoggerManager()
    loggerManager.init(Logger, PBackend, errorLink)
    loggerManager.start()
    logger = loggerManager.create_proxy()
    logger.enable('M001')
    logger.info("starting", 'M001')

    ## Setup the defaults (fallbacks).
    #runtime.set_backend(PBackend)

    # Setup the app. At the end of the setup, the app is ready to go.
    imapManager = RepositoryManager()
    maildirManager = RepositoryManager()
    stateManager = RepositoryManager()
    engineManager = EngineManager()

    imapManager.set_backends(PBackend, PBackend)
    maildirManager.set_backends(PBackend, PBackend)
    stateManager.set_backends(PBackend, PBackend)
    engineManager.set_backend(PBackend)

    imapManager.init(ImapRepository, ImapEndpoint, errorLink, logger)
    maildirManager.init(MaildirRepository, MaildirEndpoint, errorLink, logger)
    stateManager.init(StateRepository, StateEndpoint, errorLink, logger)
    chans = tuple(i.get_repoChan() for i in [imapManager, maildirManager, stateManager])
    engineManager.init(ConvertEngine, errorLink, logger, *chans)

    imapManager.set_maxEndpoints(1)
    maildirManager.set_maxEndpoints(1)
    stateManager.set_maxEndpoints(1)
    # Setup end.

    # Start here #
    imapManager.start()
    maildirManager.start()
    stateManager.start()
    engineManager.start()

    #TODO: introduce a tracker for the workers (make use of errorLink) and loop.
    engineManager.join()
    imapManager.stop()
    maildirManager.stop()
    stateManager.stop()

    exitCode = 0

except KeyboardInterrupt:
    exitCode = 253
    for manager in [engineManager, imapManager, maildirManager, stateManager]:
        try:
            manager.stop()
        except:
            pass
except Exception:
    for manager in [engineManager, imapManager, maildirManager, stateManager]:
        try:
            manager.kill()
        except:
            pass
finally:
    loggerManager.stop()

end = time.time(); print("elapsed time: {}".format(end - start))
sys.exit(exitCode)
