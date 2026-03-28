import csv
import random

# Datos base extraídos de tu lista
empresas = [
    ["Acciona", 213.40, 217.00, 209.60], ["Acciona Ener", 20.40, 21.40, 20.30],
    ["Acerinox", 12.27, 12.48, 12.17], ["ACS", 102.50, 104.80, 100.90],
    ["Aena", 25.63, 25.72, 25.37], ["Amadeus", 48.60, 50.26, 48.30],
    ["ArcelorMittal", 43.52, 44.79, 43.03], ["B. Sabadell", 3.02, 3.08, 3.01],
    ["Bankinter", 13.33, 13.56, 13.24], ["BBVA", 17.91, 18.41, 17.82],
    ["CaixaBank", 10.05, 10.27, 10.02], ["Cellnex Telecom", 26.49, 26.49, 25.98],
    ["Colonial SFL", 4.91, 4.97, 4.88], ["Enagás", 17.14, 17.17, 15.53],
    ["Endesa", 34.90, 35.17, 34.53], ["Ferrovial Se", 54.66, 55.14, 54.28],
    ["Fluidra", 20.04, 20.10, 19.76], ["Grifols", 8.73, 8.83, 8.61],
    ["IAG", 4.11, 4.17, 4.08], ["Iberdrola", 19.13, 19.31, 18.97],
    ["Inditex", 49.50, 50.56, 48.98], ["Indra", 45.00, 47.08, 44.84],
    ["Logista", 31.76, 31.80, 31.28], ["Mapfre", 3.73, 3.76, 3.72],
    ["Merlin Properties", 13.93, 14.25, 13.79], ["Naturgy", 25.64, 25.76, 25.30],
    ["Puig Brands B", 17.10, 17.55, 17.03], ["Redeia", 14.21, 14.61, 14.21],
    ["Repsol", 24.07, 24.43, 23.77], ["ROVI", 78.90, 80.00, 78.35],
    ["Sacyr", 4.17, 4.17, 4.10], ["B. Santander", 9.40, 9.55, 9.32],
    ["Solaria", 22.78, 24.12, 22.57], ["Telefónica", 3.67, 3.70, 3.63],
    ["Unicaja Banco", 2.49, 2.52, 2.47]
]

meses = ["28/01/25", "28/02/25", "28/03/25", "28/04/25", "28/05/25", "28/06/25", 
         "28/07/25", "28/08/25", "28/09/25", "28/10/25", "28/11/25", "28/12/25"]

with open('ibex_2025.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Nombre", "Ultima", "Max", "Min", "Hora/Fecha"])
    
    for emp in empresas:
        nombre, base_ult, base_max, base_min = emp
        for fecha in meses:
            # Añadimos una variación aleatoria de +/- 5% para simular meses distintos
            var = random.uniform(0.95, 1.05)
            ultima = round(base_ult * var, 2)
            max_val = round(base_max * var, 2)
            min_val = round(base_min * var, 2)
            
            writer.writerow([nombre, ultima, max_val, min_val, fecha])

print("Archivo 'ibex_2025.csv' generado con éxito.")