from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import app_auth, app_users, app_products, app_password, app_bill, app_location
from database import mysql
from settings import ENVIRONMENT

app = FastAPI()

if ENVIRONMENT == 'prod':
    origins = ['https://zapacommerce.web.app']
else:
    origins = ['https://zapacommerce-development.web.app', 'http://localhost:4200']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(app_auth, prefix='/api')
app.include_router(app_users, prefix='/api')
app.include_router(app_products, prefix='/api/products')
app.include_router(app_bill, prefix='/api/bill')
app.include_router(app_password, prefix='/api')
app.include_router(app_location, prefix='/api')


@app.on_event('startup')
def connect_db():
    mysql.sql_conn = mysql.db_connection()
