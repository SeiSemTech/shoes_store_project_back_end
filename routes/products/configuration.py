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


app_configuration = APIRouter()


@app_configuration.post(
    path='/configuration',
    status_code=201,
    tags=['Configuration'],
    summary="Create configuration in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def create_configuration(request: Configuration):
    query_path = path.join("products", "product", "configuration", "get_configuration_id_by_name.sql")
    configuration_id = execute_query(query_path, True, **request.dict())

    # VALIDATE IF THE CONFIGURATION EXIST
    if len(configuration_id) > 0:
        return HTTPException(HTTP_409_CONFLICT, detail='Already exist')

    # IF THE CATEGORY DOES NOT EXIST, IT IS CREATED
    else:
        query_path = path.join("products", "create_configuration.sql")
        execute_query(query_path, False, **request.dict())
        response = jsonable_encoder({
            "message": "success"
        })

    # Return message
    return JSONResponse(content=response)


@app_configuration.delete(
    path='/configuration/{current_id}',
    status_code=201,
    tags=['Configuration'],
    summary="Delete configuration in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def delete_configuration(current_id: int):

    query_path = path.join("products", "delete_configuration.sql")
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


@app_configuration.patch(
    path='/configuration',
    status_code=200,
    tags=['Configuration'],
    summary="Update configuration in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def update_configuration(request: Configuration):
    query_path = path.join("products", "update_configuration.sql")
    execute_query(query_path, False, **request.dict())
    return {"message": "Operation successful"}


@app_configuration.patch(
    path='/configuration',
    status_code=200,
    tags=['Configuration'],
    summary="Update Product Configuration in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def update_product_configuration(request: Product):
    query_path = path.join("products", "update_product_configuration.sql")
    execute_query(query_path, False, **request.dict())
    return {"message": "Operation successful"}


@app_configuration.get(
    path='/configuration/{current_id}',
    status_code=200,
    tags=['Configuration'],
    summary="Read configuration by ID in SQL database",
    dependencies=[Depends(JWTBearer(['Usuario Registrado', 'Administrador']))]
)
async def get_configuration_by_id(current_id: int):
    query_path = path.join("products", "get_configuration_by_id.sql")

    data = execute_query(
        query_name=query_path,
        fetch_data=True,
        id=current_id
    )
    if len(data) > 0:
        return {
            "configuration": data
        }
    else:
        return HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No configurations have been published"
        )

@app_configuration.get(
    path='/configurations',
    status_code=200,
    tags=['Configuration'],
    summary="Read configurations in SQL database",
    dependencies=[Depends(JWTBearer(['Usuario Registrado', 'Administrador']))]
)
async def get_all_configurations():
    query_path = path.join("products", "get_all_configurations.sql")
    data = execute_query(
        query_name=query_path,
        fetch_data=True
    )

    if len(data) > 0:
        return {
            "configurations": data  # TODO RETURN TOKEN
        }
    else:
        return HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No configurations have been published"
        )
