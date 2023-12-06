# import os

# # Obtener la carpeta actual
# carpeta_actual = os.getcwd()
# print(f'Carpeta actual: {carpeta_actual}')

# # Obtener archivos y carpetas en la ubicación del .py
# archivos_y_carpetas = os.listdir(carpeta_actual)
# print(f'Archivos y carpetas en la ubicación del .py: {archivos_y_carpetas}')

# # Especificar la ruta de la otra carpeta
# otra_carpeta = os.path.join(carpeta_actual, 'usersDirectorys')

# # Obtener carpetas en la otra carpeta
# carpetas_en_otra_carpeta = [nombre for nombre in os.listdir(otra_carpeta) if os.path.isdir(os.path.join(otra_carpeta, nombre))]
# print(f'Carpetas en la otra carpeta: {carpetas_en_otra_carpeta}')



str = "Jaime-Zipi-Utri"

v = str.split("-")

print(len(v))

v.pop(2)

str2 = "-".join(v)
print(str2)
