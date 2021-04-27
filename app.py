from fastapi import FastAPI, Depends, WebSocket
from routes import app_login, app_user
from database import mysql

app = FastAPI()

app.include_router(app_login, prefix='/api')
app.include_router(app_user, prefix='/api')


@app.on_event('startup')
def connect_db():
    mysql.sql_conn = mysql.db_connection()
