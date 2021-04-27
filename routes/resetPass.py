from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    price: float


app_resetpass = APIRouter()


@app_resetpass.post("/resetpass")
async def resetpass(token, doc_usuario, password, item: Item):

    if not token:
        print("no token")
    return item
    return{
        "token": token,
        "doc_usuario": doc_usuario,
        "pass": password
        
    }