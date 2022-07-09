from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import models,schemas,utils
from sqlalchemy.orm import Session
from ..database import get_db
router=APIRouter(prefix="/users",tags=['Users'])
@router.post("/",status_code=201,response_model=schemas.userresp)
def create_users_alchem(user: schemas.UserCreate , db: Session = Depends(get_db)):
  # hash the password
    hashed_pass=utils.hash(user.password)
    user.password=hashed_pass
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    #return{"data":new_post}
    return new_user

@router.get("/{id}",response_model=schemas.userresp)
def get_users_alchem(id: int, db: Session = Depends(get_db)):
  # hash the password
     user=db.query(models.User).filter(models.User.id== id).first()
     if not user:
         raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"User with id {id} not found")
    #return{"data":post}
     return user
