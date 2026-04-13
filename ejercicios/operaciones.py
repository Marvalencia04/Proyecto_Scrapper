# Dado el nombre de una acci´on y un rango de fechas, obtener su valor mínimo y máximo de
# cotizaci´on, as´ı como el el porcentaje de decremento y de incremento desde el valor inicial de
# cotizaci´on hasta el m´ınimo y m´aximo, respectivamente

def obtener_maximo(datos, nombre_accion):
    maximo = None
    for fila in datos:
        if fila["Nombre"] == nombre_accion:
            valor = float(fila["Ultima"])
            if maximo is None or valor > maximo:
                maximo = valor
    return maximo

def obtener_minimo(datos, nombre_accion):
    minimo = None
    for fila in datos:
        if fila["Nombre"] == nombre_accion:
            valor = float(fila["Ultima"])
            if minimo is None or valor < minimo:
                minimo = valor
    return minimo

def obtener_ultimo_valor(datos, nombre_accion):
    ultimo_valor = None
    for fila in datos:
        if fila["Nombre"] == nombre_accion:
            ultimo_valor = float(fila["Ultima"])
    return ultimo_valor

def calcular_porcentajes(datos, nombre_accion):
    minimo = obtener_minimo(datos, nombre_accion)
    maximo = obtener_maximo(datos, nombre_accion)
    ultimo_valor = obtener_ultimo_valor(datos, nombre_accion)

    if ultimo_valor is not None and minimo is not None and maximo is not None:
        porcentaje_decremento = ((ultimo_valor - minimo) / ultimo_valor) * 100
        porcentaje_incremento = ((maximo - ultimo_valor) / ultimo_valor) * 100
        return porcentaje_decremento, porcentaje_incremento
    else:
        return None, None