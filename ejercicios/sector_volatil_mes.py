from collections import defaultdict
from datetime import datetime
from analisis_ibex import parsear_fecha
from join_datasets import leer_csv_diccionario


# ===================================================
# 🛠 SECCIÓN: UTILS (Filtrado y Validación)
# ===================================================

def obtener_meses_validos(datos):
    """
    👉 ENTRADA: Lista de diccionarios (datos_ibex).
    👈 SALIDA: Lista de meses (int) que tienen más de 100 registros.
    """
    conteo_meses = defaultdict(int)
    for fila in datos:
        fecha = parsear_fecha(fila["Hora/Fecha"])
        if fecha:
            conteo_meses[fecha.month] += 1
    
    # Solo permitimos meses con volumen de datos real (> 100 registros)
    return sorted([m for m, conteo in conteo_meses.items() if conteo > 100])

def filtrar_mes(datos, mes_objetivo):
    """
    👉 ENTRADA: Lista de diccionarios y el mes elegido.
    👈 SALIDA: Lista de diccionarios filtrada por ese mes.
    """
    filtrados = []
    for fila in datos:
        fecha = parsear_fecha(fila["Hora/Fecha"])
        if fecha and fecha.month == mes_objetivo:
            filtrados.append(fila)
    return filtrados


# ===================================================
# 📉 SECCIÓN: REDUCE (Análisis de Volatilidad)
# ===================================================

def volatilidad_sector(datos_mes_join):
    """
    👉 ENTRADA: Datos enriquecidos tras el JOIN.
    👈 SALIDA: Ranking de volatilidad media por sector.
    """
    sectores = defaultdict(list)

    # Fase MAP: Diferencia de precios por sector
    for fila in datos_mes_join:
        try:
            maximo = float(fila["Max"])
            minimo = float(fila["Min"])
            sector = fila["Sector"]

            diff = maximo - minimo
            sectores[sector].append(diff)
        except:
            continue

    # Fase REDUCE: Media de volatilidad
    resultado = []
    for sector, valores in sectores.items():
        if len(valores) > 0:
            media = round(sum(valores) / len(valores), 2)
            resultado.append((sector, media))

    resultado.sort(key=lambda x: x[1], reverse=True)

    if not resultado:
        print("⚠️ No hay datos suficientes para calcular la volatilidad en este mes.")
        return

    print("\n⚡ Sectores más volátiles del mes:\n")
    for s, v in resultado:
        print(f"{s:20} {v}")


# ===================================================
# 🚀 SECCIÓN: MAIN (Orquestación)
# ===================================================

if __name__ == "__main__":

    from analisis_ibex import leer_todos_los_csv
    from join_datasets import join_por_nombre

    # 1. Carga inicial (UTILS)
    datos = leer_todos_los_csv()
    info = leer_csv_diccionario("../info_empresas.csv")

    # 2. Identificar meses con datos reales
    meses_reales = obtener_meses_validos(datos)

    if not meses_reales:
        print("❌ No se han encontrado meses con datos suficientes para analizar.")
    else:
        print(f"📆 Meses con datos disponibles: {meses_reales}")
        
        # 3. Entrada de usuario con validación
        try:
            mes_usuario = int(input("👉 Introduce mes (1-12): "))

            if mes_usuario not in meses_reales:
                print(f"⚠️ El mes {mes_usuario} no tiene datos suficientes (>100 registros).")
            else:
                # 4. Procesamiento
                datos_mes = filtrar_mes(datos, mes_usuario)
                datos_join = join_por_nombre(datos_mes, info)
                
                # 5. Resultado final
                volatilidad_sector(datos_join)

        except ValueError:
            print("❌ Error: Por favor, introduce un número válido.")