from fastapi import FastAPI,Response,status,HTTPException,Depends,File, UploadFile,APIRouter
from sqlalchemy.orm import Session
import models,schemas,utils
from . import oauth2
from database import get_db


router=APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def Vote(vote_post:schemas.Vote,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    print(vote_post.post_id)
    print(vote_post.dir)
    #post=models.Vote(**vote_post.model_dump)
    post=db.query(models.Post).filter(models.Post.id==vote_post.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post {vote_post.post_id} not exists")
    if vote_post.dir not in [0,1]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Not allowed any other numbers other than 0 or 1")
    vote_query=db.query(models.Vote).filter(models.Vote.post_id==vote_post.post_id,models.Vote.user_id==current_user.id)
    found_vote=vote_query.first()
    if vote_post.dir==1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"User {current_user.id} already liked the {vote_post.post_id}")
        new_post=models.Vote(post_id=vote_post.post_id,user_id=current_user.id)
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return {"Successfully added post",new_post}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Vote not find")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return{"Vote deleted successfully",found_vote}


