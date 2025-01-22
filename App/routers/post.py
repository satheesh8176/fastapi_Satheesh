from fastapi import FastAPI,Response,status,HTTPException,Depends,File, UploadFile,APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
import models,schemas,utils
from . import oauth2
from database import get_db
from fastapi.params import Body # this package helps to get the body data completely
from typing import Optional,List,Annotated #this package helps to define the whether body field is optional or not while validating


my_posts=[{"Title":"title of post1","Content":"Content of post1","id":1},{"Title":"Food","Content":"All about food from world","id":2}]


router=APIRouter(
    #prefix="/posts"
    tags=['Posts']
)

my_posts=[{"Title":"title of post1","Content":"Content of post1","id":1},{"Title":"Food","Content":"All about food from world","id":2}]

def find_post(id):
    print(type(id))
   # print(type(my_posts['id']))
    for p in my_posts:
        print(p["id"])
        print(id)
        if p["id"] == id:
            return p
        else:
            continue

def find_index(id):
    for i,p in enumerate(my_posts):
        if p["id"]==id:
            return i

@router.get("/")
async def root():
    return{"message":"Welcome to my API!!!!"}

#@router.get("/posts",response_model=List[schemas.Post])
@router.get("/posts",response_model=List[schemas.PostVote])
#def get_posts(db:Session=Depends(get_db),current_user:int =Depends(oauth2.get_current_user)):
def get_posts(db:Session=Depends(get_db),current_user:int =Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search:Optional[str]=""):    
   # cursor.execute("""SELECT *FROM posts""")
    #post=cursor.fetchall()
    #if models.Post.owner_id==current_user.id:
    print(limit)
    print(search)
    #post=db.query(models.Post).filter(models.Post.owner_id==current_user.id).all() -- this is for user based get based on user authentication
    post=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    result=db.query(models.Post,func.count(models.Vote.post_id).label("Votes")).join(
        models.Vote,models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).all()
    #if not post:
    #    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"no posts/data created by this user {current_user.id}")
    #else:
    #raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"no posts/data created by the current user{current_user.id}")
    #print(post)
    #print(result)
    #return {"data":post}
    #results_dict = [{"post": post.__dict__, "votes": votes} for post, votes in result]
    return result

@router.post("/createposts")
def get_posts():
    return{"messages":"Successfully posted"}

@router.post("/postdata")
def create_post(payLoad: dict=Body(...)):
    print(payLoad)
    return{"New Message":f"Title :{payLoad['Title']} and Content:{payLoad['Content']}"}

@router.post("/Validation",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def validation_post(new_post:schemas.CreatePost,db:Session=Depends(get_db),current_user:int =Depends(oauth2.get_current_user)):
    #cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,(new_post.Title,new_post.Content,new_post.published))
    #post=cursor.fetchone()
    #conn.commit()
       #print(new_post.Title,new_post.published,new_post.rating)
   # print(new_post.model_dump())
    #post_dict=new_post.model_dump()   # this creates the post body into dictionary format.
    #post_dict['id']=randrange(0, 100000)
    #my_posts@routerend(post_dict)
    #print(new_post.model_dump())
    #newpost=models.Post(title=new_post.Title,content=new_post.Content,published=new_post.published) # on this we need to provide the every column from model
    print(current_user.id)
    print(current_user.email)
    newpost=models.Post(owner_id=current_user.id,**new_post.model_dump()) # this one helps to grab all the columns from model instead of mentioneing all individually
    #print(newpost)
    db.add(newpost)
    db.commit()
    db.refresh(newpost) # THis one will make sure newpost will have up to date data after insert/update from end point body
    #return {"new_post": newpost}
    return newpost

@router.get("/posts/latest",response_model=schemas.Post)
def get_latest_post():
    post=my_posts[len(my_posts)-1]
    #return{"Details":post}
    return post





# getting onerecord

@router.get("/posts/{id}",response_model=schemas.Post)
def get_post(id: int,db:Session=Depends(get_db),current_user:int =Depends(oauth2.get_current_user)): #,response: Response):
    #print(id)
    #print(type(id))
    #cursor.execute("""SELECT *FROM posts WHERE id = %s""",(str (id)))
    #post=cursor.fetchone()
    post=db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} was not found")
    if post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User is not authenticated")
    #post=find_post(id)
   # if not post:
   #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} was not found")
   #     #response.status_code=404
        #return{"Data not found":response.status_code}
    #print(post)
    return post

@router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),current_user:int =Depends(oauth2.get_current_user)):
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """,(str(id)))
    #del_post=cursor.fetchone()
    #post=find_index(id)
    #my_posts.pop(post)
    post=db.query(models.Post).filter(models.Post.id==id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{id} is not a valid ID to delete")
    if post.first().owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User is not authenticated")
    post.delete(synchronize_session=False)
    db.commit()
    return {"Message":"post deleted successfully"}
    #conn.commit()
    #my_posts.pop(del_post)
    #return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/posts/{id}",status_code=status.HTTP_202_ACCEPTED,response_model=schemas.Post)
def update_post(id:int,post:schemas.UpdatePost,db:Session=Depends(get_db),current_user:int =Depends(oauth2.get_current_user)):
   #print(post.model_dump())
    #print(post)
    #cursor.execute("""UPDATE posts SET title= %s WHERE id =%s RETURNING * """,(post.Title,(str(id))))
    #updated_post=cursor.fetchone()
    #index=find_index(id)
    #my_posts.pop(post)
    updpost=db.query(models.Post).filter(models.Post.id==id)
    if updpost.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{id} is not a valid ID to delete")
    if updpost.first().owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User is not authenticated")
    updpost.update(post.model_dump(),synchronize_session=False)
    db.commit()
    #conn.commit()
    #upd_post=post.model_dump()
    #upd_post["id"]=id
    #my_posts[index]=upd_post
    #return{"Message Updtaed with ":updpost.first()}
    return updpost.first()

#---------------------- ORM code -------------------
@router.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts=db.query(models.Post).all()
    print(posts)
    return{"Data":posts}