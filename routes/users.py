from os import path
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse


from configurations.sengrid_configuration import EMAIL_CONFIGURATIONS
from interface.actors import NormalUserRegister
from database.mysql import execute_query
from starlette.status import HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND
from internal.auth.auth_bearer import JWTBearer
from internal.password import create_password_grant
from utils.sendgrid import send_dynamic_email
from settings import PASSWORD_LINK

app_users = APIRouter()


# TODO IMPLEMENT PIPELINE QUERIES

@app_users.post(
    path='/create',
    status_code=201,
    tags=['Users'],
    summary="Create user in SQL database"
)
async def create_users(request: NormalUserRegister):
    query_path = path.join("users", "user_email.sql")
    user = request.dict()

    email = execute_query(
        query_name=query_path,
        fetch_data=True,
        email=user['email']
    )
    if not email:
        query_path = path.join("users", "role_get.sql")
        role = execute_query(
            query_name=query_path,
            fetch_one=True,
            role_type='Usuario Registrado'
        )
        user['is_active'] = True
        user['role_id'] = role['role_id']

        query_path = path.join("users", "user_create.sql")
        execute_query(
            query_name=query_path,
            fetch_data=False,
            **user
        )

        query_path = path.join("users", "user_id.sql")
        user_id = execute_query(
            query_name=query_path,
            fetch_one=True,
            email=user['email']
        )
        try:
            template = EMAIL_CONFIGURATIONS['welcome']
        except KeyError:
            return HTTPException(HTTP_404_NOT_FOUND, detail='The user already exists')

        grant_key = create_password_grant()
        query_path = path.join("password", "create_grant.sql")
        execute_query(
            query_name=query_path,
            user_id=user_id['user_id'],
            grant_key=grant_key
        )

        send_dynamic_email(user['email'], template, link=PASSWORD_LINK + grant_key)

        return JSONResponse(content={
            "status_code": HTTP_201_CREATED,
            "message": "User created successfully"
        })
    else:
        return HTTPException(HTTP_409_CONFLICT, detail='The user already exists')


@app_users.get(
    path='/role',
    status_code=HTTP_200_OK,
    tags=['Users'],
    summary="Reset password via authorized token"
)
async def get_role(token: str = Depends(JWTBearer(['Usuario Registrado', 'Administrador']))):
    """
    Validate in database if user exist and change password
    """
    return JSONResponse(content={'role': JWTBearer.get_role(token)})
