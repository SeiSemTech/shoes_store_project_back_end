from os import path
from database.mysql import execute_query
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_424_FAILED_DEPENDENCY
from interface.products import *
from fastapi import APIRouter, HTTPException, Depends
from internal.auth.auth_bearer import JWTBearer
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pymysql.err import IntegrityError

app_product = APIRouter()

#Method to create a category
@app_product.post(
    path='/create_category',
    status_code=201,
    tags=['Category'],
    summary="Create category in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def create_category(request: Category):

    category = request.dict()
    query_path = path.join("products", "get_categoryID_by_name.sql")
    category_id = execute_query(query_path, True, **category)
    #VALIDATE IF THE CATEGORY EXIST
    if category_id:
        query_path = path.join("products", "get_category_status_by_id.sql")
        status = execute_query(query_path, fetch_one=True, **category_id[0])
        #IF THE CATEGORY EXIST, THE STATUS IS VALIDATED TO CHANGE THE STATUS IN CASE IT IS DISABLED
        if status["status"] == 1:
            return HTTPException(HTTP_409_CONFLICT, detail='Already exist')
        #update status to enable if the category exist but it is disabled
        else:
            query_path = path.join("products", "update_category_status.sql")
            new_category = {"id": category_id[0]['id'], "status": 1}
            execute_query(query_path, False, **new_category)
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


@app_product.post(
    path='/create_configuration',
    status_code=201,
    tags=['Product'],
    summary="Create configuration in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def create_configuration(request: Configuration):

    query_path = path.join("products", "get_configurationID_by_name.sql")
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


@app_product.post(
    path='/create_product_configuration',
    status_code=201,
    tags=['Product'],
    summary="Create Product Configuration in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def create_product_configuration(request: ProductConfiguration):
    query_path = path.join("products", "create_product_configuration.sql")
    execute_query(query_path, False, **request.dict())
    response = jsonable_encoder({
        "message": "success"
        })

    #Return message
    return JSONResponse(content=response)


# Función para traer todos los artículos del sistema // David
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


# Función para traer todos los artículos del sistema // David
@app_product.get(
    path='/get_activated_products',
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
            "products": data  # TODO RETURN TOKEN
        }
    else:
        return HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No products have been published"
        )



# Función para llamar un artículo en el sistema por el Id del mismo //David
@app_product.get(
    path='/get_product_by_id/{product_id}',
    status_code=200,
    tags=['Product'],
    summary="Read product by ID in SQL database",
    dependencies=[Depends(JWTBearer(['Usuario Registrado', 'Administrador']))]
)
async def get_product_by_id(product_id: int):
    query_path = path.join("products", "get_product_by_id.sql")
    product_id_dict = {'id': product_id}

    data = execute_query(
        query_name=query_path,
        fetch_data=True,
        **product_id_dict
    )
    if len(data) > 0:
        return {
            "product": data  # TODO RETURN TOKEN
        }
    else:
        return HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No products have been published"
        )


# Función para traer todas las categorias del sistema
@app_product.get(
    path='/get_categories',
    status_code=200,
    tags=['Product'],
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

@app_product.post(
    path='/delete_category/{category_id}',
    status_code=201,
    tags=['Article'],
    summary="Delete category in SQL database"
)
async def delete_category(category_id: int):

    category_dict = {'id': category_id, 'status': 0}
    query_path = path.join("products", "update_category_status.sql")
    try:
        execute_query(query_path, False, **category_dict)
        response = jsonable_encoder({
            "message": "success"
        })
    except:
        return HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No categories have been found"
        )

    # Return message
    return JSONResponse(content=response)

@app_product.post(
    path='/delete_product/{product_id}',
    status_code=201,
    tags=['Article'],
    summary="Delete product in SQL database"
)
async def delete_product(product_id: int):
    query_path = path.join("products", "update_product_status.sql")
    product_dict = {'id': product_id, 'status': 0}
    try:
        execute_query(query_path, False, **product_dict)

        response = jsonable_encoder({
            "message": "success"
        })
    except:
        return HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No products have been found"
        )

    # Return message
    return JSONResponse(content=response)

