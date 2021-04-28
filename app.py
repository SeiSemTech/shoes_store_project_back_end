from fastapi import FastAPI
from routes import app_auth, app_user
from database import mysql

app = FastAPI()

app.include_router(app_auth, prefix='/api')
app.include_router(app_user, prefix='/api')


@app.on_event('startup')
def connect_db():
    mysql.sql_conn = mysql.db_connection()
