from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from interface.actors import Roles
from typing import List

from internal.auth.auth_handler import decode_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, roles: List[Roles] = [], auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.roles = roles

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=401, detail="Not authorized.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwt_token: str) -> bool:
        is_valid_token: bool = False

        try:
            payload = decode_jwt(jwt_token)
            role = payload['role']
        except:
            payload = None
        if payload and (len(role) == 0 or role in self.roles):
            is_valid_token = True
        return is_valid_token

    @classmethod
    def get_role(cls, jwt_token: str) -> bool:
        try:
            payload = decode_jwt(jwt_token)
            role = payload['role']
        except:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")
        return role

    @classmethod
    def get_email(cls, jwt_token: str) -> bool:
        try:
            payload = decode_jwt(jwt_token)
            email = payload['user_id']
        except:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")
        return email
