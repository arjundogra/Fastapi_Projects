from fastapi import APIRouter
from sqlalchemy import text
from core.auth import create_access_token, verify_access_token
from schemas import users
from models.users import Users
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from database_connection import get_db
from utils.helper import hash_password, verify_password
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model= users.UserResponseModel, status_code=status.HTTP_201_CREATED)
def register_user(req: users.CreateUserRequest, db: Session = Depends(get_db)):
    try:
        existing_user = db.execute(text("Select * from users where email = :email"), {"email": req.email}).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        new_user = Users(name=req.name, email=req.email, hashed_password=hash_password(req.password))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.post("/login")
def login(req: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        user = db.execute(text("Select * from users where email = :email"), {"email": req.username}).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
        if not verify_password(req.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password") 
        jwt_token = create_access_token(data={"sub": str(user.id)})
        return JSONResponse(content={'access_token': jwt_token, 'token_type': 'bearer'})
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.get("/me", response_model=users.UserResponseModel)
def get_current_user(user_id: int = Depends(verify_access_token), db: Session = Depends(get_db)):
    try:
        user = db.execute(text("Select * from users where id = :id"), {"id": user_id}).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))