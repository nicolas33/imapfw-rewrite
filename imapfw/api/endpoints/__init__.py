"""

The public API.

Import the objects made public from the real objects defined in their
uncorrelated path. This allows more fine-grained control of what is made public
and how to structure the underlying code.

"""

__all__ = [
    'ImapEndpoint',
    'MaildirEndpoint',
    'StateEndpoint',
]

from imapfw.endpoints import ImapEndpoint, MaildirEndpoint, StateEndpoint
