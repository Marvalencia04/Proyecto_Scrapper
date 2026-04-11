from join_datasets import leer_csv_diccionario, join_por_nombre
from analisis_ibex import leer_todos_los_csv

# 1. Datos IBEX (ya los tienes)
datos_ibex = leer_todos_los_csv()

# 2. Datos extra (sector, país, etc.)
info_empresas = leer_csv_diccionario("../info_empresas.csv")

# 3. JOIN
datos_join = join_por_nombre(datos_ibex, info_empresas)

print("Total registros con JOIN:", len(datos_join))
print(info_empresas[0])
print("Ejemplo IBEX:", datos_ibex[0]["Nombre"])
print("Ejemplo EXTRA:", info_empresas[0]["Nombre"])
# ejemplo
print("\nEjemplo:")
print(datos_join[0])
