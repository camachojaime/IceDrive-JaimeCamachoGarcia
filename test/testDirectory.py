import sys

import Ice
Ice.loadSlice('icedrive_directory/icedrive.ice')
import IceDrive

# import icedrive_directory.directory

class Client(Ice.Application):
    def run(self, argv):
        proxy = self.communicator().stringToProxy(argv[1])

        #printer = Example.PrinterPrx.checkedCast(proxy)
        directoryService = IceDrive.DirectoryServicePrx.checkedCast(proxy)
        directory = IceDrive.DirectoryPrx.checkedCast(proxy)

        if not directoryService and not directory:
            raise RuntimeError('Invalid proxy')
        
        else:

            while True:

                # option = input("1- Obtener usuario\ttestDirectoryService\n" +
                #       "2- testDirectory\n" +
                #       "3- Salir\n"
                #       "Numero: ")
                
                directory = directoryService.getRoot(input("Nombre usuario: "))

                # IceDrive.DirectoryPrx.uncheckedCast(proxy)

                if directory:

                    while True:

                        option = input("0- getParent\n" +
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
                            #print()

                        elif option == str(2):

                            #print(directory.route)
                            # directoryAux = directory.getChild(input("Acceder a: "))

                            # dir2 = directory.getChild(input("Acceder a: "))
                            # print('')
                            # print(type(dir2))
                            # print(dir2.route)

                            dir = None
                            dir = directory.getChild(input("Acceder a:"))
                            print('')

                            if dir:
                                # print(type(directory))
                                # print(type(directoryAux.route))
                                # print(directoryAux.route)
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



                        elif option == str(6):
                            print(directory.getBlobId("Hola"))

                        elif option == 'E':
                            break

                else:
                    print("USUARIO NO ENCONTRADO")
                    break
                



client = Client()
sys.exit(client.main(sys.argv))