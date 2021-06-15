from fastapi import APIRouter
from os import path
from database.mysql import execute_query
from starlette.status import HTTP_503_SERVICE_UNAVAILABLE
from starlette.status import HTTP_404_NOT_FOUND, HTTP_200_OK
from interface.bill import *
from fastapi import HTTPException, Depends
from internal.auth.auth_bearer import JWTBearer
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from configurations.sengrid_configuration import EMAIL_CONFIGURATIONS
from utils.sendgrid import send_dynamic_email

from typing import List


app_bill = APIRouter()


# Función para traer todas las categorias del sistema
@app_bill.get(
    path='/description',
    status_code=200,
    tags=['Bill'],
    summary="Get all get categories in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def get_all_bill_description():
    query_path = path.join("bill", "get_all_bill_description.sql")
    data = execute_query(
        query_name=query_path,
        fetch_data=True
    )

    if len(data) > 0:
        return {
            "bill_description": data
        }
    else:
        return HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No bill descriptions have been published"
        )


#Method to create a bill, bill_description, and update the product configuration stock
@app_bill.post(
    path='',
    status_code=200,
    tags=['Bill'],
    summary="Create a bill"
)
async def create_bill(request: List[BillFront], token : str = Depends(JWTBearer(['Usuario Registrado', 'Administrador']))):
    email = JWTBearer.get_email(token)
    query_path = path.join("users", "user_id.sql")
    user_id = execute_query(
        query_name=query_path,
        fetch_one=True,
        email=email
    )['user_id']
    query_path = path.join("bill", "create_bill.sql")
    execute_query(query_path, id_user=user_id, total_quantity=0, total_price=0)
    
    #Traer ID de la factura, ordenado por fecha en orden descendente, se trae la fecha actual
    query_path = path.join("bill", "select_bill.sql")
    id_bill = execute_query(
        query_name=query_path,
        fetch_one=True,
        id_user=user_id
    )['id']
    if id_bill:
       # Crear BillDescription, Validar si se puede enviar todo, restar en stock de Product_configuration
        total_quantity = 0
        total_price = 0
        for x in range(len(request)):
            product_configuration = request[x].dict()
            query_path = path.join("bill", "create_bill_description.sql")
            execute_query(query_path, True, id_bill=id_bill, **product_configuration)

            total_quantity += product_configuration["quantity"]
            total_price += product_configuration["price"]

            query_path = path.join("products", "update_product_configuration_stock.sql")
            execute_query(query_path, False, id=product_configuration["id_product_config"], stock=product_configuration["quantity"])

        query_path = path.join("bill", "update_bill_total.sql")
        execute_query(query_path, False, id_bill=id_bill, total_quantity=total_quantity, total_price=total_price)

        return HTTPException(
            status_code=HTTP_200_OK,
            detail="The bill has created success"
        )
    else:
        return HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="It was not found a bill"
        )


#Method to create a bill, bill_description, and update the product configuration stock
@app_bill.get(
    path='/user',
    status_code=200,
    tags=['Bill'],
    summary="Create a bill"
)
async def get_bills_by_user_id(token : str = Depends(JWTBearer(['Usuario Registrado', 'Administrador']))):
    email = JWTBearer.get_email(token)
    query_path = path.join("users", "user_id.sql")
    user_id = execute_query(
        query_name=query_path,
        fetch_one=True,
        email=email
    )['user_id']

    query_path = path.join("bill", "get_history_bill_by_user_id.sql")
    data = execute_query(
        query_name=query_path,
        fetch_data=True,
        id_user=user_id
    )

    if len(data) > 0:
        return {
            "bill_description": data
        }
    else:
        return HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No bill descriptions have been published for this user"
        )


##
## Método para enviar e-mail del histórico de la compra
##1

# #Method to create a bill, bill_description, and update the product configuration stock
# @app_bill.get(
#     path='/bill',
#     status_code=200,
#     tags=['Bill'],
#     summary="Send a Email whit History bills"
# )
# async def send_email_history_bill(user_id : int):
#
#         #
#         # Traer el user_id
#         #
#         query_path = path.join("users", "get_user_email_by_id.sql") # TODO
#         email = execute_query(
#             query_name=query_path,
#             fetch_data=True,
#             user_id = user_id
#         )
#
#         query_path = path.join("users", "get_history_bill_by_user_id.sql") # TODO
#         data = execute_query(
#             query_name=query_path,
#             fetch_data=True,
#             user_id = user_id
#         )
#         try:
#             template = EMAIL_CONFIGURATIONS['bill_history']
#         except KeyError:
#             return HTTPException(HTTP_404_NOT_FOUND, detail='Not have found')
#
#         grant_key = create_password_grant()
#         send_dynamic_email(email, template, link=PASSWORD_LINK + grant_key)
#
#         return HTTPException(
#             status_code=HTTP_200_OK,
#             detail="The email has send success"
#         )
#

@app_bill.post(
    path='/send_email',
    status_code=201,
    tags=['Bill'],
    summary="Send products purchased to customer email"
)
async def send_bill_email(request: BillCustomerOrder, token: str = Depends(JWTBearer(['Usuario Registrado', 'Administrador']))):
    try:
        template = EMAIL_CONFIGURATIONS['bill']
        email = JWTBearer.get_email(token)

        order_dict = request.dict()
        send_dynamic_email(email, template, order=order_dict['order'])
        response = jsonable_encoder({
            "message": "Se ha enviado con exito la factura al correo"
        })
        return JSONResponse(content=response)
    except KeyError:
        return HTTPException(HTTP_404_NOT_FOUND, detail='Configuration key not found')
    except:
        return HTTPException(
            status_code=HTTP_503_SERVICE_UNAVAILABLE,
            detail="Problem with email provider"
        )

@app_bill.patch(
    path='/update_bill_status',
    status_code=200,
    tags=['Bill'],
    summary="Update Bill Status in SQL database",
    dependencies=[Depends(JWTBearer(['Administrador']))]
)
async def update_bill_satus(request: BillUpdateStatus ):
    query_path = path.join("products", "update_bill_satus.sql")
    execute_query(query_path, False, **request.dict())
    return HTTPException(
        status_code=HTTP_200_OK,
        detail="The bill has updated success"
    )