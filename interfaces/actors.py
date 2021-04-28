from pydantic import BaseModel
from enum import Enum


class Roles(str, Enum):
    admin: str = "Administrador"
    user: str = "Usuario Registrado"
    visitor: str = "Usuario Anonimo"


class User(BaseModel):
    user_id: int
    name: str
    email: str
    phone: str
    role_id: Roles
    is_active: bool


class NormalUserRegister(BaseModel):
    name: str
    email: str
    phone: str

