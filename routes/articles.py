from fastapi import APIRouter, HTTPException
from database.mysql import execute_query
from starlette.status import HTTP_409_CONFLICT, HTTP_201_CREATED
from fastapi.responses import JSONResponse
from interfaces.articles import Product

app_article = APIRouter()

@app_article.post(
    path='/create',
    status_code=201,
    tags=['Article'],
    summary="Create article in SQL database"
)




@app_article.get(
    path='/read',
    status_code=200,
    tags=['Article'],
    summary="Read articles in SQL database"
)
async def getAllArticles():

    data = execute_query(
        query_name="get_all_articles.sql",
        fetch_data=True,
        **request.dict()
    )

    if len(data) > 0:
        return {
            "articles": data  # TODO RETURN TOKEN
        }
    else:
        return HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No articles have been published"
        )

    return { data }