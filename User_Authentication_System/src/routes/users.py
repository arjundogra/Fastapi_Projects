from fastapi import APIRouter, status, HTTPException, Depends
from schemas.users import CreateRequest, LoginRequest
from sqlalchemy.orm import Session
from sqlalchemy import or_
from database_connection import get_db
import bcrypt
from models.users import Users
from core.security import create_access_token, verify_access_token


userRouter = APIRouter()


@userRouter.post('/create', status_code=status.HTTP_201_CREATED)
async def createUser(req: CreateRequest, db : Session = Depends(get_db)):
    try:
        user = db.query(Users).filter(or_(Users.email == req.email, Users.username == req.username)).first()
        if user:
            raise HTTPException(status_code=400, detail="User Already Exists")
        hashedPassword = bcrypt.hashpw(req.password.get_secret_value().encode(), bcrypt.gensalt())
        createUserModel : Users = Users(username=req.username, email=req.email , hashed_password=hashedPassword.decode())
        db.add(createUserModel)
        db.commit()
        token = create_access_token(data={"sub": createUserModel.username})
        return {"status": "User Created Successfully", "token": token}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@userRouter.post('/login')
async def loginUser(req: LoginRequest, db: Session = Depends(get_db)):
    try:
        user = db.query(Users).filter(Users.username == req.username).first()
        if not user:
            raise HTTPException(status_code=404,detail="User Not Found")
        if bcrypt.checkpw(req.password.get_secret_value().encode(), user.hashed_password.encode()):
            return {"status": "Login Successful"}
        else:
            raise HTTPException(status_code=401, detail="Invalid Credentials")
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@userRouter.get('/me')
async def getCurrentUser(token_data = Depends(verify_access_token)):
    return {"user": token_data}

