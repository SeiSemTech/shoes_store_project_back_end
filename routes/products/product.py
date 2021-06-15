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

from typing import List
app_product = APIRouter()


@app_product.post(
    path='/product',
    status_code=201,
    tags=['Product'],
    summary="Create product in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def create_product(request: Product):
    query_path = path.join("products", "get_product_id_by_name.sql")
    product_id = execute_query(query_path, True, **request.dict())

    if len(product_id) > 0:
        query_path = path.join("products", "get_product_status_by_id.sql")
        status = execute_query(query_path, fetch_one=True, **product_id[0])
        # IF THE PRODUCT EXIST, THE STATUS IS VALIDATED TO CHANGE THE STATUS IN CASE IT IS DISABLED
        if status["status"] == 1:
            return HTTPException(HTTP_409_CONFLICT, detail='Already exist')
        # Update status to enable if the category exist but it is disabled
        else:
            new_product = {"id": product_id[0]['id'], "status": 1}
            query_path = path.join("products", "update_product_status.sql")
            execute_query(query_path, False, **new_product)
            response = jsonable_encoder({
                "message": "Re-activated"
            })

    # IF THE CATEGORY DOES NOT EXIST, IT IS CREATED
    else:
        query_path = path.join("products", "create_product.sql")
        execute_query(query_path, False, **request.dict())
        response = jsonable_encoder({
            "message": "success"
        })
    # Return message
    return JSONResponse(content=response)


@app_product.get(
    path='/products',
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
            "products": data
        }
    else:
        return HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No products have been published"
        )


@app_product.get(
    path='/activated_products',
    status_code=200,
    tags=['Product'],
    summary="Read products in SQL database",
    dependencies=[Depends(JWTBearer(['Usuario Registrado', 'Administrador']))]
)
async def get_all_products():
    query_path = path.join("products", "get_all_activated_products.sql")
    data = execute_query(
        query_name=query_path,
        fetch_data=True
    )

    if len(data) > 0:
        return {
            "products": data
        }
    else:
        return HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No products have been published"
        )


@app_product.get(
    path='/product/{current_id}',
    status_code=200,
    tags=['Product'],
    summary="Read product by ID in SQL database",
    dependencies=[Depends(JWTBearer(['Usuario Registrado', 'Administrador']))]
)
async def get_product_by_id(current_id: int):
    query_path = path.join("products", "get_product_by_id.sql")

    data = execute_query(
        query_name=query_path,
        fetch_data=True,
        id=current_id
    )
    if len(data) > 0:
        return {
            "product": data
        }
    else:
        return HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No products have been published"
        )


@app_product.delete(
    path='/product/{current_id}',
    status_code=201,
    tags=['Product'],
    summary="Deactivate product in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def delete_product(current_id: int):
    query_path = path.join("products", "update_product_status.sql")
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


@app_product.delete(
    path='/product/force_delete/{current_id}',
    status_code=201,
    tags=['Product'],
    summary="Delete product in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def delete_product(current_id: int):
    query_path = path.join("products", "product", "delete_product.sql")
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


@app_product.patch(
    path='/update',
    status_code=200,
    tags=['Product'],
    summary="Update product in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def update_product(request: Product):
    query_path = path.join("products", "update_product.sql")
    execute_query(query_path, False, **request.dict())
    return {"message": "Operation successful"}


@app_product.get(
    path='/activated_all_products',
    status_code=200,
    tags=['Product'],
    summary="Read products in SQL database",
    dependencies=[Depends(JWTBearer(['Usuario Registrado', 'Administrador']))]
)
async def get_all_products():
     
    query_path = path.join("products", "get_all_activated_categories.sql")
    categories = execute_query(
        query_name=query_path,
        fetch_data=True
    )

    if len(categories) > 0:

        for categories_index in range(len(categories)):
            query_path = path.join("products", "get_all_activated_products_by_category_id.sql")
            products = execute_query(
                query_name=query_path,
                fetch_data=True,
                category_id=categories[categories_index]['id']
            )
            categories[categories_index]["products"] = products
            for product_index in range(len(products)):
                query_path = path.join("products", "get_all_activated_products_configurations.sql")
                products_configuration = execute_query(
                    query_name=query_path,
                    fetch_data=True,
                    product_id=products[product_index]['id']
                )
                categories[categories_index]["products"][product_index]["configurations"] = products_configuration
        return {
            "categories": categories
        }
        
    else:
        return HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No products have been published"
        )
