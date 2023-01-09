from pydantic import BaseModel 
import mysql.connector
from datetime import datetime
import models.database as database

Database = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678"
)

cursor = Database.cursor()




class messagerie(BaseModel):
   id_annonce:int 
   id_sender : int
   id_receiver : int
   msg_content : str
   
   def get_messages(id):
      database.recherche_filter(cursor, 'website', 'messagerie','id_receiver',id)
      k = cursor.fetchall()
    
      return k[::-1]

   def send_messages(msg):
    now = datetime.now()
    print(10)
    database.insert_row(cursor, 'website', 'messagerie', {'id_annonce':msg.id_annonce,'id_sender':msg.id_sender,'id_receiver':msg.id_receiver,'msg_content':msg.msg_content,'msg_date':now.strftime("%Y/%m/%d %H:%M:%S")})
    Database.commit()
    return 200 