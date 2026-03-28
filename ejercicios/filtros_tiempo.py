from leer_csv import *
from datetime import datetime

datos = leer_datos_csv('./ibex_2025.csv')

# Generar un listado semanal (de la semana actual) donde se indique, para cada acción, su valor inicial, final, mínimo y máximo.
def filtrar_por_semana(numero_semana):
    #datos = leer_csv.leer_datos_csv(nombre_archivo)
    datos_filtrados = []

    for fila in datos:
        fecha_str = fila["Hora/Fecha"]
        fecha = datetime.strptime(fecha_str, "%d/%m/%y")
        
        if fecha.isocalendar()[1] == numero_semana:
            datos_filtrados.append(fila)

    return datos_filtrados

# Generar un listado mensual (del mes actual) donde se indique, para cada acción, su valor inicial, final, mínimo y máximo
def filtrar_por_mes(numero_mes):
    #datos = leer_csv.leer_datos_csv(nombre_archivo)
    datos_filtrados = []

    for fila in datos:
        fecha_str = fila["Hora/Fecha"]
        fecha = datetime.strptime(fecha_str, "%d/%m/%y")
        
        if fecha.month == numero_mes:
            datos_filtrados.append(fila)

    return datos_filtrados

# Filtrar por rango de fechas (por ejemplo, del 01/03/2025 al 31/03/2025)
def filtrar_por_rango_fechas(fecha_inicio_str, fecha_fin_str):
    fecha_inicio = datetime.strptime(fecha_inicio_str, "%d/%m/%y")
    fecha_fin = datetime.strptime(fecha_fin_str, "%d/%m/%y")
    
    datos_filtrados = []

    for fila in datos:
        fecha_str = fila["Hora/Fecha"]
        fecha = datetime.strptime(fecha_str, "%d/%m/%y")
        
        if fecha_inicio <= fecha <= fecha_fin:
            datos_filtrados.append(fila)

    return datos_filtrados


# ejecutar filtros
semana_31 = filtrar_por_semana(31)
mes_3 = filtrar_por_mes(3)
rango_fechas = filtrar_por_rango_fechas("01/03/25", "31/06/25")