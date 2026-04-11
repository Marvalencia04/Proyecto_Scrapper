import datetime
from leer_csv import *
from filtros_tiempo import filtrar_por_rango_fechas, filtrar_por_semana, filtrar_por_mes
from operaciones import obtener_maximo, obtener_minimo, obtener_ultimo_valor, calcular_porcentajes

datos = leer_datos_csv('./ibex_2025.csv')

# 3. Dado el nombre de una acci´on y un rango de fechas, obtener su valor m´ınimo y m´aximo de
# cotizaci´on, as´ı como el el porcentaje de decremento y de incremento desde el valor inicial de
# cotizaci´on hasta el m´ınimo y m´aximo, respectivamente.

def ejercicio4(accion):
    hoy = datetime.now()
    semana_actual = hoy.isocalendar()[1]
    mes_actual = hoy.month
    
    datos_filtrados_hoy = filtrar_por_rango_fechas(hoy.strftime("%d/%m/%y"), hoy.strftime("%d/%m/%y"))
    datos_filtrados_semana = filtrar_por_semana(semana_actual)
    datos_filtrados_mes = filtrar_por_mes(mes_actual)
    
    maximo_hoy = obtener_maximo(datos_filtrados_hoy, accion)
    maximo_semana = obtener_maximo(datos_filtrados_semana, accion)
    maximo_mes = obtener_maximo(datos_filtrados_mes, accion)
    minimo_hoy = obtener_minimo(datos_filtrados_hoy, accion)
    minimo_semana = obtener_minimo(datos_filtrados_semana, accion)
    minimo_mes = obtener_minimo(datos_filtrados_mes, accion)


    return {
        "maximo_hoy": maximo_hoy,
        "maximo_semana": maximo_semana,
        "maximo_mes": maximo_mes,
        "minimo_hoy": minimo_hoy,
        "minimo_semana": minimo_semana,
        "minimo_mes": minimo_mes,
    }

# uso, pasar parametros por consola
if __name__ == "__main__":
    accion = input("Ingrese el nombre de la acción: ")
    
    resultado = ejercicio4(accion)
    print(resultado)
    