from pydantic import BaseModel, EmailStr
from pydantic.types import StrictBool, conint 
from datetime import datetime 
from typing import Optional


class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  id: Optional[str] = None


#--structure of data required to create a new user id
class UserCreate(BaseModel):
  email: EmailStr
  password: str

#--structure of Create User POST all
class UserOut(BaseModel):
  id: int
  email: EmailStr
  created: datetime

  class Config:
    orm_mode = True

class UserLogin(BaseModel):
  email: EmailStr
  password: str


##--extension of BaseModel to fit POST (.models.Post()) data
##--this is the Pydantic model that defines the schema/structure of a request
##--request is passed through the Pydantic model to limit the request to a required schema
class PostBase(BaseModel):
  title: str
  content: str
  published: bool = True
  
class PostCreate(PostBase):
  pass 

#--structure of data returned to the user from an api call (no id, no timestamp)
#--class is refered to in the main.py fastapi decorator "response_model" parameter
class Post(PostBase):
  id: int
  created: datetime 
  user_id: int 
  owner: UserOut  # class referenced above
  #all columns from PostCase class are inheritted by default. no need to specify them
  class Config:
    orm_mode = True
    #--this class returns a SQLALCHEMY model, not a dictionary
    #--tells pydantic to ignore the default rule of reading only dictionaries.
    #--tells pydantic to convert the sqlalchemy model to a pydantic model

class PostOut(BaseModel):
  Post: Post
  votes: int

  class Config:
    orm_mode = True
"""
  id: int
  created: datetime
  user_id: int
  published: bool
  title: str 
  content: str 
  class Config:
    orm_mode = True
"""

class Vote(BaseModel):
  post_id: int 
  dir: bool #could also be conint(le=1)