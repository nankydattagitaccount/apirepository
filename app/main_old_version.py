
from asyncio.windows_events import NULL
from multiprocessing import synchronize
from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional,List
from random  import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models,schemas,utils
from .database import engine,SessionLocal
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

while True:

    try:
        conn =    psycopg2.connect(host='localhost', database='fastapi',user='postgres',password='root',cursor_factory=RealDictCursor)
        cursor =  conn.cursor()
        print("Database connection was succesfull")
        break
    except Exception as error:
            print("Coonecting to database failed")
            print("Error:", error)
            time.sleep(2)

app_post =[{"title": "My Name is Khan", "content": "Bollywood Movie", "id":1},
{"title": "My Name is Reddy", "content": "Tollywood Movie", "id":2}
]

def find_post(inputvar):
    for p in app_post:
        if p['id']== inputvar:
          return p

def find_index_post(inputvar):
    for i,p in enumerate(app_post):
        if p['id']== inputvar:
           return i

class Post(BaseModel):
     title: str
     content: str
     published: bool = True
     rating: Optional[int] = NULL

@app.get("/")
def read_root():
    return {"Good Day !!! Nanky"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    cursor_getall=cursor.fetchall()
    #return {"Data": cursor_getall}
    return cursor_getall
 
@app.get("/sqlalchemy/posts", response_model=List[schemas.Resp])
def get_posts_alchemall( db: Session = Depends(get_db)):
    posts=db.query(models.Post).all()
    #return{"status": posts}
    return posts

@app.post("/sqlalchemy/posts",status_code=201,response_model=schemas.Resp)
def create_posts_alchem(post: schemas.CreatePost , db: Session = Depends(get_db)):
   # new_post=models.Post(title=post.title,content=post.content,published=post.published)
    new_post=models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    #return{"data":new_post}
    return new_post

@app.post("/users",status_code=201,response_model=schemas.userresp)
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

@app.get("/users/{id}",response_model=schemas.userresp)
def get_users_alchem(id: int, db: Session = Depends(get_db)):
  # hash the password
     user=db.query(models.User).filter(models.User.id== id).first()
     if not user:
         raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"User with id {id} not found")
    #return{"data":post}
     return user



@app.get("/sqlalchemy/posts/{id}",response_model=List[schemas.Resp])
def get_posts_alchem(id: int  , db: Session = Depends(get_db)):
   # new_post=models.Post(title=post.title,content=post.content,published=post.published)
    post=db.query(models.Post).filter(models.Post.id== id).all()
    if not post:
         raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"Post with id {id} not found")
    #return{"data":post}
    return post


@app.delete("/sqlalchemy/posts/{id}",status_code=204)
def delete_posts_alchem(id: int  ,db: Session = Depends(get_db)):
   # new_post=models.Post(title=post.title,content=post.content,published=post.published)
  post=db.query(models.Post).filter(models.Post.id== id)

  if post.first()==None:
         raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"Post with id {id} not found")

  post.delete(synchronize_session=False)
  db.commit()

@app.put("/sqlalchemy/posts/{id}",response_model=schemas.Resp)
def update_posts_alchem(id: int , updt_post:schemas.UpdatePost, db: Session = Depends(get_db)):
   # new_post=models.Post(title=post.title,content=post.content,published=post.published)
  post=db.query(models.Post).filter(models.Post.id== id)
  if post.first()==None:
         raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"Post with id {id} not found")

  #post.update({'title': 'hey this is my updated title', 'content':'this is my updated content'},synchronize_session=False)
  post.update(updt_post.dict(),synchronize_session=False)
  
  db.commit()
  return updt_post

@app.post("/posts", status_code=201)
def create_posts(new_post: Post):
   # new_post_dict=new_post.dict()
   # new_post_dict['id']=randrange(0,10000000)
   # app_post.append(new_post_dict) 
    cursor.execute("""INSERT INTO posts(title,content,published) VALUES (%s,%s,%s) returning * """,(new_post.title,new_post.content,new_post.published))
    curr_ins_out=cursor.fetchone()
    conn.commit()
    return{"Message Post Created Sucesfully": curr_ins_out }
    #return{"Message Post Created Sucesfully": new_post_dict }



@app.get("/posts/getLatestPost")
def get_latest_post():
      findpost=app_post[len(app_post)-1]
      return{"Message Found Latest Post is": findpost}
 


@app.get("/posts/{id}")
def get_post(id : int , res: Response):
    #print(id)
    #return{"Message": f"Here is the id that you passed {id}"}
    cursor.execute("""SELECT * FROM public."Post" WHERE id = %s   """, (str(id)))
    test_post=cursor.fetchone()
    print(test_post)
    
    #findpost=find_post(int(id))
    #if not find_post
    if not test_post:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"Post with id {id} not found")
     #  res.status_code=status.HTTP_404_NOT_FOUND
     #  return{"Message": f"Post with id {id} not found"}
    return{"Message Found Post": test_post}


@app.delete("/posts/{id}",status_code=204)
def delete_post(id: int):
   cursor.execute("""DELETE FROM public."Post" WHERE id = %s  returning * """, (str(id),))
   del_post=cursor.fetchone()
   print(del_post)
   conn.commit()
   if del_post==None:

  # index=find_index_post(id)
  # if index==None:
              raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"Post with id {id} not found")
   #app_post.pop(index)
   return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, new_post: Post):
    cursor.execute("""UPDATE public."Post" set title=%s, content=%s, published=%s WHERE id = %s  returning * """, (new_post.title,new_post.content,new_post.published,str(id)))
    updt_post=cursor.fetchone()
    conn.commit()
   # index=find_index_post(id)
   # if index==None:
    if updt_post==None:
              raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"Post with id {id} not found")
   # post_dict = new_post.dict()
   # post_dict['id']=id
   # app_post[index]= post_dict
   # return {"data": post_dict}
    return {"data": updt_post}

