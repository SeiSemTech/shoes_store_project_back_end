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


app_category = APIRouter()


# Method to create a category
@app_category.post(
    path='/category',
    status_code=201,
    tags=['Categories'],
    summary="Create category in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def create_category(request: Category):
    category = request.dict()
    query_path = path.join("products", "get_categoryID_by_name.sql")
    category_id = execute_query(query_path, True, **category)
    # VALIDATE IF THE CATEGORY EXIST
    if category_id:
        query_path = path.join("products", "get_category_status_by_id.sql")
        status = execute_query(query_path, fetch_one=True, **category_id[0])
        # IF THE CATEGORY EXIST, THE STATUS IS VALIDATED TO CHANGE THE STATUS IN CASE IT IS DISABLED
        if status["status"] == 1:
            return HTTPException(HTTP_409_CONFLICT, detail='Already exist')
        # update status to enable if the category exist but it is disabled
        else:
            query_path = path.join("products", "update_category_status.sql")
            new_category = {"id": category_id[0]['id'], "status": 1}
            execute_query(query_path, False, **new_category)
            response = jsonable_encoder({
                "message": "Re-activated"
            })

    # IF THE CATEGORY DOES NOT EXIST, IT IS CREATED
    else:
        query_path = path.join("products", "create_category.sql")
        execute_query(query_path, False, **request.dict())
        response = jsonable_encoder({
            "message": "success"
        })

    # Return message
    return JSONResponse(content=response)


# Función para traer todas las categorias del sistema
@app_category.get(
    path='/categories',
    status_code=200,
    tags=['Categories'],
    summary="Read categories in SQL database",
    dependencies=[Depends(JWTBearer(['Usuario Registrado', 'Administrador']))]
)
async def get_all_categories():
    query_path = path.join("products", "get_all_categories.sql")
    data = execute_query(
        query_name=query_path,
        fetch_data=True
    )

    if len(data) > 0:
        return {
            "categories": data  # TODO RETURN TOKEN
        }
    else:
        return HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No categories have been published"
        )


#DELETE METHODS
@app_category.delete(
    path='/category/{current_id}',
    status_code=201,
    tags=['Categories'],
    summary="Delete category in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def delete_category(current_id: int):
    query_path = path.join("products", "update_category_status.sql")
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



@app_category.patch(
    path='/category',
    status_code=200,
    tags=['Categories'],
    summary="Update category in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def update_category(request: Category):
    query_path = path.join("products", "update_category.sql")
    execute_query(query_path, False, **request.dict())
    return {"message": "Operation successful"}
