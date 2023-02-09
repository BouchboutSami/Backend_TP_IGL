from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
import os
from pydantic import BaseModel
import database
from dotenv import load_dotenv
from Web_Scraping_TP_IGL.IGL_scraping import *
from models import annonces
from models import messages
import datetime

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
    
class filtreAnnonce(BaseModel):
    recherche:str
    wilaya:str
    commune:str
    typeAnnonce:str
    
class message(BaseModel):
    Message_content:str
    id_destinataire:int
    id_emetteur:int

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


@app.post("/")
async def root():
    return "data from backend"

    
@app.post("/scrap/")
async def scrap(wilaya:number):
    result = ScrapOuedkniss(wilaya.val)
    for annonce in result:
        try:
        #  annonce["image"]=annonce["image"][] 
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
    create_annonce(annoncerecu)
    print("fin insertion")
    Database.commit()
    return 202


@app.post("/Signup")
async def CreateUser(newUser:user):
    database.insert_row(cursor,"testp","users",{"username":newUser.username,"email":newUser.email,"password":newUser.password,"isadmin":0})
    Database.commit()
    cursor.execute("SELECT * FROM testp.users WHERE email = '{}'".format(newUser.email))
    result = cursor.fetchone()
    return {"id":result[0],"username":result[1],"email":result[2],"password":result[3],"isadmin":0}

@app.post("/UserExists")
async def UserExists(newUser:user):
    cursor.execute("SELECT * FROM testp.users WHERE email = '{}' AND password = '{}'".format(newUser.email, newUser.password))
    result = cursor.fetchone()
    if (result == None):
        return False
    return True


@app.post("/getUserbyID")
async def GetIdOfUser(User:user):
    cursor.execute("SELECT id,isadmin,username FROM testp.users WHERE email = '{}' AND password = '{}'".format(User.email, User.password))
    result = cursor.fetchone()
    return result


@app.post("/getAnnonceid")
async def getbyID(id:number):
    cursor.execute(f"SELECT * FROM testp.annonces WHERE id_annonce= {id.val}")
    result = cursor.fetchone()
    return result

@app.post("/getuserid")
async def getannoncebyID(id:number):
    cursor.execute(f"SELECT * FROM testp.users WHERE id= {id.val}")
    result = cursor.fetchone()
    return result

@app.post("/GetAnnoncesfiltered")
async def getAnnoncesbyFilter(filtre:filtreAnnonce):
    filtres = remove_empty_strings(filtre)
    sql = "SELECT * FROM testp.annonces WHERE"
    cpt = 0
    if ("recherche" in filtres):
        cpt += 1
        sql += f" AND description LIKE '%{(filtre.recherche).lower()}%' "
    if ("typeAnnonce" in filtres):
        cpt += 1
        sql += f" AND type_annonce = '{filtre.typeAnnonce}'"
    if ("wilaya" in filtres):
        cpt += 1
        sql += f" AND wilaya = '{filtre.wilaya}'"
    if ("commune" in filtres):
        cpt += 1
        sql += f" AND commune = '{filtre.commune}'"
    sql = sql.replace("AND","",1)
    if (cpt == 0):sql="SELECT * FROM testp.annonces" 
    sql += " LIMIT 0, 50"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result
    
@app.post("/annonces_utilisateur")
async def get_all_annonce_of_utilisateur(id_contact:number):
     cursor.execute(f"SELECT * FROM testp.annonces WHERE id_contact = {id_contact.val}")
     result = cursor.fetchall()
     return result
    
@app.post("/Deleteannonce/")
def delete_data(id_annonce:number):
    print("hh")
    cursor.execute(f"DELETE FROM testp.annonces WHERE id_annonce = {id_annonce.val}")
    Database.commit()
    return 202

@app.post("/Sendmessage/") 
async def message_send(msg:message):
    x = datetime.datetime.now()
    x = x.strftime('%Y-%m-%d') 
    sql = f"INSERT INTO messages(`Message_content`,id_emetteur,create_time,id_destinataire) VALUES('{msg.Message_content}',{msg.id_emetteur},'{x}',{msg.id_destinataire});"
    cursor.execute(sql)
    Database.commit()
    return 202

@app.post("/GetmessagesUser/")
async def messages_utilisateur(id_receiver:number):
    cursor.execute(f"SELECT * FROM testp.messages WHERE id_destinataire ={id_receiver.val}")
    result = cursor.fetchall()
    return result

@app.post("/GetAllusers")
async def Allusers():
    cursor.execute(f"SELECT * FROM testp.users")
    result = cursor.fetchall()
    return result


    
    
    
    
    
    
    
    
    
    
    
    
    
    
def remove_empty_strings(obj:filtreAnnonce):
    filtre = {}
    if (obj.recherche != ""):filtre["recherche"]=obj.recherche
    if (obj.wilaya != ""):filtre["wilaya"]=obj.wilaya
    if (obj.typeAnnonce != ""):filtre["typeAnnonce"]=obj.typeAnnonce
    if (obj.commune != ""):filtre["commune"]=obj.commune
    return filtre
        
        
    