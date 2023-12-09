import sys

import Ice
Ice.loadSlice('icedrive_directory/icedrive.ice')
import IceDrive

# import icedrive_directory.directory

class Client(Ice.Application):
    def run(self, argv):
        proxy = self.communicator().stringToProxy(argv[1])

        directoryService = IceDrive.DirectoryServicePrx.checkedCast(proxy)
        directory = IceDrive.DirectoryPrx.checkedCast(proxy)

        if not directoryService and not directory:
            raise RuntimeError('Invalid proxy')
        
        else:

            while True:

                print()
                directory = directoryService.getRoot(input("Nombre usuario: "))

                if directory:

                    while True:

                        option = input("\nMenu:\n" +
                                    "0- getParent\n" +
                                    "1- getChilds\n" +
                                    "2- getChild\n" +
                                    "3- createChild\n" +
                                    "4- removeChild\n" +
                                    "5- getFiles\n" +
                                    "6- getBlobId\n" +
                                    "7- linkFile\n" +
                                    "8- unlinkFile\n" +
                                    "9- Cambiar usuario\n" +
                                    "E- Exit\n\n" +
                                    "\tOpcion: ")
                    
                        if option == str(0):
                        
                            directoryAux = directory.getParent()
                            if directoryAux:
                                # print(directoryAux.route)
                                directory = directoryAux
                            else:
                                print("Esta en root")
                    
                        elif option == str(1):
                            print("\n\t" + str(directory.getChilds()) + "\n")

                        elif option == str(2):

                            dir = None
                            dir = directory.getChild(input("\n\tAcceder a:"))
                            print('')

                            if dir:
                                directory = dir
                            else:
                                print("No se encontro la carpeta")

                        elif option == str(3):

                            dir = None
                            dir = directory.createChild(input("\nNombre de la nueva carpeta: "))
                            print('')
                            
                            if dir:
                                directory = dir
                            else:
                                print('Carpeta ya existente')
                        
                        elif option == str(4):
                        
                            dir = None
                            dir = directory.removeChild(input("\nNombre de la carpeta: "))
                            print('')

                            if dir:
                                directory = dir

                            else:
                                print('La carpeta no existe')
                        
                        elif option == str(5):

                            files = directory.getFiles()
                            print()
                            print(files)
                            print()

                        elif option == str(6):
                            print(directory.getBlobId(input("\n\tNombre archivo (con extension): ")))
                            print()
                        
                        elif option == str(7):
                            
                            directory.linkFile(input("\n\tNombre archivo (con extension): "), input("\n\tBlob_id: "))
                            print()
                            # filename = input()
                        
                        elif option == str(8):

                            directory.unlinkFile(input("\n\tNombre archivo (con extension): "))
                            print()


                        elif option == 'E':
                            break

                else:
                    print("USUARIO NO ENCONTRADO")
                    break
                



client = Client()
sys.exit(client.main(sys.argv))