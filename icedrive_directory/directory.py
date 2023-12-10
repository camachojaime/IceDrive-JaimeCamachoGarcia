"""Module for servants implementations."""
import sys
#import json
import os

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

driveRoute = None   # Poner en fichero de configuracion


class Directory(IceDrive.Directory):
    """Implementation of the IceDrive.Directory interface."""

    def __init__(self):
        self.route = ""
        self.childs = []
        self.files = []


    def getParent(self, current: Ice.Current = None) -> IceDrive.DirectoryPrx:
        """Return the proxy to the parent directory, if it exists. None in other case."""
        
        v = self.route.split('/')

        if len(v) > 1:
            v.pop()

            self.route = '/'.join(v)

            proxy = current.adapter.addWithUUID(self)
            return IceDrive.DirectoryPrx.uncheckedCast(proxy)
        
        raise IceDrive.RootHasNoParent()
        # return None


    def getChilds(self, current: Ice.Current = None) -> List[str]:
        """Return a list of names of the directories contained in the directory."""

        directorys = os.path.join(os.getcwd(), "usersDirectorys", self.route)
        
        # self.childs = []
        # for dir in os.listdir(directorys):
        #     if os.path.isdir(os.path.join(directorys, dir)):
        #         self.childs.append(dir)

        return [nombre for nombre in os.listdir(directorys) if os.path.isdir(os.path.join(directorys, nombre))]


    def getChild(self, name: str, current: Ice.Current = None) -> IceDrive.DirectoryPrx:
        """Return the proxy to one specific directory inside the current one."""

        route = os.path.join(self.route, name)

        if name in self.getChilds():
        #try:
            self.route = route

            proxy = current.adapter.addWithUUID(self)
            return IceDrive.DirectoryPrx.uncheckedCast(proxy)
        
        #except:
        raise IceDrive.ChildNotExists( name, route)
        # return None


    def createChild(self, name: str, current: Ice.Current = None) -> IceDrive.DirectoryPrx:
        """Create a new child directory and returns its proxy."""

        route = os.path.join(os.getcwd(), "usersDirectorys", self.route, name)
        
        if name not in self.getChilds():
            route = os.path.join(os.getcwd(), "usersDirectorys", self.route, name)
            os.makedirs(route)

            proxy = current.adapter.addWithUUID(self)
            return IceDrive.DirectoryPrx.uncheckedCast(proxy)

        raise IceDrive.ChildAlreadyExists( name, route)
        # return None


    def removeChild(self, name: str, current: Ice.Current = None) -> None:
        """Remove the child directory with the given name if exists."""

        if name in self.getChilds():
            os.rmdir(os.path.join(os.getcwd(), "usersDirectorys", self.route, name))


    def getFiles(self, current: Ice.Current = None) -> List[str]:
        """Return a list of the files linked inside the current directory."""

        directorys = os.path.join(os.getcwd(), "usersDirectorys", self.route)
        
        files = []
        for f in os.listdir(directorys):
            if not os.path.isdir(os.path.join(directorys, f)):
                files.append(f)
        
        return files


    def getBlobId(self, filename: str, current: Ice.Current = None) -> str:
        """Return the "blob id" for a given file name inside the directory."""

        if filename in self.getFiles():
            with open(os.path.join(os.getcwd(), "usersDirectorys", self.route, filename), 'r') as file:
                return(file.read())
        
        raise IceDrive.FileNotFound(filename)
        # return ""


    def linkFile(self, filename: str, blob_id: str, current: Ice.Current = None) -> None:
        """Link a file to a given blob_id."""

        if filename not in self.getFiles():
            with open(os.path.join(os.getcwd(), "usersDirectorys", self.route, filename), 'w') as file:
                file.write(blob_id)
        
        raise IceDrive.FileAlreadyExists(filename)


    def unlinkFile(self, filename: str, current: Ice.Current = None) -> None:
        """Unlink (remove) a filename from the current directory."""

        if filename in self.getFiles():
            os.remove(os.path.join(os.getcwd(), "usersDirectorys", self.route, filename))
        
        raise IceDrive.FileNotFound(filename)


class DirectoryService(IceDrive.DirectoryService):
    """Implementation of the IceDrive.Directory interface."""


    def getRoot(self, user: str, current: Ice.Current = None) -> IceDrive.DirectoryPrx:
        """Return the proxy for the root directory of the given user."""

        print(TXYELLOW + "Buscando usuario..." + TXENDC) 

        usersDirectorys = os.path.join(os.getcwd(), 'usersDirectorys')

        directory = Directory()
        directory.route += user

        if user in os.listdir(usersDirectorys) and os.path.isdir(os.path.join(usersDirectorys, user)):
            print(TXPURPLE + "Usuario encontrado!!!" + TXENDC)                  

            proxy = current.adapter.addWithUUID(directory)
            return IceDrive.DirectoryPrx.uncheckedCast(proxy)
        
        os.mkdir(os.path.join(usersDirectorys, user))
        print(TXPURPLE + "Usuario creado!!!" + TXENDC)  

        proxy = current.adapter.addWithUUID(directory)
        return IceDrive.DirectoryPrx.uncheckedCast(proxy)


# class Server(Ice.Application):
#     '''Server class'''
#     def run(self, argv):
#         '''Run method'''

#         print(TXPURPLE + "[DIRECTORY] Launching directory..." + TXENDC)

#         broker = self.communicator()
#         servant = DirectoryService()

#         adapter = broker.createObjectAdapter("DirectoryServiceAdapter")
#         proxy = adapter.add(servant, broker.stringToIdentity("DirectoryService1"))

#         print(proxy)

#         adapter.activate()
#         self.shutdownOnInterrupt()
#         broker.waitForShutdown()

#         sys.stdout.flush()


# server = Server()
# sys.exit(server.main(sys.argv))


