import os
import re
import csv

"""
Script para auditar el stock de licencias y renovaciones de test que
tenemos en la carpeta TEST.
Cada tipo de test tiene una estructura en el nombre distinta.
Por otar parte, hay que distinguir las vendidas de las libres.
Las vendidas tienen un patrón del tio añomesdía (20210115).
Las libres:
BADyG y PP -> 01522_NumerosLicencia_GestorBADyG-E1.pdf
BECOLE -> LICENCIA DE ACTIVACIÓN NIVEL BECOLE M-4.pdf
DIX y PAIB -> dix_2-40.pdf
La función tree_printer obtiene un listado de todos los archivos pdf.
La función list_files toma la lista de los archivos pdf de tree_printer y
separa el nombre del archivo del path. Según el tipo de test, limpia el nombre
del archivo y lo adjunta a la lista de test.
La función tipo_test cuenta los nombres de los archivos, según el tipo de test
y crea un diccionario con el nombre del test y la frecuencia.
Por último, se crea un archivo licencias_test_inventario.csv con el listado de
test y su stock.
"""
# path con la ubicación de los test
path = r"X:\CEPE Compartida\TEST"
# patrones para diferenciar unos test de otros
patron_BADyG = r"^0[0-9]{,5}_"
patron_BADyG_multi = r"^GestorBADyG"
patron_BECOLE = r"LICENCIA DE ACTIVACIÓN NIVEL BECOLE"
patron_BECOLE_renov = r"RENOVACION USOS BECOLE"
patron_DIX = r"dix"
patron_PAIB = r"PAIB"


def tree_printer(root):
    """
    La función tree_printer obtiene un listado de todos los archivos pdf en el
    path de los test
    """
    files_l = []
    dir_l = []
    for root, dirs, files in os.walk(root):
        for d in dirs:
            dir_name = os.path.join(root, d)
            dir_l.append(dir_name)
        for f in files:
            file_name = os.path.join(root, f)
            # filtramos los pdfs y quitamos la extensión
            if file_name[-4:] == ".pdf":
                files_l.append(file_name)
    return dir_l, files_l


def list_file():
    """
    La función list_files toma la lista de los archivos pdf de tree_printer y
    separa el nombre del archivo del path. Según el tipo de test,
    limpia el nombre del archivo y lo adjunta a la lista de test.
    """
    # se llama a tree_printer para obtener el listado de ficheros
    dir_l, files_l = tree_printer(path)
    files_test = []
    for item in files_l:
        # Separamos el nombre por "\" y nos quedamos con el final
        file = item.split("\\")[-1]
        # pasamos por tres filtros para aplicar limpieza adecuada y adjuntar al
        # listado de ficheros de test
        if re.match(patron_BADyG, file):
            file_clean = file.replace("_30", "-30")
            files_test.append(file_clean)
        elif re.match(patron_BADyG_multi, file):
            file_clean = file.replace("yG_Li", "yG-Li")
            files_test.append(file_clean)
        elif re.match(patron_BECOLE, file) or re.match(patron_BECOLE_renov, file):
            file_clean = file.replace("-", "_")
            files_test.append(file_clean)
        elif re.match(patron_DIX, file) or re.match(patron_PAIB, file):
            file_clean_0 = file.replace("-", ".")
            file_clean_1 = file_clean_0.replace("_", "-")
            file_clean = file_clean_1.replace(".", "_")
            files_test.append(file_clean)
    return files_test


# Me gustó la función
"""def arreglar_nombre():
    files = [file.replace("_30", "-30") for file in list_file()]
    return files"""


def tipo_test():
    """
    La función tipo_test cuenta los nombres de los archivos, según el
    tipo de test y crea un diccionario con el nombre del test y la frecuencia.
    """
    # llamamos a la función list_file() para que nos de el listado de ficheros
    # de test
    files = list_file()
    test_d = {}
    for file in files:
        # separamos el nombre con "_" y eliminamos la extensión
        test_split = file[:-4].split("_")
        # Pasamos por filtros según el tipo de test. El tipo de test
        # lleva asociado un patrón diferente en el nombre y nos quedarmos
        # con la primera parte o con la última, según convenga.
        if re.match(patron_BADyG, file):
            test = test_split[-1]
            test_d[test] = test_d.get(test, 0) + 1
        elif re.match(patron_BADyG_multi, file):
            test = test_split[0]
            test_d[test] = test_d.get(test, 0) + 1
        elif re.match(patron_BECOLE, file) or re.match(patron_BECOLE_renov, file):
            test = test_split[0]
            test_d[test] = test_d.get(test, 0) + 1
        elif re.match(patron_DIX, file) or re.match(patron_PAIB, file):
            test = test_split[0]
            test_d[test] = test_d.get(test, 0) + 1
    return test_d


# Creamos el fichero csv con el inventario de licencias
with open('licencias_test_inventario.csv', 'w', newline="") as csvfile:
    fieldnames = ['TEST', 'Inventario']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for key, value in tipo_test().items():
        writer.writerow({'TEST': key, 'Inventario': value})
# mostamos en pantalla el stock de test
for key, value in tipo_test().items():
    print("\n", key, " -> ", value)
# me gustó la función
# files = [f for f in files_l.split("\\")[-1] if re.match(xxx, f)]
