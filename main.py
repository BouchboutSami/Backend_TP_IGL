from fastapi import FastAPI
import mysql.connector
import os
import database
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

Database = mysql.connector.connect(
    host="localhost",
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD")
)


cursor = Database.cursor()

@app.get("/")
async def root():
   database.insert_row(cursor,"testp","users",{"firstname":"sami","lastname":"bcht","email":"fef@gm","password":"fr","age":"32"})
   Database.commit()
   return 200