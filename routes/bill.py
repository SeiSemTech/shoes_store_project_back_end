from fastapi import APIRouter
from os import path
from database.mysql import execute_query
from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_503_SERVICE_UNAVAILABLE
from interface.bill import BillCustomerOrder

from fastapi import HTTPException, Depends
from internal.auth.auth_bearer import JWTBearer
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pymysql.err import IntegrityError
from configurations.sengrid_configuration import EMAIL_CONFIGURATIONS
from utils.sendgrid import send_dynamic_email

app_bill = APIRouter()


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
