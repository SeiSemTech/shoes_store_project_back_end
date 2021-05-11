from os import path
from database.mysql import execute_query
from starlette.status import HTTP_404_NOT_FOUND

from interface.articles import *
from fastapi import APIRouter, HTTPException, Depends
from internal.auth.auth_bearer import JWTBearer

app_article = APIRouter()


@app_article.post(
    path='/create_category',
    status_code=201,
    tags=['Article'],
    summary="Create article in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def create_category(request: Category):
    query_path = path.join("articles", "create_category.sql")
    execute_query(query_path, False, **request.dict())
    return ""


@app_article.post(
    path='/create_product',
    status_code=201,
    tags=['Article'],
    summary="Create product in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def create_product(request: Product):
    query_path = path.join("articles", "create_product.sql")
    execute_query(query_path, False, **request.dict())
    return ""


@app_article.post(
    path='/create_configuration',
    status_code=201,
    tags=['Article'],
    summary="Create configuration in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def create_configuration(request: Configuration):
    query_path = path.join("articles", "create_configuration.sql")
    execute_query(query_path, False, **request.dict())
    return ""


@app_article.post(
    path='/create_product_configuration',
    status_code=201,
    tags=['Article'],
    summary="Create product configuration in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def create_product_configuration(request: ProductConfiguration):
    execute_query("create_product_configuration.sql", False, **request.dict())
    return ""


# DELETE METHODS
@app_article.post(
    path='/delete_category',
    status_code=201,
    tags=['Article'],
    summary="Delete category in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def delete_category(request: Category):
    execute_query("disable_category.sql", False, **request.dict())
    return ""


@app_article.post(
    path='/delete_product',
    status_code=201,
    tags=['Article'],
    summary="Delete product in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def delete_product(request: Product):

    execute_query("disable_product.sql", False, **request.dict())
    return ""


@app_article.post(
    path='/delete_configuration',
    status_code=201,
    tags=['Article'],
    summary="Delete configuration in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def delete_configuration(request: Configuration):
    execute_query("delete_configuration.sql", False, **request.dict())
    return ""


@app_article.post(
    path='/delete_product_configuration',
    status_code=201,
    tags=['Article'],
    summary="Delete product configuration in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def delete_product_configuration(request: ProductConfiguration):
    execute_query("delete_product_configuration.sql", False, **request.dict())
    return ""


# LIST METHODS
@app_article.get(
    path='/get_articles',
    status_code=200,
    tags=['Article'],
    summary="Read articles in SQL database",
    dependencies=[Depends(JWTBearer(['Usuario Registrado', 'Administrador']))]
)
async def get_all_articles():
    query_path = path.join("articles", "get_article_by_id.sql")
    data = execute_query(
        query_name=query_path,
        fetch_data=True
    )

    if len(data) > 0:
        return {
            "articles": data
        }
    else:
        return HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No articles have been published"
        )

#Función para llamar un artículo en el sistema por el Id del mismo //David
@app_article.get(
path='/read',
status_code=200,
tags=['Article'],
summary="Read article by ID in SQL database"
)
async def getArticlesXId(request: ArticleId):

    data = execute_query(
        query_name="get_articles_by_id.sql",
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