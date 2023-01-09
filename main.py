from fastapi import FastAPI
import mysql.connector
from pydantic import BaseModel
from models import annonces
from models import messages
from datetime import datetime
app = FastAPI()

Database = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678"
)

 
cursor = Database.cursor()

@app.get("/")
async def root():
    
    return 200 
@app.get("/annonce/{id_annonce}")
async def get_annonce_info_by_id(id_annonce:int):
    return annonces.annonce.get_annonce_id(id_annonce)


@app.get("/annonces_utilisateur/{id_contact}")
async def get_all_annonce_of_utilisateur(id_contact:int):
     return annonces.annonce.get_all_annonces_of_utilisateur(id_contact)
    

@app.get("/annonces_motcle/{mot_cle}")
async def annonces_by_mot_cle(mot_cle:str):
     return annonces.annonce.get_annonces_by_mot_cle(mot_cle)



@app.get("/annonces")
async def get_annonces_all():
    return annonces.annonce.get_all_annonces()


@app.post("/annonce")     
async def creat_annonce(annonce:annonces.annonce):
     annonces.annonce.create_annonce(annonce)
     return 200 

@app.get("/annonce_filterd/")
def get_annonce_filtered(type_annonce:str ="",wilaya:str = "",commune:str = ""):
    return annonces.annonce.get_filtred_annonces(type_annonce,wilaya,commune)
    

     
    return  annonces.annonce.get_filtred_annonces(filter)
@app.get("/annonce/date")
def get_annonce_date(date1:str ,date2:str):
    database.recherche_filter_date(cursor,'website','annonces','date_publication',date1,date2)
    
    return cursor.fetchall()

@app.delete("/annonce/{id_annonce}") 
def delete_data(id_annonce:int):
    return annonces.annonce.delete_annonce(id_annonce)

@app.post("/message/") 
async def message_send(msg:messages.messagerie):
    return messages.messagerie.send_messages(msg)

@app.get("/message/{id_receiver}")
async def messages_utilisateur(id_receiver:int):
    return messages.messagerie.get_messages(id_receiver)
