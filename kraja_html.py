from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


driver = webdriver.Firefox()
driver.get("https://store.steampowered.com/search?category1=998")

def skrol(browser: webdriver.Firefox, kolikokrat: int):
    '''Ker se stran, ki jo obdelujem sproti nalaga, ko uporabnik drsi po strani,
    je potrebno za zajem podatkov najprej priti do dna strani, zato obstaja ta funkcija'''
    body = browser.find_element(By.TAG_NAME, "body")
    for i in range(kolikokrat):
        body.send_keys(Keys.PAGE_DOWN)
        print(i)
        time.sleep(0.2)

def skopiraj_html(browser: webdriver.Firefox, kolikokrat: int):
    skrol(browser, kolikokrat)
    body = browser.find_element(By.TAG_NAME, 'body')
    return body.get_attribute('outerHTML')

def shrani_vsebino(browser: webdriver.Firefox, kolikokrat: int, datoteka: str):
    html = skopiraj_html(browser, kolikokrat)
    with open(datoteka, 'w', encoding='UTF-8') as dat:
        dat.write(html)

shrani_vsebino(driver, 2500, 'html.txt')
