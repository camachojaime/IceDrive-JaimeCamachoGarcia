"""Module for servants implementations."""
import sys
import json

from typing import List

import Ice
#Ice.loadSlice('icedrive.ice')
Ice.loadSlice('icedrive_directory/icedrive.ice')
import IceDrive
#Ice.loadSlice('icedrive_directory/icedrive.ice')

TXPURPLE = '\033[95m'           # Success color (purple)
TXRED = '\033[91m'              # Error color (red)
TXYELLOW = '\033[93m'           # Yellow color
TXORANGE = '\033[38;5;208m'     # Orange color
TXENDC = '\033[0m'              # Standar color



def isRoot(str):
    with open("test/tree.json") as file:
        tree = json.load(file)

    if tree:
        for i in tree:
            if i["root"] == str:
                return True

    return False



class Directory(IceDrive.Directory):
    """Implementation of the IceDrive.Directory interface."""

    def __init__(self):
        self.route = ""
        #self.isRoot = False

    def getParent(self, current: Ice.Current = None) -> IceDrive.DirectoryPrx:
        """Return the proxy to the parent directory, if it exists. None in other case."""

    def getChilds(self, current: Ice.Current = None) -> List[str]:
        """Return a list of names of the directories contained in the directory."""

    def getChild(self, name: str, current: Ice.Current = None) -> IceDrive.DirectoryPrx:
        """Return the proxy to one specific directory inside the current one."""

    def createChild(
        self, name: str, current: Ice.Current = None
    ) -> IceDrive.DirectoryPrx:
        """Create a new child directory and returns its proxy."""

    def removeChild(self, name: str, current: Ice.Current = None) -> None:
        """Remove the child directory with the given name if exists."""

    def getFiles(self, current: Ice.Current = None) -> List[str]:
        """Return a list of the files linked inside the current directory."""

    def getBlobId(self, filename: str, current: Ice.Current = None) -> str:
        """Return the "blob id" for a given file name inside the directory."""

    def linkFile(
        self, filename: str, blob_id: str, current: Ice.Current = None
    ) -> None:
        """Link a file to a given blob_id."""

    def unlinkFile(self, filename: str, current: Ice.Current = None) -> None:
        """Unlink (remove) a filename from the current directory."""


class DirectoryService(IceDrive.DirectoryService):
    """Implementation of the IceDrive.Directory interface."""
    

    def getRoot(self, user: str, current: Ice.Current = None) -> IceDrive.DirectoryPrx:
        """Return the proxy for the root directory of the given user."""

        if isRoot(user):

            print(TXYELLOW + "ENTRA" + TXENDC)                  

            directory = Directory()         # Servant
            directory.route += user + "/"
            print(directory.route)

            broker = self.communicator()

            print(TXYELLOW + "AFTER_BROKER" + TXENDC)

            adapter = broker.createObjectAdapter("DirectoryAdapter")
            proxy = adapter.add(directory, broker.stringToIdentity("directory1"))
        
            print(proxy)

            sys.stdout.flush()

            print(TXYELLOW + "AFTER_FLUSH" + TXENDC)

            adapter.activate()
            self.shutdownOnInterrupt()
            broker.waitForShutdown()
            
        
        else:
            print("not in tree")


class Server(Ice.Application):
    '''Server class'''
    def run(self, argv):
        '''Run method'''

        print(TXPURPLE + "[DIRECTORY] Launching directory service..." + TXENDC)

        broker = self.communicator()
        servant = DirectoryService()


        adapter = broker.createObjectAdapter("DirectoryServiceAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("directoryService1"))
        

        print(proxy)
        sys.stdout.flush()

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()


server = Server()
sys.exit(server.main(sys.argv))


        
