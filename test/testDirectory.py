import sys

import Ice
Ice.loadSlice('icedrive_directory/icedrive.ice')
import IceDrive

class Client(Ice.Application):
    def run(self, argv):
        proxy = self.communicator().stringToProxy(argv[1])

        #printer = Example.PrinterPrx.checkedCast(proxy)
        directoryService = IceDrive.DirectoryServicePrx.checkedCast(proxy)

        if not directoryService:
            raise RuntimeError('Invalid proxy')
        
        else:

            while True:

                option = input("1- Option1\n" +
                      "2- Option2\n" +
                      "Numero: ")
                
                if option == str(1):


                    directoryService.getRoot(input("Nombre usuario: "))

                elif option == str(2):
                    break



client = Client()
sys.exit(client.main(sys.argv))