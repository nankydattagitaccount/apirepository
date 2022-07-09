from datetime import datetime
from pydantic import BaseModel,EmailStr
from typing import Optional
from pydantic.types import conint

class Post(BaseModel):
      title: str
      content: str
      published: bool = True
     #rating: Optional[int] = NULL


class userresp(BaseModel):
      id: int
      email:EmailStr

      class Config:
       orm_mode = True 

     
class Resp(Post):
      id: int
      created_at: datetime
      owner_id: int
      owner: userresp
      
      class Config:
           orm_mode = True

class Output(BaseModel): 
     
     Post: Resp
     votes:int
     class Config:
           orm_mode = True


class CreatePost(BaseModel):
     title: str
     content: str
     published: bool = True
     #rating: Optional[int] = NULL

class UpdatePost(BaseModel):
     title: str
     content: str
     #published: bool
     #rating: Optional[int] = NULL



class UserCreate(BaseModel):
      email:EmailStr
      password:str


class userlogin(BaseModel):
      email:EmailStr
      password:str

class Token(BaseModel):
       access_token:str
       token_type:str

class TokenData(BaseModel):
      id: Optional[str]

class Vote(BaseModel):
      post_id: int
      dir: conint(le=1)

     