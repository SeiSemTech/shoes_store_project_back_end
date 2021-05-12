from fastapi import APIRouter
from os import path
from database.mysql import execute_query
from starlette.status import HTTP_404_NOT_FOUND, HTTP_424_FAILED_DEPENDENCY
from pymysql.err import IntegrityError
from interface.products import *
from fastapi import HTTPException, Depends
from internal.auth.auth_bearer import JWTBearer
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


app_product_configuration = APIRouter()


@app_product_configuration.post(
    path='/product_configuration',
    status_code=201,
    tags=['Product Configuration'],
    summary="Create Product Configuration in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def product_configuration(request: ProductConfiguration):
    query_path = path.join("products", "create_product_configuration.sql")
    execute_query(query_path, False, **request.dict())
    response = jsonable_encoder({
        "message": "success"
    })

    return JSONResponse(content=response)


@app_product_configuration.get(
    path='/product_configuration/{current_id}',
    status_code=200,
    tags=['Product Configuration'],
    summary="Read product configuration by ID in SQL database",
    dependencies=[Depends(JWTBearer(['Usuario Registrado', 'Administrador']))]
)
async def get_product_configuration_by_id(current_id: int):
    query_path = path.join("products", "get_product_configuration_by_id.sql")

    data = execute_query(
        query_name=query_path,
        fetch_data=True,
        id=current_id
    )
    if len(data) > 0:
        return {
            "product_configuration": data
        }
    else:
        return HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No products configurations have been published"
        )


@app_product_configuration.delete(
    path='/product_configuration/{current_id}',
    status_code=201,
    tags=['Product Configuration'],
    summary="Delete product configuration in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def delete_product_configuration(current_id: int):
    query_path = path.join("products", "delete_product_configuration.sql")
    try:
        execute_query(query_path, False, id=current_id)
        response = jsonable_encoder({
            "message": "success"
        })
    except IntegrityError:
        return HTTPException(
            status_code=HTTP_424_FAILED_DEPENDENCY,
            detail="Database error, probably foreing key dependency error"
        )
    except:
        return HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No products have been found"
        )
    return JSONResponse(content=response)


@app_product_configuration.get(
    path='/product_configurations',
    status_code=200,
    tags=['Product Configuration'],
    summary="Read product configurations in SQL database",
    dependencies=[Depends(JWTBearer(['Usuario Registrado', 'Administrador']))]
)
async def get_all_product_configurations():
    query_path = path.join("products", "get_all_product_configurations.sql")
    data = execute_query(
        query_name=query_path,
        fetch_data=True
    )

    if len(data) > 0:
        return {
            "product_configurations": data
        }
    else:
        return HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No product configurations have been published"
        )

@app_product_configuration.patch(
    path='/product_configuration',
    status_code=200,
    tags=['Product Configuration'],
    summary="Update Product Configuration in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def update_product_configuration(request: Product):
    query_path = path.join("products", "update_product_configuration.sql")
    execute_query(query_path, False, **request.dict())
    return {"message": "Operation successful"}