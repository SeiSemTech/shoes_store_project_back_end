from fastapi import APIRouter, HTTPException
from interfaces.actors import User
from database.mysql import execute_query

app_user = APIRouter()


@app_user.post(
    path='/create',
    status_code=200,
    tags=['Usuarios'],
    summary="Create user in SQL database"
)
async def create_users(request: User):
    execute_query('user_create.sql', False, **request)

    return {
        "result": "El usuario fue creado con exito"
    }
