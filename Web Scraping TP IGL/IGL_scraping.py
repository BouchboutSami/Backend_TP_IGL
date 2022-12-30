from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from communes import *
import time
filtre_wilaya = [25,16]
page=1
url = "https://www.ouedkniss.com/immobilier/{}?".format(str(page))
for wilaya in filtre_wilaya:
  filtre= "regionIds={}-{}&".format(wilayaString(wilaya),wilaya)
  url += filtre
url = url[:-1] 
driver = webdriver.Chrome("./chromedriver")
driver.set_window_size(1920, 1080)
driver.get(url)
y = 1000
for timer in range(0,8):
         driver.execute_script("window.scrollTo(0, "+str(y)+")")
         y += 1000  
         time.sleep(1)
         
html = driver.page_source
doc = BeautifulSoup(html,"html.parser")
content = doc.find_all("a",{"class":"d-flex flex-column flex-grow-1 v-card v-card--link v-sheet o-announ-card-content theme--dark"})
links=[]
for link in content:
  links.append("https://ouedkniss.com"+link["href"])
  
  
# Titre : H1 -- text-h5 text-lg-h4 font-weight-light text-capitalize
# Prix : DIV -- mt-1 line-height-2 primary--text text-h6 ( playing with child spans)
# Superficie : DIV -- spec-name col-sm-3 col-5 than span class mr-1 mb-1

print(len(links))
for link in links:
  driver.get(link)
  try:
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_all_elements_located((By.TAG_NAME,"h1")))
  except:
    print("not found")
    continue
  driver.execute_script("window.scrollTo(0, 1000)")
  html_annonce = driver.page_source
  doc_annonce = BeautifulSoup(html_annonce,"html.parser")
  title = doc_annonce.find("h1",{"class":"text-h5 text-lg-h4 font-weight-light text-capitalize"})
  if (title is not None):
    print(title.text)



    

 
# id (automatique)
# CATEGORIE / TYPE : classe :pa-0 v-btn v-btn--flat v-btn--router v-btn--text theme--dark v-size--default secondary--text 
# le premier est la categorie le deuxieme est le type
# SUPERFICIE : class : spec-name col-sm-3 col-5 puis si le texte est superficie on cherche la classe mr-1 mb-1
# DESCRIPTION : class : __description mb-2 --collapsed puis class align-left
# PRIX : span avec dir="ltr"
# PATH PIC : div avec class v-image__image v-image__image--cover

  





