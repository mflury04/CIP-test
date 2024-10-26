import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

# Pfad für die CSV-Datei
csv_file_path = "../../../../Documents/HSLU/3_Semeter/CIP/painkillers_CIPtest.csv"

# Initialisiere den WebDriver
driver = webdriver.Chrome()

try:
    # Öffne die Webseite
    driver.get("https://www.amavita.ch/de?np=1&gad_source=1&gclid=CjwKCAjwvKi4BhABEiwAH2gcw4keRDDb10pvZ6zRYls_uqzfWm86Hwjqm7by03rznUHOg9JohVJ7tBoCxvQQAvD_BwE")

    # Warte, bis das Suchfeld sichtbar ist
    wait = WebDriverWait(driver, 20)
    search_box = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="search"]')))

    # Tippe den Suchbegriff ein
    search_box.send_keys("Schmerzmittel")

    # Warte auf den Suchbutton und klicke darauf
    submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Suche ausführen"]')))
    submit_button.click()

    # Füge eine kurze Pause hinzu, um sicherzustellen, dass die Suchergebnisse geladen werden
    time.sleep(5)

    # CSV-Datei erstellen und die Spalten definieren
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Schreibe die Kopfzeile in die CSV-Datei
        writer.writerow(["product_name", "price", "type", "dose", "stock", "category", "details_url"])

        # Schleife über alle Seiten
        total_pages = 3  # Wir wissen, dass es 3 Seiten gibt
        for page in range(1, total_pages + 1):
            print(f"Scraping Seite {page}...")

            # Warte, bis die Suchergebnisse geladen sind
            search_results = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="SearchResultList"]')))

            # Produktinformationen sammeln (neuer Selektor für Produktkacheln)
            products = driver.find_elements(By.CSS_SELECTOR, 'div[class*="MuiGrid2-root"]')

            # Debug: Anzahl der gefundenen Produkte
            print(f"Gefundene Produkte auf Seite {page}: {len(products)}")

            # Schleife durch die Produkte
            for index, product in enumerate(products):
                try:
                    # Produktname (versuche das Element zu finden)
                    product_name = product.find_element(By.CSS_SELECTOR, 'div[class*="ProductTileTopContent"]').text

                    # Preis (prüfe, ob der Preis vorhanden ist)
                    try:
                        product_price = product.find_element(By.CSS_SELECTOR, 'div[data-testid="Price"]').text.strip()

                    except:
                        product_price = "Kein Preis verfügbar"

                    # Typ (angenommen, der Typ ist der erste Teil des Produktnamens, z.B. "Algifor")
                    product_type = product_name.split()[0]

                    # Dosis extrahieren (mit regulärem Ausdruck nach der Zahl und "mg" suchen)
                    try:
                        product_dose = re.search(r'\d+\s?mg(?:/\d+\s?ml)?', product_name).group()
                    except:
                        product_dose = "not found"

                    # Stock (Stückzahl oder Volumen aus dem Produktnamen extrahieren)
                    try:
                        # Suche nach Stock-Informationen (z.B. "10 Stk", "200 ml") direkt im Produktnamen
                        product_stock = re.search(r'\d+\s?(Stk|ml|Stück|Flasche)', product_name).group()

                        # Ersetze "Stück" durch "Stk", um Konsistenz zu wahren
                        product_stock = product_stock.replace("Stück", "Stk")

                        # Falls die Dosis Angaben wie "100 mg/5 ml" enthält und der Stock "5 ml" ist, korrigiere es auf das Gesamtvolumen der Flasche
                        if "mg/" in product_dose:
                            # Suche nach dem Gesamtvolumen in ml (z.B. "200 ml" in "200 ml, Flasche, Suspension")
                            total_volume = re.search(r'\d+\s?ml', product_name.split("\n")[-1])  # Nimm nur die Zeile mit dem Gesamtvolumen
                            if total_volume:
                                product_stock = total_volume.group()

                    except:
                        product_stock = "Keine Angabe verfügbar"

                    # Kategorie (manuell auf "Schmerzmittel" gesetzt)
                    product_category = "Painkillers"

                    # Produkt-Details-URL (Hole die URL aus dem 'a'-Tag)
                    try:
                        details_url = product.find_element(By.CSS_SELECTOR, 'a[class*="MuiTypography-body1"]').get_attribute("href")
                    except:
                        details_url = "Keine URL verfügbar"

                    # Schreibe die Produktinformationen in die CSV-Datei
                    writer.writerow([product_name, product_price, product_type, product_dose, product_stock, product_category, details_url])

                except Exception as e:
                    print(f"Fehler beim Produkt {index + 1}: {e}")

            # Nach jedem Durchlauf der Seite 1 oder 2, auf den nächsten Button klicken
            if page < total_pages:
                try:
                    # Klicke auf den Button für die nächste Seite
                    next_page_button = wait.until(EC.element_to_be_clickable((By.XPATH, f'//button[@aria-label="Go to page {page + 1}"]')))
                    next_page_button.click()

                    # Warte, bis die neue Seite geladen ist
                    time.sleep(5)

                except Exception as e:
                    print(f"Fehler beim Seitenwechsel: {e}")

    print(f"Die Daten wurden erfolgreich in {csv_file_path} gespeichert.")

finally:
    # Schließe den WebDriver
    driver.quit()