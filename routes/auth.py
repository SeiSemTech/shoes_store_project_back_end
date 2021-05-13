from os import path
from fastapi import APIRouter, HTTPException
from interface.auth import LoginUser
from database.mysql import execute_query
from starlette.status import HTTP_404_NOT_FOUND
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


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
    query_path = path.join("auth", "login.sql")
    data = execute_query(
        query_name=query_path,
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
