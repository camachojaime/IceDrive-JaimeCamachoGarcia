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
        #self.isRoot = False


    def getParent(self, current: Ice.Current = None) -> IceDrive.DirectoryPrx:                      # DO
        """Return the proxy to the parent directory, if it exists. None in other case."""
        
        v = self.route.split('/')
        # print('ROUTE: ' + self.route)
        # print(v)

        if len(v) > 1:
            # v.pop(len(v)-1)
            # v.pop(len(v)-1)

            v.pop()

            self.route = '/'.join(v)
            # print("After: " + self.route)
            # print(self.route)

            proxy = current.adapter.addWithUUID(self)
            return IceDrive.DirectoryPrx.uncheckedCast(proxy)

        return None


    def getChilds(self, current: Ice.Current = None) -> List[str]:                                      # DO
        """Return a list of names of the directories contained in the directory."""

        directorys = os.path.join(os.getcwd(), "usersDirectorys", self.route)
        
        # self.childs = []
        # for dir in os.listdir(directorys):
        #     if os.path.isdir(os.path.join(directorys, dir)):
        #         self.childs.append(dir)

        return [nombre for nombre in os.listdir(directorys) if os.path.isdir(os.path.join(directorys, nombre))]
        # return self.childs


    def getChild(self, name: str, current: Ice.Current = None) -> IceDrive.DirectoryPrx:                # DO
        """Return the proxy to one specific directory inside the current one."""

        # print(os.getcwd())

        #self.route = os.getcwd() + "/usersDirectorys/" + self.route

        if name in self.getChilds():
            #self.route = self.route + name + "/"
            self.route = os.path.join(self.route, name)

            proxy = current.adapter.addWithUUID(self)
            return IceDrive.DirectoryPrx.uncheckedCast(proxy)

            # Dir2 = Directory()
            # Dir2.route = self.route
            # proxy = current.adapter.addWithUUID(Dir2)
            # return IceDrive.DirectoryPrx.uncheckedCast(proxy)

        # return False
        return None

        # usersDirectorys = os.path.join(os.getcwd(), self.route)
        # users = [nombre for nombre in os.listdir(usersDirectorys) if os.path.isdir(os.path.join(usersDirectorys, nombre))]


    def createChild(self, name: str, current: Ice.Current = None) -> IceDrive.DirectoryPrx:
        """Create a new child directory and returns its proxy."""

        if name not in self.getChilds():                                            # Si no se llama aqui a getChilds, hay que llamarlo luego para actualizar la lista
            # route = os.getcwd() + "/usersDirectorys/" + self.route + name
            route = os.path.join(os.getcwd(), "usersDirectorys", self.route, name)
            # print(route)

            os.makedirs(route)
            # print("Hecho")

            proxy = current.adapter.addWithUUID(self)
            return IceDrive.DirectoryPrx.uncheckedCast(proxy)

        # return False
        return None


    def removeChild(self, name: str, current: Ice.Current = None) -> None:
        """Remove the child directory with the given name if exists."""

        if name in self.getChilds():
            route = os.getcwd() + "/usersDirectorys/" + self.route + name
            os.rmdir(route)

        #     proxy = current.adapter.addWithUUID(self)
        #     return IceDrive.DirectoryPrx.uncheckedCast(proxy)

        # return None


        # os.rmdir()


    def getFiles(self, current: Ice.Current = None) -> List[str]:
        """Return a list of the files linked inside the current directory."""

        directorys = os.path.join(os.getcwd(), "usersDirectorys", self.route)

        # print(os.path.isdir(os.path.join(os.getcwd(), "usersDirectorys", "Jaime", "archJaime.txt")))
        
        files = []
        for f in os.listdir(directorys):
            if not os.path.isdir(os.path.join(directorys, f)):
                files.append(f)
        
        return files

        # for dir in os.listdir(directorys):
        #     if os.path.isdir(os.path.join(directorys, dir)):
        #         self.childs.append(dir)

        # return [nombre for nombre in os.listdir(directorys) if os.path.isdir(os.path.join(directorys, nombre))]


    def getBlobId(self, filename: str, current: Ice.Current = None) -> str:
        """Return the "blob id" for a given file name inside the directory."""
        
        #   if user in os.listdir(usersDirectorys) and os.path.isdir(os.path.join(usersDirectorys, user)):
        
        if filename in self.getFiles():
            with open(os.path.join(os.getcwd(), "usersDirectorys", self.route, filename), 'r') as file:
                return(file.read())
            #blob = file.read()
        
        return ""
        #return blob


    def linkFile(self, filename: str, blob_id: str, current: Ice.Current = None) -> None:
        """Link a file to a given blob_id."""

        if filename not in self.getFiles():
            #with open(os.path.join(os.getcwd(), "usersDirectorys", self.route, filename+".txt"), 'w') as file:
            with open(os.path.join(os.getcwd(), "usersDirectorys", self.route, filename), 'w') as file:
                file.write(blob_id)


    def unlinkFile(self, filename: str, current: Ice.Current = None) -> None:
        """Unlink (remove) a filename from the current directory."""

        #print(filename in self.getFiles())
        if filename in self.getFiles():
            #print("ENTRA")
            #os.remove(os.path.join(os.getcwd(), "usersDirectorys", self.route, filename+".txt"))
            os.remove(os.path.join(os.getcwd(), "usersDirectorys", self.route, filename))


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

            # directory = Directory()         # Servant
            # # directory.route += user + "/"
            # directory.route += user
            # print(directory.route)

            proxy = current.adapter.addWithUUID(directory)
            return IceDrive.DirectoryPrx.uncheckedCast(proxy)
        
        os.mkdir(os.path.join(usersDirectorys, user))
        print(TXPURPLE + "Usuario creado!!!" + TXENDC)  

        # directory = Directory()
        # directory.route += user
        # print(directory.route)

        proxy = current.adapter.addWithUUID(directory)
        return IceDrive.DirectoryPrx.uncheckedCast(proxy)

        # print(TXRED + "Usuario no encontrado!!!" + TXENDC)
        # return None


class Server(Ice.Application):
    '''Server class'''
    def run(self, argv):
        '''Run method'''

        print(TXPURPLE + "[DIRECTORY] Launching directory..." + TXENDC)

        broker = self.communicator()
        servant = DirectoryService()

        adapter = broker.createObjectAdapter("DirectoryServiceAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("DirectoryService1"))

        print(proxy)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        # servant_proxy = adapter.addWithUUID(self)
        sys.stdout.flush()

        # self.shutdownOnInterrupt()
        # self.communicator().waitForShutdown()


server = Server()
sys.exit(server.main(sys.argv))