@app_product.post(
    path='/delete_configuration/{configuration_id}',
    status_code=201,
    tags=['Article'],
    summary="Delete configuration in SQL database"
)
async def delete_configuration(configuration_id: int):
    query_path = path.join("products", "delete_configuration.sql")
    configuration_id_dict = {'id': configuration_id}

    try:
        execute_query(query_path, False, **configuration_id_dict)
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

    #Return message
    return JSONResponse(content=response)

@app_product.post(
    path='/delete_product_configuration/{product_configuration_id}',
    status_code=201,
    tags=['Article'],
    summary="Delete product configuration in SQL database"
)
async def delete_product_configuration(product_configuration_id: int):

    query_path = path.join("products", "delete_product_configuration.sql")
    product_configuration_id_dict = {'id': product_configuration_id}
    try:
        execute_query(query_path, False, **product_configuration_id_dict)
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

    # Return message
    return JSONResponse(content=response)
#
# INICIO FUNCIONES UPDATE GENERALES
#
#David - Función para actualizar PRODUCT

@app_product.post(
    path='/update_product',
    status_code=200,
    tags=['Product'],
    summary="Update product in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def update_product(request: Product):
    query_path = path.join("products", "update_product.sql")
    execute_query(query_path, False, **request.dict())
    return {"message": "Operation successful"}

# David - Función para actualizar CATEGORY

@app_product.post(
    path='/update_category',
    status_code=200,
    tags=['Product'],
    summary="Update category in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def update_category(request: Category):
    query_path = path.join("products", "update_category.sql")
    execute_query(query_path, False, **request.dict())
    return {"message": "Operation successful"}

#David - Función para actualizar CONFIGURATION

@app_product.post(
    path='/update_configuration',
    status_code=200,
    tags=['Product'],
    summary="Update configuration in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def update_configuration(request: Configuration):
    query_path = path.join("products", "update_configuration.sql")
    execute_query(query_path, False, **request.dict())
    return {"message": "Operation successful"}

#David - Función para actualizar PRODUCT_CONFIGURATION

@app_product.post(
    path='/update_product_configuration',
    status_code=200,
    tags=['Product'],
    summary="Update Product Configuration in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def update_product_configuration(request: ProductConfiguration):
    query_path = path.join("products", "update_product_configuration.sql")
    execute_query(query_path, False, **request.dict())
    return {"message": "Operation successful"}
#
# FIN FUNCIONES UPDATE GENERALES
#

#
# INICIO CONSULTAS CONFIGURATION Y PRODUCT_CONFIGURATION
#
# CONFIGURATION
#
# David - Función configuración por id
@app_product.get(
    path='/get_configuration_by_id/{configuration_id}',
    status_code=200,
    tags=['Configuration'],
    summary="Read configuration by ID in SQL database",
    dependencies=[Depends(JWTBearer(['Usuario Registrado', 'Administrador']))]
)
async def get_configuration_by_id(configuration_id: int):
    query_path = path.join("products", "get_configuration_by_id.sql")
    configuration_id_dict = {'id': configuration_id}

    data = execute_query(
        query_name=query_path,
        fetch_data=True,
        **configuration_id_dict
    )
    if len(data) > 0:
        return {
            "configuration": data  # TODO RETURN TOKEN
        }
    else:
        return HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No configurations have been published"
        )

# David - Función todas las configuraciones
@app_product.get(
    path='/get_all_configurations',
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

#
# PRODUCT_CONFIGURATION
#
# David- Función para traer un Product_Configuration por Id

@app_product.get(
    path='/get_product_configuration_by_id/{product_configuration_id}',
    status_code=200,
    tags=['Configuration'],
    summary="Read product configuration by ID in SQL database",
    dependencies=[Depends(JWTBearer(['Usuario Registrado', 'Administrador']))]
)
async def get_product_configuration_by_id(product_configuration_id: int):
    query_path = path.join("products", "get_product_configuration_by_id.sql")
    product_configuration_id_dict = {'id': product_configuration_id}

    data = execute_query(
        query_name=query_path,
        fetch_data=True,
        **product_configuration_id_dict
    )
    if len(data) > 0:
        return {
            "product_configuration": data  # TODO RETURN TOKEN
        }
    else:
        return HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No products configurations have been published"
        )

# David - Función todas las product_configurtions
@app_product.get(
    path='/get_all_product_configurations',
    status_code=200,
    tags=['Configuration'],
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
            "product_configurations": data  # TODO RETURN TOKEN
        }
    else:
        return HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No product configurations have been published"
        )

