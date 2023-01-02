from fastapi import FastAPI, Query
import mysql.connector
import os
import database
from dotenv import load_dotenv
from typing import List
from Web_Scraping_TP_IGL.IGL_scraping import *

load_dotenv()
app = FastAPI()

Database = mysql.connector.connect(
    host="localhost",
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD")
)

cursor = Database.cursor()

@app.get("/")
async def root():
    return 200

@app.get("/login") 
async def login(email_user:str,password:str):
    cursor.execute("USE testp")
    commande= "SELECT * FROM users WHERE email='{}'".format(email_user)
    cursor.execute(commande)
    myresult=cursor.fetchone()
    print(myresult[3])
    if(myresult==None):
        return "Wrong email"
    elif (myresult[4] != password):
        return "Wrong password"
    else:
        return "Acces autorisé"
    
@app.get("/scrape")
async def scrape(nb_pages:int,wilayas:List[int] = Query(None)):
    result = ScrapOuedkniss(nb_pages,wilayas)
    return result