#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# URL der Seite
url = 'https://www.amavita.ch/de?np=1&gad_source=1&gclid=CjwKCAjwpbi4BhByEiwAMC8JnZM31yHncdNcnGdphjevwhBEJWNpDUIaSUvsV7iuaP4wdgxoAPsjwBoCnn0QAvD_BwE'

# User-Agent-Header hinzufügen, um die Anfrage wie von einem Browser aussehen zu lassen
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
}

# Anfrage mit Header senden
page = requests.get(url, headers=headers)

# Überprüfen, ob die Seite erfolgreich geladen wurde
if page.status_code == 200:
    soup = BeautifulSoup(page.text, 'html.parser')
    print(soup.prettify())
else:
    print(f"Fehler beim Laden der Seite: Statuscode {page.status_code}")


# Initialisiere den WebDriver
driver = webdriver.Chrome()

try:
    # Öffne die Webseite
    driver.get(
        "https://www.amavita.ch/de?np=1&gad_source=1&gclid=CjwKCAjwvKi4BhABEiwAH2gcw4keRDDb10pvZ6zRYls_uqzfWm86Hwjqm7by03rznUHOg9JohVJ7tBoCxvQQAvD_BwE")

    # Warte, bis das Suchfeld sichtbar ist
    wait = WebDriverWait(driver, 20)
    search_box = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="search"]')))

    # Tippe den Suchbegriff ein
    #search_box.send_keys("Schmerzmittel")
    search_box.send_keys("Schmerzmittel")

    # Warte auf den Suchbutton und klicke darauf
    submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Suche ausführen"]')))
    submit_button.click()

# Füge eine kurze Pause hinzu, um sicherzustellen, dass die Suchergebnisse geladen werden
    time.sleep(10)

    # Warte, bis die Suchergebnisse geladen sind
    search_results = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="SearchResultList"]')))

    # Produktinformationen sammeln (neuer Selektor für Produktkacheln)
    products = driver.find_elements(By.CSS_SELECTOR, 'div[class*="MuiGrid2-root"]')  # Neuer Selektor für Produktkacheln

    # Debug: Anzahl der gefundenen Produkte
    print(f"Gefundene Produkte: {len(products)}")

    # Schleife durch die Produkte
    for index, product in enumerate(products):
        try:
            # Produktname (versuche das Element zu finden)
            product_name = product.find_element(By.CSS_SELECTOR, 'a[class*="MuiTypography-body1"]').text

            # Menge/Details (prüfe, ob das Element vorhanden ist)
            try:
                product_details = product.find_element(By.CSS_SELECTOR, 'div[class*="MuiBox-root css-b24htn"]').text
            except:
                product_details = "Keine Details verfügbar"

            # Preis (prüfe, ob der Preis vorhanden ist)
            try:
                product_price = product.find_element(By.CSS_SELECTOR,
                                                     'span[class*="MuiTypography-root MuiTypography-body1"]').text
            except:
                product_price = "Kein Preis verfügbar"

            # Abholbarkeit (prüfe, ob die Abholbarkeit vorhanden ist)
            try:
                abholung = product.find_element(By.CSS_SELECTOR, 'div[class*="css-pynurg"]').text
            except:
                abholung = "Keine Abholinformationen verfügbar"

            # Drucke die Produktinformationen
            print(f"Produkt {index + 1}:")
            print(f"Produkt: {product_name}")
            print(f"Menge: {product_details}")
            print(f"Preis: {product_price}")
            print(f"Abholen: {abholung}")
            print("-" * 20)

        except Exception as e:
            print(f"Fehler beim Produkt {index + 1}: {e}")

    # Füge eine kurze Pause hinzu, um das Ergebnis zu sehen
    time.sleep(10)

finally:
    # Schließe den WebDriver
    driver.quit()

