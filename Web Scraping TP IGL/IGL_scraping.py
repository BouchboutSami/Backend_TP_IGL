from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from wilayas import *
import time

filtre_wilaya = [16]
url = "https://www.ouedkniss.com/immobilier/1?"
for wilaya in filtre_wilaya:
  filtre= "regionIds={}-{}&".format(data_wilayas[wilaya],wilaya)
  url += filtre
url = url[:-1] 
print(url)
driver = webdriver.Chrome("./chromedriver")
driver.set_window_size(1920, 1080)
driver.get(url)
time.sleep(5)
html = driver.page_source
doc = BeautifulSoup(html,"html.parser")
content = doc.find_all("a",{"class":"d-flex flex-column flex-grow-1 v-card v-card--link v-sheet o-announ-card-content theme--dark"})
print(content[0])

