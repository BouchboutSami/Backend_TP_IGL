import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def testGoogleLogin():
    driver = webdriver.Chrome("./chromedriver")
    driver.set_window_size(1920, 1080)
    driver.get("http://localhost:3000/login")
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((By.TAG_NAME,"iframe")))
    btngoogle = driver.find_element(By.CLASS_NAME,"nsm7Bb-HzV7m-LgbsSe-bN97Pc-sM5MNb")
    btngoogle.click()
    time.sleep(3)
    return "Succes"

