from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import app_auth, app_user
from database import mysql

app = FastAPI()

origins = ['https://zapacommerce.web.app']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(app_auth, prefix='/api')
app.include_router(app_user, prefix='/api')


@app.on_event('startup')
def connect_db():
    mysql.sql_conn = mysql.db_connection()
