from pydantic import BaseModel
from enum import Enum


class Roles(str, Enum):
    admin: str = "Administrador"
    user: str = "Usuario Registrado"
    visitor: str = "Usuario Anonimo"


class User(BaseModel):
    id: int
    email: str
    name: str
    last_name: str
    password: str
    phone: str
    is_active: str
    role: Roles
