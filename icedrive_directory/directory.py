"""Module for servants implementations."""

from typing import List

import Ice

import IceDrive

import os
from discovery import Discovery


TXPURPLE = '\033[95m'           # Success color (purple)
TXRED = '\033[91m'              # Error color (red)
TXYELLOW = '\033[93m'           # Yellow color
TXORANGE = '\033[38;5;208m'     # Orange color
TXENDC = '\033[0m'              # Standar color


class Directory(IceDrive.Directory):
    """Implementation of the IceDrive.Directory interface."""


    def __init__(self, discovery, user):
        self.route = ""
        self.childs = []
        self.files = []

        self.discovery = discovery
        self.user = user


    def getPath(self, current: Ice.Current = None) -> str:
        """Return the path for the directory within the user space."""

    def getParent(self, current: Ice.Current = None) -> IceDrive.DirectoryPrx:
        """Return the proxy to the parent directory, if it exists. None in other case."""

        if self.user.isAlive():
            v = self.route.split('/')

            if len(v) > 1:
                v.pop()

                self.route = '/'.join(v)

                proxy = current.adapter.addWithUUID(self)
                return IceDrive.DirectoryPrx.uncheckedCast(proxy)
            
            raise IceDrive.RootHasNoParent()

        print(TXRED + "User not is alive" + TXENDC)
    


    def getChilds(self, current: Ice.Current = None) -> List[str]:
        """Return a list of names of the directories contained in the directory."""

        if self.user.isAlive():
            directorys = os.path.join(os.getcwd(), "usersDirectorys", self.route)
            
            # self.childs = []
            # for dir in os.listdir(directorys):
            #     if os.path.isdir(os.path.join(directorys, dir)):
            #         self.childs.append(dir)

            return [nombre for nombre in os.listdir(directorys) if os.path.isdir(os.path.join(directorys, nombre))]

        print(TXRED + "User not is alive" + TXENDC)



    def getChild(self, name: str, current: Ice.Current = None) -> IceDrive.DirectoryPrx:
        """Return the proxy to one specific directory inside the current one."""

        if self.user.isAlive():
            route = os.path.join(self.route, name)

            if name in self.getChilds():
            #try:
                self.route = route

                proxy = current.adapter.addWithUUID(self)
                return IceDrive.DirectoryPrx.uncheckedCast(proxy)
            
            #except:
            raise IceDrive.ChildNotExists( name, route)
        
        print(TXRED + "User not is alive" + TXENDC)
        


    def createChild(
        self, name: str, current: Ice.Current = None
    ) -> IceDrive.DirectoryPrx:
        """Create a new child directory and returns its proxy."""

        if self.user.isAlive():
            route = os.path.join(os.getcwd(), "usersDirectorys", self.route, name)
            
            if name not in self.getChilds():
                route = os.path.join(os.getcwd(), "usersDirectorys", self.route, name)
                os.makedirs(route)

                proxy = current.adapter.addWithUUID(self)
                return IceDrive.DirectoryPrx.uncheckedCast(proxy)

            raise IceDrive.ChildAlreadyExists( name, route)
        
        print(TXRED + "User not is alive" + TXENDC)



    def removeChild(self, name: str, current: Ice.Current = None) -> None:
        """Remove the child directory with the given name if exists."""

        if self.user.isAlive():
            if name in self.getChilds():
                os.rmdir(os.path.join(os.getcwd(), "usersDirectorys", self.route, name))
        
        print(TXRED + "User not is alive" + TXENDC)



    def getFiles(self, current: Ice.Current = None) -> List[str]:
        """Return a list of the files linked inside the current directory."""

        if self.user.isAlive():
            directorys = os.path.join(os.getcwd(), "usersDirectorys", self.route)
            
            files = []
            for f in os.listdir(directorys):
                if not os.path.isdir(os.path.join(directorys, f)):
                    files.append(f)
            
            return files
        
        print(TXRED + "User not is alive" + TXENDC)



    def getBlobId(self, filename: str, current: Ice.Current = None) -> str:
        """Return the "blob id" for a given file name inside the directory."""

        if self.user.isAlive():
            if filename in self.getFiles():
                with open(os.path.join(os.getcwd(), "usersDirectorys", self.route, filename), 'r') as file:
                    return(file.read())
            
            raise IceDrive.FileNotFound(filename)
        
        print(TXRED + "User not is alive" + TXENDC)



    def linkFile(
        self, filename: str, blob_id: str, current: Ice.Current = None
    ) -> None:
        """Link a file to a given blob_id."""

        if self.user.isAlive():
            blobService = self.discovery.getBlobService()

            if blobService.link(blob_id):

                if filename not in self.getFiles():
                    with open(os.path.join(os.getcwd(), "usersDirectorys", self.route, filename), 'w') as file:
                        file.write(blob_id)
            
                raise IceDrive.FileAlreadyExists(filename)
            
            raise IceDrive.TemporaryUnavailable("BlobService")
        
        print(TXRED + "User not is alive" + TXENDC)


    def unlinkFile(self, filename: str, current: Ice.Current = None) -> None:
        """Unlink (remove) a filename from the current directory."""

        if self.user.isAlive():
            blob_service = self.discovery.getBlobId()

            if filename in self.getFiles():

                with open(os.path.join(os.getcwd(), "usersDirectorys", self.route, filename), 'r') as file:
                    blob_id = file.read()
                    blob_service.Unlink(blob_id)

                os.remove(os.path.join(os.getcwd(), "usersDirectorys", self.route, filename))
            
            raise IceDrive.FileNotFound(filename)
        
        print(TXRED + "User not is alive" + TXENDC)





class DirectoryService(IceDrive.DirectoryService):
    """Implementation of the IceDrive.Directory interface."""


    def __init__(self, discovery):
        self.discovery = discovery


    def getRoot(self, user: IceDrive.UserPrx, current: Ice.Current = None) -> IceDrive.DirectoryPrx:
        """Return the proxy for the root directory of the given user."""

        auth = self.discovery.getAuthenticationPrx()

        print(TXYELLOW + "Buscando usuario..." + TXENDC)
        userName = user.getUsername()
        
        usersDirectorys = os.path.join(os.getcwd(), 'usersDirectorys')
        
        directory = Directory(self.discovery, user)
        directory.route += userName
        
        if auth.verifyUser(user):

            if userName in os.listdir(usersDirectorys) and os.path.isdir(os.path.join(usersDirectorys, userName)):
                print(TXPURPLE + "Usuario encontrado!!!" + TXENDC)                  

                proxy = current.adapter.addWithUUID(directory)
                return IceDrive.DirectoryPrx.uncheckedCast(proxy)

            os.mkdir(os.path.join(usersDirectorys, userName))
            print(TXPURPLE + "Usuario creado!!!" + TXENDC)

            proxy = current.adapter.addWithUUID(directory)
            return IceDrive.DirectoryPrx.uncheckedCast(proxy)
        

        raise IceDrive.TemporaryUnavailable("Authentication")


