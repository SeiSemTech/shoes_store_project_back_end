from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from interfaces.auth import LoginUser
from database.mysql import execute_query
app_resetpass = APIRouter()


@app_resetpass.post("/resetpass")
async def resetpass(current_user: LoginUser = Depends(get_current_user)):

    execute_query("update_password.sql",True,**current_user)
    
    return 
    