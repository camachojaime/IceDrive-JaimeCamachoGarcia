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

    def getAuthentication(self):
        return self.conjunto_authentication.pop()



    def announceDirectoryService(self, prx: IceDrive.DirectoryServicePrx, current: Ice.Current = None) -> None:
        """Receive an Directory service announcement."""

        logging.info("[DirectoryService Proxy] %s", prx)

        self.conjunto_directoryService.add(prx)

    def getDirectoryService(self):
        return self.conjunto_directoryService.pop()



    def announceBlobService(self, prx: IceDrive.BlobServicePrx, current: Ice.Current = None) -> None:
        """Receive an Blob service announcement."""

        logging.info("[BlobService Proxy] %s", prx)

        self.conjunto_blobService.add(prx)

    def getBlobService(self):
        return self.conjunto_blobService.pop()
