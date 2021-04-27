import jwt
import datetime
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

pwd_context = CryptContext(schemes=["bcrypt"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# Create Access JWT Token
def create_jwt_token(user: User, google_token):
    current_time = datetime.datetime.utcnow()
    expiration_time = current_time + datetime.timedelta(minutes=JWT_EXPIRATION_MINUTES)
    jwt_payload = {"sub": user['email'],
                   "iat": current_time.timestamp(),
                   "exp": expiration_time.timestamp(),
                   'gt': google_token}
    jwt_token = jwt.encode(jwt_payload, JWT_SECRET_KEY, JWT_ALGORITHM)
    return {'access_token': jwt_token,
            'token_type': "bearer"}


# Check whether JWT token is correct
async def check_jwt_token(token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    try:
        jwt_payload = jwt.decode(token.credentials, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
        username = jwt_payload.get("sub")
        expiration = jwt_payload.get("exp")
        is_valid = await db_get_user(username)
        if time.time() < expiration and bool(is_valid):
            return True
    except Exception as e:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,
                            headers={"WWW-Authenticate": "Bearer"})
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, headers={"WWW-Authenticate": "Bearer"})


async def get_current_user(token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        token: str = payload.get("gt")
        if username is None or token is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    user = await db_get_user(username)
    if user is None or token is None:
        raise credentials_exception
    return user, token
