
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

class Settings:
    user: str = os.getenv('user')
    password: str = os.getenv('password')
    host: str = os.getenv('host')
    port: str = os.getenv('port')
    database: str = os.getenv('database')

    db_url = rf'mysql+mysqlconnector://{user}:{quote_plus(password)}@{host}:{port}/{database}'

settings = Settings()