import pandas as pd
import glob

# -------- INPUT USUARIO --------
accion = input("Nombre de la acción: ")
fecha_inicio = input("Fecha inicio (YYYY-MM-DD): ")
fecha_fin = input("Fecha fin (YYYY-MM-DD): ")

# -------- CARGAR TODOS LOS CSV --------
archivos = glob.glob("ibex_*.csv")
df = pd.concat([pd.read_csv(f) for f in archivos])

# Convertimos timestamp a fecha real
df["Hora/Fecha"] = pd.to_datetime(df["Hora/Fecha"])

# -------- FILTROS --------
df = df[df["Nombre"] == accion]
df = df[(df["Hora/Fecha"] >= fecha_inicio) & (df["Hora/Fecha"] <= fecha_fin)]

if df.empty:
    print("No hay datos para esa acción en ese rango")
    exit()

# Ordenamos por fecha
df = df.sort_values("Hora/Fecha")

# -------- CALCULOS --------
precio_inicial = df.iloc[0]["Ultima"]
precio_min = df["Ultima"].min()
precio_max = df["Ultima"].max()

decremento = ((precio_min - precio_inicial) / precio_inicial) * 100
incremento = ((precio_max - precio_inicial) / precio_inicial) * 100

# -------- RESULTADOS --------
print("\nRESULTADOS")
print("Precio inicial:", precio_inicial)
print("Precio mínimo:", precio_min)
print("Precio máximo:", precio_max)
print(f"Decremento hasta mínimo: {decremento:.2f}%")
print(f"Incremento hasta máximo: {incremento:.2f}%")