from fastapi import FastAPI
import mysql.connector
from pydantic import BaseModel
import database
from datetime import datetime
app = FastAPI()

Database = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678"
)

class annonce(BaseModel):
    id_annonce : int
    categorie:str
    type_annonce : str
    surface : int
    description : str
    prix : int
    id_contacts : int
    wilaya :str
    commune :str
    adresse :str
    path_pics :str
    titre : str

 
cursor = Database.cursor()
" "
@app.get("/")
async def root():
    
    return 200 
@app.get("/annonces")
async def get_annonce_byid():
    database.use_db(cursor,'website')
      
    cursor.execute("SELECT * FROM annonces ;")
    return cursor.fetchall()


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