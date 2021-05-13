from pydantic import BaseModel


class ForgotPassword(BaseModel):
    email: str
    password: str
    code: str
