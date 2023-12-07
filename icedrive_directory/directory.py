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


# def isRoot(str):
#     # Try
#     # with open("tree.json") as file:
#     #     tree = json.load(file)

#     # if tree:
#     #     for i in tree:
#     #         if i["root"] == str:
#     #             return True

#     # return False


#     usersDirectorys = os.path.join(os.getcwd(), 'usersDirectorys')
#     users = [nombre for nombre in os.listdir(usersDirectorys) if os.path.isdir(os.path.join(usersDirectorys, nombre))]

#     if str in users:
#         return True

#     return False
        







class Directory(IceDrive.Directory):
    """Implementation of the IceDrive.Directory interface."""

    def __init__(self):
        self.route = ""
        #self.isRoot = False

    def getParent(self, current: Ice.Current = None) -> IceDrive.DirectoryPrx:
        """Return the proxy to the parent directory, if it exists. None in other case."""
        
        if len(self.route.split('/')) == 1:
            return False                        # Poner otra condicion para poner el return fuera
        else:
            v = self.route.split('/')
            v.pop(len(v)-1)
            self.route = '/'.join(v)

            print(self.route)

            proxy = current.adapter.addWithUUID(self)
            return IceDrive.DirectoryPrx.uncheckedCast(proxy)


    def getChilds(self, current: Ice.Current = None) -> List[str]:
        """Return a list of names of the directories contained in the directory."""

        route = "usersDirectorys/" + self.route
        directorys = os.path.join(os.getcwd(), route)                                                               # Add files y extension
        return [nombre for nombre in os.listdir(directorys) if os.path.isdir(os.path.join(directorys, nombre))]


    def getChild(self, name: str, current: Ice.Current = None) -> IceDrive.DirectoryPrx:
        """Return the proxy to one specific directory inside the current one."""

        # print(os.getcwd())

        #self.route = os.getcwd() + "/usersDirectorys/" + self.route

        if name in self.getChilds():
            self.route = self.route + name + "/"
            print(self.route)                                   # DELETE

            proxy = current.adapter.addWithUUID(self)
            return IceDrive.DirectoryPrx.uncheckedCast(proxy)

            # Dir2 = Directory()
            # Dir2.route = self.route
            # proxy = current.adapter.addWithUUID(Dir2)
            # return IceDrive.DirectoryPrx.uncheckedCast(proxy)

        return False

        # usersDirectorys = os.path.join(os.getcwd(), self.route)
        # users = [nombre for nombre in os.listdir(usersDirectorys) if os.path.isdir(os.path.join(usersDirectorys, nombre))]


    def createChild(self, name: str, current: Ice.Current = None) -> IceDrive.DirectoryPrx:
        """Create a new child directory and returns its proxy."""
        
        if name not in self.getChilds():
            route = os.getcwd() + "/usersDirectorys/" + self.route + name
            print(route)

            os.makedirs(route)
            print("Hecho")

            proxy = current.adapter.addWithUUID(self)
            return IceDrive.DirectoryPrx.uncheckedCast(proxy)

        return False



    def removeChild(self, name: str, current: Ice.Current = None) -> None:
        """Remove the child directory with the given name if exists."""

    def getFiles(self, current: Ice.Current = None) -> List[str]:
        """Return a list of the files linked inside the current directory."""

    def getBlobId(self, filename: str, current: Ice.Current = None) -> str:             # Metodo prueba
        """Return the "blob id" for a given file name inside the directory."""
        return "Hola mundo 2.0"

    def linkFile(self, filename: str, blob_id: str, current: Ice.Current = None) -> None:
        """Link a file to a given blob_id."""

    def unlinkFile(self, filename: str, current: Ice.Current = None) -> None:
        """Unlink (remove) a filename from the current directory."""


class DirectoryService(IceDrive.DirectoryService):
    """Implementation of the IceDrive.Directory interface."""

    def __init__(self):
        self.broker = None
    

    def getRoot(self, user: str, current: Ice.Current = None) -> IceDrive.DirectoryPrx:
        """Return the proxy for the root directory of the given user."""

        print(TXYELLOW + "Buscando usuario..." + TXENDC) 


        usersDirectorys = os.path.join(os.getcwd(), 'usersDirectorys')
        # print("pasa")
        users = [nombre for nombre in os.listdir(usersDirectorys) if os.path.isdir(os.path.join(usersDirectorys, nombre))]
        # print("sjssjjs")
        # print(len(users))
        # print(users)
        # print(type(users))
        # print(user)
        # print(user == 'Jaime')
        # print(user in users)
        if user in users:

            print(TXPURPLE + "Usuario encontrado!!!" + TXENDC)                  

            directory = Directory()         # Servant
            directory.route += user + "/"
            print(directory.route)

            proxy = current.adapter.addWithUUID(directory)
            return IceDrive.DirectoryPrx.uncheckedCast(proxy)

        print(TXRED + "Usuario no encontrado!!!" + TXENDC)                  
        #return False
            
        # else:
        #     print(TXRED + "Usuario no encontrado" + TXENDC)


class Server(Ice.Application):
    '''Server class'''
    def run(self, argv):
        '''Run method'''

        print(TXPURPLE + "[DIRECTORY] Launching directory..." + TXENDC)

        # root = input("Introduzca usuario: ")

        broker = self.communicator()
        servant = DirectoryService()
        # servant.route = root
        # servant.route = input("Introduzca usuario: ")

        adapter = broker.createObjectAdapter("DirectoryServiceAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("DirectoryService1"))

        # print(str(proxy) + "\n\n" +
        #       "Introduzca el anterior proxy en otra terminal de comandos\n\n" +
        #       "\t$ python3 Client.py 'proxy'")
        # sys.stdout.flush()
        print(proxy)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        # adapter = self.communicator().createObjectAdapter("DirectoryAdapter")
        # adapter.activate()

        # broker2 = self
        # broker3 = self.communicator()
        #servant = Directory()

        # adapter = self.communicator().createObjectAdapter("DirectoryAdapter")
        # # proxy = adapter.add(servant, broker.stringToIdentity("directory1"))
        # proxy = adapter.add(self, broker.stringToIdentity("directory1"))


        # servant = DirectoryService()
        # servant_proxy = adapter.addWithUUID(servant)

        # servant = DirectoryService()
        servant_proxy = adapter.addWithUUID(self)


        # print(servant_proxy)
        sys.stdout.flush()

        # adapter.activate()
        # self.shutdownOnInterrupt()
        # broker.waitForShutdown()

        self.shutdownOnInterrupt()
        self.communicator().waitForShutdown()


server = Server()
sys.exit(server.main(sys.argv))


