import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

Oauth2 = OAuth2PasswordBearer(tokenUrl="/login")

ALGORITHM = "HS256"
SECRET_KEY="138423kjadflajdfklajdfklajdfklajdfklajdfklajdfklajdfk"
REFERESH_SECRET_KEY="138423kjadflajdfklajdfklajdfklajdfklajdfklajdfklajdfk"
Duration = 60

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=2)
    to_encode.update({"exp":expire,"iat":datetime.utcnow()})
    jwt_token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return jwt_token

def create_refresh_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp":expire, "iat":datetime.utcnow()})
    jwt_token = jwt.encode(to_encode, REFERESH_SECRET_KEY, ALGORITHM)
    return jwt_token


def verify_access_token(token = Depends(Oauth2)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        if id is None:
            raise credentials_exception
        return int(id)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired", headers={"WWW-Authenticate":"Bearer"})
    except jwt.InvalidTokenError:
        raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    