from fastapi import APIRouter
from os import path
from database.mysql import execute_query
from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_503_SERVICE_UNAVAILABLE
from interface.bill import BillCustomerOrder

from starlette.status import HTTP_404_NOT_FOUND, HTTP_200_OK
from interface.products import *
from interface.bill import *
from fastapi import HTTPException, Depends
from internal.auth.auth_bearer import JWTBearer
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pymysql.err import IntegrityError
from configurations.sengrid_configuration import EMAIL_CONFIGURATIONS
from utils.sendgrid import send_dynamic_email

from typing import List
from fastapi import FastAPI, Query


app_bill = APIRouter()



#Method to create a bill, bill_description, and update the product configuration stock
@app_bill.post(
    path='/bill',
    status_code=200,
    tags=['Bill'],
    summary="Create a bill"
)
async def create_bill(request: List[BillFront], token : str = Depends(JWTBearer(['Usuario Registrado', 'Administrador']))):
    print("")
    #Crear la factura
    #
    #Traer id del usuario x el Email
    email = JWTBearer.get_email(token)
    query_path = path.join("auth", "get_user_id_by_email.sql")# TODO 
    user_id = execute_query(
        query_name=query_path,
        fetch_data=True,
        email = email
    )
    query_path = path.join("bill", "create_bill.sql")# TODO 
    execute_query(query_path, False, user_id) # los totales se hacen en el sql, en el chat de whatsapp jose explica como obtener el user id
    
    #Traer ID de la factura, ordenado por fecha en orden descendente, se trae la fecha actual
    query_path = path.join("bill", "select_bill.sql")# TODO 
    id_bill = execute_query(
        query_name=query_path,
        fetch_data=True,
        user_id = user_id
    )
    if len(id_bill) > 0:
       #Crear BillDescription, Validar si se puede enviar todo, restar en stock de Product_configuration
        total_quantity = 0
        total_price = 0
        for x in range(len(request)):
            product_configuration = request[x].dict()
               
            query_path = path.join("bill", "create_bill_description.sql")# TODO 
            execute_query(query_path, True, id_bill, product_configuration) 
            #Validar como envian estos parametros
            total_quantity = total_quantity + product_configuration["stock"]
            total_price = total_price + product_configuration["price"]         
            
            #Update en stock del product configuration
            query_path = path.join("bill", "update_product_configuration_stock.sql") # TODO 
            execute_query(query_path, False, product_configuration["product_id"], product_configuration["stock"]) 
            #
            #Falta consultar el stock actual para restarlo a la compra
            #(Se va a padir al fron que no pasen cuánto compraron, si no, lo que queda)

        #Update Bill total (esperar por lo mismo de arriba)
        query_path = path.join("bill", "update_bill_total.sql") # TODO 
        execute_query(query_path, False, id_bill, total_quantity, total_price) 
        ##
        ## Método para enviar e-mail de confirmación de compra
        ##

        query_path = path.join("users", "get_user_email_by_id.sql") # TODO 
        email = execute_query(
            query_name=query_path,
            fetch_data=True,
            user_id = user_id
        )
        try:
            template = EMAIL_CONFIGURATIONS['bill_created']
        except KeyError:
            return HTTPException(HTTP_404_NOT_FOUND, detail='The bill already exists')

        grant_key = create_password_grant()
        send_dynamic_email(email, template, link=PASSWORD_LINK + grant_key)
        return HTTPException(
            status_code=HTTP_200_OK,
            detail="The bill has created success"
        )
    else:
        return HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="It was not found a bill"
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
