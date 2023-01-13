import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

Database = mysql.connector.connect(
    host="localhost",
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD"),
    database="testp"
)

cursor = Database.cursor()

# ------------------------------- DATABASE OPERATIONS -------------------------------------- #
def use_db(cursor,db_name):
  cursor.execute("USE {}".format(db_name))

def create_database(cursor,db_name):
  cursor.execute("CREATE DATABASE "+db_name)

def show_databases(cursor):
  cursor.execute("SHOW DATABASES")
  for database in cursor:
    print(database)

def show_tables(cursor,db_name):
  use_db(cursor,db_name)
  cursor.execute("SHOW TABLES")
  for table in cursor:
     print(table)

def create_table(cursor,db_name,table_name,*attributs):
  columns = ",".join(attributs)
  use_db(cursor,db_name)
  cursor.execute("CREATE TABLE {} ({});".format(table_name,columns))

def add_column(cursor,db_name,table_name,attribut):
  use_db(cursor,db_name)
  cursor.execute("ALTER TABLE {} ADD COLUMN {}".format(table_name,attribut))

def insert_row(cursor,db_name,table_name,valeurs):
  try:
    use_db(cursor,db_name)
    nvattributs="("
    oldtuple=()
    for key in valeurs:
      nvattributs += key+", "
      newtuple = oldtuple + (valeurs[key],)
      oldtuple = newtuple
    nvattributs = nvattributs[:-2]+")"
    nb_val = "%s, "*len(valeurs)
    nb_val = "("+nb_val[:-2]+")"
    sql = "INSERT INTO {} {} VALUES {}".format(table_name,nvattributs,nb_val)
    cursor.execute(sql,newtuple)
    cursor.close()
    Database.close()
  except:
    print("error")
    
  
def Select_everything(cursor,db_name,table_name):
  use_db(cursor,db_name)
  cursor.execute("SELECT * FROM {}".format(table_name))