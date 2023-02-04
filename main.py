from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
import os
from pydantic import BaseModel
import database
from dotenv import load_dotenv
from typing import List
from Web_Scraping_TP_IGL.IGL_scraping import *

load_dotenv()
app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3001",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class number(BaseModel):
    val: int

class annonce(BaseModel):
    categorie:str
    type_annonce : str
    surface : int
    description : str
    prix : int
    id_contact : int
    wilaya :str
    commune :str
    image :str
    titre : str
    date_publication:str
    telephone:int
    
class user(BaseModel):
    username:str
    email:str
    password:str

Database = mysql.connector.connect(
    host="localhost",
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD"),
    database="testp"
)

cursor = Database.cursor()

def create_annonce(annonce):
        database.insert_row(cursor,'testp','annonces',{'categorie':annonce.categorie,'type_annonce':annonce.type_annonce ,'surface':annonce.surface,'description':annonce.description,'prix':annonce.prix,'id_contact':annonce.id_contact,'wilaya':annonce.wilaya ,'commune':annonce.commune,'telephone':annonce.telephone,'image':annonce.image ,'titre':annonce.titre,'date_publication':annonce.date_publication}
 )  


@app.get("/")
async def root():
    return "data from backend"

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
    
@app.post("/scrap/")
async def scrap(wilaya:number):
    print("hhh",wilaya.val)
    result = ScrapOuedkniss(wilaya.val)
    print("rrr",len(result))
    for annonce in result:
        try:
         database.insert_row(cursor,"testp","annonces",annonce)
         print("inserted")
         Database.commit()
        except:
            print("Error")
            continue
    return result

@app.post("/DeposerAnnonce/")
async def DeposerAnnonce(annoncerecu:annonce):
    print("debut insertion")
    print(annoncerecu)
    create_annonce(annoncerecu)
    print("fin insertion")
    Database.commit()
    return 202


@app.post("/Signup")
async def CreateUser(newUser:user):
    database.insert_row(cursor,"testp","users",{"username":newUser.username,"email":newUser.email,"password":newUser.password})
    Database.commit()
    cursor.execute("SELECT * FROM testp.users WHERE email = '{}'".format(newUser.email)) 
    return cursor.fetchone()

@app.post("/UserExists")
async def UserExists(newUser:user):
    cursor.execute("SELECT * FROM testp.users WHERE email = '{}' AND password = '{}'".format(newUser.email, newUser.password))
    result = cursor.fetchone()
    if (result == None):
        return False
    return True


@app.post("/getUserbyID")
async def GetuserByid(User:user):
    cursor.execute("SELECT id FROM testp.users WHERE email = '{}' AND password = '{}'".format(User.email, User.password))
    result = cursor.fetchone()
    return result


@app.post("/getAnnonceid")
async def getannoncebyID(id:number):
    print("hello")
    cursor.execute(f"SELECT * FROM testp.annonces WHERE id_annonce= {id.val}")
    result = cursor.fetchone()
    return result
        
        
    