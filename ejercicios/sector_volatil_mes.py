from collections import defaultdict
from datetime import datetime
from analisis_ibex import parsear_fecha
from join_datasets import leer_csv_diccionario


# ---------------------------------------------------
# 1️⃣ FILTRAR MES
# ---------------------------------------------------
def filtrar_mes(datos, mes_objetivo):
    filtrados = []

    for fila in datos:
        fecha = parsear_fecha(fila["Hora/Fecha"])
        if fecha and fecha.month == mes_objetivo:
            filtrados.append(fila)

    return filtrados


# ---------------------------------------------------
# 2️⃣ VOLATILIDAD POR SECTOR
# ---------------------------------------------------
def volatilidad_sector(datos_mes_join):
    sectores = defaultdict(list)

    for fila in datos_mes_join:
        try:
            maximo = float(fila["Max"])
            minimo = float(fila["Min"])
            sector = fila["Sector"]

            diff = maximo - minimo
            sectores[sector].append(diff)

        except:
            continue

    resultado = []
    for sector, valores in sectores.items():
        if len(valores) > 0:
            media = round(sum(valores) / len(valores), 2)
            resultado.append((sector, media))

    resultado.sort(key=lambda x: x[1], reverse=True)

    print("\n⚡ Sectores más volátiles del mes:\n")
    for s, v in resultado:
        print(f"{s:20} {v}")


# ---------------------------------------------------
# 3️⃣ MAIN
# ---------------------------------------------------
if __name__ == "__main__":

    from analisis_ibex import leer_todos_los_csv
    from join_datasets import join_por_nombre

    datos = leer_todos_los_csv()
    info = leer_csv_diccionario("../info_empresas.csv")

    mes = int(input("👉 Introduce mes (1-12): "))

    datos_mes = filtrar_mes(datos, mes)

    datos_join = join_por_nombre(datos_mes, info)

    volatilidad_sector(datos_join)