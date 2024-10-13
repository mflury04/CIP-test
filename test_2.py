#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
#time.sleep(5)
#page = driver.page_source


try:
    # Open the website
    driver.get(
        "https://www.amavita.ch/de?np=1&gad_source=1&gclid=CjwKCAjwvKi4BhABEiwAH2gcw4keRDDb10pvZ6zRYls_uqzfWm86Hwjqm7by03rznUHOg9JohVJ7tBoCxvQQAvD_BwE")

    # Wait for the navigation menu to be clickable
    wait = WebDriverWait(driver, 20)

    # Find the "Medikamente" button and click it
    medikamente_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="NavigationMenuItem"]')))
    medikamente_button.click()

    # Wait for the "Schmerzen und Fieber" category to appear and click it
    schmerzen_fieber_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Schmerzen & Fieber']")))
    schmerzen_fieber_button.click()

    # Wait for the "Schmerzmittel" category to appear and click it
    schmerzmittel_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Schmerzmittel']")))
    schmerzmittel_button.click()

    # Scroll the page to load all products
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(7)  # Warte etwas, bis alle Produkte geladen sind

    # Wait for the product list to be visible
    product_list = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="SearchResultList"]')))

    # Now you can continue scraping the products from the "Schmerzen und Fieber" category
    # Example: Get all product names
    # products = [product.text for product in product_elements]
    # for product in products:
    #     print(product)

finally:
    # Close the browser
    driver.quit()