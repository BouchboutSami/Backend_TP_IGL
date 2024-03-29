import base64
from bs4 import BeautifulSoup
import requests
import datetime as dt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
f = open("donnees_communes.json")
dz_data = json.loads(f.read())
import time

def ScrapOuedkniss(wilaya):
 nb_pages=1 
 resultat=[]
 for page in range(1,nb_pages+1):
   options = Options()
   options.add_argument('--force-dark-mode')
   url = "https://www.ouedkniss.com/immobilier/{}?".format(str(page))
   filtre= "regionIds={}&".format(wilaya)
   url += filtre 
   url = url[:-1]
   print(url)
   driver = webdriver.Chrome("./chromedriver",options=options)
   driver.set_window_size(1920, 1080)
   driver.get(url)
  #  wait = WebDriverWait(driver, 15)
  #  wait.until(EC.presence_of_element_located((By.TAG_NAME,"Button")))
  #  btnMenu = driver.find_element(By.TAG_NAME,"Button")
  #  btnMenu.click()
  #  time.sleep(1)
  #  Btnsombre = driver.find_element(By.XPATH,"//*[@class='v-input v-input--hide-details theme--light v-input--selection-controls v-input--switch']")
  #  Btnsombre.click()
  #  time.sleep(1)
  #  quitter = driver.find_element(By.XPATH,"//*[@class='mx-2 v-btn v-btn--flat v-btn--icon v-btn--round theme--dark v-size--default']")
  #  quitter.click()
  #  time.sleep(2)
   y = 1000
   for timer in range(0,8):
      driver.execute_script("window.scrollTo(0, "+str(y)+")")
      y += 1000  
      time.sleep(1)     
   html = driver.page_source
   doc = BeautifulSoup(html,"html.parser")
   content = doc.find_all("a",{"class":"d-flex flex-column flex-grow-1 v-card v-card--link v-sheet o-announ-card-content pb-1 theme--dark"})
   if (len(content)==0):
     return "Erreur lors du Web Scraping vérifiez que votre connexion Internet"
   links=[]
   for link in content:
    links.append("https://ouedkniss.com"+link["href"])
   print(len(links))
   for link in range(4):
    driver.get(links[link])
    # wait = WebDriverWait(driver, 15)
    # wait.until(EC.presence_of_element_located((By.TAG_NAME,"Button")))
    # btnMenu = driver.find_element(By.TAG_NAME,"Button")
    # btnMenu.click()
    # time.sleep(1)
    # Btnsombre = driver.find_element(By.XPATH,"//*[@class='v-input--selection-controls__ripple primary--text']")
    # Btnsombre.click()
    # Btnsombre.click()
    # time.sleep(1)
    # quitter = driver.find_element(By.XPATH,"//*[@class='mx-2 v-btn v-btn--flat v-btn--icon v-btn--round theme--dark v-size--default']")
    # quitter.click()
    try:
      superficie=0
      wait = WebDriverWait(driver, 15)
      wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
      time.sleep(3)
      driver.execute_script("window.scrollTo(0, 1000)")
      time.sleep(1)
      html_annonce = driver.page_source
      doc_annonce = BeautifulSoup(html_annonce,"html.parser")
      title = ((doc_annonce.find("h1",{"class":"text-h5 text-lg-h4 font-weight-light text-capitalize"})).text)[1:-1]
      categorie_et_type = doc_annonce.find_all("a",{"class":"pa-0 v-btn v-btn--flat v-btn--router v-btn--text theme--dark v-size--default secondary--text"})
      prix_num = doc_annonce.find("span",{"dir":"ltr"})
      spec_names = doc_annonce.find_all("div",{"class":"spec-name col-sm-3 col-5"})
      for spec in spec_names:
        if spec.text == "Superficie":
          superficie=int(((spec.parent.find("span",{"class":"mr-1 mb-1"})).text)[1:-4])
        if spec.text == " Date " :
          date = ((spec.findNext("div",{"class":"col-sm-9 col-7"})).text)[1:-1]
          date = (date[:-9]).replace("/","-")
          date = dt.datetime.strptime(date, "%d-%m-%Y")
          date = str(date.date().isoformat())
      type_annonce= (categorie_et_type[-2].text)[1:-1] if categorie_et_type[1] is not None else "Undefined"
      categorie_annonce = (categorie_et_type[-1].text)[1:-1] if categorie_et_type[2] is not None else "Undefined"
      description = ((doc_annonce.find("div",{"class":"__description mb-2"})).text)[14:-1]
      image_path = getURL((doc_annonce.find("div",{"class":"v-image__image v-image__image--cover"}))["style"])
      image = base64.b64encode((requests.get(image_path)).content)
      wilaya_commune = (doc_annonce.find("div",{"py-2 text-wrap text-capitalize d-flex flex-wrap flex-gap-2"})).text.split("-")
      wilaya= wilaya_commune[0][1:-1]
      commune = wilaya_commune[1][1:-1]
      num_tel = ((doc_annonce.find("a",{"class":"primary v-btn v-btn--depressed v-btn--rounded theme--dark v-size--default"}))["href"])[4:]
    except:
      print("not found")
      continue
    print("found")
    prix=""
    if (prix_num is not None):
      prix_unite = doc_annonce.find("span",{"dir":"ltr"}).find_next("span")
      prix = prix_num.text + prix_unite.text
      prix = GetPrice(prix)
    else:
      prix = 0
    resultat.append({"categorie":categorie_annonce,"type_annonce":type_annonce,"surface":superficie,"description":description,"prix":prix,"id_contact":None,"wilaya":wilaya,"commune":commune,"image":image,"titre":title,"date_publication":date,"telephone":num_tel})
 return resultat


def communes(wilaya):
  communes = [commune for commune in dz_data if commune["wilaya"].lower() == wilaya.lower()]
  communes = [x["commune"] for x in communes]
  return sorted(communes)

def wilayaString(codeWilaya):
  for x in dz_data:
    if( x["wilaya_code"] == str(codeWilaya)):
      return x["wilaya"]
  return ""

def GetPrice(ancienPrix:str):
  remplacements = {"Millions":"10000","Milliards":"10000000","DA":"1","m²":"1","/":"1"," ":"1","000":"1000"}
  ops = ancienPrix.split(" ")
  if ops[0].isnumeric() and ops[1].isnumeric():
    ops[0]=int(str(ops[0])+str(ops[1]))
    ops[1]=1
  newops=[]
  for op in ops:
    valid=False
    for key in remplacements:
      if op == key:
        valid= True
        newops.append(remplacements[key])
        break
    if valid == False:
      newops.append(op)
  res=1
  mul=1
  for op in newops:
    try:
      mul = float(op)
    except:
      mul =1
      
    res *= mul
  return int(res)

def getURL(styleimage:str):
  elements = styleimage.split('"')
  return elements[1]

def wilayaFromCommune(commune:str):
  for x in dz_data:
    if (x["commune"].lower() == commune.lower()):
      return x["wilaya"]
   





