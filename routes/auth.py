from fastapi import APIRouter, HTTPException
from interfaces.auth import LoginUser
from database.mysql import execute_query
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND


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
    # TODO AUTHENTICATE VIA OAUTH
    data = execute_query(
        query_name="login.sql",
        fetch_data=True,
        **request.dict()
    )
    if len(data) > 0:
        return {
            "user": data  # TODO RETURN TOKEN
        }
    else:
        return HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="User not found or incorrect password"
        )


@app_auth.post(
    path='/reset_password',
    status_code=200,
    tags=['Authentication'],
    summary="Reset password via authorized token"
)
async def reset_password(request: LoginUser):

    data = execute_query("get_user_id_by_email.sql", True, **request.dict())
    execute_query("update_password.sql", False, **request.dict(), **data[0])

    return "success"



