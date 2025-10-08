import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
import os

Oauth2 = OAuth2PasswordBearer(tokenUrl="/users/login")

ALGORITHM = os.environ.get("ALGORITHM","HS256")
SECRET_KEY=os.environ.get("SECRET_KEY","YourSecretKeyHereChangeIt")
REFERESH_SECRET_KEY=os.environ.get("REFERESH_SECRET_KEY","YourRefereshSecretKeyHereChangeIt")
Duration = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES",30)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire_date = datetime.utcnow() + timedelta(minutes=Duration)
    to_encode.update({"exp": expire_date, 'iat': datetime.utcnow()})
    jwt_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_token

def verify_access_token(token: str = Depends(Oauth2)) -> int:
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=ALGORITHM)
        id : str = payload.get("sub")
        if id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})
        return int(id)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired", headers={"WWW-Authenticate":"Bearer"})
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})   
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))