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
    result = ScrapOuedkniss(wilaya.val)
    for annonce in result:
        try:
         print(annonce)
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
    cursor.execute("SELECT id,isadmin FROM testp.users WHERE email = '{}' AND password = '{}'".format(User.email, User.password))
    result = cursor.fetchone()
    return result


@app.post("/getAnnonceid")
async def getannoncebyID(id:number):
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
        sql += f" AND description LIKE '%{filtre.recherche}%'"
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
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result
    
@app.get("/annonces_utilisateur/{id_contact}")
async def get_all_annonce_of_utilisateur(id_contact:int):
     return annonces.get_all_annonces_of_utilisateur(id_contact)
 
@app.get("/annonce/date")
def get_annonce_date(date1:str ,date2:str):
    database.recherche_filter_date(cursor,'website','annonces','date_publication',date1,date2)
    return cursor.fetchall()
    
@app.delete("/annonce/{id_annonce}") 
def delete_data(id_annonce:int):
    return annonce.delete_annonce(id_annonce)

@app.post("/message/") 
async def message_send(msg:messages.messagerie):
    return messages.messagerie.send_messages(msg)

@app.get("/message/{id_receiver}")
async def messages_utilisateur(id_receiver:int):
    return messages.messagerie.get_messages(id_receiver)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
def remove_empty_strings(obj:filtreAnnonce):
    filtre = {}
    if (obj.recherche != ""):filtre["recherche"]=obj.recherche
    if (obj.wilaya != ""):filtre["wilaya"]=obj.wilaya
    if (obj.typeAnnonce != ""):filtre["typeAnnonce"]=obj.typeAnnonce
    if (obj.commune != ""):filtre["commune"]=obj.commune
    return filtre
        
        
    