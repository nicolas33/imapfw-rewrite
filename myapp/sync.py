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
    imapRepositoryManager = RepositoryManager(PBackend, PBackend)
    maildirRepositoryManager = RepositoryManager(PBackend, PBackend)
    stateRepositoryManager = RepositoryManager(PBackend, PBackend)

    imapRepositoryManager.init(ImapRepository, ImapEndpoint)
    maildirRepositoryManager.init(MaildirRepository, MaildirEndpoint)
    stateRepositoryManager.init(StateRepository, StateEndpoint)

    # The engine can be run in main or in a worker.
    engine = ConvertEngine() # In main.
    # Or engine.loop in a worker if the engine is a service.

    #engineWorker = wm.create_localWorker(engine.run)
    # Setup end.

    # Start here #
    imapRepositoryManager.start()
    maildirRepositoryManager.start()
    stateRepositoryManager.start()

    # Or engineManager.start()
    engine.run(
        errorLink,
        imapRepositoryManager.get_repoChan(),
        maildirRepositoryManager.get_repoChan(),
        stateRepositoryManager.get_repoChan(),
    )

    imapRepositoryManager.stop()
    maildirRepositoryManager.stop()
    stateRepositoryManager.stop()

except KeyboardInterrupt:
    for manager in [imapRepositoryManager, maildirRepositoryManager,
            stateRepositoryManager]:
        try:
            manager.stop()
        except:
            pass
except Exception:
    for manager in [imapRepositoryManager, maildirRepositoryManager,
            stateRepositoryManager]:
        try:
            manager.kill()
        except:
            pass
finally:
    loggerManager.stop()

sys.exit(engine.get_exitCode())
