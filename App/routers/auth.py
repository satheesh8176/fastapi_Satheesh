from fastapi import APIRouter,Depends,HTTPException,status,responses
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db
from sqlalchemy.orm import Session
import models,schemas,utils
from . import oauth2

router=APIRouter(
    tags=['AUthentication']
)

@router.post("/login")
#def login(user_credential:schemas.UserLogin,db:Session=Depends(get_db)):
def login(user_credential:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):    
    #hash_password=utils.hashing(user_credential.password)
    #{ "username":"wewew", "password":"sfdssd"} ---from Oauth2PasswordRequestForm module.
    #user_login=db.query(models.User).filter(models.User.email==user_credential.email).first()
    user_login=db.query(models.User).filter(models.User.email==user_credential.username).first()
    password1=user_login.password
    print(password1)

    if not user_login:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"invalid credentials")
    if not utils.verify(user_credential.password,user_login.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"invalid credentials")
    
    #create a token now
    auth_token=oauth2.create_access_token(data={"user_id":user_login.id})
    #retunr token
    return {"access_token":auth_token,"token_typ":"bearer"}




