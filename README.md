# contar_ficheros_test
Contar ficheros de licencias de test
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
