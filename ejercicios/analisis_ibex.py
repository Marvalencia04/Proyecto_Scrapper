import csv
import os
from datetime import datetime
from collections import defaultdict

# ===================================================
# 0️⃣ PARSEADOR FLEXIBLE DE FECHA (CSV antiguos + nuevos)
# ===================================================

def parsear_fecha(fecha_str):
    formatos = [
        "%Y-%m-%d %H:%M:%S",  # nuevo scraper
        "%d/%m/%y %H:%M:%S",
        "%d/%m/%y",           # csv antiguos con año corto
        "%d/%m"               # csv MUY antiguos sin año
    ]
    
    for formato in formatos:
        try:
            fecha = datetime.strptime(fecha_str, formato)
            
            # 👉 Si el formato no tenía año (27/03), añadimos el año actual
            if formato == "%d/%m":
                fecha = fecha.replace(year=datetime.now().year)
            
            return fecha

        except ValueError:
            pass
    
    raise ValueError(f"Formato de fecha desconocido: {fecha_str}")

# ===================================================
# 1️⃣ LEER TODOS LOS CSV DE /Datos
# ===================================================

def leer_todos_los_csv():
    carpeta = "../Datos"
    datos_totales = []

    for archivo in os.listdir(carpeta):
        if archivo.endswith(".csv"):
            ruta = os.path.join(carpeta, archivo)
            with open(ruta, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    datos_totales.append(row)

    print(f"✔ Se han cargado {len(datos_totales)} registros de CSV")
    return datos_totales

datos = leer_todos_los_csv()

# ===================================================
# 2️⃣ FILTROS DE FECHA
# ===================================================

def filtrar_por_semana(datos, numero_semana):
    return [
        fila for fila in datos
        if parsear_fecha(fila["Hora/Fecha"]).isocalendar()[1] == numero_semana
    ]

def filtrar_por_mes(datos, numero_mes):
    return [
        fila for fila in datos
        if parsear_fecha(fila["Hora/Fecha"]).month == numero_mes
    ]

# ===================================================
# 3️⃣ AGRUPAR POR ACCIÓN
# ===================================================

def agrupar_por_accion(datos_filtrados):
    acciones = defaultdict(list)

    for fila in datos_filtrados:
        nombre = fila["Nombre"]
        valor = float(fila["Ultima"])
        fecha = parsear_fecha(fila["Hora/Fecha"])

        acciones[nombre].append((fecha, valor))

    for accion in acciones:
        acciones[accion].sort(key=lambda x: x[0])

    return acciones

# ===================================================
# 4️⃣ CALCULAR VARIACIÓN %
# ===================================================

def calcular_variacion_por_accion(datos_filtrados):
    acciones = agrupar_por_accion(datos_filtrados)
    variaciones = []

    for nombre, registros in acciones.items():
        if len(registros) < 2:
            continue

        valor_inicial = registros[0][1]
        valor_final = registros[-1][1]
        variacion = ((valor_final - valor_inicial) / valor_inicial) * 100

        variaciones.append((nombre, round(variacion, 2)))

    return variaciones

# ===================================================
# 5️⃣ TOP SUBIDAS / BAJADAS
# ===================================================

def top_subidas(datos_filtrados, n=5):
    variaciones = calcular_variacion_por_accion(datos_filtrados)
    variaciones.sort(key=lambda x: x[1], reverse=True)
    return variaciones[:n]

def top_bajadas(datos_filtrados, n=5):
    variaciones = calcular_variacion_por_accion(datos_filtrados)
    variaciones.sort(key=lambda x: x[1])
    return variaciones[:n]

# ===================================================
# 6️⃣ EJECUCIÓN
# ===================================================

hoy = datetime.now()
semana_actual = hoy.isocalendar()[1]
mes_actual = hoy.month

datos_semana = filtrar_por_semana(datos, semana_actual)
datos_mes = filtrar_por_mes(datos, mes_actual)

print("\n📈 TOP 5 SUBIDAS SEMANA")
for accion in top_subidas(datos_semana):
    print(accion)

print("\n📉 TOP 5 BAJADAS SEMANA")
for accion in top_bajadas(datos_semana):
    print(accion)

print("\n📈 TOP 5 SUBIDAS MES")
for accion in top_subidas(datos_mes):
    print(accion)

print("\n📉 TOP 5 BAJADAS MES")
for accion in top_bajadas(datos_mes):
    print(accion)