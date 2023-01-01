from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utils import *
import time

def ScrapOuedkniss(nb_pages:int,wilayas:list[int]):
 resultat=[]
 filtre_wilaya = wilayas
 for page in range(1,nb_pages+1):
   url = "https://www.ouedkniss.com/immobilier/{}?".format(str(page))
   for wilaya in filtre_wilaya:
    filtre= "regionIds={}-{}&".format(wilayaString(wilaya),wilaya)
    url += filtre
   url = url[:-1]
   print(url)
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
   for link in links:
    driver.get(link)
    try:
      wait = WebDriverWait(driver, 15)
      wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
      time.sleep(3)
      driver.execute_script("window.scrollTo(0, 1000)")
      time.sleep(1)
      html_annonce = driver.page_source
      doc_annonce = BeautifulSoup(html_annonce,"html.parser")
      title = (doc_annonce.find("h1",{"class":"text-h5 text-lg-h4 font-weight-light text-capitalize"})).text
      categorie_et_type = doc_annonce.find_all("a",{"class":"pa-0 v-btn v-btn--flat v-btn--router v-btn--text theme--dark v-size--default secondary--text"})
      prix_num = doc_annonce.find("span",{"dir":"ltr"})
      spec_names = doc_annonce.find_all("div",{"class":"spec-name col-sm-3 col-5"})
      for spec in spec_names:
        if spec.text == "Superficie":
          superficie=(spec.parent.find("span",{"class":"mr-1 mb-1"})).text
        if spec.text == " Date " :
          date = (spec.findNext("div",{"class":"col-sm-9 col-7"})).text
      type_annonce=categorie_et_type[-2].text if categorie_et_type[1] is not None else "Undefined"
      categorie_annonce = categorie_et_type[-1].text if categorie_et_type[2] is not None else "Undefined"
      description = ((doc_annonce.find("div",{"class":"__description mb-2"})).text)[12:]
      image_path = getURL((doc_annonce.find("div",{"class":"v-image__image v-image__image--cover"}))["style"])
    except:
      print("not found")
      continue
    prix=""
    if (prix_num is not None):
      prix_unite = doc_annonce.find("span",{"dir":"ltr"}).find_next("span")
      prix = prix_num.text + prix_unite.text
      prix = GetPrice(prix)
    else:
      prix = 0
    print(prix,categorie_annonce)
    
ScrapOuedkniss(1,[16])
  
   





