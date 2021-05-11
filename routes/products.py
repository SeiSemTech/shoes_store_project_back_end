from database.mysql import execute_query
from starlette.status import HTTP_404_NOT_FOUND

from interface.products import *
from fastapi import APIRouter, HTTPException, Depends
from internal.auth.auth_bearer import JWTBearer

app_product = APIRouter()


@app_product.post(
    path='/create_category',
    status_code=201,
    tags=['product'],
    summary="Create product in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def create_category(request: Category):
    execute_query("create_category.sql", False, **request.dict())
    return ""


@app_product.post(
    path='/create_product',
    status_code=201,
    tags=['Product'],
    summary="Create product in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def create_product(request: Product):
    execute_query("create_product.sql", False, **request.dict())
    return ""


@app_product.post(
    path='/create_configuration',
    status_code=201,
    tags=['Product'],
    summary="Create configuration in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def create_configuration(request: Configuration):
    execute_query("create_configuration.sql", False, **request.dict())
    return ""

#Función para traer todos los artículos del sistema // David
@app_product.get(
    path='/get_products',
    status_code=200,
    tags=['Product'],
    summary="Read products in SQL database",
    dependencies=[Depends(JWTBearer(['Usuario Registrado', 'Administrador']))]
)
async def get_all_products():
    data = execute_query(
        query_name="get_all_products.sql",
        fetch_data=True,
        #**request.dict()
    )

    if len(data) > 0:
        return {
            "products": data  # TODO RETURN TOKEN
        }
    else:
        return HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No products have been published"
        )

#Función para llamar un artículo en el sistema por el Id del mismo //David
@app_product.get(
path='/read',
status_code=200,
tags=['Product'],
summary="Read product by ID in SQL database"
)
async def getProductsXId(request: id):

    data = execute_query(
        query_name="get_products_by_id.sql",
        fetch_data=True,
        **request.dict()
    )

    if len(data) > 0:
        return {
            "products": data  # TODO RETURN TOKEN
        }
    else:
        return HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No products have been published"
        )