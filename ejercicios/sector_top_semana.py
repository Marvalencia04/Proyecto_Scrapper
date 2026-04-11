from analisis_ibex import *
from join_datasets import *
from datetime import datetime
from collections import defaultdict

# ===================================================
# 🛠 SECCIÓN: HERRAMIENTAS (Carga y Validación)
# ===================================================

# 👉 ENTRADA: Archivos CSV brutos
# 👈 SALIDA: Listas de diccionarios
datos_ibex = leer_todos_los_csv()
datos_extra = leer_csv_diccionario("../info_empresas.csv")

def obtener_semanas_validas(datos_ibex):
    """
    👉 ENTRADA: Lista de diccionarios del IBEX.
    👈 SALIDA: Lista de semanas que tienen datos suficientes para ser analizadas (>100 registros).
    """
    conteo_semanas = defaultdict(int)
    for fila in datos_ibex:
        fecha = parsear_fecha(fila["Hora/Fecha"])
        if fecha:
            semana = fecha.isocalendar()[1]
            conteo_semanas[semana] += 1
    
    # Solo devolvemos semanas con datos suficientes (evita las que solo tienen 35 registros)
    return sorted([s for s, conteo in conteo_semanas.items() if conteo > 100])

# ===================================================
# 🗺 SECCIÓN: MAP (Cruce de Datos)
# ===================================================

def realizar_join_sectores(var_dict, datos_extra):
    """
    👉 ENTRADA: Variaciones y datos de sectores.
    👈 SALIDA: Variaciones agrupadas por Sector.
    """
    sectores = defaultdict(list)
    for nombre, variacion in var_dict.items():
        for empresa in datos_extra:
            if empresa["Nombre"] == nombre:
                sector = empresa["Sector"]
                sectores[sector].append(variacion)
    return sectores

# ===================================================
# 📉 SECCIÓN: REDUCE (Cálculo Final)
# ===================================================

def calcular_medias_sectoriales(sectores_agrupados):
    """
    👉 ENTRADA: Diccionario por sectores.
    👈 SALIDA: Ranking de medias por sector.
    """
    media_sector = []
    for sector, valores in sectores_agrupados.items():
        media = round(sum(valores) / len(valores), 2)
        media_sector.append((sector, media))
    
    media_sector.sort(key=lambda x: x[1], reverse=True)
    return media_sector

# ===================================================
# 🚀 EJECUCIÓN PRINCIPAL
# ===================================================

if __name__ == "__main__":
    print("📊 Analizador IBEX Profesional\n")

    # 1. Identificar solo semanas con datos útiles
    semanas_reales = obtener_semanas_validas(datos_ibex)

    if not semanas_reales:
        print("❌ No se han encontrado semanas con datos suficientes para analizar.")
    else:
        print("📆 Semanas con datos completos disponibles:")
        print("------------------------------------------")
        for s in semanas_reales:
            print(f"Semana {s}")

        # 2. Selección de semana
        try:
            semana_usuario = int(input("\n👉 Selecciona una semana válida: "))

            if semana_usuario not in semanas_reales:
                print(f"⚠️ La semana {semana_usuario} no tiene datos suficientes. Elige una de la lista.")
            else:
                # 3. Proceso MapReduce
                datos_semana = filtrar_por_semana(datos_ibex, semana_usuario)
                variaciones = calcular_variacion_por_accion(datos_semana)
                var_dict = {nombre: var for nombre, var in variaciones}

                sectores_agrupados = realizar_join_sectores(var_dict, datos_extra)
                resultados = calcular_medias_sectoriales(sectores_agrupados)

                # 4. Mostrar resultados
                print(f"\n🏆 Resultados Sectoriales Semana {semana_usuario}:\n")
                for sector, media in resultados:
                    print(f"{sector:20} {media}%")

        except ValueError:
            print("❌ Error: Introduce un número entero.")