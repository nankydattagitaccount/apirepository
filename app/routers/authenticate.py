from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models,schemas,utils,OAuth2
from ..database import get_db
router=APIRouter(prefix="/login",tags=['Authenticate'])

@router.post("/",status_code=201,response_model=schemas.Token)
#def create_login_alchem( user_cred:schemas.userlogin ,db: Session = Depends(get_db)):
def create_login_alchem( user_cred:OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(get_db)):
     #user=db.query(models.User).filter(models.User.email==user_cred.email).first()
     user=db.query(models.User).filter(models.User.email==user_cred.username).first()
     if not user:
         raise HTTPException (status_code=status.HTTP_403_FORBIDDEN,
                              detail=f"Invalid Credentials")
     if not utils.verify(user_cred.password, user.password):
            raise HTTPException (status_code=status.HTTP_403_FORBIDDEN,
                              detail=f"Invalid Credentials")                   
    #return{"data":post}
     
    #Create a token
     access_token = OAuth2.create_access_token(data={"user_id":user.id})
     return{"access_token":access_token, "token_type":"bearer"} 