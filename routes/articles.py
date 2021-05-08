from fastapi import APIRouter, HTTPException
from database.mysql import execute_query
from starlette.status import HTTP_409_CONFLICT, HTTP_201_CREATED
from fastapi.responses import JSONResponse
from interfaces.article import *

app_article = APIRouter()

@app_article.post(
    path='/create',
    status_code=201,
    tags=['Article'],
    summary="Create article in SQL database"
)