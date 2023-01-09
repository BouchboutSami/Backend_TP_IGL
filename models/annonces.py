from pydantic import BaseModel
import mysql.connector
import models.database as database
from datetime import datetime

Database = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678"
)

cursor = Database.cursor()

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

    
    def get_filtred_annonces( le_type ,la_wilaya ,la_commune ):
        database.use_db(cursor,"website")
        sql = "SELECT * FROM annonces WHERE "
        queries = dict(type_annonce=le_type,wilaya=la_wilaya,commune=la_commune)
        for i in queries.copy() :
            if(queries[i] =='' ):
                l = queries.pop(i,None)
        if(len(queries) < 2 ):
            
            
            x = list(queries)[0]
            y = queries[x]
            sql  =sql+"{} = \"{}\" ;".format(x,y)
            
        else :
            for  i in range(len(queries)):
                x = list(queries)[i]
                y = queries[x]
                sql  =sql+"{} = \"{}\" ".format(x,y)
                sql += " AND "
            sql = sql[:-4]+";"
        print(sql)    
        cursor.execute(sql)
        return cursor.fetchall()
 

       

        





    
    def get_annonce_id(id):
        database.use_db(cursor,"website")
        cursor.execute(f"SELECT * FROM annonces where id_annonce = {id}")
        return cursor.fetchone()
    def  get_all_annonces_of_utilisateur(id_contact:int):
        database.use_db(cursor,"website")
        cursor.execute("SELECT * FROM annonces WHERE id_contact = {} ;".format(id_contact))
        return cursor.fetchall()
    def get_annonces_by_mot_cle(mot_cle:str):
       database.use_db(cursor,"website")
       sql = "SELECT * FROM annonces WHERE  titre LIKE  \"%{0}%\" OR categorie LIKE \"%{0}%\" OR type_annonce LIKE \"%{0}%\" OR description LIKE \"%{0}%\" OR wilaya LIKE \"%{0}%\"  OR commune LIKE \"%{0}%\" OR adresse LIKE \"%{0}%\" ;".format(mot_cle)
       cursor.execute(sql)
       return cursor.fetchall()

    def get_all_annonces():
        database.use_db(cursor,'website')
        cursor.execute("SELECT * FROM annonces ;")
        k= cursor.fetchall()
        return k[::-1]
    def create_annonce(annonce):
        now = datetime.now()
    
        database.insert_row(cursor,'website','annonces',{'categorie':annonce.categorie,'type_annonce':annonce.type_annonce ,'surface':annonce.surface,'description':annonce.description,'prix':annonce.prix,'id_contact':annonce.id_contacts,'wilaya':annonce.wilaya ,'commune':annonce.commune,'adresse':annonce.adresse,'path_pics':annonce.path_pics ,'titre':annonce.titre,'date_publication':now.strftime("%Y/%m/%d")}
 )  
        Database.commit() 

    def delete_annonce(id_annonce:int):
        database.delete_data(cursor, 'website', 'annonces','id_annonce' ,id_annonce)
        Database.commit() 
        return 200        

    