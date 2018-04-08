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

from imapfw.api.managers import RepositoryManager, EngineManager
from imapfw.api.logger import Logger
# Usual apps should have helpers from imapfw.apps, e.g.
# classic remote/local/state repositories.


#from myapp.repositories.home import HomeImap, HomeMaildir, HomeState



#XXX: both the engine and the logger shouldn't run in the same process.
try:
    errorLink = ErrorLink(PBackend)

    # Enable logging.
    loggerManager = LoggerManager()
    loggerManager.init(PBackend, errorLink)
    log = loggerManager.get_chan()

    # Setup the defaults (fallbacks).
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
    chans = tuple(i.get_chan() for i in [imapManager, maildirManager, stateManager])
    engine.init(ConvertEngine, errorLink, logger, *chans)

    imapManager.set_maxEndpoints(1)
    maildirManager.set_maxEndpoints(1)
    stateManager.set_maxEndpoints(1)
    # Setup end.

    # Start here #
    imapManager.start()
    maildirManager.start()
    stateManager.start()
    engine.start()

    engine.join()
    imapManager.stop()
    maildirManager.stop()
    stateManager.stop()

except KeyboardInterrupt:
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

sys.exit(engine.get_exitCode())
