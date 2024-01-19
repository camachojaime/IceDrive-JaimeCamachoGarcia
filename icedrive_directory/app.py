"""Authentication service application."""

import logging
import sys
from typing import List
import time, threading

import Ice
import IceStorm

import IceDrive
from discovery import Discovery

from .directory import DirectoryService


class DirectoryApp(Ice.Application):
    """Implementation of the Ice.Application for the Authentication service."""

    def run(self, args: List[str]) -> int:
        """Execute the code for the AuthentacionApp class."""



        # SetUP IceStorm
        properties = self.communicator().getProperties()
        topic_name = properties.getProperty("DirectoryQueryTopic")

        topic_manager = IceStorm.TopicManagerPrx.checkedCast(
            self.communicator().propertyToProxy("IceStorm.TopicManager.Proxy")
        )

        try:
            topic = topic_manager.retrieve(topic_name)
        except:
            topic = topic_manager.create(topic_name)



        # DiscoveryPub
        discovery_pub = IceDrive.DiscoveryPrx.uncheckedCast(topic.getPublisher())
        threading.Thread(target=self.sendAnnoucement, args=(discovery_pub, servant_proxy), daemon=True).start()



        adapter = self.communicator().createObjectAdapter("DirectoryAdapter")
        adapter.activate()

        servant = DirectoryService()
        servant_proxy = adapter.addWithUUID(servant)
        directoryPrx = IceDrive.DirectoryPrx.uncheckedCast(servant_proxy)

        servantDis = Discovery()
        servantDis_proxy = adapter.addWithUUID(servantDis)
        discoveryPrx = IceDrive.DiscoveryPrx.uncheckedCast(servantDis_proxy)    ######

        self.sendAnnounces(discovery_pub, directoryPrx)


        ###
        topic.subscribeAndGetPublisher({}, discoveryPrx)

        logging.info("Proxy: %s", directoryPrx)

        self.shutdownOnInterrupt()
        self.communicator().waitForShutdown()

        return 0


    def sendAnnounces(self, publisher, servicePrx):
        
        while True:
            publisher.announceDirectoryServicey(servicePrx)
            print(servicePrx)
            time.sleep(5)
        


def main():
    """Handle the icedrive-authentication program."""
    app = DirectoryApp()
    return app.main(sys.argv)
