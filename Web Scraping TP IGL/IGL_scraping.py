from bs4 import BeautifulSoup
from selenium import webdriver
from wilayas import *
import requests

filtre_wilaya = [1,16,24]
url = "https://www.ouedkniss.com/immobilier/1?"
for wilaya in filtre_wilaya:
  filtre= "regionIds={}-{}&".format(data_wilayas[wilaya],wilaya)
  url += filtre
url = url[:-2]

driver = webdriver.Chrome('./chromedriver')
driver.get(url)

html = driver.page_source
doc = BeautifulSoup(html,"html.parser")

# WEB SCRAPING PART

