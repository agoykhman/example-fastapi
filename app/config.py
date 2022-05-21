from pydantic import BaseSettings
#environment variable validation
#defaults provided. if None, then pydantic will check the envrinment variables


class Settings(BaseSettings):
  database_hostname: str 
  database_port: str 
  database_password: str 
  database_name: str 
  database_user_name: str
  secret_key: str 
  algorithm: str 
  access_token_expire_minutes: int 

  class Config:
    env_file = '.env'

settings = Settings()
#database password = settings.database_password
