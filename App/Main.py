#  VIRTUAL ENVIRONMENT SETUP 
# PYTHON INTERPRETER SELECTION
#
# C:\Satheesh\Learnings\API_Project>py -3 -m venv venv 
#C:\Satheesh\Learnings\API_Project>py -3 venv venv
#C:\Users\reddy\AppData\Local\Programs\Python\Python312\python.exe: can't open file 'C:\\Satheesh\\Learnings\\API_Project\\venv': [Errno 2] No such file or directory

#C:\Satheesh\Learnings\API_Project>py -3 -m venv venv

#C:\Satheesh\Learnings\API_Project>venv\Scripts\activate.bat

#(venv) C:\Satheesh\Learnings\API_Project>
# C:\Satheesh\Learnings\API_Project\App>uvicorn Main:app --reload


from importlib.resources import contents
from fastapi import FastAPI,Response,status,HTTPException,Depends,File, UploadFile
from fastapi.params import Body # this package helps to get the body data completely
from pydantic import BaseModel # THis one helps to validate the body while posting the data in 
from typing import Optional,List,Annotated #this package helps to define the whether body field is optional or not while validating
from random import randrange 
import csv
from sqlalchemy.orm import Session
import models
from database import engine,SessionLocal,get_db
import io
from routers import post,user,auth,vote
from config import settings
from fastapi.middleware.cors import CORSMiddleware # Cross origin resourse sharing which allows to access our endpoint to specific web server

models.Base.metadata.create_all(bind=engine)

app=FastAPI()

origins=['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)



@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile,db:Session=Depends(get_db)):
    data=open(file.filename,encoding='utf-8')
    csv_data=csv.reader(data)
    data_lines = list(csv_data)
    
   # csv1_data=io.StringIO()
    #csv1_data=io.StringIO(contents.decode('utf=8'))
    #csv1_data=io.StringIO(da.decode('utf-8'))
    #csv_reader=csv.DictReader(csv1_data)
    #json_data=[row for row in csv_reader]
    #print(json_data)
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400,detail="Only CSV files allowed")
    contents= await file.read()
    csv1_data=contents.decode('utf-8').splitlines()
    csv_reader=csv.reader(csv1_data)
    #json_data=[row for row in csv_reader]
    for row in csv_reader:
       tdata=models.Isocodes(country_code=row[0],alpha_2=row[1],alpha_3=row[2],region=row[3],sub_region=row[4])
       db.add(tdata)
    db.commit()
    db.close()
    #return json_data[1]