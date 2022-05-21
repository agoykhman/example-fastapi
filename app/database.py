from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings 

#--connection string -------
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_user_name}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
# string format as 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'

#--connection engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#-model will be an extension of this Base class
Base = declarative_base()

#--Dependency. Used to open & close SQL session any time a function in the API end point is called
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
