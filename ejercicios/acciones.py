import csv
import os
from datetime import datetime
from collections import defaultdict

# ===================================================
# 🛠 SECCIÓN: HERRAMIENTAS (Utilidades y Limpieza)
# ===================================================

def leer_datos_csv():
    """
    👉 ENTRADA: Archivos .csv en la carpeta '../Datos'.
    👈 SALIDA: Lista de diccionarios con los datos crudos.
    """
    carpeta = "../Datos"
    datos_totales = []

    for archivo in os.listdir(carpeta):
        if archivo.endswith(".csv"):
            ruta = os.path.join(carpeta, archivo)
            with open(ruta, mode='r', encoding='utf-8', errors='ignore') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if not row.get("Nombre"):
                        continue
                    datos_totales.append(row)

    print(f"✔ Se han cargado {len(datos_totales)} registros de CSV")
    return datos_totales

def parsear_fecha(fecha_str):
    """
    👉 ENTRADA: Un String de fecha en diversos formatos.
    👈 SALIDA: Un objeto datetime o None si falla.
    """
    formatos = ["%Y-%m-%d %H:%M:%S", "%d/%m/%y", "%d/%m", "%d/%m/%Y"]
    for fmt in formatos:
        try:
            return datetime.strptime(fecha_str, fmt)
        except:
            continue
    return None

def parsear_precio(valor):
    """
    👉 ENTRADA: String de precio (ej: "1.234,50").
    👈 SALIDA: Float limpio (ej: 1234.50) o None.
    """
    try:
        # Quitamos punto de miles y cambiamos coma decimal por punto
        return float(valor.replace(".", "").replace(",", "."))
    except:
        return None

def filtrar_por_rango(datos, fecha_inicio_str, fecha_fin_str):
    """
    👉 ENTRADA: (Lista datos, String fecha inicio, String fecha fin).
    👈 SALIDA: Lista de diccionarios dentro del rango temporal.
    """
    fecha_inicio = datetime.strptime(fecha_inicio_str, "%d/%m/%y")
    fecha_fin = datetime.strptime(fecha_fin_str, "%d/%m/%y")
    filtrados = []

    for fila in datos:
        fecha = parsear_fecha(fila.get("Hora/Fecha"))
        if fecha and fecha_inicio <= fecha <= fecha_fin:
            filtrados.append(fila)
    return filtrados

# ===================================================
# 🗺 SECCIÓN: MAP (Agrupación y Ordenación)
# ===================================================

def agrupar_por_accion(datos_filtrados):
    """
    👉 ENTRADA: Lista de diccionarios filtrados.
    👈 SALIDA: Diccionario { 'Nombre': [(fecha, precio), ...] } ordenado cronológicamente.
    """
    acciones = defaultdict(list)

    for fila in datos_filtrados:
        nombre = fila.get("Nombre")
        precio = parsear_precio(fila.get("Ultima"))
        fecha = parsear_fecha(fila.get("Hora/Fecha"))

        if nombre and precio and fecha:
            acciones[nombre].append((fecha, precio))

    # Ordenar cada lista de precios por su fecha (Fase Shuffle/Sort)
    for acc in acciones:
        acciones[acc].sort(key=lambda x: x[0])

    return acciones

# ===================================================
# 📉 SECCIÓN: REDUCE (Cálculo de Resultados)
# ===================================================

def acciones_con_incremento(datos_filtrados, porcentaje_min):
    """
    👉 ENTRADA: (Lista de datos, Float con el umbral mínimo).
    👈 SALIDA: Lista de tuplas (Nombre, Variación) que superan el umbral.
    """
    # 1. Llamamos al MAP para organizar los datos
    acciones = agrupar_por_accion(datos_filtrados)
    resultados = []

    # 2. Reducimos la lista de precios a una sola variación porcentual
    for nombre, registros in acciones.items():
        if len(registros) < 2:
            continue

        valor_inicial = registros[0][1]
        valor_final = registros[-1][1]

        if valor_inicial == 0:
            continue

        variacion = ((valor_final - valor_inicial) / valor_inicial) * 100

        # 3. Filtramos por el criterio de negocio (porcentaje mínimo)
        if variacion >= porcentaje_min:
            resultados.append((nombre, round(variacion, 2)))

    # Devolvemos ordenado por mayor incremento
    return sorted(resultados, key=lambda x: x[1], reverse=True)

# ===================================================
# 🚀 MAIN (Interfaz de Usuario)
# ===================================================

if __name__ == "__main__":
    datos = leer_datos_csv()

    print("\n--- 🔍 Buscador de Incrementos ---")
    f_inicio = input("Fecha inicio (dd/mm/yy): ")
    f_fin = input("Fecha fin (dd/mm/yy): ")
    pct_min = float(input("Porcentaje mínimo de incremento: "))

    # Proceso de filtrado y análisis
    datos_filtrados = filtrar_por_rango(datos, f_inicio, f_fin)
    resultados = acciones_con_incremento(datos_filtrados, pct_min)

    print(f"\n📈 Acciones con incremento >= {pct_min}%:")
    print(f"📅 Rango analizado: {f_inicio} → {f_fin}\n")

    if not resultados:
        print("❌ No se encontraron acciones con ese incremento en esas fechas.")
    else:
        for r in resultados:
            print(f"🔹 {r[0]}: {r[1]}%")