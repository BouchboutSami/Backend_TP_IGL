from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import mysql.connector
import os
import database
from pydantic import BaseModel
from dotenv import load_dotenv


load_dotenv()
app = FastAPI()

Database = mysql.connector.connect(
     host="localhost",
     user=os.getenv("ME"),
     password=os.getenv("PASSWORD")
 )
class user(BaseModel):
    id:int
    nom: str
    prenom: str
    email: str
    password:str
    password_hash:str


cursor = Database.cursor()

@app.get("/")
async def root():
    database.create_table(cursor,"UserBDD","user","id INT PRIMARY KEY AUTO_INCREMENT NOT NULL","nom VARCHAR(100)","prenom VARCHAR(100)","email VARCHAR(200)","password VARCHAR(200)","password_hash VARCHAR(200)")
    database.show_tables(cursor,"UserBDD")
    Database.commit()
    return 200

@app.get("/login") 
async def login(email_user:str,password:str):
    cursor.execute("USE {}".format("UserBDD"))
    commande= "SELECT * FROM user WHERE email='{}'".format(email_user)
    cursor.execute(commande)
    myresult=cursor.fetchone()
    print(myresult)
    if(myresult==None or myresult[5]!=password ):
        return "Acces_Non_Autorise"
    else:
        return "Acces_Autorise"   

@app.get("/signup")
async def signup(nom_user:str,prenom_user:str,email_user:str,password_user:str):
    cursor.execute("USE {}".format("UserBDD"))
    commande= "INSERT INTO user (nom, prenom, email, password) VALUES (%s,%s,%s,%s)"
    val=(nom_user,prenom_user,email_user,password_user)
    cursor.execute(commande,val)
    Database.commit()
    print(cursor.rowcount,"record inserted")
