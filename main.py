from fastapi import FastAPI
import mysql.connector
from pydantic import BaseModel
import database
from models.annonces import *
from models.messages import *
from datetime import datetime
app = FastAPI()

Database = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678"
)

 
cursor = Database.cursor()
" "
@app.get("/")
async def root():
    
    return 200 
@app.get("/annonce/{id_annonce}")
async def get_annonce_info_by_id(id_annonce:int):
    database.use_db(cursor,'website')
    cursor.execute("SELECT * FROM annonces WHERE id_annonce = {} ;".format(id_annonce))
    return cursor.fetchall()


@app.get("/annonces_utilisateur/{id_contact}")
async def get_all_annonce_of_utilisateur(id_contact:int):
    database.use_db(cursor,'website')
    cursor.execute("SELECT * FROM annonces WHERE id_contact = {} ;".format(id_contact))
    return cursor.fetchall()

@app.get("/annonces_motcle/{mot_cle}")
async def get_annonces_by_mot_cle(mot_cle:str):
    database.use_db(cursor,'website')
    sql = "SELECT * FROM annonces WHERE  titre LIKE  \"%{0}%\" OR categorie LIKE \"%{0}%\" OR type_annonce LIKE \"%{0}%\" OR description LIKE \"%{0}%\" OR wilaya LIKE \"%{0}%\"  OR commune LIKE \"%{0}%\" OR adresse LIKE \"%{0}%\" ;".format(mot_cle)
    cursor.execute(sql)
    
    return cursor.fetchall()



@app.get("/annonces")
async def get_annonces_all():
    database.use_db(cursor,'website')
      
    cursor.execute("SELECT * FROM annonces ;")
    k= cursor.fetchall()
    return k[::-1]


@app.post("/annonce")     
async def creat_annonce(annonce:annonce):
    now = datetime.now()
    print(now.strftime("%Y/%m/%d"))
    database.insert_row(cursor,'website','annonces',{'categorie':annonce.categorie,'type_annonce':annonce.type_annonce ,'surface':annonce.surface,'description':annonce.description,'prix':annonce.prix,'id_contact':annonce.id_contacts,'wilaya':annonce.wilaya ,'commune':annonce.commune,'adresse':annonce.adresse,'path_pics':annonce.path_pics ,'titre':annonce.titre,'date_publication':now.strftime("%Y/%m/%d")}
)
     
    Database.commit() 
    return 200

@app.get("/annonce/{type_filter}/{filter_value}")
def get_annonce(type_filter:str, filter_value:str):
    database.recherche_filter(cursor,'website','annonces',type_filter,filter_value)
    k = cursor.fetchall()
    
    return k
@app.get("/annonce/date")
def get_annonce_date(date1:str ,date2:str):
    database.recherche_filter_date(cursor,'website','annonces','date_publication',date1,date2)
    
    return cursor.fetchall()

@app.delete("/annonce/{id_annonce}") 
def delete_data(id_annonce:int):
    database.delete_data(cursor, 'website', 'annonces','id_annonce' ,id_annonce)
    Database.commit() 
    return 200 

@app.post("/message/") 
async def message_send(msg:messagerie):
    now = datetime.now()
    print(10)
    database.insert_row(cursor, 'website', 'messagerie', {'id_annonce':msg.id_annonce,'id_sender':msg.id_sender,'id_receiver':msg.id_receiver,'msg_content':msg.msg_content,'msg_date':now.strftime("%Y/%m/%d %H:%M:%S")})
    Database.commit()
    return 200

@app.get("/message/{id_receiver}")
async def messages_utilisateur(id_receiver:int):
    database.recherche_filter(cursor, 'website', 'messagerie','id_receiver',id_receiver)
    k = cursor.fetchall()
    
    return k[::-1]
