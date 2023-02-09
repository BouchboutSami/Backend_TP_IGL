import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options



driver = webdriver.Chrome("./chromedriver")
driver.set_window_size(1920, 1080)
driver.get("http://localhost:3000/login")
wait = WebDriverWait(driver, 15)
wait.until(EC.presence_of_element_located((By.TAG_NAME,"input")))
inputemail = driver.find_element(By.XPATH,"//*[@id='root']/div/div/div/div/form/label[1]/input")
inputpassword = driver.find_element(By.XPATH,"//*[@id='root']/div/div/div/div/form/label[2]/div/input")
btnlogin = driver.find_element(By.XPATH,"//*[@id='root']/div/div/div/div/form/button")
inputemail.send_keys("ks_aidouni@esi.dz")
inputpassword.send_keys("Wacim2002")
btnlogin.click()
time.sleep(1)
depotannonce = driver.find_element(By.XPATH,"//*[@id='root']/div/div/div/div[1]/nav/div/ul/li[1]/a")
depotannonce.click()
typeAnnonce =  driver.find_element(By.XPATH,"//*[@id='root']/div/div/div/div/form/div[1]/select");
for option in typeAnnonce.find_elements(By.TAG_NAME,"option"):
    if option.text == 'Location':
        option.click() # select() in earlier versions of webdriver
        break
time.sleep(1)
typeBien = driver.find_element(By.XPATH,"//*[@id='root']/div/div/div/div/form/div[2]/select")
for option in typeBien.find_elements(By.TAG_NAME,"option"):
    if option.text == 'Villa':
        option.click() # select() in earlier versions of webdriver
        break
time.sleep(1)
wilaya = driver.find_element(By.XPATH,"//*[@id='root']/div/div/div/div/form/div[3]/select")
for option in wilaya.find_elements(By.TAG_NAME,"option"):
    if option.text == 'Alger':
        option.click() # select() in earlier versions of webdriver
        break
time.sleep(1)
commune = driver.find_element(By.XPATH,"//*[@id='root']/div/div/div/div/form/div[4]/select")
for option in commune.find_elements(By.TAG_NAME,"option"):
    if option.text == 'Rouiba':
        option.click() # select() in earlier versions of webdriver
        break
time.sleep(1)
titre = driver.find_element(By.XPATH,"//*[@id='root']/div/div/div/div/form/div[5]/input")
titre.send_keys("TEST FONCTIONNEL 2")
time.sleep(1)
numTel = driver.find_element(By.XPATH,"//*[@id='root']/div/div/div/div/form/div[6]/input")
numTel.send_keys("0770825414")
time.sleep(1)
superficie = driver.find_element(By.XPATH,"//*[@id='root']/div/div/div/div/form/div[7]/input")
superficie.send_keys("250")
time.sleep(1)
prix = driver.find_element(By.XPATH,"//*[@id='root']/div/div/div/div/form/div[8]/input")
prix.send_keys("400000")
time.sleep(1)
image = driver.find_element(By.XPATH,"//*[@id='root']/div/div/div/div/form/div[9]/input")
image.send_keys(os.getcwd() + "/tests/maison.jpg")
time.sleep(1)
description = driver.find_element(By.XPATH,"//*[@id='root']/div/div/div/div/form/div[10]/textarea")
description.send_keys("Description du test fonctionnel 2")
time.sleep(1)
btnSubmit = driver.find_element(By.XPATH,"//*[@id='root']/div/div/div/div/form/button")
btnSubmit.click()
driver.execute_script("window.scrollTo(0, 2000)")
time.sleep(4)


