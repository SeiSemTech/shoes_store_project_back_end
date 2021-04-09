from fastapi import APIRouter, HTTPException


app_login = APIRouter()


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

