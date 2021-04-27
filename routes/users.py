from fastapi import APIRouter, HTTPException
from interfaces.actors import User
from database.mysql import sql_conn

app_user = APIRouter()


@app_user.post(
    path='/create',
    status_code=200,
    tags=['Usuarios'],
    summary="",
    description=""
)
async def create_users(request: User):
    """
    """
    email = request.body['email']


    return {
        "fancy_json": "Go on"
    }
