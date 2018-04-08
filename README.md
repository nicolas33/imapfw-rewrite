
# DESIGN


## Main

The main worker (process and thread) is the user app. The user defines the
in-memory architecture.

Workers are started and stopped via manager instances. The managers are helpers
to setup and start the business logic in workers.

We have:

- RepositoryManager
- EngineManager
- LoggerManager
- etc...


Due to a python limitation, all the channels used by a worker MUST be defined
before it gets started (so it's passed as argument).

The user can choose which worker backend to use for each one (multiprocessing,
threading, etc).

## Worker

Each worker run the business logic:

- Repository (ImapRepository, MaildirRepository, StateRepository, etc)
- Engine
- Logger
- etc...

All the workers loop.
All the workers are passed channels.
All the workers send messages to the other workers via the channels.
All the workers have one ErrorLink channel (read in main) so it can stop the
workers on errors.


## RespositoryManager

The repository manager handles:

- the repository: designed to receive all the requests from the engine.
- the endpoints: each endpoint is attached to the repository via a channel. It's
  the abstract on top of a socket. However, it's high-level. It is a chain of
  controllers on top of one reader and one writer.


## IOC

The user can redefine any class. There are the following namespaces:

- imapfw.api: the classes intented to be redefined by the user.
- imapfw.contrib: the classes written by the users for the users.
- imapfw: the core (should not be redefined by the users).
- imapfw.apps: the apps provided by the project, written as any other user app.


## The apps

In the app, the user can use the classes in imapfw.api as-is or redefine them in
the app package. So, we should have imports like:

```python
from imapfw.api import Something # as-is

from .repositories.imap import MyImapRepository # redefined
```

and in `app/repositories/imap` we have something like:

```python
from imapfw.api.repositories import ImapRepository

class MyImapRepository(ImapRepository):
    """Redefinitions."""
```
