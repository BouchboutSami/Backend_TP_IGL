from fastapi import FastAPI
import mysql.connector
from pydantic import BaseModel
import database

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
    database.insert_row(cursor,'website','annonces',{'categorie':annonce.categorie,'type_annonce':annonce.type_annonce ,'surface':annonce.surface,'description':annonce.description,'prix':annonce.prix,'id_contact':annonce.id_contacts,'wilaya':annonce.wilaya ,'commune':annonce.commune,'adresse':annonce.adresse,'path_pics':annonce.path_pics }
)
    Database.commit() 
    return 200
