import csv
import glob
from datetime import datetime
from collections import defaultdict
import statistics
from join_datasets import leer_csv_diccionario

# ---------------------------------------------------
# PARSEAR FECHA (independiente del resto del proyecto)
# ---------------------------------------------------
def parsear_fecha(fecha_str):
    formatos = ["%Y-%m-%d %H:%M:%S", "%d/%m/%y", "%d/%m"]
    for f in formatos:
        try:
            return datetime.strptime(fecha_str, f)
        except:
            pass
    return None


# ---------------------------------------------------
# NORMALIZAR TEXTO (clave para que el JOIN funcione)
# ---------------------------------------------------
def norm(texto):
    return texto.strip().lower()


# ---------------------------------------------------
# Leer TODOS los CSV de cotizaciones
# ---------------------------------------------------
def leer_cotizaciones():
    archivos = glob.glob("../Datos/ibex_*.csv")
    datos = []

    for archivo in archivos:
        with open(archivo, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                fecha = parsear_fecha(row["Hora/Fecha"])
                if fecha is None:
                    continue

                row["Fecha"] = fecha
                row["Nombre_norm"] = norm(row["Nombre"])
                datos.append(row)

    print(f"✔ Cotizaciones cargadas: {len(datos)}")
    return datos


# ---------------------------------------------------
# Filtrar último mes
# ---------------------------------------------------
def filtrar_ultimo_mes(datos):
    hoy = datetime.now()
    return [d for d in datos if d["Fecha"].month == hoy.month]


# ---------------------------------------------------
# Calcular volatilidad por acción
# ---------------------------------------------------
def calcular_volatilidad(datos_mes):
    precios_por_accion = defaultdict(list)

    for fila in datos_mes:
        nombre = fila["Nombre_norm"]

        # soporte coma decimal
        precio = float(fila["Ultima"].replace(",", "."))
        precios_por_accion[nombre].append(precio)

    volatilidad = {}
    for accion, precios in precios_por_accion.items():
        if len(precios) > 2:
            volatilidad[accion] = statistics.stdev(precios)

    return volatilidad


# ---------------------------------------------------
# JOIN con dataset empresas
# ---------------------------------------------------
def preparar_info_empresas():
    filas = leer_csv_diccionario("../info_empresas.csv")

    info = {}
    for fila in filas:
        nombre = norm(fila["Nombre"])
        info[nombre] = fila

    print(f"✔ Dataset empresas cargado: {len(info)}")
    return info


def unir_con_empresas(volatilidad, info_empresas):
    resultado = []

    for accion, vol in volatilidad.items():
        if accion in info_empresas:
            sector = info_empresas[accion]["Sector"]
            nombre_real = info_empresas[accion]["Nombre"]
            resultado.append((nombre_real, sector, round(vol, 4)))

    return resultado


# ---------------------------------------------------
# TOP estabilidad por sector
# ---------------------------------------------------
def top_estables_por_sector(datos_join):
    mejores = {}

    for accion, sector, vol in datos_join:
        if sector not in mejores or vol < mejores[sector][1]:
            mejores[sector] = (accion, vol)

    return mejores


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------
if __name__ == "__main__":

    datos = leer_cotizaciones()
    info_empresas = preparar_info_empresas()

    datos_mes = filtrar_ultimo_mes(datos)
    volatilidad = calcular_volatilidad(datos_mes)
    datos_join = unir_con_empresas(volatilidad, info_empresas)

    print("\n🏆 Acción MÁS ESTABLE por sector")
    for sector, (accion, vol) in top_estables_por_sector(datos_join).items():
        print(f"{sector}: {accion} (volatilidad {vol})")

    print("\n📉 TOP 10 acciones más estables IBEX")
    top10 = sorted(datos_join, key=lambda x: x[2])[:10]
    for accion in top10:
        print(accion)