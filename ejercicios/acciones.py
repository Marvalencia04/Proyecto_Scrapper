import csv
import os
from datetime import datetime
from collections import defaultdict

# -----------------------------
# LEER TODOS LOS CSV
# -----------------------------
def leer_datos_csv():
    carpeta = "../Datos"
    datos_totales = []

    for archivo in os.listdir(carpeta):
        if archivo.endswith(".csv"):
            ruta = os.path.join(carpeta, archivo)

            with open(ruta, mode='r', encoding='utf-8', errors='ignore') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    # limpiar caracteres raros
                    if not row.get("Nombre"):
                        continue
                    datos_totales.append(row)

    print(f"✔ Se han cargado {len(datos_totales)} registros de CSV")
    return datos_totales


# -----------------------------
# PARSEAR FECHA ROBUSTO
# -----------------------------
def parsear_fecha(fecha_str):
    formatos = [
        "%Y-%m-%d %H:%M:%S",
        "%d/%m/%y",
        "%d/%m",
        "%d/%m/%Y"
    ]

    for fmt in formatos:
        try:
            return datetime.strptime(fecha_str, fmt)
        except:
            continue

    return None


# -----------------------------
# LIMPIAR PRECIO
# -----------------------------
def parsear_precio(valor):
    try:
        return float(valor.replace(".", "").replace(",", "."))
    except:
        return None


# -----------------------------
# FILTRAR POR RANGO
# -----------------------------
def filtrar_por_rango(datos, fecha_inicio_str, fecha_fin_str):
    fecha_inicio = datetime.strptime(fecha_inicio_str, "%d/%m/%y")
    fecha_fin = datetime.strptime(fecha_fin_str, "%d/%m/%y")

    filtrados = []

    for fila in datos:
        fecha = parsear_fecha(fila.get("Hora/Fecha"))

        if fecha and fecha_inicio <= fecha <= fecha_fin:
            filtrados.append(fila)

    return filtrados


# -----------------------------
# AGRUPAR POR ACCIÓN
# -----------------------------
def agrupar_por_accion(datos_filtrados):
    acciones = defaultdict(list)

    for fila in datos_filtrados:
        nombre = fila.get("Nombre")
        precio = parsear_precio(fila.get("Ultima"))
        fecha = parsear_fecha(fila.get("Hora/Fecha"))

        if nombre and precio and fecha:
            acciones[nombre].append((fecha, precio))

    for acc in acciones:
        acciones[acc].sort(key=lambda x: x[0])

    return acciones


# -----------------------------
# ACCIONES CON INCREMENTO
# -----------------------------
def acciones_con_incremento(datos_filtrados, porcentaje_min):
    acciones = agrupar_por_accion(datos_filtrados)
    resultados = []

    for nombre, registros in acciones.items():
        if len(registros) < 2:
            continue

        valor_inicial = registros[0][1]
        valor_final = registros[-1][1]

        if valor_inicial == 0:
            continue

        variacion = ((valor_final - valor_inicial) / valor_inicial) * 100

        if variacion >= porcentaje_min:
            resultados.append((nombre, round(variacion, 2)))

    return sorted(resultados, key=lambda x: x[1], reverse=True)


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":

    datos = leer_datos_csv()

    fecha_inicio = input("Fecha inicio (dd/mm/yy): ")
    fecha_fin = input("Fecha fin (dd/mm/yy): ")
    porcentaje = float(input("Porcentaje mínimo de incremento: "))

    datos_filtrados = filtrar_por_rango(datos, fecha_inicio, fecha_fin)
    resultados = acciones_con_incremento(datos_filtrados, porcentaje)

    print(f"\n📈 Acciones con incremento >= {porcentaje}%:")
    print(f"📅 Rango: {fecha_inicio} → {fecha_fin}\n")

    for r in resultados:
        print(r)