"""Authentication service application."""

import logging
import sys
from typing import List
import time

import Ice
import IceStorm

import IceDrive

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
        







        adapter = self.communicator().createObjectAdapter("DirectoryAdapter")
        adapter.activate()

        servant = DirectoryService()
        servant_proxy = adapter.addWithUUID(servant)

        self.sendAnnouncet(discovery_pub, servant_proxy)        ## unche


        #
        topic.subscribeAndGetPublisher({}, )

        logging.info("Proxy: %s", servant_proxy)

        self.shutdownOnInterrupt()
        self.communicator().waitForShutdown()

        return 0


    def sendAnnouncet(self, publisher, servicePrx):
        publisher.announceDirectoryServicey(servicePrx)   #############################################   Cada 5 segundos
        print("5 segundos")
        time.sleep(5)
        self.sendAnnouncet(publisher, servicePrx)
        


def main():
    """Handle the icedrive-authentication program."""
    app = DirectoryApp()
    return app.main(sys.argv)
