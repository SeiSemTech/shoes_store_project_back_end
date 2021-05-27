from os import path
from datetime import datetime
from fastapi import APIRouter, HTTPException
from configurations.sengrid_configuration import EMAIL_CONFIGURATIONS
from internal.password import create_password_grant
from settings import PASSWORD_LINK
from utils.sendgrid import send_dynamic_email
from interface.password import ForgotPassword
from database.mysql import execute_query
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


app_password = APIRouter()


@app_password.get(
    path='/password/{email}',
    status_code=HTTP_200_OK,
    tags=['Password'],
    summary="Reset password via authorized token"
)
async def get_password(email: str):
    """
    Validate in database if user exist and change password
    """
    try:
        template = EMAIL_CONFIGURATIONS['forgot']
    except KeyError:
        return HTTPException(HTTP_404_NOT_FOUND, detail='Configuration key not found')

    query_path = path.join("users", "user_id.sql")
    user_id = execute_query(
        query_name=query_path,
        fetch_one=True,
        email=email
    )

    grant_key = create_password_grant()
    query_path = path.join("password", "create_grant.sql")
    execute_query(
        query_name=query_path,
        user_id=user_id['user_id'],
        grant_key=grant_key
    )

    send_dynamic_email(email, template, link=PASSWORD_LINK + grant_key)

    response = jsonable_encoder({
        "message": "Se han enviado instrucciones para restablecer tu contraseña."
    })
    return JSONResponse(content=response)


@app_password.post(
    path='/password',
    status_code=HTTP_200_OK,
    tags=['Password'],
    summary="Reset password via authorized token"
)
async def reset_password(request: ForgotPassword):
    """
    Validate in database if user exist and change password
    """
    query_path = path.join("users", "user_id.sql")
    user_id = execute_query(
        query_name=query_path,
        fetch_one=True,
        email=request.email
    )

    query_path = path.join("password", "get_grant.sql")
    grant = execute_query(
        query_name=query_path,
        fetch_one=True,
        user_id=user_id['user_id']
    )

    current_date = datetime.utcnow()
    if current_date < grant['expire_at'] and grant['grant_key'] == request.code:
        query_path = path.join("password", "update.sql")
        execute_query(query_path, user_id=user_id['user_id'], password=request.password)

        response = jsonable_encoder({
            "message": "Contraseña restablecida correctamente"
        })
        return JSONResponse(content=response)
    else:
        return HTTPException(HTTP_401_UNAUTHORIZED, detail='El codigo expiro o no es correcto')
