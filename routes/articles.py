from fastapi import APIRouter, HTTPException
from database.mysql import execute_query
from starlette.status import HTTP_409_CONFLICT, HTTP_201_CREATED
from fastapi.responses import JSONResponse
from interfaces.articles import *

app_article = APIRouter()

@app_article.post(
    path='/create_category',
    status_code=201,
    tags=['Article'],
    summary="Create article in SQL database"
)

async def create_category(request: Category):
    
    execute_query("create_category.sql", False, **request.dict())
    return ""

@app_article.post(
    path='/create_product',
    status_code=201,
    tags=['Article'],
    summary="Create product in SQL database"
)
async def create_product(request: Product):

    execute_query("create_product.sql", False, **request.dict())
    return ""

@app_article.post(
    path='/create_configuration',
    status_code=201,
    tags=['Article'],
    summary="Create configuration in SQL database"
)
async def create_configuration(request: Configuration):

    execute_query("create_configuration.sql", False, **request.dict())
    return ""

@app_article.post(
    path='/create_productConfiguration',
    status_code=201,
    tags=['Article'],
    summary="Create product configuration in SQL database"
)
async def create_ProductConfiguration(request: ProductConfiguration):

    execute_query("create_ProductConfiguration.sql", False, **request.dict())
    return ""

#DELETE METHODS 

@app_article.post(
    path='/delete_category',
    status_code=201,
    tags=['Article'],
    summary="Delete category in SQL database"
)

async def delete_catefory(request: Category):
    
    execute_query("disable_category.sql", False, **request.dict())
    return ""

@app_article.post(
    path='/delete_product',
    status_code=201,
    tags=['Article'],
    summary="Delete product in SQL database"
)

async def delete_product(request: Product):

    execute_query("disable_product.sql", False, **request.dict())
    return ""

@app_article.post(
    path='/delete_configuration',
    status_code=201,
    tags=['Article'],
    summary="Delete configuration in SQL database"
)
async def delete_configuration(request: Configuration):

    execute_query("delete_configuration.sql", False, **request.dict())
    return ""

@app_article.post(
    path='/delete_productConfiguration',
    status_code=201,
    tags=['Article'],
    summary="Delete product configuration in SQL database"
)
async def delete_ProductConfiguration(request: ProductConfiguration):

    execute_query("delete_ProductConfiguration.sql", False, **request.dict())
    return ""





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