from selenium import webdriver
from selenium.webdriver.common.by import By # IMPORTANTE: faltaba esto
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

start_url = "https://www.expansion.com/mercados/cotizaciones/indices/ibex35_I.IB.html"
options = webdriver.FirefoxOptions()
# FORZAMOS ventana grande para que cargue la estructura de escritorio
options.add_argument("--window-size=1920,1080")

# Usamos Firefox
with webdriver.Firefox(options=options) as driver:
    driver.maximize_window()
    wait = WebDriverWait(driver, 25)
    driver.get(start_url)

    # --- GESTIÓN DE COOKIES (Sin esto, a veces no encuentra la tabla) ---
    try:
        # Esperamos a que el botón de aceptar cookies sea clicable
        cookie_btn = wait.until(EC.element_to_be_clickable((By.ID, "ue-accept-notice-button")))
        cookie_btn.click()
        time.sleep(1) # Pausa breve para que desaparezca el banner
    except:
        print("No se detectó banner de cookies.")

    # --- RECUPERAMOS LISTADO ---
    # Usamos By.XPATH para el método find_elements
    try:
    
        xpath_filas = "//section[@id='sections']//table/tbody/tr"
        print("Buscando datos en..."+xpath_filas)
        
        wait.until(EC.presence_of_element_located((By.XPATH, xpath_filas)))
        commodities = driver.find_elements(By.XPATH, xpath_filas)

        print(f"¡Conseguido! Encontradas {len(commodities)} filas.\n")

        for stock in commodities:
            cells = stock.find_elements(By.CSS_SELECTOR, "th, td")
            
            # 1. Extraemos el texto y limpiamos espacios y saltos de línea
            raw_values = [c.text.replace('\n', ' ').strip() for c in cells]
            
            # 2. FILTRO ANTI-RUIDO: 
            # Si la fila no tiene al menos el nombre y un precio (2 columnas), la ignoramos
            # También comprobamos que el primer elemento no esté vacío
            if len(raw_values) < 2 or not raw_values[0]:
                continue
            
            # 3. Limpieza de datos (tu lógica de puntos y comas)
            clean_values = []
            for i, v in enumerate(raw_values):
                if i == 0:
                    clean_values.append(v)
                else:
                    v_clean = v.replace('.', '').replace(',', '.')
                    clean_values.append(v_clean)
            
            # 4. Imprimimos solo si hay datos reales
            print(",".join(clean_values))

    except Exception as e:
        print(f"Error: No se pudo encontrar la tabla.")
        driver.save_screenshot("error_clase.png")
        print("He guardado 'error_clase.png' para revisión.")

    input("\nPresiona Enter para cerrar el navegador...")