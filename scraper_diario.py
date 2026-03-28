from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
from datetime import datetime

# --- CONFIG ---
URL = "https://www.expansion.com/mercados/cotizaciones/indices/ibex35_I.IB.html"
WINDOW_SIZE = "1920,1080"

# --- Nombre del fichero diario ---
hoy = datetime.now().strftime("%Y-%m-%d")
CSV_FILE = f"ibex_{hoy}.csv"

# --- Inicializamos CSV con cabecera si no existe ---
try:
    with open(CSV_FILE, "x", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Nombre","Ultima","Max","Min","Hora/Fecha"])
except FileExistsError:
    pass  # Si ya existe, seguimos agregando

# --- Función para scrapear y guardar ---
def scrapear():
    options = webdriver.FirefoxOptions()
    options.add_argument(f"--window-size={WINDOW_SIZE}")
    with webdriver.Firefox(options=options) as driver:
        wait = WebDriverWait(driver, 25)
        driver.get(URL)

        # --- Cookies ---
        try:
            cookie_btn = wait.until(
                EC.element_to_be_clickable((By.ID, "ue-accept-notice-button"))
            )
            cookie_btn.click()
            time.sleep(1)
        except:
            print("No se detectó banner de cookies.")

        # --- Tabla ---
        xpath_filas = "//section[@id='sections']//table/tbody/tr"
        wait.until(EC.presence_of_element_located((By.XPATH, xpath_filas)))
        filas = driver.find_elements(By.XPATH, xpath_filas)

        datos = []

        for stock in filas:
            cells = stock.find_elements(By.CSS_SELECTOR, "th, td")
            raw_values = [c.text.replace('\n',' ').strip() for c in cells]

            # Filtro filas válidas
            if len(raw_values) < 7 or not raw_values[0]:
                continue

            # Extraemos solo lo que nos interesa
            nombre = raw_values[0]
            ultima = raw_values[1].replace('.', '').replace(',', '.')
            maximo = raw_values[5].replace('.', '').replace(',', '.')
            minimo = raw_values[6].replace('.', '').replace(',', '.')
            hora = raw_values[-1]

            datos.append([nombre, ultima, maximo, minimo, hora])

        # Guardamos en CSV
        with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(datos)

        print(f"Guardadas {len(datos)} filas en {CSV_FILE}")

# --- Bucle horario ---
hora_inicio = 9
minuto_inicio = 30
hora_fin = 18
minuto_fin = 30
intervalo_seg = 60*60  # 1 hora

print("Scraper IBEX iniciado. Ctrl+C para detener.")
try:
    while True:
        ahora = datetime.now()
        # Ejecutar solo en horario permitido
        if (ahora.weekday() < 6 and
            (ahora.hour > hora_inicio or (ahora.hour == hora_inicio and ahora.minute >= minuto_inicio)) and
            (ahora.hour < hora_fin or (ahora.hour == hora_fin and ahora.minute <= minuto_fin))):
            
            print(f"\n[{ahora.strftime('%H:%M:%S')}] Ejecutando scraper...")
            scrapear()
        else:
            print(f"[{ahora.strftime('%H:%M:%S')}] Fuera de horario de mercado, esperando...")

        time.sleep(intervalo_seg)

except KeyboardInterrupt:
    print("Scraper detenido manualmente.")