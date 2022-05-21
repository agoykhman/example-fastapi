from pydoc import plain
from passlib.context import CryptContext

#--selection of hashing algorithm for creating User passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password:str):
  return pwd_context.hash(password)

def verify(plain_password, hashed_password):
  return pwd_context.verify(plain_password, hashed_password)
  