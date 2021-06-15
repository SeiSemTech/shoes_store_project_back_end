from fastapi import APIRouter
from starlette.status import HTTP_502_BAD_GATEWAY
from interface.location import *
from fastapi import HTTPException, Depends
from internal.auth.auth_bearer import JWTBearer
import requests


app_location = APIRouter()
URL = "https://seim-location.azurewebsites.net/location"

@app_location.post(
    path='/address',
    status_code=201,
    tags=['Location'],
    summary="Send address",
    dependencies=[Depends(JWTBearer(['Usuario Registrado', 'Administrador']))]
)

async def very_address(request: Location):
    try:
        response = requests.post(URL, json=request.dict())    
        return response.json()
    except:
        return HTTPException(HTTP_502_BAD_GATEWAY, detail='Bad Gateway')
    