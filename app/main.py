#--IMPLEMENTATION USING SQL ALCHEMY OBJECT RELATIONAL MAPPING --#
from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware 
#from sqlalchemy.orm import Session 
from . import models 
from . database import engine 
from . routers import post, user, auth, votes
from . config import settings

#alembic autogenerates tables. no need to autogenerate with sqlalchemy
#models.Base.metadata.create_all(bind = engine)


#module on LOCALHOST---------------------
app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

##-ROOT DIRECTORY---------------------------------------------------
@app.get("/")  # http://127.0.0.1:8000/
def root():
  return {"message": "Hello World. Deployed from CI/CD pipeline up through Ubuntu"}  # returns json in browner

#--bring in the routes defined in post.py to CRUD post objects
app.include_router(post.router)

#--bring in the routes defined in user.py to CRUD user objects
app.include_router(user.router)

#--bring in the routes defined in auth.py for user login 
app.include_router(auth.router)

#--bring in the routers defined in votes.py for user voting or delete vote
app.include_router(votes.router)