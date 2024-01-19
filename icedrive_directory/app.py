"""Authentication service application."""

import logging
import sys
from typing import List

import Ice
import IceStorm

import IceDrive

from .directory import DirectoryService


class DirectoryApp(Ice.Application):
    """Implementation of the Ice.Application for the Authentication service."""

    def run(self, args: List[str]) -> int:
        """Execute the code for the AuthentacionApp class."""

        print("")

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
        discovery_pub.announceDirectoryServicey()   #############################################   Cada 5 segundos







        adapter = self.communicator().createObjectAdapter("DirectoryAdapter")
        adapter.activate()

        servant = DirectoryService()
        servant_proxy = adapter.addWithUUID(servant)


        #
        topic.subscribeAndGetPublisher({}, )

        logging.info("Proxy: %s", servant_proxy)

        self.shutdownOnInterrupt()
        self.communicator().waitForShutdown()

        return 0


def main():
    """Handle the icedrive-authentication program."""
    app = DirectoryApp()
    return app.main(sys.argv)
