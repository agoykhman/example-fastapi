#definding models for the ORM
from pydantic import EmailStr
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship 
from sqlalchemy.sql.sqltypes import TIMESTAMP 
from sqlalchemy.sql.expression import text
from .database import Base 

##--sqlalchemy ORM model defining the schema of the database table
##--totally different Post() object from .main.Post. 
##--**this is the table that should exist. not the post requet**
class Post(Base):
  __tablename__ = 'posts'

  id = Column(Integer, primary_key = True, nullable = False)
  title = Column(String, nullable = False)
  content = Column(String, nullable = False)
  published = Column(Boolean, server_default = 'True', nullable = False)
  created = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))
  user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable = False)

  owner = relationship("User")
  #INNER JOIN [USERS] based on User class. #
  # .schemas.PostBase.owner == [USERS] row
  # data will display as nested dict, "owner": {id:x, email:y, created:z }

#--table of users
#--sqlalchemy requirement is to extend Base
class User(Base):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True, nullable=False)
  email = Column(String, nullable=False, unique = True)
  password = Column(String, nullable=False)
  created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
  phone_number = Column(String)

class Vote(Base):
  __tablename__ = "votes"
  user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, primary_key = True)
  post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False, primary_key = True)
  created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))