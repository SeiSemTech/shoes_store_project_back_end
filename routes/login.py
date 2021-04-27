from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

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

@app_login.get(
    path='/login',
    status_code=200,
    tags=['Authentication'],
    summary="Authenticate user via Google and validate if user is authorized",
    description="Login to google with OAUTH service and query the database to validate users"
)
async def login():
    """
    Authenticate user via Google and validate if user
    have access to the application.
    """
    return {
        "fancy_json": "Go on"
    }


@app_login.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    return{
        "fancy_json": "Go out"
    }