from analisis_ibex import *
from join_datasets import *
from datetime import datetime
from collections import defaultdict

print("📊 Analizador IBEX por sectores y semanas\n")

# ---------------------------------------------------
# 1️⃣ Cargar datos
# ---------------------------------------------------
datos_ibex = leer_todos_los_csv()
datos_extra = leer_csv_diccionario("../info_empresas.csv")

# ---------------------------------------------------
# 2️⃣ Mostrar semanas disponibles
# ---------------------------------------------------
semanas_disponibles = sorted({
    parsear_fecha(fila["Hora/Fecha"]).isocalendar()[1]
    for fila in datos_ibex
    if parsear_fecha(fila["Hora/Fecha"])
})

print("📆 Semanas disponibles en los datos:")
print("-----------------------------------")
for s in semanas_disponibles:
    print("Semana", s)

# ---------------------------------------------------
# 3️⃣ Elegir semana por consola
# ---------------------------------------------------
semana_usuario = int(input("\n👉 Escribe la semana a analizar: "))

# ---------------------------------------------------
# 4️⃣ Filtrar datos de esa semana
# ---------------------------------------------------
datos_semana = filtrar_por_semana(datos_ibex, semana_usuario)
print(f"\n📅 Registros encontrados semana {semana_usuario}: {len(datos_semana)}")

# ---------------------------------------------------
# 5️⃣ Calcular variación semanal por acción
# ---------------------------------------------------
variaciones = calcular_variacion_por_accion(datos_semana)

# convertir lista -> diccionario
var_dict = {nombre: var for nombre, var in variaciones}

# ---------------------------------------------------
# 6️⃣ JOIN CORRECTO (variaciones + info empresas)
# ---------------------------------------------------
sectores = defaultdict(list)

for nombre, variacion in var_dict.items():
    for empresa in datos_extra:
        if empresa["Nombre"] == nombre:
            sector = empresa["Sector"]
            sectores[sector].append(variacion)

# ---------------------------------------------------
# 7️⃣ Media por sector
# ---------------------------------------------------
media_sector = []
for sector, valores in sectores.items():
    media = round(sum(valores) / len(valores), 2)
    media_sector.append((sector, media))

media_sector.sort(key=lambda x: x[1], reverse=True)

# ---------------------------------------------------
# 8️⃣ Mostrar resultados
# ---------------------------------------------------
print("\n🏆 Sectores que más suben esa semana:\n")
for sector, media in media_sector:
    print(f"{sector:20} {media}%")