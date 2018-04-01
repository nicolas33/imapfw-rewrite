# Set the license here.


from imapfw.api.repositories import (
    ImapRepository,
    MaildirRepository,
    StateRepository,
)


class HomeImap(ImapRepository):
    """Handle the controllers and drivers.

    Dispatch the incoming commands to the controllers.
    """

    #XXX: move into ImapRepository
    def __init__(self):
        self.reader = None
        self.witer = None
        self.active_controllers = []
        self.available_controllers = []

    #XXX: move into ImapRepository
    def set_channels(self, reader, writer):
        self.reader = reader
        self.witer = writer

    #XXX: move into ImapRepository
    def loop(self):
        """ """
        # Read the incoming commands, dispatch to the controllers.

class HomeMaildir(MaildirRepository):
    """Handle the controllers and drivers."""


class StateRepo(StateRepository):
    """Handle the controllers and drivers."""
