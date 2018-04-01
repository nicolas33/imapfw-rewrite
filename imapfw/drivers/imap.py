# The MIT License (MIT).
# Copyright (c) 2018-2018, Nicolas Sebrecht & contributors.

from imapfw.imap import Imap as ImapBackend

from .driver import Driver


class ImapDriver(Driver):
    """The Imap driver, possibly redefined by the user."""

    def __init__(self, *args):
        super(ImapDriver, self).__init__(*args)
        self.imap = ImapBackend() #TODO: expose

    def connect(self):
        host = self.conf.get('host')
        port = int(self.conf.get('port'))
        return self.imap.connect(host, port)

    def getCapability(self):
        return self.imap.getCapability()

    def getFolders(self):
        return self.imap.getFolders()

    def getMessages(self, messages, attributes):

        return self.imap.getMessages(messages, attributes)

    def getNamespace(self):
        return self.imap.getNamespace()

    def login(self):
        user = self.conf.get('username')
        password = self.conf.get('password')
        return self.imap.login(user, password)

    def logout(self):
        self.imap.logout()

    def searchUID(self, conditions=None):
        return self.imap.searchUID(conditions)

    def select(self, folder):
        return self.imap.select(folder)

    #def append(self, server,  mail):
        #response = server.append(mail)
        #return response

    #def update(self, server, mail):
        #response = server.update(mail)
        #return response

    #def fetch(self, server, uids):
        #response = server.fetch(uids)
        #return response
