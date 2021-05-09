from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import app_auth, app_user, app_article
from database import mysql
from settings import ENVIRONMENT

app = FastAPI()

if ENVIRONMENT == 'prod':
    origins = ['https://zapacommerce.web.app']
else:
    origins = ['http://localhost:4200']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(app_auth, prefix='/api')
app.include_router(app_user, prefix='/api')
app.include_router(app_article, prefix='/api/articles')

@app.on_event('startup')
def connect_db():
    mysql.sql_conn = mysql.db_connection()
