import csv
import os
from datetime import datetime
from collections import defaultdict

# -----------------------------
# LEER CSV
# -----------------------------
def leer_datos_csv(nombre_archivo):
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

# -----------------------------
# PARSEAR FECHA (soporta timestamp y solo fecha)
# -----------------------------
def parsear_fecha(fecha_str):
    for fmt in ("%Y-%m-%d %H:%M:%S", "%d/%m/%y", "%d/%m"):
        try:
            return datetime.strptime(fecha_str, fmt)
        except:
            continue
    raise ValueError(f"Formato de fecha desconocido: {fecha_str}")

# -----------------------------
# FILTRAR POR RANGO DE FECHAS
# -----------------------------
def filtrar_por_rango(datos, fecha_inicio_str, fecha_fin_str):
    fecha_inicio = datetime.strptime(fecha_inicio_str, "%d/%m/%y")
    fecha_fin = datetime.strptime(fecha_fin_str, "%d/%m/%y")
    filtrados = []

    for fila in datos:
        fecha = parsear_fecha(fila["Hora/Fecha"])
        if fecha_inicio <= fecha <= fecha_fin:
            filtrados.append(fila)
    return filtrados

# -----------------------------
# AGRUPAR POR ACCION
# -----------------------------
def agrupar_por_accion(datos_filtrados):
    acciones = defaultdict(list)
    for fila in datos_filtrados:
        nombre = fila["Nombre"]
        valor = float(fila["Ultima"].replace(',', '.'))
        fecha = parsear_fecha(fila["Hora/Fecha"])
        acciones[nombre].append((fecha, valor))
    for accion in acciones:
        acciones[accion].sort(key=lambda x: x[0])
    return acciones

# -----------------------------
# BUSCAR ACCIONES QUE SUBIERON X %
# -----------------------------
def acciones_con_incremento(datos_filtrados, porcentaje_min):
    acciones = agrupar_por_accion(datos_filtrados)
    resultados = []

    for nombre, registros in acciones.items():
        if len(registros) < 2:
            continue
        valor_inicial = registros[0][1]
        valor_final = registros[-1][1]

        variacion = ((valor_final - valor_inicial) / valor_inicial) * 100
        if variacion >= porcentaje_min:
            resultados.append((nombre, round(variacion, 2)))

    resultados.sort(key=lambda x: x[1], reverse=True)
    return resultados

# -----------------------------
# EJEMPLO DE USO
# -----------------------------
if __name__ == "__main__":
    archivo = "../Datos/ibex_2026-03-30.csv"  # Cambia al CSV que quieras
    datos = leer_datos_csv(archivo)

    # Parámetros de usuario
    fecha_inicio = input("Fecha inicio (dd/mm/yy): ")
    fecha_fin = input("Fecha fin (dd/mm/yy): ")
    porcentaje = float(input("Porcentaje mínimo de incremento: "))

    datos_filtrados = filtrar_por_rango(datos, fecha_inicio, fecha_fin)
    resultados = acciones_con_incremento(datos_filtrados, porcentaje)

    print(f"\n📈 Acciones con incremento >= {porcentaje}% entre {fecha_inicio} y {fecha_fin}:")
    for accion in resultados:
        print(accion)