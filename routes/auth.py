from fastapi import APIRouter, HTTPException, Depends
from interface.auth import LoginUser
from database.mysql import execute_query
from starlette.status import HTTP_404_NOT_FOUND, HTTP_200_OK
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from internal.auth.auth_bearer import JWTBearer
from internal.auth.auth_handler import sign_jwt

app_auth = APIRouter()


@app_auth.post(
    path='/login',
    status_code=201,
    tags=['Authentication'],
    summary="Authenticate user via email and password and validate if user is authorized"
)
async def login(request: LoginUser):
    """
    Authenticate user via OAUTH2 and validate if user
    have access to the application.
    """
    data = execute_query(
        query_name="login.sql",
        fetch_one=True,
        **request.dict()
    )
    if data:
        token = sign_jwt(data['email'], data['role_type'])
        response = jsonable_encoder({
            "token": token
        })
        return JSONResponse(content=response)
    else:
        return HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="User not found or incorrect password"
        )


@app_auth.post(
    path='/reset_password',
    status_code=HTTP_200_OK,
    tags=['Authentication'],
    summary="Reset password via authorized token",
    dependencies=[Depends(JWTBearer(['Usuario Registrado', 'Administrador']))]
)
async def reset_password(request: LoginUser):
    """
    Validate in database if user exist and change password
    """
    data = execute_query("get_user_id_by_email.sql", fetch_one=True, **request.dict())
    execute_query("update_password.sql", **request.dict(), **data)

    response = jsonable_encoder({
        "message": "password_reset"
    })
    return JSONResponse(content=response)
