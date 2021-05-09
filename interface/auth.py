from pydantic import BaseModel


class LoginUser(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str


class Payload(BaseModel):
    email: str
    role: str
    expires: float
