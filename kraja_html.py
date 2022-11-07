from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


driver = webdriver.Firefox()
driver.get("https://store.steampowered.com/search/?category1=998&filter=topsellers")

def skrol(browser: webdriver.Firefox, kolikokrat: int):
    body = browser.find_element(By.TAG_NAME, "body")
    for _ in range(kolikokrat):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)

def skopiraj_html(browser: webdriver.Firefox, kolikokrat: int):
    skrol(browser, kolikokrat)
    body = browser.find_element(By.TAG_NAME, 'body')
    return body.get_attribute('outerHTML')

def shrani_vsebino(browser: webdriver.Firefox, kolikokrat: int, datoteka: str):
    html = skopiraj_html(browser, kolikokrat)
    with open(datoteka, 'w', encoding='UTF-8') as dat:
        dat.write(html)

shrani_vsebino(driver, 7900, 'html.txt')
