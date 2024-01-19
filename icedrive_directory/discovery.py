"""Servant implementations for service discovery."""
import logging

import Ice

import IceDrive


class Discovery(IceDrive.Discovery):
    """Servants class for service discovery."""


    def __init__(self):
        conjunto_authentication = set()
        conjunto_directoryService = set()
        conjunto_blobService = set()




    def announceAuthentication(self, prx: IceDrive.AuthenticationPrx, current: Ice.Current = None) -> None:
        """Receive an Authentication service announcement."""

        logging.info("[Authentication Proxy] %s", prx)

        self.conjunto_authentication.add(prx)

    def getAuthenticationPrx(self ,current: Ice.Current = None) -> IceDrive.AuthenticationPrx:

        while len(self.conjunto_authentication) != 0:
            prx = self.conjunto_authentication.pop()
            self.conjunto_authentication.add(prx)

            try:
                prx.ice_ping()
                return prx
            
            except Ice.Exception:
                self.conjunto_authentication.remove(prx)
        
        return None




    def announceDirectoryService(self, prx: IceDrive.DirectoryServicePrx, current: Ice.Current = None) -> None:
        """Receive an Directory service announcement."""

        logging.info("[DirectoryService Proxy] %s", prx)

        self.conjunto_directoryService.add(prx)

    def getDirectoryServicePrx(self ,current: Ice.Current = None) -> IceDrive.AuthenticationPrx:

        while len(self.conjunto_directoryService) != 0:
            prx = self.conjunto_directoryService.pop()
            self.conjunto_directoryService.add(prx)

            try:
                prx.ice_ping()
                return prx
            
            except Ice.Exception:
                self.conjunto_directoryService.remove(prx)
        
        return None




    def announceBlobService(self, prx: IceDrive.BlobServicePrx, current: Ice.Current = None) -> None:
        """Receive an Blob service announcement."""

        logging.info("[BlobService Proxy] %s", prx)

        self.conjunto_blobService.add(prx)

    def getAuthenticationPrx(self ,current: Ice.Current = None) -> IceDrive.AuthenticationPrx:

        while len(self.conjunto_blobService) != 0:
            prx = self.conjunto_blobService.pop()
            self.conjunto_blobService.add(prx)

            try:
                prx.ice_ping()
                return prx
            
            except Ice.Exception:
                self.conjunto_blobService.remove(prx)
        
        return None
