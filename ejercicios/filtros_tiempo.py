from leer_csv import *
from datetime import datetime

datos = leer_datos_csv('./ibex_2025.csv')

def parsear_fecha(fecha_str):
    formatos = [
        "%d/%m/%y %H:%M:%S",  # con hora (nuevo)
        "%d/%m/%y"            # sin hora (viejo)
    ]
    
    for formato in formatos:
        try:
            return datetime.strptime(fecha_str, formato)
        except ValueError:
            pass
    
    raise ValueError(f"Formato de fecha desconocido: {fecha_str}")


# Generar un listado semanal (de la semana actual) donde se indique, para cada acción, su valor inicial, final, mínimo y máximo.
def filtrar_por_semana(numero_semana):
    #datos = leer_csv.leer_datos_csv(nombre_archivo)
    datos_filtrados = []

    for fila in datos:
        fecha_str = fila["Hora/Fecha"]
        fecha = parsear_fecha(fecha_str)

        if fecha.isocalendar()[1] == numero_semana:
            datos_filtrados.append(fila)

    return datos_filtrados

# Generar un listado mensual (del mes actual) donde se indique, para cada acción, su valor inicial, final, mínimo y máximo
def filtrar_por_mes(numero_mes):
    #datos = leer_csv.leer_datos_csv(nombre_archivo)
    datos_filtrados = []

    for fila in datos:
        fecha_str = fila["Hora/Fecha"]
        fecha = parsear_fecha(fecha_str)
        
        if fecha.month == numero_mes:
            datos_filtrados.append(fila)

    return datos_filtrados

# Filtrar por rango de fechas (por ejemplo, del 01/03/2025 al 31/03/2025)
def filtrar_por_rango_fechas(fecha_inicio_str, fecha_fin_str):
    fecha_inicio = parsear_fecha(fecha_inicio_str)
    fecha_fin = parsear_fecha(fecha_fin_str)

    datos_filtrados = []

    for fila in datos:
        fecha_str = fila["Hora/Fecha"]
        fecha = parsear_fecha(fecha_str)

        if fecha_inicio <= fecha <= fecha_fin:
            datos_filtrados.append(fila)

    return datos_filtrados


# ejecutar filtros
semana_31 = filtrar_por_semana(31)
mes_3 = filtrar_por_mes(3)
rango_fechas = filtrar_por_rango_fechas("01/03/25", "31/06/25")