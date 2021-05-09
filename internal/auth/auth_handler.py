import time
from typing import Dict
import jwt
from settings import JWT_EXPIRATION_MINUTES, JWT_SECRET_KEY, JWT_ALGORITHM


def sign_jwt(user_id: str, role: str) -> Dict[str, any]:
    payload = {
        "user_id": user_id,
        "role": role,
        "expires": time.time() + (int(JWT_EXPIRATION_MINUTES) * 60)
    }
    return {
        "access_token": jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    }


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
