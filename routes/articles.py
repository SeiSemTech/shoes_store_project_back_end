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
    execute_query("create_category.sql", False, **request.dict())
    return ""


@app_article.post(
    path='/create_product',
    status_code=201,
    tags=['Article'],
    summary="Create product in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def create_product(request: Product):
    execute_query("create_product.sql", False, **request.dict())
    return ""


@app_article.post(
    path='/create_configuration',
    status_code=201,
    tags=['Article'],
    summary="Create configuration in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def create_configuration(request: Configuration):
    execute_query("create_configuration.sql", False, **request.dict())
    return ""

#Función para traer todos los artículos del sistema // David
@app_article.get(
    path='/get_articles',
    status_code=200,
    tags=['Article'],
    summary="Read articles in SQL database",
    dependencies=[Depends(JWTBearer(['Usuario Registrado', 'Administrador']))]
)
async def get_all_articles():
    data = execute_query(
        query_name="get_all_articles.sql",
        fetch_data=True,
        #**request.dict()
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