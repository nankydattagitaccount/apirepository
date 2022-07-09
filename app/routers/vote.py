from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import  models,schemas,OAuth2
from sqlalchemy.orm import Session
from ..database import get_db

router=APIRouter(prefix="/vote",tags=['Votes'])


@router.post("/",status_code=201)
def create_votes_alchemall( vote: schemas.Vote, db: Session = Depends(get_db), current_user_id : int = Depends(OAuth2.get_current_user)):

     post=db.query(models.Post).filter(models.Post.id== vote.post_id)

     if post.first()==None:
         raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"Post with id {vote.post_id} not found")

     vote_query=db.query(models.Vote).filter(models.Vote.user_id== current_user_id.id,models.Vote.post_id== vote.post_id)
     found_vote=vote_query.first()
     if (vote.dir==1):
            if found_vote:
                raise HTTPException (status_code=status.HTTP_409_CONFLICT,
                              detail=f"User with id {current_user_id.id} has already voted on the bespoke post {vote.post_id}")
              
            new_vote=models.Vote(post_id=vote.post_id,user_id=current_user_id.id)
            db.add(new_vote)
            db.commit()
            return {"message":"succesfully added vote"}                    

     else:
            if not found_vote:
                raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"No Vote Found")
          
     vote_query.delete(synchronize_session=False)  
     db.commit()
        
     return {"message":"succesfully deleted vote"}        

           
           

