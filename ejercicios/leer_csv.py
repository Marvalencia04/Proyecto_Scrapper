import csv

__all__ = ['leer_datos_csv']

# Función para leer datos de un archivo CSV y devolverlos como una lista de diccionarios
# exportara para usar en otros módulos
def leer_datos_csv(nombre_archivo):
    datos = []
    with open(nombre_archivo, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            datos.append(row)
    return datos