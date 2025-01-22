from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from pymongo import MongoClient
from config import settings


#SQLALCHEMY_DATABASE_URL= 'postgresql://postgres:root@localhost/FastAPI'

SQLALCHEMY_DATABASE_URL= f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL) # this one helps connecting database through SQLALCHEMY 

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base() # declarative_base() function creates a base class for all your declarative class definitions. This base class maintains a catalog of classes and mapped tables in the application.ORM Mapping: Using this base class, you can define your table structures as Python classes. These classes will be automatically mapped to database tables.

def get_db(): # this one is to get the DB session whenever request from code to connect the DB
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

while True:
 try:
    conn=psycopg2.connect(host='localhost',database='FastAPI',user='postgres',password='root',cursor_factory=RealDictCursor)
    cursor=conn.cursor()
    print("Database connection was successful")
    break
 except Exception as error:
    print("Connection to databse dailed")
    print("Error:",error)
    time.sleep(10) 

#while True:  Mongo Connection 

try:
   # conn_mongo=pymongo..connect(host='localhost',database='testsatheesh',user='',password='',cursor_factory=RealDictCursor)
    #cursor=conn_mongo.cursor()
    uri="mongodb://localhost:27017/"
    client=MongoClient(uri)
    print("mongo server connected successfully")
    database=client.get_database("testsatheesh")
    table=database.get_collection("test1")
    query={"Name":"Satheesh1"}
    test = table.find_one(query)
    print(test)
    client.close()
    print("Mongo Database connection was successful")
    #break
except Exception as error:
    print("Connection to databse dailed")
    print("Error:",error)
    time.sleep(10) 
    #break