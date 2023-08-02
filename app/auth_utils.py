import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
# from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError



def jwt_check(token: str):
    if token:
        try:
            payload = jwt.decode(token, "my-secret", algorithms=["HS256"])
            email = payload.get("sub")
            is_admin = payload.get("is_admin")
            if email is None:
                raise HTTPException(status_code=401, detail="Invalid authentication token")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid authentication token")
    else:
        return HTTPException(status_code=401, detail="Invalid authentication token")

    return {"is_admin": is_admin, "email": email}


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "my-secret", algorithm="HS256")
    return encoded_jwt