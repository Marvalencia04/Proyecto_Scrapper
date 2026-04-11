import csv

# ---------------------------------------------------
# LECTURA ROBUSTA CSV
# ---------------------------------------------------
def leer_csv_diccionario(path):
    with open(path, "r", encoding="utf-8-sig", errors="ignore") as f:
        reader = csv.DictReader(f, delimiter=',')

        datos = []
        for row in reader:
            limpio = {k.strip(): v.strip() for k, v in row.items() if k}
            datos.append(limpio)

        return datos


# ---------------------------------------------------
# JOIN POR NOMBRE (ROBUSTO)
# ---------------------------------------------------
def join_por_nombre(datos_ibex, datos_extra):
    extra_dict = {}

    for fila in datos_extra:
        nombre = fila.get("Nombre")  # evita KeyError
        if nombre:
            extra_dict[nombre] = fila

    resultado = []

    for fila in datos_ibex:
        nombre = fila.get("Nombre")  # también más seguro aquí

        if nombre in extra_dict:
            combinado = {**fila, **extra_dict[nombre]}
            resultado.append(combinado)

    return resultado