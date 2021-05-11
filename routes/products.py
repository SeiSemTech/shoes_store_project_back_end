from os import path
from database.mysql import execute_query
from starlette.status import HTTP_404_NOT_FOUND

from interface.products import *
from fastapi import APIRouter, HTTPException, Depends
from internal.auth.auth_bearer import JWTBearer
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

app_product = APIRouter()


@app_product.post(
    path='/create_category',
    status_code=201,
    tags=['product'],
    summary="Create product in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def create_category(request: Category):

    query_path = path.join("products", "get_categoryID_by_name.sql")
    category_id = execute_query(query_path, True, **request.dict())
    #VALIDATE IF THE CATEGORY EXIST
    if len(category_id) > 0:
        query_path = path.join("products", "get_category_status_by_id.sql")
        status=execute_query(query_path, True, **category_id)
        #IF THE CATEGORY EXIST, THE STATUS IS VALIDATED TO CHANGE THE STATUS IN CASE IT IS DISABLED
        if status[0] == "enabled":
            response = jsonable_encoder({
            "message": "already exist"
            })
        #update status to enable if the category exist but it is disabled
        else:
            query_path = path.join("products", "update_category_satatus.sql")
            execute_query(query_path, False, **request.dict())
            response = jsonable_encoder({
                "message": "Re-activated"
            })
            
    #IF THE CATEGORY DOES NOT EXIST, IT IS CREATED
    else:
        query_path = path.join("products", "create_category.sql")
        execute_query(query_path, False, **request.dict())
        response = jsonable_encoder({
                "message": "success"
            })

    #Return message
    return JSONResponse(content=response)
    


@app_product.post(
    path='/create_product',
    status_code=201,
    tags=['Product'],
    summary="Create product in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def create_product(request: Product):

    query_path = path.join("products", "get_productID_by_name.sql")
    product_id = execute_query(query_path, True, **request.dict())

    if len(product_id) > 0:
        query_path = path.join("products", "get_product_status_by_id.sql")
        status=execute_query(query_path, True, **category_id)
        #IF THE PRODUCT EXIST, THE STATUS IS VALIDATED TO CHANGE THE STATUS IN CASE IT IS DISABLED
        if status[0] == "enabled":
            response = jsonable_encoder({
            "message": "already exist"
            })
        #update status to enable if the category exist but it is disabled
        else:
            query_path = path.join("products", "update_product_satatus.sql")
            execute_query(query_path, False, **request.dict())
            response = jsonable_encoder({
                "message": "Re-activated"
            })
            
    #IF THE CATEGORY DOES NOT EXIST, IT IS CREATED
    else:
        query_path = path.join("products", "create_product.sql")
        execute_query(query_path, False, **request.dict())
        response = jsonable_encoder({
                "message": "success"
            })

    #Return message
    return JSONResponse(content=response)




@app_product.post(
    path='/create_configuration',
    status_code=201,
    tags=['Product'],
    summary="Create configuration in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def create_configuration(request: Configuration):
    query_path = path.join("products", "create_configuration.sql")
    execute_query(query_path, False, **request.dict())
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
    query_path = path.join("products", "get_all_products.sql")
    data = execute_query(
        query_name=query_path,
        fetch_data=True
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
    summary="Read product by ID in SQL database",
    dependencies=[Depends(JWTBearer(['Usuario Registrado', 'Administrador']))]
)
async def get_products_by_id(request: int):
    query_path = path.join("products", "get_products_by_id.sql")

    data = execute_query(
        query_name=query_path,
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