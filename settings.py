import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

ENVIRONMENT = os.environ.get("ENVIRONMENT")
SHOES_DATABASE = os.environ.get('SHOES_DATABASE')

JWT_EXPIRATION_MINUTES = os.environ.get('JWT_EXPIRATION_MINUTES')
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM')


MYSQL_USER = os.environ.get('MYSQLCONNSTR_MYSQL_USER')
MYSQL_PASSWORD = os.environ.get('MYSQLCONNSTR_MYSQL_PASSWORD')
MYSQL_HOST = os.environ.get('MYSQLCONNSTR_MYSQL_HOST')
