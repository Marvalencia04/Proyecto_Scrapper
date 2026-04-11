from leer_csv import *
from filtros_tiempo import filtrar_por_rango_fechas
from operaciones import obtener_maximo, obtener_minimo, obtener_ultimo_valor, calcular_porcentajes

datos = leer_datos_csv('./ibex_2025.csv')

# 3. Dado el nombre de una acci´on y un rango de fechas, obtener su valor m´ınimo y m´aximo de
# cotizaci´on, as´ı como el el porcentaje de decremento y de incremento desde el valor inicial de
# cotizaci´on hasta el m´ınimo y m´aximo, respectivamente.

def ejercicio3(accion, rango_fechas):
    datos_filtrados = filtrar_por_rango_fechas(rango_fechas[0], rango_fechas[1])
    
    maximo = obtener_maximo(datos_filtrados, accion)
    minimo = obtener_minimo(datos_filtrados, accion)
    ultimo_valor = obtener_ultimo_valor(datos_filtrados, accion)
    porcentaje_decremento, porcentaje_incremento = calcular_porcentajes(datos_filtrados, accion)

    return {
        "maximo": maximo,
        "minimo": minimo,
        "ultimo_valor": ultimo_valor,
        "porcentaje_decremento": porcentaje_decremento,
        "porcentaje_incremento": porcentaje_incremento
    }

# uso, pasar parametros por consola
if __name__ == "__main__":
    accion = input("Ingrese el nombre de la acción: ")
    fecha_inicio = input("Ingrese la fecha de inicio (dd/mm/yy): ")
    fecha_fin = input("Ingrese la fecha de fin (dd/mm/yy): ")
    
    resultado = ejercicio3(accion, (fecha_inicio, fecha_fin))
    print(resultado)
    