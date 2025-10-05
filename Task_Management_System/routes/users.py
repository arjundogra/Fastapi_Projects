from fastapi import APIRouter, Depends, HTTPException, status, Cookie
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
import jwt
from database_connection import get_db
from sqlalchemy.orm import Session
from schemas import users
from models.users import Users
import bcrypt
from core.auth import ALGORITHM, REFERESH_SECRET_KEY, create_access_token, create_refresh_token, verify_access_token

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/create", response_model=users.ResponseModel, status_code=status.HTTP_201_CREATED)
async def create_user(req: users.CreateRequest, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(Users).filter(Users.email == req.email).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        hashed_password = bcrypt.hashpw(req.password.get_secret_value().encode('utf-8'), bcrypt.gensalt())
        new_user = Users(name=req.name, email=req.email, hashed_password=hashed_password.decode('utf-8'))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/login", response_model=users.LoginResponse)
async def login_user(req: users.LoginRequest, db: Session = Depends(get_db)):
    try:
        user = db.query(Users).filter(Users.email == req.email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
        if not bcrypt.checkpw(req.password.get_secret_value().encode('utf-8'), user.hashed_password.encode('utf-8')):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password") 
        jwt_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)}) 
        resp = JSONResponse(content={'access_token': jwt_token, 'token_type': 'bearer'}) 
        resp.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
        return resp
    
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.get("/getuser", response_model=users.ResponseModel)
def get_user(user_id: int = Depends(verify_access_token), db: Session = Depends(get_db)):
    try:
        print(user_id)
        user = db.query(Users).filter(Users.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
        # return {"name": "John"}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.get('/refresh')
async def refresh_token(refresh_token: str = Cookie(None), db: Session = Depends(get_db)):
    print(refresh_token)
    if refresh_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing")
    try:
        payload = jwt.decode(refresh_token, REFERESH_SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
        user = db.query(Users).filter(Users.id == int(user_id)).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        new_access_token = create_access_token(data={"sub": str(user.id)})
        new_refresh_token = create_refresh_token(data={"sub": str(user.id)})
        resp = JSONResponse(content={'access_token': new_access_token, 'token_type': 'bearer'})
        resp.set_cookie(key="refresh_token", value=new_refresh_token, httponly=True)
        return resp
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

@router.post('/token')
async def token(req: OAuth2PasswordRequestForm = Depends()):
    access_token = create_access_token(data={"sub": "1"})
    return {"access_token": access_token, "token_type": "bearer"}