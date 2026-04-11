import csv
import os
from datetime import datetime, timedelta
from collections import defaultdict

# ===================================================
# 🛠 SECCIÓN: Herramientas (Utilidades y Lectura)
# ===================================================

def parsear_fecha(fecha_str):
    """
    👉 ENTRADA: String con fecha.
    👈 SALIDA: Objeto datetime.
    """
    formatos = ["%Y-%m-%d %H:%M:%S", "%d/%m/%y %H:%M:%S", "%d/%m/%y", "%d/%m"]
    for formato in formatos:
        try:
            fecha = datetime.strptime(fecha_str, formato)
            if formato == "%d/%m":
                fecha = fecha.replace(year=datetime.now().year)
            return fecha
        except ValueError:
            pass
    raise ValueError(f"Formato desconocido: {fecha_str}")

def leer_todos_los_csv():
    """
    👉 ENTRADA: Carpeta '../Datos'.
    👈 SALIDA: Lista global de diccionarios con datos brutos.
    """
    carpeta = "../Datos"
    datos_totales = []
    if not os.path.exists(carpeta):
        print(f"❌ Error: La carpeta {carpeta} no existe.")
        return []
        
    for archivo in os.listdir(carpeta):
        if archivo.endswith(".csv"):
            ruta = os.path.join(carpeta, archivo)
            with open(ruta, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    datos_totales.append(row)
    return datos_totales

def filtrar_por_semana(datos, numero_semana):
    """
    👉 ENTRADA: Datos brutos y número de semana.
    👈 SALIDA: Lista de registros que coinciden con esa semana.
    """
    return [
        fila for fila in datos
        if parsear_fecha(fila["Hora/Fecha"]).isocalendar()[1] == numero_semana
    ]

def filtrar_por_mes(datos, numero_mes):
    """
    👉 ENTRADA: Datos brutos y número de mes (1-12).
    👈 SALIDA: Lista de registros que coinciden con ese mes.
    """
    return [
        fila for fila in datos
        if parsear_fecha(fila["Hora/Fecha"]).month == numero_mes
    ]

# ===================================================
# 🗺 SECCIÓN: MAP (Agrupación y Ordenación)
# ===================================================

def agrupar_por_accion(datos_filtrados):
    """
    👉 ENTRADA: Lista de diccionarios (del filtro).
    👈 SALIDA: Diccionario { 'Nombre': [(fecha1, precio1), ...] } ordenado por fecha.
    """
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
# 📉 SECCIÓN: REDUCE (Cálculos y Rankings)
# ===================================================

def calcular_variacion_por_accion(datos_filtrados):
    """
    👉 ENTRADA: Datos filtrados por tiempo.
    👈 SALIDA: Lista de tuplas (Nombre, Variación%).
    """
    acciones = agrupar_por_accion(datos_filtrados)
    variaciones = []
    for nombre, registros in acciones.items():
        if len(registros) < 2: continue
        v_ini, v_fin = registros[0][1], registros[-1][1]
        variacion = ((v_fin - v_ini) / v_ini) * 100
        variaciones.append((nombre, round(variacion, 2)))
    return variaciones

def obtener_top(datos_filtrados, n=5, reverse=True):
    """
    👉 ENTRADA: Datos filtrados.
    👈 SALIDA: Top N subidas (reverse=True) o bajadas (reverse=False).
    """
    variaciones = calcular_variacion_por_accion(datos_filtrados)
    variaciones.sort(key=lambda x: x[1], reverse=reverse)
    return variaciones[:n]

# ===================================================
# 🚀 EJECUCIÓN PRINCIPAL
# ===================================================

if __name__ == "__main__":
    datos = leer_todos_los_csv()
    
    # --- LÓGICA DE FECHAS (Semana y Mes Pasado) ---
    hoy = datetime.now()
    
    # 1. SEMANA PASADA: Restamos 7 días
    fecha_semana_pasada = hoy - timedelta(days=7)
    semana_objetivo = fecha_semana_pasada.isocalendar()[1]
    
    # 2. MES PASADO: Restamos los días actuales + 1 para caer en el mes anterior
    # Ejemplo: Si hoy es 5 de Abril, restamos 5 días para llegar al 31 de Marzo.
    primer_dia_mes_actual = hoy.replace(day=1)
    ultimo_dia_mes_pasado = primer_dia_mes_actual - timedelta(days=1)
    mes_objetivo = ultimo_dia_mes_pasado.month

    # --- PROCESAMIENTO ---
    datos_semana = filtrar_por_semana(datos, semana_objetivo)
    datos_mes = filtrar_por_mes(datos, mes_objetivo)

    # --- RESULTADOS SEMANALES ---
    print(f"\n--- 📅 SEMANA PASADA (Semana {semana_objetivo}) ---")
    if not datos_semana:
        print("⚠️ No hay datos.")
    else:
        print("📈 Top Subidas:", obtener_top(datos_semana, reverse=True))
        print("📉 Top Bajadas:", obtener_top(datos_semana, reverse=False))

    # --- RESULTADOS MENSUALES ---
    print(f"\n--- 📅 MES PASADO (Mes {mes_objetivo}) ---")
    if not datos_mes:
        print("⚠️ No hay datos.")
    else:
        print("📈 Top Subidas:", obtener_top(datos_mes, reverse=True))
        print("📉 Top Bajadas:", obtener_top(datos_mes, reverse=False))