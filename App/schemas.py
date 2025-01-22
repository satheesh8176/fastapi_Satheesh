from typing import Optional
from pydantic import BaseModel,EmailStr # THis one helps to validate the body while posting the data in 
from datetime import datetime

class PostBase(BaseModel):
    title:str
    content:str
    published:bool = True
   # rating:Optional[int] =None
   # id:Optional[int]=None

class CreatePost(PostBase):   # Inheritence from PosrBase class
    pass

class UpdatePost(BaseModel):
    title:str
    content:str
    published:bool
    #owner_id:int
   # rating:Optional[int] =None
   # id:Optional[int]=None

class UserOut(BaseModel):
    id:int
    email:str
    created_at:datetime
    class config():
        orm_mode=True

class Post(BaseModel):
    id:int
    title:str
    content:str
    published:bool
    created_at:datetime
    owner_id:int
    owner:UserOut  # this is pydantic model and inherit the schema and assign this to variable .And this will return the UserOut class as a response 
    
    class config():
        orm_mode=True

class PostVote(BaseModel):
    Post:Post
    Vote:int

    class config():
        orm_mode=True

class UserCreate(BaseModel):
    email:EmailStr
    password:str


class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[int]=None


class Vote(BaseModel):
    post_id:int
    dir:int