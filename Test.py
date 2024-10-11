#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# URL der Amavita-Website
url = "https://www.amavita.ch/de?srsltid=AfmBOoqy7INqIdgsbs250nSeWEnMKIxJGgFOhcPFGRX_O18htqmBWpgk"
#
# request approach
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
print(soup.prettify())

# Initialisiere den Webdriver und öffnet die Webseite
driver = webdriver.Chrome()
driver.get(url)  # Die URL deiner Webseite

def click_pharmacy_search():
    try:
        # Öffne die Seite
        driver.get(url)

        # Warte, bis der Button "Apotheke finden" sichtbar ist
        wait = WebDriverWait(driver, 10)
        pharmacy_button = wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Apotheke finden"))
        )

        # Klicke auf den Button
        pharmacy_button.click()

        # Optional: Warte, bis die nächste Seite geladen ist oder prüfe, ob das gewünschte Element der neuen Seite vorhanden ist
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='PLZ oder Ort']"))
        )

        print("Apotheke finden wurde erfolgreich angeklickt und die Seite ist geladen.")

    except Exception as e:
        print(f"Fehler beim Anklicken des Apotheke finden Buttons: {e}")
    finally:
        # WebDriver schließen
        driver.quit()


# Funktion aufrufen
click_pharmacy_search()