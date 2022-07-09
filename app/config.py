from pydantic import BaseSettings
import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('C:/Users/Admin/Documents/FastAPI/venv/.env')
load_dotenv(dotenv_path=dotenv_path)

class Settings(BaseSettings):
       database_hostname: str = os.getenv('DATABASE_HOSTNAME')
       database_port: str =  os.getenv('DATABASE_PORT')
       database_password: str  =  os.getenv('DATABASE_PASSWORD')
       database_name: str =  os.getenv('DATABASE_NAME')
       database_username: str =  os.getenv('DATABASE_USERNAME')
       secret_key: str =  os.getenv('SECRET_KEY')
       algorithm: str =  os.getenv('ALGORITHM')
       access_token_expire_minutes: int =  os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
       


settings_var = Settings()

