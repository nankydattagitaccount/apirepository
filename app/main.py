from fastapi import FastAPI
from typing import Optional,List
from random  import randrange
import time
from . import models
from fastapi.middleware.cors import CORSMiddleware
from .database import engine,SessionLocal
from .routers import posts,user,authenticate,vote
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins=["https://www.google.com","https://www.youtube.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(posts.router)
app.include_router(user.router)
app.include_router(authenticate.router)
app.include_router(vote.router)

@app.get("/")
def read_root():
    return {"Good Day !!! Nanky"}


