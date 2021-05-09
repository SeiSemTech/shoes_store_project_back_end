from fastapi import APIRouter, HTTPException
from interface.actors import NormalUserRegister
from database.mysql import execute_query
from starlette.status import HTTP_409_CONFLICT, HTTP_201_CREATED
from fastapi.responses import JSONResponse

app_user = APIRouter()


@app_user.post(
    path='/create',
    status_code=201,
    tags=['Usuarios'],
    summary="Create user in SQL database"
)
async def create_users(request: NormalUserRegister):

    user = request.dict()

    email = execute_query(
        query_name='user_email.sql',
        fetch_data=True,
        **{'email': user['email']}
    )
    if not email:
        role = execute_query(
            query_name='role_get.sql',
            fetch_data=True,
            fetch_one=True,
            **{'role_type': 'Usuario Registrado'}
        )
        user['is_active'] = True
        user['role_id'] = role['role_id']

        execute_query(
            query_name='user_create.sql',
            fetch_data=False,
            **user
        )
        return JSONResponse({
            "status_code": HTTP_201_CREATED,
            "message": "User created successfully"
        })
    else:
        return HTTPException(HTTP_409_CONFLICT, detail='The user already exists')
