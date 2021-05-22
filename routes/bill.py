from fastapi import APIRouter
from os import path
from database.mysql import execute_query
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_424_FAILED_DEPENDENCY
from interface.products import *
from fastapi import HTTPException, Depends
from internal.auth.auth_bearer import JWTBearer
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pymysql.err import IntegrityError

app_bill = APIRouter()