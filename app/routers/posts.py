from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import  models,schemas,OAuth2
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import get_db
from typing import Optional,List
router=APIRouter(prefix="/sqlalchemy/posts",tags=['Posts'])


@router.get("/", response_model=List[schemas.Output])
def get_posts_alchemall( db: Session = Depends(get_db),current_user_id : int = Depends(OAuth2.get_current_user),Limit:int = 10, Skip:int =0, Search: Optional[str]=""):
   # posts=db.query(models.Post).filter(models.Post.content.contains(Search)).limit(Limit).offset(Skip).all()

   # post=db.query(models.Post).filter(models.Post.owner_id == int(current_user_id.id)).all()
   # posts=db.query(models.Post).all()
    #return{"status": posts}
    results=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.content.contains(Search)).limit(Limit).offset(Skip).all()
  
    return results



@router.post("/",status_code=201,response_model=schemas.Resp)
def create_posts_alchem(post: schemas.CreatePost , db: Session = Depends(get_db), user_id : int = Depends(OAuth2.get_current_user)):
   # new_post=models.Post(title=post.title,content=post.content,published=post.published)
    new_post=models.Post(owner_id=user_id.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    #return{"data":new_post}
    return new_post


@router.get("/{id}",response_model=List[schemas.Resp])
def get_posts_alchem(id: int  , db: Session = Depends(get_db),user_id : int = Depends(OAuth2.get_current_user)):
   # new_post=models.Post(title=post.title,content=post.content,published=post.published)
    post=db.query(models.Post).filter(models.Post.id== id).all()
    if not post:
         raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"Post with id {id} not found")
    #return{"data":post}
    return post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts_alchem(id: int  ,db: Session = Depends(get_db), current_user_id : int = Depends(OAuth2.get_current_user)):
   # new_post=models.Post(title=post.title,content=post.content,published=post.published)
  post=db.query(models.Post).filter(models.Post.id== id)

  if post.first()==None:
         raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"Post with id {id} not found")
 
  if post.first().owner_id != int(current_user_id.id):
         raise HTTPException (status_code=status.HTTP_403_FORBIDDEN,
                              detail="You do not have access to delete this post")

  post.delete(synchronize_session=False)
  db.commit()
  return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
def update_posts_alchem(id: int , updt_post:schemas.UpdatePost, db: Session = Depends(get_db),user_id : int = Depends(OAuth2.get_current_user)):
   # new_post=models.Post(title=post.title,content=post.content,published=post.published)
  post=db.query(models.Post).filter(models.Post.id== id)
  if post.first()==None:
         raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Post with id {id} not found")
 
  if post.first().owner_id != int(user_id.id):
         raise HTTPException (status_code=status.HTTP_403_FORBIDDEN,
                              detail=f"You do not have access to update this post")
  #post.update({'title': 'hey this is my updated title', 'content':'this is my updated content'},synchronize_session=False)
  post.update(updt_post.dict(),synchronize_session=False)
  
  db.commit()
  return updt_post