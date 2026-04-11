import csv
import glob
from datetime import datetime
from collections import defaultdict
import statistics
# Asumimos que esta función lee un CSV y devuelve una lista de diccionarios
from join_datasets import leer_csv_diccionario 

# ===================================================
# 🛠 SECCIÓN: HERRAMIENTAS (Limpieza, Formato y Lectura)
# ===================================================

def parsear_fecha(fecha_str):
    """
    👉 ENTRADA: String con la fecha del CSV.
    👈 SALIDA: Objeto datetime o None.
    """
    formatos = ["%Y-%m-%d %H:%M:%S", "%d/%m/%y", "%d/%m"]
    for f in formatos:
        try:
            return datetime.strptime(fecha_str, f)
        except:
            pass
    return None

def norm(texto):
    """
    👉 ENTRADA: Texto sucio (con espacios o mayúsculas).
    👈 SALIDA: Texto normalizado (lowercase y sin espacios).
    """
    return texto.strip().lower()

def leer_cotizaciones():
    """
    👉 ENTRADA: Archivos ibex_*.csv en carpeta '../Datos'.
    👈 SALIDA: Lista de diccionarios con Fecha parseada y Nombre normalizado.
    """
    archivos = glob.glob("../Datos/ibex_*.csv")
    datos = []
    for archivo in archivos:
        with open(archivo, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                fecha = parsear_fecha(row["Hora/Fecha"])
                if fecha is None: continue
                row["Fecha"] = fecha
                row["Nombre_norm"] = norm(row["Nombre"])
                datos.append(row)
    print(f"✔ Cotizaciones cargadas: {len(datos)}")
    return datos

def filtrar_ultimo_mes(datos):
    """
    👉 ENTRADA: Lista total de datos.
    👈 SALIDA: Lista filtrada por el mes actual.
    """
    hoy = datetime.now()
    return [d for d in datos if d["Fecha"].month == hoy.month]

# ===================================================
# 🗺 SECCIÓN: MAP & JOIN (Preparación y Cruce)
# ===================================================

def preparar_info_empresas():
    """
    👉 ENTRADA: Archivo '../info_empresas.csv'.
    👈 SALIDA: Diccionario { 'nombre_norm': {datos_empresa} } para búsqueda rápida.
    """
    filas = leer_csv_diccionario("../info_empresas.csv")
    info = {}
    for fila in filas:
        nombre = norm(fila["Nombre"])
        info[nombre] = fila
    print(f"✔ Dataset empresas cargado: {len(info)}")
    return info

def unir_con_empresas(volatilidad_dict, info_empresas):
    """
    👉 ENTRADA: (Diccionario volatilidad, Diccionario info_empresas).
    👈 SALIDA: Lista de tuplas enriquecida: (Nombre Real, Sector, Volatilidad).
    """
    resultado = []
    for accion, vol in volatilidad_dict.items():
        if accion in info_empresas:
            sector = info_empresas[accion]["Sector"]
            nombre_real = info_empresas[accion]["Nombre"]
            resultado.append((nombre_real, sector, round(vol, 4)))
    return resultado

# ===================================================
# 📉 SECCIÓN: REDUCE (Cálculo Estadístico y Top)
# ===================================================

def calcular_volatilidad(datos_mes):
    """
    👉 ENTRADA: Datos filtrados.
    👈 SALIDA: Diccionario { 'accion': desviacion_estandar }.
    """
    precios_por_accion = defaultdict(list)
    for fila in datos_mes:
        nombre = fila["Nombre_norm"]
        precio = float(fila["Ultima"].replace(",", "."))
        precios_por_accion[nombre].append(precio)

    volatilidad = {}
    for accion, precios in precios_por_accion.items():
        if len(precios) > 2:
            volatilidad[accion] = statistics.stdev(precios)
    return volatilidad

def top_estables_por_sector(datos_join):
    """
    👉 ENTRADA: Lista enriquecida post-join.
    👈 SALIDA: Diccionario con la acción de menor volatilidad por sector.
    """
    mejores = {}
    for accion, sector, vol in datos_join:
        if sector not in mejores or vol < mejores[sector][1]:
            mejores[sector] = (accion, vol)
    return mejores

# ===================================================
# 🚀 MAIN
# ===================================================
if __name__ == "__main__":
    # Ingesta
    datos = leer_cotizaciones()
    info_empresas = preparar_info_empresas()

    # Proceso
    datos_mes = filtrar_ultimo_mes(datos)
    volatilidad = calcular_volatilidad(datos_mes) # Reducción 1
    datos_join = unir_con_empresas(volatilidad, info_empresas) # Join

    # Salida
    print("\n🏆 Acción MÁS ESTABLE por sector")
    for sector, (accion, vol) in top_estables_por_sector(datos_join).items():
        print(f"{sector}: {accion} (volatilidad {vol})")

    print("\n📉 TOP 10 acciones más estables IBEX")
    top10 = sorted(datos_join, key=lambda x: x[2])[:10]
    for accion in top10:
        print(accion)