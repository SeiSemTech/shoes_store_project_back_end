from fastapi import APIRouter
from os import path
from database.mysql import execute_query
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_424_FAILED_DEPENDENCY
from interface.products import *
from interface.bill import *
from fastapi import HTTPException, Depends
from internal.auth.auth_bearer import JWTBearer
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pymysql.err import IntegrityError

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

async def create_bill(request: List[BillFront], user_id : int):
    print("")
    # #Crear la factura
    # query_path = path.join("bill", "create_bill.sql")
    # execute_query(query_path, False, user_id) # los totales se hacen en el sql, en el chat de whatsapp jose explica como obtener el user id
    
    # #Traer ID de la factura, ordenado por fecha en orden descendente, se trae la fecha actual
    # query_path = path.join("bill", "select_bill.sql")

    # id_bill = execute_query(
    #    query_name=query_path,
    #    fetch_data=True,
    #    id=current_id
    # )
    # if len(id_bill) > 0:
    #    #Crear BillDescription, Validar si se puede enviar todo, restar en stock de Product_configuration
    #    total_quantity = 0
    #    total_price = 0
    #    for x in range(len(request)):
    #         product_configuration = request[x].dict()
               
    #         query_path = path.join("bill", "create_bill_description.sql")
    #         execute_query(query_path, True, id_bill, product_configuration) 
    #         #Validar como envian estos parametros
    #         total_quantity = total_quantity + product_configuration["stock"]
    #         total_price = total_price + product_configuration["price"]         
            
    #         #Update en stock del product configuration
    #         query_path = path.join("bill", "create_bill_description.sql")
    #         execute_query(query_path, False, product_configuration["product_id"], product_configuration["stock"]) 

    #     #Update Bill total (esperar por lo mismo de arriba)
    #     query_path = path.join("bill", "update_bill_total.sql")
    #     execute_query(query_path, False, id_bill, total_quantity, total_price) 

    #     return {
    #         "message" : "success" 
    #     }         
    # else:
    #     return HTTPException(
    #         status_code=HTTP_404_NOT_FOUND,
    #         detail="It was not found a bill"
    #     )


