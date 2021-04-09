from fastapi import FastAPI, Depends, WebSocket
from routes import app_login

app = FastAPI()

app.include_router(app_login, prefix='/api')

