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
   database.create_table(cursor,"testp","annonces","id INT PRIMARY KEY NOT NULL","nom VARCHAR(100)","prenom VARCHAR(100)")
   return 200