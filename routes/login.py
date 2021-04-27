from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import json
from fastapi import APIRouter
from interfaces.auth import LoginUser

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

app_login = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app_login.post(
    path='/login',
    status_code=200,
    tags=['Authentication'],
    summary="Authenticate user via email and password and validate if user is authorized",
    description="Login to via OAUTH2 service and query the database to validate users"
)
async def login(request: LoginUser):
    """
    Authenticate user via OAUTH2 and validate if user
    have access to the application.
    """
    print(json.dumps(request))
    return {
        "fancy_json": "Go on"
    }



